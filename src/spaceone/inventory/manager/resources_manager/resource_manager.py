import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.connector.resources import ResourcesConnector

_LOGGER = logging.getLogger(__name__)


class ResourcesManager(AzureManager):
    connector_name = "ResourcesConnector"

    def collect_exist_resources(self, params: dict) -> list:
        """ " """

        resources_info = []
        resources_conn: ResourcesConnector = self.locator.get_connector(
            self.connector_name, **params
        )

        resources_obj = resources_conn.list_resources()

        for resource_obj in resources_obj:
            resource_info = self.convert_nested_dictionary(resource_obj)
            type = resource_info.get("type").split("/")[1]
            if type not in resources_info:
                resources_info.append(type)

        return resources_info
