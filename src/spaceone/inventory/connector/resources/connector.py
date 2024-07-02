import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ["ResourcesConnector"]
_LOGGER = logging.getLogger(__name__)


class ResourcesConnector(AzureConnector):
    def __init__(self, **kwargs):
        super().__init__()
        self.set_connect(kwargs.get("secret_data"))

    def list_resources(self) -> list:
        return self.resource_client.resources.list()
