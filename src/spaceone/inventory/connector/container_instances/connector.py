import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *
__all__ = ['ContainerInstancesConnector']
_LOGGER = logging.getLogger(__name__)


class ContainerInstancesConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_container_groups(self):
        return self.container_instance_client.container_groups.list()

    def get_container_groups(self, resource_group_name, container_group_name):
        return self.container_instance_client.container_groups.get(resource_group_name=resource_group_name,
                                                                   container_group_name=container_group_name)
