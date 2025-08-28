from plugin.connector.virtual_machines.virtual_machines_connector import (
    VirtualMachinesConnector,
)


class VirtualMachineVmManager:
    def __init__(self, vm_conn):
        self.vm_conn: VirtualMachinesConnector = vm_conn

    def get_vm_info(
        self,
        vm,
        disks,
        nics,
        resource_group,
        subscription,
        network_security_groups,
        primary_ip,
        skus_dict,
    ):
        """
        server_data = {
            "name": ""
            "ip_addresses": [],
            "data":  {
                "primary_ip_address": "",
                "os": {
                    "os_distro": "",
                    "os_arch": "",
                    "os_details": "",
                    "os_type": "LINUX" | "WINDOWS"
                },
                "azure": {
                    "boot_diagnostics": "true" | "false",
                    "ultra_ssd_enabled": "true" | "false",
                    "write_accelerator_enabled": "true" | "false",
                    "priority": "Regular" | "Low" | "Spot",
                    "tags": {
                        "key": "",
                        "value": ""
                    },
                },
                "hardware": {
                    "core": 0,
                    "memory": 0
                },
                "compute": {
                    "keypair": "",
                    "availability_zone": "",
                    "instance_state": "",
                    "instance_type": "",
                    "launched_at": "datetime",
                    "instance_id": "",
                    "instance_name": "",
                    "security_groups": [
                        {
                            "id": "",
                            "name": "",
                            "display": ""
                        },
                        ...
                    ],
                    "image": "",
                    "account": "",
                    "tags": {
                        "id": ""
                    }
                },
                "nics": [
                    {  nics_info },
                    ...
                ],
                "disks": [
                    {  disk_info },
                    ...
                ]
            }
        }
        """

        resource_group_name = resource_group.name

        vm_dict = self.get_vm_dict(vm, nics)
        os_data = self.get_os_data(vm.storage_profile)
        azure_data = self.get_azure_data(vm)
        compute_data = self.get_compute_data(
            vm, resource_group_name, network_security_groups, subscription
        )
        resource_group_data = self.get_resource_group_data(resource_group)
        hardware_data = self.get_hardware_data(vm, skus_dict, compute_data)

        vm_dict.update(
            {
                "data": {
                    "os": os_data,
                    "hardware": hardware_data,
                    "azure": azure_data,
                    "compute": compute_data,
                    "resource_group": resource_group_data,
                    "disks": disks,
                    "nics": nics,
                    "primary_ip_address": self.get_primary_ip_address(primary_ip),
                }
            }
        )

        return vm_dict

    def get_vm_dict(self, vm, nic_vos):
        vm_data = {
            "name": vm.name,
            "region_code": vm.location,
            "ip_addresses": self.get_ip_addresses(nic_vos),
        }
        return vm_data

    def get_os_data(self, vm_storage_profile):
        try:
            if vm_storage_profile.image_reference is not None:
                offer = vm_storage_profile.image_reference.offer
                os_type = self.get_os_type(vm_storage_profile.os_disk)
                image_reference = vm_storage_profile.image_reference

                if os_type and offer is not None:
                    return {
                        "os_distro": self.get_os_distro(os_type, offer),
                        "details": self.get_os_details(image_reference),
                        "os_type": os_type,
                    }
                else:
                    return {
                        "os_distro": vm_storage_profile.os_disk.os_type,
                        # "details": self.get_os_details(image_reference),
                        "os_type": os_type,
                    }

        except Exception as e:
            print(f"[ERROR: GET OS Data]: {e}")

        return None

    def get_compute_data(
        self, vm, resource_group_name, network_security_groups, subscription_id
    ):
        vm_info = self.vm_conn.get_vm(resource_group_name, vm.name)
        compute_data = {
            # 'keypair': self.get_keypair(vm.os_profile.linux_configuration),
            "keypair": "",  # TODO: not implemented yet
            "instance_state": self.get_instance_state(vm_info.instance_view.statuses),
            "instance_type": vm.hardware_profile.vm_size,
            "launched_at": self.get_launched_time(vm_info.instance_view.statuses),
            "instance_id": vm.id,
            "instance_name": vm.name,
            "security_groups": self.get_security_groups(
                vm.network_profile.network_interfaces, network_security_groups
            ),
            "image": self.get_image_detail(
                vm.location, vm.storage_profile.image_reference, subscription_id
            ),
            "tags": {"vm_id": vm.vm_id},
        }

        if vm.zones:
            compute_data.update({"az": f"{vm.location}-{vm.zones[0]}"})
        else:
            compute_data.update({"az": vm.location})

        return compute_data

    def get_azure_data(self, vm):
        azure_data = {
            "ultra_ssd_enabled": self.get_ultra_ssd_enabled(vm.additional_capabilities),
            "write_accelerator_enabled": self.get_write_accelerator_enabled(
                vm.storage_profile.os_disk
            ),
            "priority": self.get_vm_priority(vm),
            "tags": self.get_tags(vm.tags),
        }

        if (
            getattr(vm, "diagnostics_profile")
            and getattr(vm.diagnostics_profile, "boot_diagnostics")
            and vm.diagnostics_profile.boot_diagnostics
        ):
            azure_data.update(
                {
                    "boot_diagnostics": self.get_boot_diagnostics(
                        vm.diagnostics_profile.boot_diagnostics
                    )
                }
            )

        return azure_data

    def get_vm_size(self, location):
        return self.vm_conn.list_virtual_machine_sizes(location)

    @staticmethod
    def get_hardware_data(vm, skus_dict, compute_data):
        """
        skus_dict = [
            {
                'memory': '0.75',
                'family': 'basicAFamily',
                'name': 'Basic_A0',
                'resource_type': 'virtualMachines',
                'size': 'A0',
                'tier': 'Basic',
                'core': '1'},
            },
        ]
        """

        location = vm.location.lower()
        instance_type = compute_data["instance_type"]

        hardware_data = []
        for sku in skus_dict[location]:
            if sku["name"] == instance_type:
                hardware_data = sku.copy()
                if "core" in hardware_data:
                    hardware_data["core"] = float(hardware_data["core"])
                if "memory" in hardware_data:
                    hardware_data["memory"] = float(hardware_data["memory"])
                break
        return hardware_data

    def get_os_distro(self, os_type, offer):
        return self.extract_os_distro(os_type, offer)

    @staticmethod
    def get_write_accelerator_enabled(os_disk):
        if hasattr(
            os_disk.write_accelerator_enabled, "os_disk.write_accelerator_enabled"
        ):
            return os_disk.write_accelerator_enabled
        return False

    @staticmethod
    def get_boot_diagnostics(boot_diagnostics):
        if hasattr(boot_diagnostics.enabled, "boot_diagnostics.enabled"):
            return boot_diagnostics.enabled
        return True

    @staticmethod
    def get_keypair(linux_configuration):
        if hasattr(linux_configuration, "ssh") and linux_configuration.ssh:
            key = linux_configuration.ssh.public_keys[0]

            return key.path.split("/")[2]
        return ""

    @staticmethod
    def get_ip_addresses(nic_vos):
        ip_addrs = []
        for nic_vo in nic_vos:
            ip_addrs.extend(nic_vo.get("ip_addresses"))

            if nic_vo["public_ip_address"]:
                ip_addrs.append(nic_vo.get("public_ip_address"))

        return list(set(ip_addrs))

    @staticmethod
    def get_primary_ip_address(primary_ip):
        for key, value in primary_ip.items():
            if value:
                return key

        return ""

    @staticmethod
    def get_vm_priority(vm):
        if hasattr(vm, "priority") and vm.priority:
            return vm.priority
        else:
            return "Regular"

    @staticmethod
    def get_vm_hardware_info(list_sizes, size):
        result = {}
        for list_size in list_sizes:
            if list_size.name == size:
                result.update(
                    {
                        "core": list_size.number_of_cores,
                        "memory": round(float(list_size.memory_in_mb / 1024), 2),
                    }
                )
                break

        return result

    @staticmethod
    def get_security_groups(vm_network_interfaces, network_security_groups):
        security_groups = []
        nic_names = []

        if vm_network_interfaces is None:
            vm_network_interfaces = []

        for vm_nic in vm_network_interfaces:
            nic_name = vm_nic.id.split("/")[-1]
            nic_names.append(nic_name)

        for nsg in network_security_groups:
            network_interfaces = nsg.network_interfaces
            if network_interfaces:
                for nic in network_interfaces:
                    nic_name2 = nic.id.split("/")[-1]
                    for nic_name in nic_names:
                        if nic_name == nic_name2:
                            nsg_data = {
                                "display": nsg.name,
                                "id": nsg.id,
                                "name": nsg.name,
                            }
                            security_groups.append(nsg_data)
                            break
                    break
        if len(security_groups) > 0:
            return security_groups
        return None

    @staticmethod
    def get_launched_time(statuses):
        if statuses is None:
            statuses = []

        for status in statuses:
            if status.display_status == "Provisioning succeeded":
                return status.time.isoformat()

        return None

    @staticmethod
    def get_instance_state(statuses):
        try:
            if statuses:
                return statuses[-1].code.split("/")[-1].upper()
        except Exception:
            pass

        return None

    @staticmethod
    def get_resource_group_data(resource_group):
        resource_group_data = {
            "resource_group_name": resource_group.name,
            "resource_group_id": resource_group.id,
        }
        return resource_group_data

    @staticmethod
    def get_ultra_ssd_enabled(additional_capabilities):
        if additional_capabilities:
            return additional_capabilities.ultra_ssd_enabled
        else:
            return False

    @staticmethod
    def get_os_type(os_disk):
        if os_disk.os_type is not None:
            return os_disk.os_type.upper()

    @staticmethod
    def extract_os_distro(os_type, offer):
        if offer is not None and os_type is not None:
            try:
                offer.lower()

                if os_type == "LINUX":
                    os_map = {
                        "suse": "suse",
                        "rhel": "redhat",
                        "centos": "centos",
                        "cent": "centos",
                        "fedora": "fedora",
                        "ubuntu": "ubuntu",
                        "ubuntuserver": "ubuntu",
                        "oracle": "oraclelinux",
                        "oraclelinux": "oraclelinux",
                        "debian": "debian",
                    }

                    for key in os_map:
                        if key in offer:
                            return os_map[key]

                    return "linux"

                elif os_type == "WINDOWS":
                    os_distro_string = None
                    offer_splits = offer.split("-")

                    version_cmps = ["2016", "2019", "2012"]

                    for cmp in version_cmps:
                        if cmp in offer_splits:
                            os_distro_string = f"win{cmp}"

                    if os_distro_string is not None and "R2_RTM" in offer_splits:
                        os_distro_string = f"{os_distro_string}r2"

                    if os_distro_string is None:
                        os_distro_string = "windows"

                    return os_distro_string

            except Exception as e:
                print(f"[ERROR: Cannot extract os distro info]: {e}")

    @staticmethod
    def get_os_details(image_reference):
        if image_reference:
            publisher = image_reference.publisher
            offer = image_reference.offer
            sku = image_reference.sku
            if publisher and offer and sku:
                os_details = f"{publisher}, {offer}, {sku}"
                return os_details

        return None

    @staticmethod
    def get_image_detail(location, image_reference, subscription_id):
        publisher = getattr(image_reference, "publisher", None)
        offer = getattr(image_reference, "offer", None)
        sku = getattr(image_reference, "sku", None)
        version = getattr(image_reference, "exact_version", None)

        if publisher and offer and sku and version:
            image_detail = (
                f"/Subscriptions/{subscription_id}/Providers/Microsoft.Compute/Locations/{location}"
                f"/Publishers/{publisher}/ArtifactTypes/VMImage/Offers/{offer}/Skus/{sku}/Versions/{version}"
            )
            return image_detail

        return None

    @staticmethod
    def get_tags(tags):
        tags_result = []
        if tags:
            for k, v in tags.items():
                tags_result.append({"key": k, "value": v})

        return tags_result
