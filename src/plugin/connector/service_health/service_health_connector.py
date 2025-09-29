import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class ServiceHealthConnector(AzureBaseConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get("secret_data"))

    def list_health_history(self, query_start_time: str = None):
        return self.resource_health_client.events.list_by_subscription_id(
            query_start_time=query_start_time, api_version="2018-07-01"
        )
