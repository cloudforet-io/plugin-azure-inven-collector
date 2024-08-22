import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class NATGatewaysConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_nat_gateways(self):
        return self.network_client.nat_gateways.list_all()

    def get_public_ip_addresses(self, resource_group_name, public_ip_address_name):
        return self.network_client.public_ip_addresses.get(resource_group_name, public_ip_address_name)

    def get_public_ip_prefixes(self, resource_group_name, public_ip_prefixes_name):
        return self.network_client.public_ip_prefixes.get(resource_group_name, public_ip_prefixes_name)

    def get_subnet(self, resource_group_name, subnet_name, vnet_name):
        return self.network_client.subnets.get(resource_group_name=resource_group_name, virtual_network_name=vnet_name, subnet_name=subnet_name)