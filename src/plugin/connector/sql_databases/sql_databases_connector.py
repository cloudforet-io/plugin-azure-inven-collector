import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class SqlDatabasesConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_servers(self):
        return self.sql_client.servers.list()

    def list_databases_in_server(self, resource_group_name, server_name):
        return self.sql_client.databases.list_by_server(resource_group_name=resource_group_name, server_name=server_name)

    def list_sync_groups_by_databases(self, resource_group, server_name, database_name):
        return self.sql_client.sync_groups.list_by_database(resource_group_name=resource_group,
                                                            database_name=database_name,
                                                            server_name=server_name)

    def list_sync_agents_by_server(self, resource_group, server_name):
        return self.sql_client.sync_agents.list_by_server(resource_group_name=resource_group, server_name=server_name)

    def list_replication_link_by_server(self, resource_group_name, server_name):
        return self.sql_client.replication_links.list_by_server(resource_group_name=resource_group_name,
                                                                server_name=server_name)

    def list_replication_link(self, resource_group_name, server_name, database_name):
        return self.sql_client.replication_links.list_by_database(resource_group_name=resource_group_name,
                                                                  server_name=server_name, database_name=database_name)

    def get_database_auditing_settings(self, resource_group_name, server_name, database_name):
        return self.sql_client.database_blob_auditing_policies.get(resource_group_name=resource_group_name,
                                                                                server_name=server_name,
                                                                                database_name=database_name)