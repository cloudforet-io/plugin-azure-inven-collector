import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.cognitive_services.cognitive_services_connector import (
    CognitiveServicesConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class CognitiveServicesManager(AzureBaseManager):
    cloud_service_group = "CognitiveService"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.CognitiveServices/accounts"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Artificial Intelligence"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-cognitive-service.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        cognitive_services_conn = CognitiveServicesConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        cognitive_services_account_list = (
            cognitive_services_conn.list_all_cognitive_services_accounts()
        )

        for cognitive_services_account in cognitive_services_account_list:
            try:
                cognitive_services_account_dict = self.convert_nested_dictionary(
                    cognitive_services_account
                )
                cognitive_services_account_id = cognitive_services_account_dict.get(
                    "id"
                )
                cognitive_services_account_dict["location"] = (
                    cognitive_services_account_dict["location"].replace(" ", "").lower()
                )

                # update cognitive services dict
                cognitive_services_account_dict = (
                    self.update_tenant_id_from_secret_data(
                        cognitive_services_account_dict, secret_data
                    )
                )
                cognitive_services_account_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            cognitive_services_account_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": cognitive_services_account_id},
                    }
                )

                self.set_region_code(cognitive_services_account_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=cognitive_services_account_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=cognitive_services_account_dict,
                        account=secret_data["subscription_id"],
                        instance_type=cognitive_services_account_dict["sku"]["name"],
                        region_code=cognitive_services_account_dict["location"],
                        reference=self.make_reference(
                            cognitive_services_account_dict.get("id")
                        ),
                        tags=cognitive_services_account_dict.get("tags", {}),
                        data_format="dict",
                    )
                )

            except Exception as e:
                _LOGGER.error(
                    f"[create_cloud_service] Error {self.service} {e}", exc_info=True
                )
                error_responses.append(
                    make_error_response(
                        error=e,
                        provider=self.provider,
                        cloud_service_group=self.cloud_service_group,
                        cloud_service_type=self.cloud_service_type,
                    )
                )

        return cloud_services, error_responses
