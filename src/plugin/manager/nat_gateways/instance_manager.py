import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.nat_gateways.nat_gateways_connector import NATGatewaysConnector
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class NATGatewaysManager(AzureBaseManager):
    cloud_service_group = "NATGateways"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.Network/natGateways"

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
            tags={"spaceone:icon": f"{ICON_URL}/azure-nat.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        nat_gateways_conn = NATGatewaysConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        nat_gateways = nat_gateways_conn.list_all_nat_gateways()

        for nat_gateway in nat_gateways:

            try:
                nat_gateway_dict = self.convert_nested_dictionary(nat_gateway)
                nat_gateway_id = nat_gateway_dict["id"]

                if (
                    sku_tier := nat_gateway_dict["sku"]
                    .get("additional_properties")
                    .get("tier")
                ):
                    nat_gateway_dict["sku"]["tier"] = sku_tier

                nat_gateway_dict = self.update_tenant_id_from_secret_data(
                    nat_gateway_dict, secret_data
                )

                # update application_gateway_dict
                nat_gateway_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            nat_gateway_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": nat_gateway_id},
                    }
                )

                if nat_gateway_dict.get("public_ip_addresses") is not None:
                    # Get Count of Public IP Address
                    nat_gateway_dict.update(
                        {
                            "public_ip_addresses_count": len(
                                nat_gateway_dict["public_ip_addresses"]
                            )
                        }
                    )

                    # Get Public IP Address Dictionary
                    if not nat_gateway_dict["public_ip_addresses"]:
                        break

                    pip_list = []

                    for pip in nat_gateway_dict["public_ip_addresses"]:
                        public_ip_prefixes_id = pip["id"]
                        pip_dict = self.get_public_ip_address_dict(
                            nat_gateways_conn, public_ip_prefixes_id
                        )
                        pip_list.append(pip_dict)

                    nat_gateway_dict["public_ip_addresses"] = pip_list

                else:
                    nat_gateway_dict.update({"public_ip_addresses_count": 0})

                if nat_gateway_dict.get("public_ip_prefixes") is not None:
                    nat_gateway_dict.update(
                        {
                            "public_ip_prefixes_count": len(
                                nat_gateway_dict["public_ip_addresses"]
                            )
                        }
                    )

                    # Get Public IP Address Dictionary
                    if not nat_gateway_dict["public_ip_prefixes"]:
                        break

                    pip_list = []

                    for pip in nat_gateway_dict["public_ip_prefixes"]:
                        public_ip_prefixes_id = pip["id"]
                        pip_dict = self.get_public_ip_prefixes_dict(
                            nat_gateways_conn, public_ip_prefixes_id
                        )
                        pip_list.append(pip_dict)

                    nat_gateway_dict["public_ip_prefixes"] = pip_list

                else:
                    nat_gateway_dict.update({"public_ip_prefixes_count": 0})

                if nat_gateway_dict.get("subnets") is not None:
                    nat_gateway_dict.update(
                        {
                            "subnets": self.get_subnets(
                                nat_gateways_conn, nat_gateway_dict["subnets"]
                            ),
                            "subnets_count": len(nat_gateway_dict["subnets"]),
                        }
                    )
                else:
                    nat_gateway_dict.update({"subnets_count": 0})

                self.set_region_code(nat_gateway_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=nat_gateway_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=nat_gateway_dict,
                        account=nat_gateway_dict["subscription_id"],
                        instance_type=nat_gateway_dict["sku"]["name"],
                        region_code=nat_gateway_dict["location"],
                        reference=self.make_reference(nat_gateway_dict.get("id")),
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

    def get_public_ip_address_dict(self, nat_gateway_conn, pip_id):
        pip_name = pip_id.split("/")[8]
        resource_group_name = pip_id.split("/")[4]
        pip_obj = nat_gateway_conn.get_public_ip_addresses(
            resource_group_name=resource_group_name, public_ip_address_name=pip_name
        )
        pip_dict = self.convert_nested_dictionary(pip_obj)
        return pip_dict

    def get_public_ip_prefixes_dict(self, nat_gateway_conn, pip_id):
        pip_name = pip_id.split("/")[8]
        resource_group_name = pip_id.split("/")[4]
        pip_obj = nat_gateway_conn.get_public_ip_prefixes(
            resource_group_name=resource_group_name, public_ip_prefixes_name=pip_name
        )

        pip_dict = self.convert_nested_dictionary(pip_obj)
        return pip_dict

    def get_subnets(self, nat_gateway_conn, subnets):
        subnet_list = []

        for subnet in subnets:
            resource_group_name = subnet["id"].split("/")[4]
            subnet_name = subnet["id"].split("/")[10]
            vnet_name = subnet["id"].split("/")[8]

            subnet_obj = nat_gateway_conn.get_subnet(
                resource_group_name=resource_group_name,
                subnet_name=subnet_name,
                vnet_name=vnet_name,
            )
            subnet_dict = self.convert_nested_dictionary(subnet_obj)
            subnet_dict.update({"virtual_network": vnet_name})

            subnet_list.append(subnet_dict)

        return subnet_list
