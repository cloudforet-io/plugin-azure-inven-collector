import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *
from spaceone.inventory.error.custom import *
__all__ = ['DisksConnector']
_LOGGER = logging.getLogger(__name__)


class DisksConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_disks(self):
        return self.compute_client.disks.list()
