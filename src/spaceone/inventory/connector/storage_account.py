import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *

__all__ = ['StorageAccountConnector']
_LOGGER = logging.getLogger(__name__)


class StorageAccountConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_storage_accounts(self):
        try:
            return self.storage_client.storage_accounts.list()
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='Storage Accounts'))

    def list_blobs(self, rg_name, account_name):
        try:
            return self.storage_client.blob_containers.list(resource_group_name=rg_name, account_name=account_name)
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='Storage Accounts Blobs'))

