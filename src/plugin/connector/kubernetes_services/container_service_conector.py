import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class ContainerServiceConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get("secret_data"))

    def list_managed_cluster(self):
        return self.container_service_client.managed_clusters.list()

    def get_managed_cluster(self, resource_group_name, cluster_name):
        return self.container_service_client.managed_clusters.get(
            resource_group_name, cluster_name
        )

    def list_agent_pools(self, resource_group_name, cluster_name):
        return self.container_service_client.agent_pools.list(
            resource_group_name, cluster_name
        )

    def list_locks(self, resource_id: str):
        url = (
            f"https://management.azure.com{resource_id}"
            "/providers/Microsoft.Authorization/locks"
            "?api-version=2016-09-01"
        )

        try:
            result = self.request_azure_api(url) or {}
            return result.get("value", [])
        except Exception as e:
            _LOGGER.warning(f"[ContainerServiceConnector.list_locks] error: {e}")
            return []
