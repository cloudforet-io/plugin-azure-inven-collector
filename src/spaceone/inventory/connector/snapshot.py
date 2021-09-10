import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *
from spaceone.inventory.error.custom import *
__all__ = ['SnapshotConnector']
_LOGGER = logging.getLogger(__name__)


class SnapshotConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_snapshots(self):
        try:
            return self.compute_client.snapshots.list()
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='Public IP Address'))
