import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['NetworkSecurityGroupConnector']
_LOGGER = logging.getLogger(__name__)


class NetworkSecurityGroupConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_network_security_groups(self):
        obj = self.network_client.network_security_groups.list_all()
        return self.network_client.network_security_groups.list_all()
