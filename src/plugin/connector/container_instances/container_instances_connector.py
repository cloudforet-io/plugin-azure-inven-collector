import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class ContainerInstancesConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_container_groups(self):
        return self.container_instance_client.container_groups.list()

    def get_container_groups(self, resource_group_name, container_group_name):
        return self.container_instance_client.container_groups.get(resource_group_name=resource_group_name,
                                                                   container_group_name=container_group_name)