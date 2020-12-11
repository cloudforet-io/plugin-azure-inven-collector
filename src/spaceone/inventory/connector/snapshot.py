import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['SnapshotConnector']
_LOGGER = logging.getLogger(__name__)


class SnapshotConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_snapshots(self):
        return self.compute_client.snapshots.list()
