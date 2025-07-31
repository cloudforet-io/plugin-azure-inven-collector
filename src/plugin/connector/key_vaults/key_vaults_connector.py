import logging

from azure.identity import DefaultAzureCredential
from azure.keyvault.certificates import CertificateClient
from azure.keyvault.secrets import SecretClient

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class KeyVaultsConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_connect(kwargs.get("secret_data"))
        # self.key_vault_secret_client = None
        # self.key_vault_certificate_client = None

    def init_key_vault_secret_client(self, subscription_id, vault_uri):
        credential = DefaultAzureCredential()
        key_vault_secret_client = SecretClient(
            credential=credential, subscription_id=subscription_id, vault_url=vault_uri
        )
        return key_vault_secret_client

    def init_key_vault_certificate_client(self, subscription_id, vault_uri):
        credential = DefaultAzureCredential()
        key_vault_certificate_client = CertificateClient(
            credential=credential, subscription_id=subscription_id, vault_url=vault_uri
        )
        return key_vault_certificate_client

    def list_all_key_vaults(self):
        return self.key_vault_client.vaults.list_by_subscription()

    def get_key_vaults(self):
        return self.key_vault_client.vaults.get()

    def list_keys(self, resource_group_name, vault_name):
        return self.key_vault_client.keys.list(
            resource_group_name=resource_group_name, vault_name=vault_name
        )

    def list_secrets(self):
        # return self.key_vault_secrets_client.list_properties_of_secrets()
        return self.key_vault_client.secrets.list()
