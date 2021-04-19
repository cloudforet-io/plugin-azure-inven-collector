import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['VnetConnector']
_LOGGER = logging.getLogger(__name__)


class VnetConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_vnet(self, resource_group):
        return self.network_client.virtual_networks.list(resource_group=resource_group)

