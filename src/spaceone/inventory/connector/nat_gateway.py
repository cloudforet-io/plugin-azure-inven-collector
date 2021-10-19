import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['NATGatewayConnector']
_LOGGER = logging.getLogger(__name__)


class NATGatewayConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_nat_gateways(self):
        return self.network_client.nat_gateways.list_all()

    def get_public_ip_addresses(self, resource_group_name, public_ip_address_name):
        try:
            return self.network_client.public_ip_addresses.get(resource_group_name, public_ip_address_name)
        except Exception as e:
            _LOGGER.error(f'[ERROR: Azure NAT Gateway Connector Get Public IP Addresses]: {e}')

    def get_public_ip_prefixes(self, resource_group_name, public_ip_prefixes_name):
        try:
            obj = self.network_client.public_ip_prefixes.get(resource_group_name, public_ip_prefixes_name)
            return obj

        except Exception as e:
            _LOGGER.error(f'[ERROR: Azure NAT Gateway Connector Get Public IP Prefixes]: {e}')

    def get_subnet(self, resource_group_name, subnet_name, vnet_name):
        try:
            obj = self.network_client.subnets.get(resource_group_name=resource_group_name, virtual_network_name=vnet_name, subnet_name=subnet_name)
            return obj

        except Exception as e:
            _LOGGER.error(f'[ERROR: Azure NAT Gateway Connector Get Subnet]: {e}')