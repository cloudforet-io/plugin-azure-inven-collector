import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class WebPubSubHubManager(AzureBaseManager):
    cloud_service_group = "WebPubSubService"
    cloud_service_type = "Hub"
    service_code = "/Microsoft.SignalRService/WebPubSub/hubs"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Application Integration"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-web-pubsub-service.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        return cloud_services, error_responses
