import logging

from spaceone.inventory.libs.connector import AzureConnector

__all__ = ['SQLDatabasesConnector']
_LOGGER = logging.getLogger(__name__)


class SQLDatabasesConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_servers(self):
        return self.sql_client.servers.list()

    def list_databases(self, resource_group_name, server_name):
        return self.sql_client.databases.list_by_server(resource_group_name=resource_group_name, server_name=server_name)

    def list_sync_group_by_database(self, resource_group_name, server_name, database_name):
        return self.sql_client.sync_groups.list_by_database(resource_group_name=resource_group_name, server_name=server_name, database_name=database_name)

