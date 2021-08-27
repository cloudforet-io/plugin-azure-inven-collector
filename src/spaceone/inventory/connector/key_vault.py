import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *
from azure.keyvault.secrets import SecretClient
from azure.keyvault.certificates import CertificateClient
from azure.identity import DefaultAzureCredential

__all__ = ['KeyVaultConnector']
_LOGGER = logging.getLogger(__name__)


class KeyVaultConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_connect(kwargs.get('secret_data'))
        self.key_vault_secret_client = None
        self.key_vault_certificate_client = None

    def init_key_vault_secret_client(self, subscription_id, vault_uri):
        try:
            credential = DefaultAzureCredential()
            key_vault_secret_client = SecretClient(credential=credential,  subscription_id=subscription_id, vault_url=vault_uri)
            return key_vault_secret_client
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR_INITIALIZE(field='Key Vault Secret Client'))

    def init_key_vault_certificate_client(self, subscription_id, vault_uri):
        try:
            credential = DefaultAzureCredential()
            key_vault_certificate_client = CertificateClient(credential=credential,  subscription_id=subscription_id, vault_url=vault_uri)
            return key_vault_certificate_client
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR_INITIALIZE(field='Key Vault Secret Client'))

    def list_all_key_vaults(self):
        try:
            return self.key_vault_client.vaults.list_by_subscription()

        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='Key Vaults'))

    def list_keys(self, resource_group_name, vault_name):
        try:
            return self.key_vault_client.keys.list(resource_group_name=resource_group_name, vault_name=vault_name)

        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='Key Vaults'))

    def list_secrets(self, resource_group_name, vault_name):
        try:
            return self.key_vault_secret_client.list_properties_of_secrets()

        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='Key Vaults'))
