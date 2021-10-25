import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *

__all__ = ['VirtualNetworkConnector']
_LOGGER = logging.getLogger(__name__)


class VirtualNetworkConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_virtual_networks(self):
        try:
            return self.network_client.virtual_networks.list_all()
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='Virtual Networks'))

    def list_all_firewalls(self, resource_group_name):
        try:
            return self.network_client.azure_firewalls.list(resource_group_name)
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='Virtual Networks Firewalls'))
