import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['StorageAccountConnector']
_LOGGER = logging.getLogger(__name__)


class StorageAccountConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_storage_accounts(self):
        obj = self.storage_client.storage_accounts.list()
        '''
        for i in obj:
            print("#####")
            print(i)
        print(obj)
        '''
        return obj

    def list_blobs(self, rg_name, account_name):
        obj = self.storage_client.blob_containers.list(resource_group_name=rg_name, account_name=account_name)
        '''
        for i in obj:
            print("###")
            print(i)
        '''
        return obj

