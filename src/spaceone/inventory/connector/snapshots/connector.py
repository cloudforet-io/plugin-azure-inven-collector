import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *
from spaceone.inventory.error.custom import *
__all__ = ['SnapshotsConnector']
_LOGGER = logging.getLogger(__name__)


class SnapshotsConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_snapshots(self):
        return self.compute_client.snapshots.list()
