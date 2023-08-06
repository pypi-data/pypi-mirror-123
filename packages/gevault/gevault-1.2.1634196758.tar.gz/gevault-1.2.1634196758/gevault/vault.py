from os.path import dirname, join, abspath
import json

import hvac

DEFAULT_CONFIG = join(dirname(abspath(__file__)), "vault-config.json")

TOKEN_ROLE = "vault-token-role"

class Vault(object):
    def __init__(self, config_file=None, server_name="default"):
        self.config_file = config_file if config_file else DEFAULT_CONFIG
        self.server_name = server_name
        self.config = self.read_config()
        self.vault = self.set_vault()
        self.token_role = TOKEN_ROLE

    def status_check(self):
        status = self.vault.sys.read_health_status(method="GET")
        try:
            return status.status_code
        except AttributeError:
            if not status["initialized"]:
                return 501
            if status["sealed"]:
                return 503
            if status["standby"]:
                return 429
            return 200

    def set_vault(self):
        vault = hvac.Client(url=self._get_url())
        token = self._get_admin_token()
        if token:
            vault.token = token
        self.vault = vault
        return vault

    def _get_url(self):
        if not self.config.get("ServerUrl", None):
            input_value = input("Specify URL of Server: ").replace('"', '').replace("'", "")
            self.update_config("ServerUrl", input_value)
            return input_value
        else:
            return self.config["ServerUrl"]

    def _get_admin_token(self):
        admin = self.config.get("admin", {})
        return admin.get("rootToken", admin.get("masterToken", None))

    def _get_unseal_keys(self):
        return self.config.get("admin", {}).get("unsealKeys", None)

    def update_config(self, key, data):
        full_config = self.__read_full_config()
        server_config = full_config.get(self.server_name, {})
        if key in ["admin", "user"]:
            new_config = server_config.get(key, {})
            new_config.update(data)
            server_config[key] = new_config
        else:
            server_config[key] = data
        full_config[self.server_name] = server_config
        with open(self.config_file, 'w') as config_file:
            config_file.write(json.dumps(full_config, indent=4))
            config_file.close()
        print("Config File at %s updated." % self.config_file)
        self.config = server_config


    def __read_full_config(self):
        try:
            with open(self.config_file, 'r') as config_file:
                config = json.loads(config_file.read())
                config_file.close()
                return config
        except (FileNotFoundError):
            return {}

    def read_config(self):
        config = self.__read_full_config()
        try:
            return config[self.server_name]
        except KeyError:
            return {}