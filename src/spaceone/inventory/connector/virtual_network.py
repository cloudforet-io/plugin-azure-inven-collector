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
        return self.network_client.virtual_networks.list_all()

    def list_all_firewalls(self, resource_group_name):
        return self.network_client.azure_firewalls.list(resource_group_name)
