import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *
__all__ = ['LoadBalancersConnector']
_LOGGER = logging.getLogger(__name__)


class LoadBalancersConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_load_balancers(self):
        return self.network_client.load_balancers.list_all()

    def get_subnets(self, resource_group_name, vnet_name, subnet_name):
        return self.network_client.subnets.get(resource_group_name, vnet_name, subnet_name)

    def list_load_balancer_backend_address_pools(self, resource_group_name, lb_name):
        return self.network_client.load_balancer_backend_address_pools.list(resource_group_name, lb_name)

    def list_load_balancer_network_interfaces(self, resource_group_name, lb_name):
        return self.network_client.load_balancer_network_interfaces.list(resource_group_name, lb_name)

    def list_network_interface_ip_configurations(self, resource_group_name, network_interface_name):
        return self.network_client.network_interface_ip_configurations.list(resource_group_name, network_interface_name)
