import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.public_ip_prefixes.public_ip_prefixes_connector import (
    PublicIPPrefixesConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class PublicIPPrefixesManager(AzureBaseManager):
    cloud_service_group = "PublicIPPrefixes"
    cloud_service_type = "IPPrefix"
    service_code = "/Microsoft.Network/publicIPPrefixes"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Networking"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-public-ip-prefix.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        public_ip_prefixes_conn = PublicIPPrefixesConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        public_ip_prefixes_list = public_ip_prefixes_conn.list_all_public_ip_prefixes()

        for ip_address in public_ip_prefixes_list:

            try:
                ip_prefix_dict = self.convert_nested_dictionary(ip_address)
                ip_address_id = ip_prefix_dict["id"]

                ip_prefix_dict = self.update_tenant_id_from_secret_data(
                    ip_prefix_dict, secret_data
                )
                ip_prefix_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            ip_address_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": ip_address_id},
                    }
                )

                prefix_length = ip_prefix_dict.get("prefix_length")
                available_ip_address_count = self._get_available_ip_address_count(
                    prefix_length
                )

                ip_prefix_dict["available_ip_address_count_display"] = (
                    available_ip_address_count
                )

                self.set_region_code(ip_prefix_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=ip_prefix_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=ip_prefix_dict,
                        account=secret_data["subscription_id"],
                        instance_type=ip_prefix_dict["sku"]["name"],
                        tags=ip_prefix_dict.get("tags", {}),
                        region_code=ip_prefix_dict["location"],
                        reference=self.make_reference(ip_prefix_dict.get("id")),
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

    @staticmethod
    def _get_available_ip_address_count(prefix_length: int) -> int:
        return 2 ** (32 - prefix_length)
