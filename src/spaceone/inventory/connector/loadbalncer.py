import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['LoadBalancerConnector']
_LOGGER = logging.getLogger(__name__)


class LoadBalancerConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_load_balancers(self):
        return self.network_client.load_balancers.list_all()
