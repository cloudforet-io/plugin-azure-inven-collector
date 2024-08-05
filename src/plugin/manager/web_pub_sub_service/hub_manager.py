import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.web_pub_sub_service.web_pubsub_service_connector import WebPubSubServiceConnector
from plugin.connector.subscriptions.subscriptions_connector import SubscriptionsConnector
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger(__name__)


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
            tags={
                "spaceone:icon": f"{ICON_URL}/azure-web-pubsub-service.svg"
            }
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        return cloud_services, error_responses

    # def create_cloud_service(self, options, secret_data, schema):
    #     cloud_services = []
    #     error_responses = []
    #
    #     web_pubsub_service_conn = WebPubSubServiceConnector(secret_data=secret_data)
    #     subscription_conn = SubscriptionsConnector(secret_data=secret_data)
    #
    #     subscription_obj = subscription_conn.get_subscription(secret_data["subscription_id"])
    #     subscription_info = self.convert_nested_dictionary(subscription_obj)
    #
    #     web_pubsub_services = web_pubsub_service_conn.list_by_subscription()
    #
    #     for web_pubsub_service in web_pubsub_services:
    #
    #         try:
    #             web_pubsub_service_dict = self.convert_nested_dictionary(
    #                 web_pubsub_service
    #             )
    #             web_pubsub_service_id = web_pubsub_service_dict["id"]
    #             resource_group_name = self.get_resource_group_from_id(
    #                 web_pubsub_service_id
    #             )
    #             resource_name = web_pubsub_service_dict["name"]
    #
    #             web_pubsub_hubs = web_pubsub_service_conn.list_hubs(
    #                 resource_group_name=resource_group_name, resource_name=resource_name
    #             )
    #
    #             web_pubsub_hubs_dict = [
    #                 self.convert_nested_dictionary(hub) for hub in web_pubsub_hubs
    #             ]
    #
    #             for web_pubsub_hub_dict in web_pubsub_hubs_dict:
    #
    #                 web_pubsub_hub_id = web_pubsub_hub_dict["id"]
    #                 resource_group_name = self.get_resource_group_from_id(web_pubsub_hub_id)
    #                 web_pubsub_hub_dict.update(
    #                     {
    #                         "tenant_id": secret_data["tenant_id"],
    #                         "location": web_pubsub_service_dict["location"],
    #                         "resource_group": resource_group_name,
    #                         "subscription_id": subscription_info["subscription_id"],
    #                         "subscription_name": subscription_info["display_name"],
    #                         "azure_monitor": {"resource_id": web_pubsub_hub_id},
    #                         "web_pubsub_svc_name": self.get_web_pubsub_name_from_id(
    #                             web_pubsub_hub_id
    #                         ),
    #                         "web_pubsub_hub_evnet_handler_count_display": len(
    #                             web_pubsub_hub_dict.get("properties", {}).get(
    #                                 "event_handlers", []
    #                             )
    #                         ),
    #                     }
    #                 )
    #
    #                 cloud_services.append(
    #                     make_cloud_service(
    #                         name=web_pubsub_hub_dict["name"],
    #                         cloud_service_type=self.cloud_service_type,
    #                         cloud_service_group=self.cloud_service_group,
    #                         provider=self.provider,
    #                         data=web_pubsub_hub_dict,
    #                         account=web_pubsub_hub_dict["subscription_id"],
    #                         region_code=web_pubsub_hub_dict["location"],
    #                         reference=self.make_reference(web_pubsub_hub_dict.get("id")),
    #                         tags=web_pubsub_hub_dict.get("tags", {}),
    #                         data_format="dict"
    #                     )
    #                 )
    #
    #         except Exception as e:
    #             _LOGGER.error(f"[create_cloud_service] Error {self.service} {e}", exc_info=True)
    #             error_responses.append(
    #                 make_error_response(
    #                     error=e,
    #                     provider=self.provider,
    #                     cloud_service_group=self.cloud_service_group,
    #                     cloud_service_type=self.cloud_service_type,
    #                 )
    #             )
    #
    #     return cloud_services, error_responses
    #
    # @staticmethod
    # def get_web_pubsub_name_from_id(dict_id):
    #     svc_name = dict_id.split("/")[-3]
    #     return svc_name
