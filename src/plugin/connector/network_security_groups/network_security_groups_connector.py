import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class NetworkSecurityGroupsConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_network_security_groups(self):
        return self.network_client.network_security_groups.list_all()

    def list_all_network_interfaces(self):
        return self.network_client.network_interfaces.list_all()

    def get_network_interfaces(self, network_interface_name, resource_group):
        return self.network_client.network_interfaces.get(network_interface_name=network_interface_name,
                                                          resource_group_name=resource_group)

    def get_subnet(self, resource_group_name, subnet_name, virtual_network_name):
        return self.network_client.subnets.get(resource_group_name=resource_group_name, subnet_name=subnet_name,
                                               virtual_network_name=virtual_network_name)
