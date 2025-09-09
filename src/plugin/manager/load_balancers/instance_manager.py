import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.load_balancers.load_balancers_connector import (
    LoadBalancersConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class LoadBalancersManager(AzureBaseManager):
    cloud_service_group = "LoadBalancers"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.Network/loadBalancers"

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
            tags={"spaceone:icon": f"{ICON_URL}/azure-loadbalancers.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        load_balancers_conn = LoadBalancersConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        load_balancers = load_balancers_conn.list_load_balancers()

        for load_balancer in load_balancers:

            try:
                load_balancer_dict = self.convert_nested_dictionary(load_balancer)
                load_balancer_dict = self.update_tenant_id_from_secret_data(
                    load_balancer_dict, secret_data
                )

                load_balancer_id = load_balancer_dict["id"]

                load_balancer_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            load_balancer_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": load_balancer_id},
                    }
                )

                # Get Network Interfaces attached in this load balancer
                load_balancer_dict.update(
                    {
                        "network_interfaces": self.get_network_interfaces(
                            load_balancers_conn,
                            load_balancer_dict["resource_group"],
                            load_balancer_dict["name"],
                        )
                    }
                )

                # Get Frontend IP Configurations information
                if load_balancer_dict.get("frontend_ip_configurations") is not None:
                    private_ip_address_list = list()
                    used_by_list = list()

                    for fic in load_balancer_dict["frontend_ip_configurations"]:
                        if fic.get(
                            "subnet"
                        ):  # If the 'public' type, Skip this part because there isn't subnet information for them.
                            fic["subnet"]["address_prefix"] = (
                                self.get_frontend_address_prefix(
                                    load_balancers_conn, fic["subnet"]
                                )
                            )
                            fic["subnet"]["name"] = self.get_frontend_ip_subnet_name(
                                fic["subnet"]["id"]
                            )

                        # Get used inbound NAT rules
                        if fic.get("inbound_nat_rules") is not None:
                            load_balancer_dict.update(
                                {
                                    "frontend_ip_configurations_used_by_display": self.get_frontend_ip_configurations_used_by_display(
                                        used_by_list, fic["inbound_nat_rules"]
                                    )
                                }
                            )

                        # Get used load balancing NAT rules
                        if fic.get("load_balancing_rules") is not None:
                            load_balancer_dict.update(
                                {
                                    "frontend_ip_configurations_used_by_display": self.get_frontend_ip_configurations_used_by_display(
                                        used_by_list, fic["load_balancing_rules"]
                                    ),
                                }
                            )

                        # Get all of private ip addresses
                        private_ip = fic.get("private_ip_address")

                        if private_ip is not None:
                            private_ip_address_list.append(private_ip)

                # Since Azure python sdk returns only one backend pool, delete the backend pool list first, and then use the new API connection
                if load_balancer_dict.get("backend_address_pools") is not None:
                    load_balancer_dict["backend_address_pools"].clear()
                    load_balancer_dict.update(
                        {
                            "backend_address_pools": self.list_load_balancer_backend_address_pools(
                                load_balancers_conn,
                                load_balancer_dict["resource_group"],
                                load_balancer_dict["name"],
                            )
                        }
                    )

                    # get backend address pool's count
                    load_balancer_dict.update(
                        {
                            "backend_address_pools_count_display": self.get_backend_address_pools_count(
                                load_balancer_dict["backend_address_pools"]
                            )
                        }
                    )

                # Get load balancing Rules for display
                if load_balancer_dict.get("load_balancing_rules") is not None:
                    load_balancer_dict.update(
                        {
                            "load_balancing_rules_display": self.get_load_balancing_rules_display(
                                load_balancer_dict["load_balancing_rules"]
                            ),
                        }
                    )

                    for lbr in load_balancer_dict["load_balancing_rules"]:
                        if lbr.get("backend_address_pool") is not None:
                            lbr.update(
                                {
                                    "backend_address_pool_display": self.get_backend_address_pool_name(
                                        lbr["backend_address_pool"]
                                    ),
                                }
                            )

                        if lbr.get("load_distribution") is not None:
                            lbr.update(
                                {
                                    "load_distribution_display": self.get_load_distribution_display(
                                        lbr["load_distribution"]
                                    )
                                }
                            )

                        if lbr.get("frontend_ip_configuration") is not None:
                            lbr.update(
                                {
                                    "frontend_ip_configuration_display": self.get_frontend_ip_configuration_display(
                                        lbr["frontend_ip_configuration"]
                                    )
                                }
                            )

                # Get Inbound NAT Rules for display
                if load_balancer_dict.get("inbound_nat_rules") is not None:
                    load_balancer_dict.update(
                        {
                            "inbound_nat_rules_display": self.get_nat_rules_display(
                                load_balancer_dict["inbound_nat_rules"]
                            )
                        }
                    )

                    for inr in load_balancer_dict["inbound_nat_rules"]:
                        inr.update(
                            {
                                "frontend_ip_configuration_display": self.get_frontend_ip_configuration_display(
                                    inr["frontend_ip_configuration"]
                                ),
                                "port_mapping_display": self.get_port_mapping_display(
                                    inr["frontend_port"], inr["backend_port"]
                                ),
                                "target_virtual_machine": self.get_matched_vm_info(
                                    inr["backend_ip_configuration"]["id"],
                                    load_balancer_dict["network_interfaces"],
                                ),
                            }
                        )

                # Get Health Probes for display
                if load_balancer_dict.get("probes") is not None:
                    load_balancer_dict.update(
                        {
                            "probes_display": self.get_probe_display_list(
                                load_balancer_dict["probes"]
                            )
                        }
                    )

                self.set_region_code(load_balancer_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=load_balancer_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=load_balancer_dict,
                        account=load_balancer_dict["subscription_id"],
                        instance_type=load_balancer_dict["sku"]["name"],
                        region_code=load_balancer_dict["location"],
                        reference=self.make_reference(load_balancer_dict.get("id")),
                        tags=load_balancer_dict.get("tags", {}),
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

    def get_network_interfaces(self, load_balancer_conn, rg_name, lb_name):
        network_interface_object_list = list(
            load_balancer_conn.list_load_balancer_network_interfaces(rg_name, lb_name)
        )
        network_interface_list = []

        # network_interfaces >> network_interfaces >> ip_configurations
        for nil in network_interface_object_list:
            network_interface_dict = self.convert_nested_dictionary(nil)
            nic_rg_name = network_interface_dict.get("id", "").split("/")[4]

            if network_interface_dict.get("ip_configurations") is not None:
                # Get LB's name, VMs name attached to Backend Pool
                for ip_configuration in network_interface_dict["ip_configurations"]:
                    if (
                        ip_configuration.get("load_balancer_backend_address_pools")
                        is not None
                    ):
                        for ic in ip_configuration[
                            "load_balancer_backend_address_pools"
                        ]:
                            # Get backend address vm name
                            backend_pool_vm_name = ic["id"].split("/")[10]

                        network_interface_dict.update(
                            {
                                "load_balancer_backend_address_pools_name_display": backend_pool_vm_name,
                            }
                        )

                # Get the primary ip configuration from a network interface card
                network_interface_dict.update(
                    {
                        "private_ip_display": self.get_ip_configuration_display(
                            network_interface_dict["ip_configurations"]
                        )
                    }
                )

            # 2) Get VM's name which is attached to this network interface card
            if network_interface_dict.get("virtual_machine") is not None:
                network_interface_dict.update(
                    {
                        "virtual_machine_name_display": network_interface_dict[
                            "virtual_machine"
                        ]["id"].split("/")[8]
                    }
                )

            network_interface_list.append(network_interface_dict)

        return network_interface_list

    def get_ip_configurations_list(
        self, load_balancer_conn, rg_name, network_interface_name
    ):
        ip_configuration_list = []
        if network_interface_name:
            ip_configurations_object = (
                load_balancer_conn.list_network_interface_ip_configurations(
                    rg_name, network_interface_name
                )
            )
            ip_configurations_object_list = list(ip_configurations_object)

            if ip_configurations_object_list:
                for ip_configuration_object in ip_configurations_object_list:
                    ip_object_dict = self.convert_nested_dictionary(
                        ip_configuration_object
                    )
                    ip_configuration_list.append(ip_object_dict)

        return ip_configuration_list

    def list_load_balancer_backend_address_pools(self, conn, rg_name, lb_name):
        backend_pools_list = list()  # return result list

        backend_pools_object = conn.list_load_balancer_backend_address_pools(
            rg_name, lb_name
        )
        backend_pools_object_list = list(
            backend_pools_object
        )  # Since return type is ItemPagedClass, change to the list before convert dictionary

        # Loop for converting backend pools objects to dictionary
        for bp in backend_pools_object_list:
            backend_pool_dict = self.convert_nested_dictionary(bp)
            backend_pools_list.append(backend_pool_dict)

        return backend_pools_list

    @staticmethod
    def get_ip_configuration_display(ip_configurations_list):
        ic_list = list()
        for ic in ip_configurations_list:
            ic_list.append(ic["private_ip_address"])
        return ic_list

    @staticmethod
    def get_frontend_address_prefix(conn, subnet):
        # Parse Vnet, LB name from subnet id
        subnet_id = subnet["id"]
        resource_group_name = subnet_id.split("/")[4]
        vnet_name = subnet_id.split("/")[8]
        subnet_name = subnet_id.split("/")[10]

        # API request for subnet dictionary
        subnet = conn.get_subnets(resource_group_name, vnet_name, subnet_name)

        return subnet.address_prefix

    @staticmethod
    def get_frontend_ip_subnet_name(subnet_id):
        subnet_name = subnet_id.split("/")[10]
        return subnet_name

    @staticmethod
    def get_frontend_ip_configurations_used_by_display(used_by_list, used_object_list):
        for used_object in used_object_list:
            used_by_list.append(used_object["id"].split("/")[10])

        return used_by_list

    @staticmethod
    def get_backend_address_pools_count(backend_address_dict):
        backend_address_pools_count = len(backend_address_dict)

        if backend_address_pools_count == 1:
            backend_address_pools_count_display = (
                str(backend_address_pools_count) + " backend pool"
            )
        else:
            backend_address_pools_count_display = (
                str(backend_address_pools_count) + " backend pools"
            )

        return backend_address_pools_count_display

    @staticmethod
    def get_matched_vm_info(find_key, find_list_pool):
        matched_vm_list = list()
        for find_object in find_list_pool:
            if (
                find_object["id"] in find_key
            ):  # if network interface card's id matches to the backend configuration's id
                if find_object.get("virtual_machine") is not None:
                    matched_vm_list.append(
                        (find_object["virtual_machine"]["id"]).split("/")[8]
                    )
        return matched_vm_list

    @staticmethod
    def get_probe_display_list(probes_list):
        probe_display_list = list()
        for probe in probes_list:
            probe_display_list.append(probe["name"])
        return probe_display_list

    @staticmethod
    def get_load_balancing_rules_display(load_balancing_rules_list):
        lbr_name_list = list()
        for lbr in load_balancing_rules_list:
            lbr_name_list.append(
                lbr["name"]
            )  # 'name' key always exists if there are load balancing rules.

        return lbr_name_list

    @staticmethod
    def get_nat_rules_display(inbound_nat_rules_list):
        nat_rules_list = list()
        for inr in inbound_nat_rules_list:
            nat_rules_list.append(
                inr["name"]
            )  # 'name' key always exists if there are inbound NAT rules.

        return nat_rules_list

    @staticmethod
    def get_backend_address_pool_name(
        lbr_backend_address_pool,
    ):  # id must exist if there is a backend address pool object
        return lbr_backend_address_pool["id"].split("/")[10]

    @staticmethod
    def get_load_distribution_display(lbr_load_distribution):
        if lbr_load_distribution == "Default":
            lbr_load_distribution_display = "None"
        elif lbr_load_distribution == "SourceIPProtocol":
            lbr_load_distribution_display = "Client IP and Protocol"
        elif lbr_load_distribution == "SourceIP":
            lbr_load_distribution_display = "Client IP"

        return lbr_load_distribution_display

    @staticmethod
    def get_frontend_ip_configuration_display(lbr_frontend_ip_configuration_dict):
        return lbr_frontend_ip_configuration_dict["id"].split("/")[10]

    @staticmethod
    def get_port_mapping_display(frontend_port, backend_port):
        if frontend_port == backend_port:
            port_mapping_display = "Default"
        else:
            port_mapping_display = "Custom"
        return port_mapping_display
