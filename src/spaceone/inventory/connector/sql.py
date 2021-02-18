import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['SqlConnector']
_LOGGER = logging.getLogger(__name__)


class SqlConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_servers(self):
        return self.sql_client.servers.list()

    def list_databases(self):
        return self.sql_client.databases.list()

    def list_server_azure_ad_administrators(self, resource_group, server_name):
        return self.sql_client.server_azure_ad_administrators.list_by_server(resource_group, server_name)

    def get_server_automatic_tuning(self, resource_group, server_name):
        return self.sql_client.server_automatic_tuning.get(resource_group, server_name)

    def get_server_auditing_settings(self, resource_group, server_name):
        return self.sql_client.server_blob_auditing_policies.get(resource_group, server_name)

    def list_failover_groups(self, resource_group, server_name):
        return self.sql_client.failover_groups.list_by_server(resource_group, server_name)

    def list_databases_by_server(self, resource_group, server_name):
        return self.sql_client.databases.list_by_server(resource_group, server_name)

    def list_elastic_pools_by_server(self, resource_group, server_name):
        return self.sql_client.elastic_pools.list_by_server(resource_group, server_name)

    def list_databases_by_elastic_pool(self, elastic_pool_name, resource_group, server_name):
        return self.sql_client.databases.list_by_elastic_pool(elastic_pool_name=elastic_pool_name, resource_group_name=resource_group, server_name=server_name)

    def list_restorable_dropped_databases_by_server(self, resource_group, server_name):
        return self.sql_client.restorable_dropped_databases.list_by_server(resource_group_name=resource_group, server_name=server_name)

