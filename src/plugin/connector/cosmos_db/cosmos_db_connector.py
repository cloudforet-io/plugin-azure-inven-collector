import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class CosmosDBConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_cosmos_db_accounts(self):
        return self.cosmosdb_client.database_accounts.list()

    def list_keys(self, account_name, resource_group_name):
        return self.cosmosdb_client.database_accounts.list_keys(account_name=account_name, resource_group_name=resource_group_name)

    def list_sql_resources(self, account_name, resource_group_name):
        return self.cosmosdb_client.sql_resources.list_sql_databases(account_name=account_name, resource_group_name=resource_group_name)
