import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.public_ip_addresses.public_ip_addresses_connector import PublicIPAddressesConnector
from plugin.connector.subscriptions.subscriptions_connector import SubscriptionsConnector
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger(__name__)


class PublicIPAddressesManager(AzureBaseManager):
    cloud_service_group = "PublicIPAddresses"
    cloud_service_type = "IPAddress"
    service_code = "/Microsoft.Network/publicIPAddresses"

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
            tags={
                "spaceone:icon": f"{ICON_URL}/azure-public-ip-address.svg"
            }
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        public_ip_addresses_conn = PublicIPAddressesConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(secret_data["subscription_id"])
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        public_ip_addresses_list = public_ip_addresses_conn.list_all_public_ip_addresses()

        for ip_address in public_ip_addresses_list:

            try:
                ip_address_dict = self.convert_nested_dictionary(ip_address)
                ip_address_id = ip_address_dict["id"]

                ip_address_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            ip_address_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": ip_address_id},
                    }
                )

                if ip_address_dict.get("ip_configuration") is not None:
                    associated_to = ip_address_dict["ip_configuration"]["id"].split("/")[8]

                    if associated_to:
                        ip_address_dict.update({"associated_to": associated_to})

                ip_address_dict = self.update_tenant_id_from_secret_data(
                    ip_address_dict, secret_data
                )

                self.set_region_code(ip_address_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=ip_address_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=ip_address_dict,
                        account=secret_data["subscription_id"],
                        instance_type=ip_address_dict["sku"]["name"],
                        tags=ip_address_dict.get("tags", {}),
                        region_code=ip_address_dict["location"],
                        reference=self.make_reference(ip_address_dict.get("id")),
                        data_format="dict"
                    )
                )

            except Exception as e:
                _LOGGER.error(f"[create_cloud_service] Error {self.service} {e}", exc_info=True)
                error_responses.append(
                    make_error_response(
                        error=e,
                        provider=self.provider,
                        cloud_service_group=self.cloud_service_group,
                        cloud_service_type=self.cloud_service_type,
                    )
                )

        return cloud_services, error_responses
