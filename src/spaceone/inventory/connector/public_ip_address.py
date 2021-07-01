import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['PublicIPAddressConnector']
_LOGGER = logging.getLogger(__name__)


class PublicIPAddressConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_public_ip_addresses(self):
        return self.network_client.public_ip_addresses.list_all()
