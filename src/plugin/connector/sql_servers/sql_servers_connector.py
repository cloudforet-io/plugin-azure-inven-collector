import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class SqlServersConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_servers(self):
        return self.sql_client.servers.list()

    def list_server_azure_ad_administrators(self, resource_group, server_name):
        return self.sql_client.server_azure_ad_administrators.list_by_server(resource_group, server_name)

    def get_server_automatic_tuning(self, resource_group, server_name):
        return self.sql_client.server_automatic_tuning.get(resource_group, server_name)

    def get_server_auditing_settings(self, resource_group, server_name):
        return self.sql_client.server_blob_auditing_policies.get(resource_group, server_name)

    def list_failover_groups(self, resource_group, server_name):
        return self.sql_client.failover_groups.list_by_server(resource_group, server_name)

    def list_encryption_protectors(self, resource_group, server_name):
        return self.sql_client.encryption_protectors.list_by_server(resource_group_name=resource_group, server_name=server_name)

    def list_databases_by_server(self, resource_group_name, server_name):
        return self.sql_client.databases.list_by_server(resource_group_name=resource_group_name, server_name=server_name)

    def list_elastic_pools_by_server(self, resource_group, server_name):
        return self.sql_client.elastic_pools.list_by_server(resource_group, server_name)

    def list_databases_by_elastic_pool(self, elastic_pool_name, resource_group, server_name):
        return self.sql_client.databases.list_by_elastic_pool(elastic_pool_name=elastic_pool_name, resource_group_name=resource_group, server_name=server_name)

    def list_restorable_dropped_databases_by_server(self, resource_group, server_name):
        return self.sql_client.restorable_dropped_databases.list_by_server(resource_group_name=resource_group, server_name=server_name)

    def list_firewall_rules_by_server(self, resource_group, server_name):
        return self.sql_client.firewall_rules.list_by_server(resource_group_name=resource_group, server_name=server_name)

    def list_virtual_network_rules_by_server(self, resource_group, server_name):
        return self.sql_client.virtual_network_rules.list_by_server(resource_group_name=resource_group, server_name=server_name)

    def list_sync_groups_by_databases(self, resource_group, server_name, database_name):
        return self.sql_client.sync_groups.list_by_database(resource_group_name=resource_group, database_name=database_name, server_name=server_name)

    def list_sync_agents_by_server(self, resource_group, server_name):
        return self.sql_client.sync_agents.list_by_server(resource_group_name=resource_group, server_name=server_name)

    def list_data_masking_rules_by_database(self, resource_group, server_name, database_name):
        return self.sql_client.data_masking_rules.list_by_database(resource_group_name=resource_group, server_name=server_name, database_name=database_name)

    def list_replication_link(self, resource_group, server_name, database_name):
        return self.sql_client.replication_links.list_by_database(resource_group_name=resource_group, server_name=server_name, database_name=database_name)
