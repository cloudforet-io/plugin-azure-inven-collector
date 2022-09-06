import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['MonitorConnector']
_LOGGER = logging.getLogger(__name__)


class MonitorConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_diagnostic_settings(self, resource_uri):
        return self.monitor_client.diagnostic_settings.list(resource_uri=resource_uri)
