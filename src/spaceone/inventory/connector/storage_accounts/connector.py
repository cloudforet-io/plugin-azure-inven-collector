import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *

__all__ = ['StorageAccountsConnector']
_LOGGER = logging.getLogger(__name__)


class StorageAccountsConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_storage_accounts(self):
        return self.storage_client.storage_accounts.list()

    def list_blob_containers(self, rg_name, account_name):
        return self.storage_client.blob_containers.list(resource_group_name=rg_name, account_name=account_name)

