import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *

__all__ = ['MySQLServerConnector']
_LOGGER = logging.getLogger(__name__)


class MySQLServerConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_connect(kwargs.get('secret_data'))

    def list_servers(self):
        try:
            return self.mysql_client.servers.list()
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='MySQL Servers'))


