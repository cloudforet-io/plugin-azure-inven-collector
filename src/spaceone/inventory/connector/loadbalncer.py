import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *
__all__ = ['LoadBalancerConnector']
_LOGGER = logging.getLogger(__name__)


class LoadBalancerConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_load_balancers(self):
        try:
            return self.network_client.load_balancers.list_all()
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='Load Balancer'))

    def get_subnets(self, resource_group_name, vnet_name, subnet_name):
        try:
            return self.network_client.subnets.get(resource_group_name, vnet_name, subnet_name)
        except ConnectionError:
            raise ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='Load Balancer Subnet')

    def list_load_balancer_backend_address_pools(self, resource_group_name, lb_name):
        try:
            return self.network_client.load_balancer_backend_address_pools.list(resource_group_name, lb_name)
        except ConnectionError:
            raise ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='Load Balancer Backend Address Pools')

    def list_load_balancer_network_interfaces(self, resource_group_name, lb_name):
        try:
            return self.network_client.load_balancer_network_interfaces.list(resource_group_name, lb_name)
        except ConnectionError:
            raise ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='Load Balancer Network Interfaces')

    def list_network_interface_ip_configurations(self, resource_group_name, network_interface_name):
        try:
            return self.network_client.network_interface_ip_configurations.list(resource_group_name, network_interface_name)
        except ConnectionError:
            raise ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='Load Balancer Network Interface IP Configurations')
