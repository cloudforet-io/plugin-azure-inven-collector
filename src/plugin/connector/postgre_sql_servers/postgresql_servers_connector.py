import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class PostgreSQLServersConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get("secret_data"))

    def list_servers(self):
        return self.postgre_sql_client.servers.list()

    def list_firewall_rules_by_server(self, resource_group_name, server_name):
        return self.postgre_sql_client.firewall_rules.list_by_server(
            resource_group_name=resource_group_name, server_name=server_name
        )

    def list_virtual_network_rules_by_server(self, resource_group_name, server_name):
        return self.postgre_sql_client.virtual_network_rules.list_by_server(
            resource_group_name=resource_group_name, server_name=server_name
        )

    def list_replicas_by_server(self, resource_group_name, server_name):
        return self.postgre_sql_client.replicas.list_by_server(
            resource_group_name=resource_group_name, server_name=server_name
        )

    def list_server_administrators(self, resource_group_name, server_name):
        return self.postgre_sql_client.server_administrators.list(
            resource_group_name=resource_group_name, server_name=server_name
        )
