import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *
__all__ = ['CosmosDBConnector']
_LOGGER = logging.getLogger(__name__)


class CosmosDBConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_cosmos_db_accounts(self):
        return self.cosmosdb_client.database_accounts.list()

    def list_keys(self, account_name, resource_group_name):
        return self.cosmosdb_client.database_accounts.list_keys(account_name= account_name, resource_group_name=resource_group_name)

    def list_sql_resources(self, account_name, resource_group_name):
        return self.cosmosdb_client.sql_resources.list_sql_databases(account_name=account_name, resource_group_name=resource_group_name)

