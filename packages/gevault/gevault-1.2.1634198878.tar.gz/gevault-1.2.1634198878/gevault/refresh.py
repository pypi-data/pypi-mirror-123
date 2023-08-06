import subprocess
from os import environ
from os.path import isfile, join
import getpass
import json
import requests

from requests.exceptions import ReadTimeout

from gevault.vault import Vault
from gevault.admin import MOUNT_POINT, SIGNING_ROLE

DEFAULT_KEY_NAME = "vault"
DEFAULT_VAULT_VARIABLE = "VAULT_TOKEN"

class Refresh(Vault):

    def __init__(self, config_file=None, server_name="default"):
        Vault.__init__(self, config_file=config_file, server_name=server_name)
        self.ssh_loc = "/Users/%s/.ssh" % getpass.getuser()
        self.key_name = self.__get_key_name()
        self.pubkey_path = "%s/%s.pub" % (self.ssh_loc, self.key_name)
        self.refresh_token = self.__get_refresh_token()

        self.gen_ssh_key()
        cert = self.request_certificate()
        self.create_cert_file(cert)

    def gen_ssh_key(self):
        print("Generating Key Pair...")
        if isfile(self.pubkey_path): ## keypair exists but is stale
            self.command("echo -e 'y' | ssh-keygen -q -t rsa -b 4096  -N '' -f %s/%s 2>/dev/null <<< y >/dev/null" % (self.ssh_loc, self.key_name))

        else: ## keypair does not exist
            self.command("echo -e 'y' | ssh-keygen -q -t rsa -b 4096 -f %s/%s -N ''" % (self.ssh_loc, self.key_name))

    def request_certificate(self):
        with open(self.pubkey_path, 'r') as pubkey:
            key = pubkey.read().replace('\n', '')

        body = {
            "valid_principals": "ubuntu,ec2-user,gecloud,cops,centos",
            "public_key": key,
            "extension":{"permit-pty": ""}
        }

        req_sess = requests.Session()
        req_sess.trust_env = False

        url = f"{self._get_url()}/v1/{MOUNT_POINT}/sign/{SIGNING_ROLE}"
        headers = {'X-Vault-Token': self.refresh_token}

        print("Requesting Signature...")
        response = req_sess.post(url, headers=headers, data=json.dumps(body), timeout=4)
        response.raise_for_status
        response_dict = json.loads(response.text)
        if response_dict.get("errors", None):
            raise Exception(response_dict["errors"])

        return json.loads(response.text)['data']['signed_key']


    def create_cert_file(self, cert):
        print("Writing Vault Key...")
        with open(join(self.ssh_loc, "%s-cert.pub" % self.key_name), 'w') as cert_file:
            cert_file.write(cert)

    def __get_key_name(self):
        if not self.config.get("user", {}).get("sshKeyName", None):
            key_name = input("SSH key name (default: %s): " % DEFAULT_KEY_NAME)
            if not key_name:
                key_name = DEFAULT_KEY_NAME
            self.update_config("user", {"sshKeyName": key_name})
        else:
            key_name = self.config["user"]["sshKeyName"]
        return key_name

    def __get_refresh_token(self):
        # Config Token
        if self.config.get("user", {}).get("refreshToken", None):
            print("Token found in config file.")
            return self.config["user"]["refreshToken"]

        # Config Variable
        variable = self.config.get("user", {}).get("refreshTokenVariable", None)
        try:
            token = environ[variable]
            print("Token found in environment variable %s." % variable)
            return token
        except KeyError:
            print("Token NOT found in environment variable %s." % variable)
        except TypeError:
            pass

        # Default Variable
        try:
            token = environ[DEFAULT_VAULT_VARIABLE]
            print("Token found in environment variable %s." % DEFAULT_VAULT_VARIABLE)
            self.update_config("user", {"refreshTokenVariable": DEFAULT_VAULT_VARIABLE})
            return token
        except KeyError:
            pass

        # Input Variable
        new_variable = input("Vault Token Variable Name: ")
        self.update_config("user", {"refreshTokenVariable": new_variable})
        try:
            token = environ[new_variable]
            print("Token found in environment variable %s." % new_variable)
            return token
        except KeyError:
            raise Exception("Variable: %s could not be found in environment" % new_variable)
        

    def command(self, com_string, silent=True, env=environ.copy()):
        process = subprocess.Popen(
            com_string,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            env=env
        )
        output = process.communicate()
        if not silent:
            print("Running Command: %s" % com_string)
            self.print_bytes(output[0])
        try:
            string_output = [x.decode("utf-8") for x in output]
        except AttributeError:
            string_output = output
        if string_output[1] and "SNIMissingWarning" not in string_output[1] and "insecure" not in string_output[1].lower():
            print("Errors:")
            self.print_bytes(string_output[1])
            raise Exception(string_output[1])
        return output

    @staticmethod
    def print_bytes(byte_string):
        if isinstance(byte_string, bytes):
            byte_string = byte_string.decode('utf-8')
        string_list = byte_string.split("/n")
        for string_item in string_list:
            print(string_item)
