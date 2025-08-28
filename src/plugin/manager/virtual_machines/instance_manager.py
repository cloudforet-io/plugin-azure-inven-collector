import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.connector.virtual_machines.virtual_machines_connector import (
    VirtualMachinesConnector,
)
from plugin.manager.base import AzureBaseManager
from plugin.manager.virtual_machines import (
    VirtualMachineDiskManager,
    VirtualMachineLoadBalancerManager,
    VirtualMachineNetworkSecurityGroupManager,
    VirtualMachineNICManager,
    VirtualMachineVmManager,
    VirtualMachineVNetManager,
)

_LOGGER = logging.getLogger("spaceone")


class VirtualMachinesManager(AzureBaseManager):
    cloud_service_group = "VirtualMachines"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.Compute/virtualMachines"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Compute", "Server"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-vm.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        vm_conn = VirtualMachinesConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        # call all managers
        vm_manager = VirtualMachineVmManager(vm_conn=vm_conn)
        disk_manager = VirtualMachineDiskManager()
        load_balancer_manager = VirtualMachineLoadBalancerManager()
        network_security_group_manager = VirtualMachineNetworkSecurityGroupManager()
        nic_manager = VirtualMachineNICManager()
        vnet_manager = VirtualMachineVNetManager()

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)
        subscription_data = {
            "subscription_id": secret_data["subscription_id"],
            "subscription_name": subscription_info["display_name"],
            "tenant_id": subscription_info["tenant_id"],
        }

        vms = list(vm_conn.list_all_vms())
        resource_groups = list(vm_conn.list_resource_groups())
        load_balancers = list(vm_conn.list_load_balancers())
        network_security_groups = list(vm_conn.list_network_security_groups())
        network_interfaces = list(vm_conn.list_network_interfaces())
        disks = list(vm_conn.list_disks())
        public_ip_addresses = list(vm_conn.list_public_ip_addresses())
        virtual_networks = list(vm_conn.list_virtual_networks())
        skus = list(vm_conn.list_skus())

        for vm in vms:
            try:
                vnet_data = None
                subnet_data = None
                lb_vos = []

                resource_group, resource_group_name = self.get_resource_info_in_vm(
                    vm, resource_groups
                )
                skus_dict = self.get_skus_resource(skus)

                disk_vos = disk_manager.get_disk_info(vm, disks)
                nic_vos, primary_ip = nic_manager.get_nic_info(
                    vm, network_interfaces, public_ip_addresses, virtual_networks
                )

                vm_resource = vm_manager.get_vm_info(
                    vm,
                    disk_vos,
                    nic_vos,
                    resource_group,
                    subscription_data["subscription_id"],
                    network_security_groups,
                    primary_ip,
                    skus_dict,
                )

                if load_balancers is not None:
                    lb_vos = load_balancer_manager.get_load_balancer_info(
                        vm, load_balancers, public_ip_addresses
                    )

                nsg_vos = (
                    network_security_group_manager.get_network_security_group_info(
                        vm, network_security_groups, network_interfaces
                    )
                )

                nic_name = vm.network_profile.network_interfaces[0].id.split("/")[-1]

                if nic_name is not None:
                    vnet_subnet_dict = vnet_manager.get_vnet_subnet_info(
                        nic_name, network_interfaces, virtual_networks
                    )

                    if vnet_subnet_dict.get("vnet_info"):
                        vnet_data = vnet_subnet_dict["vnet_info"]

                    if vnet_subnet_dict.get("subnet_info"):
                        subnet_data = vnet_subnet_dict["subnet_info"]

                # vm_resource.update({"tags": self.get_tags(vm.tags)})
                vm_resource.update({"tags": vm.tags})

                resource_id = f'/subscriptions/{subscription_data["subscription_id"]}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_resource["name"]}'

                # update vm_resource data
                vm_resource["data"].update(
                    {
                        "tenant_id": subscription_data["tenant_id"],
                        "subscription_name": subscription_data["subscription_name"],
                        "subscription_id": subscription_data["subscription_id"],
                        "resource_group": resource_group_name,
                    }
                )

                vm_resource["data"].update(
                    {
                        "load_balancer": lb_vos,
                        "security_group": nsg_vos,
                        "vnet": vnet_data,
                        "subnet": subnet_data,
                        "azure_monitor": {"resource_id": resource_id},
                        "activity_log": {"resource_uri": resource_id},
                    }
                )

                vm_resource["data"]["compute"]["account"] = subscription_data[
                    "subscription_name"
                ]

                self.set_region_code(vm_resource["region_code"])

                cloud_services.append(
                    make_cloud_service(
                        name=vm_resource["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=vm_resource["data"],
                        account=subscription_data["subscription_id"],
                        instance_type=vm_resource["data"]["compute"]["instance_type"],
                        ip_addresses=vm_resource["ip_addresses"],
                        region_code=vm_resource["region_code"],
                        reference=self.make_reference(
                            vm_resource["data"]["compute"]["instance_id"],
                            f"https://portal.azure.com/#@.onmicrosoft.com/resource/subscriptions/{subscription_data['subscription_id']}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_resource['data']['compute']['instance_name']}/overview",
                        ),
                        tags=vm_resource["tags"],
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

    # @staticmethod
    # def get_tags(tags):
    #     tags_result = []
    #     if tags:
    #         for k, v in tags.items():
    #             tags_result.append({"key": k, "value": v})
    #
    #     return tags_result

    @staticmethod
    def get_resource_info_in_vm(vm, resource_groups):
        for rg in resource_groups:
            vm_info = vm.id.split("/")
            for info in vm_info:
                if info == rg.name.upper():
                    resource_group = rg
                    resource_group_name = rg.name
                    return resource_group, resource_group_name

    @staticmethod
    def get_resources_in_resource_group(resources, resource_group_name):
        infos = []
        for resource in resources:
            id_info = resource.id.split("/")
            for info in id_info:
                if info == resource_group_name.upper():
                    infos.append(resource)
        return infos

    @staticmethod
    def get_skus_resource(skus):
        skus_dict = {}
        for sku in skus:
            if sku.resource_type == "virtualMachines":
                location = sku.locations[0].lower()
                if location not in skus_dict:
                    skus_dict[location] = []
                info = {}
                # get sku information for discriminating Instance type
                info.update(
                    {
                        "resource_type": sku.resource_type,
                        "name": sku.name,
                        "tier": sku.tier,
                        "size": sku.size,
                        "family": sku.family,
                    }
                )

                # get cpu and memory information
                for capa in sku.capabilities:
                    if capa.name == "vCPUs":
                        info["core"] = capa.value
                    elif capa.name == "MemoryGB":
                        info["memory"] = capa.value
                skus_dict[location].append(info)

        return skus_dict
