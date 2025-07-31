import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.network_security_groups.network_security_groups_connector import (
    NetworkSecurityGroupsConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class NetworkSecurityGroupsManager(AzureBaseManager):
    cloud_service_group = "NetworkSecurityGroups"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.Network/networkSecurityGroups"

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
            tags={"spaceone:icon": f"{ICON_URL}/azure-network-security-groups.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        network_security_groups_conn = NetworkSecurityGroupsConnector(
            secret_data=secret_data
        )
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        network_security_groups = (
            network_security_groups_conn.list_all_network_security_groups()
        )
        network_interfaces = [
            self.convert_nested_dictionary(ni)
            for ni in network_security_groups_conn.list_all_network_interfaces()
        ]

        for network_security_group in network_security_groups:

            try:
                network_security_group_dict = self.convert_nested_dictionary(
                    network_security_group
                )
                network_security_group_id = network_security_group_dict["id"]
                inbound_rules = []
                outbound_rules = []

                if network_security_group_dict.get("security_rules") is not None:
                    # update custom security rules
                    inbound, outbound = self.split_security_rules(
                        network_security_group_dict, "security_rules"
                    )
                    for ib in inbound:
                        inbound_rules.append(ib)
                    for ob in outbound:
                        outbound_rules.append(ob)

                # update default security rules
                if (
                    network_security_group_dict.get("default_security_rules")
                    is not None
                ):
                    inbound, outbound = self.split_security_rules(
                        network_security_group_dict, "default_security_rules"
                    )
                    for ib in inbound:
                        inbound_rules.append(ib)
                    for ob in outbound:
                        outbound_rules.append(ob)

                network_security_group_dict.update(
                    {
                        "inbound_security_rules": inbound_rules,
                        "outbound_security_rules": outbound_rules,
                    }
                )

                #  TODO : update network interface name
                """
                # get network interfaces
                if network_security_group_dict.get('network_interfaces') is not None:
                    new_network_interfaces_list, virtual_machines_display_str = self.get_network_interfaces(self, network_security_group_conn, network_security_group_dict['network_interfaces'])
                    network_security_group_dict['network_interfaces'] = new_network_interfaces_list  # Remove existing list, append new list
                    network_security_group_dict.update({
                        'virtual_machines_display': virtual_machines_display_str
                    })
                """

                virtual_machines_display_str = self.get_virtual_machine_name(
                    network_interfaces, network_security_group_id
                )
                if virtual_machines_display_str is not None:
                    network_security_group_dict.update(
                        {"virtual_machines_display": virtual_machines_display_str}
                    )

                # Change Subnet models to ID
                if network_security_group_dict.get("network_interfaces") is not None:
                    self.replace_subnet_model_to_id(
                        network_security_group_dict["network_interfaces"]
                    )

                # Get private ip address and public ip address
                if network_security_group_dict.get("network_interfaces") is not None:
                    self.get_ip_addresses(
                        network_security_group_dict["network_interfaces"]
                    )

                # Get Subnet information
                if network_security_group_dict.get("subnets") is not None:
                    network_security_group_dict["subnets"] = self.get_subnet(
                        network_security_groups_conn,
                        network_security_group_dict["subnets"],
                    )
                    if network_security_group_dict.get("subnets"):
                        for subnet in network_security_group_dict["subnets"]:
                            subnet.update(
                                {
                                    "virtual_network": self.get_virtual_network(
                                        subnet["id"]
                                    )
                                }
                            )

                # update application_gateway_dict
                network_security_group_dict = self.update_tenant_id_from_secret_data(
                    network_security_group_dict, secret_data
                )
                network_security_group_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            network_security_group_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": network_security_group_id},
                    }
                )

                self.set_region_code(network_security_group_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=network_security_group_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=network_security_group_dict,
                        account=secret_data["subscription_id"],
                        region_code=network_security_group_dict["location"],
                        reference=self.make_reference(
                            network_security_group_dict.get("id")
                        ),
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

    def get_network_interfaces(
        self, network_security_group_conn, network_interfaces_list
    ):
        network_interfaces_new_list = []
        virtual_machines_display_list = []
        virtual_machines_str = ""

        for network_interface in network_interfaces_list:
            resource_group = network_interface["id"].split("/")[4]
            network_interface_name = network_interface["id"].split("/")[
                8
            ]  # TODO : network interface name diverse
            network_interface_obj = network_security_group_conn.get_network_interfaces(
                network_interface_name, resource_group
            )
            network_interface_dict = self.convert_nested_dictionary(
                network_interface_obj
            )

            if network_interface_dict["id"] == network_interface["id"]:
                # Get virtual machine display
                if network_interface_dict.get("virtual_machine") is not None:
                    virtual_machine_display = network_interface_dict["virtual_machine"][
                        "id"
                    ].split("/")[8]
                    virtual_machines_display_list.append(virtual_machine_display)
                    network_interface_dict.update(
                        {"virtual_machine_display": virtual_machine_display}
                    )
                network_interfaces_new_list.append(network_interface_dict)
                virtual_machines_str = ", ".join(virtual_machines_display_list)

        return network_interfaces_new_list, virtual_machines_str

    def get_subnet(self, network_security_group_conn, subnets_list):
        subnets_full_list = []
        if subnets_list:
            for subnet in subnets_list:
                resource_group_name = subnet["id"].split("/")[4]
                subnet_name = subnet["id"].split("/")[10]
                virtual_network_name = subnet["id"].split("/")[8]

                subnet_obj = network_security_group_conn.get_subnet(
                    resource_group_name, subnet_name, virtual_network_name
                )
                subnet_dict = self.convert_nested_dictionary(subnet_obj)
                subnets_full_list.append(subnet_dict)

            return subnets_full_list
        return

    @staticmethod
    def split_security_rules(network_security_group_dict, mode):
        inbound_security_rules = []
        outbound_security_rules = []
        rule_list = []

        if mode == "security_rules":
            rule_list = network_security_group_dict["security_rules"]
        elif mode == "default_security_rules":
            rule_list = network_security_group_dict["default_security_rules"]

        for security_rule in rule_list:
            if security_rule.get("direction", "") == "Inbound":
                inbound_security_rules.append(security_rule)
            elif security_rule.get("direction", "") == "Outbound":
                outbound_security_rules.append(security_rule)

        return inbound_security_rules, outbound_security_rules

    @staticmethod
    def replace_subnet_model_to_id(network_interfaces_list):
        for network_interface in network_interfaces_list:
            if network_interface.get("ip_configurations") is not None:
                for ip_configuration in network_interface["ip_configurations"]:
                    ip_configuration["subnet"] = ip_configuration.get("subnet", {}).get(
                        "id", ""
                    )
        return

    @staticmethod
    def get_ip_addresses(network_interfaces_list):
        if network_interfaces_list:
            for network_interface in network_interfaces_list:
                if network_interface.get("ip_configurations") is not None:
                    for ip_configuration in network_interface["ip_configurations"]:
                        private_ip_address = ip_configuration["private_ip_address"]
                        network_interface.update(
                            {"private_ip_address": private_ip_address}
                        )

                        if ip_configuration.get("public_ip_address") is not None:
                            public_ip_address = ip_configuration["public_ip_address"][
                                "id"
                            ].split("/")[8]
                            network_interface.update(
                                {
                                    "public_ip_address": public_ip_address,
                                }
                            )
        return

    @staticmethod
    def get_virtual_network(subnet_id):
        virtual_network = subnet_id.split("/")[8]
        return virtual_network

    @staticmethod
    def get_virtual_machine_name(
        network_interfaces: list, network_security_group_id: str
    ):
        virtual_machine_name = None
        for network_interface_info in network_interfaces:
            if _network_security_group := network_interface_info.get(
                "network_security_group"
            ):
                if _network_security_group["id"].split("/")[
                    -1
                ] == network_security_group_id.split("/")[-1] and (
                    _virtual_machine := network_interface_info.get("virtual_machine")
                ):
                    virtual_machine_name = _virtual_machine["id"].split("/")[-1]
                    return virtual_machine_name
        return virtual_machine_name
