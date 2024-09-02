import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class MySQLFlexibleServersConnector(AzureBaseConnector):
    def __init__(self, secret_data=None, **kwargs):
        super().__init__(**kwargs)

        self.set_connect(secret_data)

    def list_flexible_servers(self):
        return self.mysql_flexible_client.servers.list()

    def list_firewall_rules_by_server(self, resource_group_name, server_name):
        return self.mysql_flexible_client.firewall_rules.list_by_server(resource_group_name=resource_group_name, server_name=server_name)