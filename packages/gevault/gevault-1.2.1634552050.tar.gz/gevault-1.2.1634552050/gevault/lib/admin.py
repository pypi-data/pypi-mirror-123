import json

from hvac.exceptions import InvalidRequest

from gevault.vault import Vault

MOUNT_POINT = 'ssh-client-signer'
SIGNING_ROLE = "vault-signing-role"

SHARES = 5
THRESHOLD = 3

class Admin(Vault):

    def __init__(self, config_file=None, server_name="default"):
        Vault.__init__(self, config_file=config_file, server_name=server_name)

    def initialize(self):
        """
        To be performed when a new vault cluster is being created.
        This does not apply to simply creating a new server.
        This will create new keys and will mean having to relaunch instances
        using vault creds.  Don't do this on redeploy!
        """

        if self.status_check() == 501:
            print("Initializing Vault...")
            response = self.vault.sys.initialize(SHARES, THRESHOLD)

            self.vault.token = response['root_token']
            self.update_config("admin", {
                "rootToken": response['root_token'],
                "unsealKeys": response['keys']
            })
            print("Vault Initialized.")
    
        # -------------------------------

        if self.status_check() == 503:
            self.unseal()

        # -------------------------------

        if self.status_check() == 200:
            self.set_vault()
            self.__mount_ssh_backend()
            self.write_signing_key()
            self.__create_signing_role()
            self.__create_token_role()

        if not self.config["admin"].get("masterToken", None):
            self.update_config("admin", {"masterToken": self.__create_master_token()})

    def __mount_ssh_backend(self):
        print('Mounting SSH backend...')
        try:
            self.vault.sys.enable_secrets_engine('ssh', path=MOUNT_POINT)
        except InvalidRequest:
            print("SSH backend already mounted...")


    # --- SSH Keys ---

    def write_signing_key(self, public_key=None, private_key=None):
        signing_key_address = "%s/config/ca" % MOUNT_POINT
        try:
            if not public_key and not private_key:
                self.vault.write(signing_key_address, generate_signing_key=True)
            elif public_key and private_key:
                self.vault.write(signing_key_address, public_key=public_key, private_key=private_key)
            self.update_config("admin", {"publicSigningKey": self.get_public_signing_key()})
        except InvalidRequest:
            print("Signing Key already written...")

    def get_public_signing_key(self):
        signing_key_address = "%s/config/ca" % MOUNT_POINT
        return self.vault.read(signing_key_address)['data']['public_key']


    # --- SSH ROLES ---

    def __create_signing_role(self):
        try:
            self.vault.write(
                '%s/roles/%s' % (MOUNT_POINT, SIGNING_ROLE),
                allow_user_certificates=True,
                allowed_users="*",
                key_type="ca",
                ttl="30m0s",
                default_extensions=[{ "permit-pty": "" }]
            )
        except InvalidRequest:
            print("Signing Role already created...")

    def __create_token_role(self):
        policy = {
            "path": {
                "%s/sign/*" % MOUNT_POINT: {
                    "capabilities": [
                        "read",
                        "create",
                        "update",
                        "list"
                    ]
                }
            }
        }
        self.vault.sys.create_or_update_policy(self.token_role, json.dumps(policy))
        return self.vault.auth.token.create_or_update_role(self.token_role, allowed_policies=self.token_role, renewable=True)
        # return self.vault.create_token_role(self.token_role, allowed_policies=self.token_role, period='87600h')

    def __create_master_token(self):
        return self.vault.auth.token.create(policies=['root'], ttl='87600h')['auth']['client_token']

    def __get_policy(self):
        return self.vault.sys.read_policy(name=self.token_role)

    # --- Unseal ---

    def unseal(self):
        print("Unsealing Vault...")
        vault_keys = self._get_unseal_keys()
        self.vault.sys.submit_unseal_key(vault_keys[0])
        self.vault.sys.submit_unseal_key(vault_keys[1])
        self.vault.sys.submit_unseal_key(vault_keys[2])
        print("Unseal Keys Submitted.")
