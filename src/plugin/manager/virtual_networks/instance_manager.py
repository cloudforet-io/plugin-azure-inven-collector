import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.connector.virtual_networks.virtual_networks_connector import (
    VirtualNetworksConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class VirtualNetworksManager(AzureBaseManager):
    cloud_service_group = "VirtualNetworks"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.Network/virtualNetworks"

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
            tags={"spaceone:icon": f"{ICON_URL}/azure-virtual-networks.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        virtual_networks_conn = VirtualNetworksConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        virtual_networks = virtual_networks_conn.list_all_virtual_networks()

        for virtual_network in virtual_networks:

            try:
                virtual_network_dict = self.convert_nested_dictionary(virtual_network)
                virtual_network_id = virtual_network_dict["id"]

                # update vnet_dict
                virtual_network_dict = self.update_tenant_id_from_secret_data(
                    virtual_network_dict, secret_data
                )
                virtual_network_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            virtual_network_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": virtual_network_id},
                    }
                )

                if virtual_network_dict.get("subnets") is not None:
                    subnets = virtual_network_dict["subnets"]
                    resource_group = virtual_network_dict["resource_group"]

                    # Change attached network interfaces objects to id
                    self.change_subnet_object_to_ids_list(subnets)

                    virtual_network_dict.update(
                        {
                            "subnets": self.update_subnet_info(subnets),
                            "service_endpoints": self.get_service_endpoints(subnets),
                            "private_endpoints": self.get_private_endpoints(subnets),
                            "azure_firewall": self.get_azure_firewall(
                                virtual_networks_conn, subnets, resource_group
                            ),
                            "connected_devices": self.get_connected_devices(subnets),
                        }
                    )

                # If not 'custom dns servers', add default azure dns server dict to vnet
                if virtual_network_dict.get("dhcp_options") is None:
                    dhcp_option_dict = {"dns_servers": ["Azure provided DNS service"]}
                    virtual_network_dict.update({"dhcp_options": dhcp_option_dict})

                self.set_region_code(virtual_network_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=virtual_network_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=virtual_network_dict,
                        account=virtual_network_dict["subscription_id"],
                        region_code=virtual_network_dict["location"],
                        reference=self.make_reference(virtual_network_dict.get("id")),
                        tags=virtual_network_dict.get("tags", {}),
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

    def get_azure_firewall(self, vnet_conn, subnet_list, resource_group_name):
        # Get Azure firewall information
        azure_firewall_list = []
        for subnet in subnet_list:
            if subnet.get("connected_devices_list"):
                for device in subnet["connected_devices_list"]:
                    if (
                        device["type"] == "azureFirewalls"
                    ):  # The subnet which has 'AzureFirewall' is typed as 'azureFirewalls'
                        firewall_obj = vnet_conn.list_all_firewalls(
                            resource_group_name
                        )  # List all firewalls in the resource group
                        for firewall in firewall_obj:
                            firewall_dict = self.convert_nested_dictionary(firewall)
                            for ip_configuration in firewall_dict["ip_configurations"]:
                                if ip_configuration.get("subnet") is not None:
                                    if (
                                        subnet["id"] in ip_configuration["subnet"]["id"]
                                    ):  # If subnet id matches the firewall's subnet id
                                        firewall_dict["subnet"] = subnet["id"].split(
                                            "/"
                                        )[10]
                                        azure_firewall_list.append(firewall_dict)

        return azure_firewall_list

    @staticmethod
    def change_subnet_object_to_ids_list(subnets_dict):
        subnet_id_list = []
        for subnet in subnets_dict:
            subnet_id_list.append(subnet["id"])
            if subnet.get("private_endpoints") is not None:
                for private_endpoint in subnet["private_endpoints"]:
                    if private_endpoint.get("network_interfaces") is not None:
                        for ni in private_endpoint["network_interfaces"]:
                            if ni.get("network_security_group") is not None:
                                ni["network_interfaces"] = ni["id"]
                                ni["subnets"] = subnet_id_list

        return subnet_id_list

    @staticmethod
    def update_subnet_info(subnet_list):
        for subnet in subnet_list:
            # Get network security group's name
            if subnet.get("network_security_group") is not None:
                subnet["network_security_group"]["name"] = subnet[
                    "network_security_group"
                ]["id"].split("/")[8]

            # Get private endpoints
            if subnet.get("private_endpoints") is not None:
                for private_endpoint in subnet["private_endpoints"]:
                    private_endpoint.update(
                        {
                            "name": private_endpoint["id"].split("/")[8],
                            "subnet": subnet["name"],
                            "resource_group": private_endpoint["id"].split("/")[4],
                        }
                    )

        return subnet_list

    @staticmethod
    def get_service_endpoints(subnet_list):
        service_endpoint_list = []
        for subnet in subnet_list:
            # Put subnet name to service endpoints dictionary
            if subnet.get("service_endpoints") is not None:
                for service_endpoint in subnet["service_endpoints"]:
                    service_endpoint["subnet"] = subnet["name"]
                    service_endpoint_list.append(service_endpoint)

        return service_endpoint_list

    @staticmethod
    def get_private_endpoints(subnet_list):
        private_endpoint_list = []
        for subnet in subnet_list:
            if subnet.get("private_endpoints") is not None:
                for private_endpoint in subnet["private_endpoints"]:
                    private_endpoint_list.append(private_endpoint)

        return private_endpoint_list

    @staticmethod
    def get_connected_devices(subnet_list):
        connected_devices_list = []
        for subnet in subnet_list:
            device_dict = {}

            if subnet.get("ip_configurations") is not None:
                for ip_configuration in subnet["ip_configurations"]:
                    device_dict["name"] = subnet["name"]
                    device_dict["type"] = ip_configuration["id"].split("/")[7]
                    device_dict["device"] = ip_configuration["id"].split("/")[8]
                    connected_devices_list.append(device_dict)

        return connected_devices_list
