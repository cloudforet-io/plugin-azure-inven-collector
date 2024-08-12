class VirtualMachineNICManager:
    def get_nic_info(
        self, vm, network_interfaces, public_ip_addresses, virtual_networks
    ):
        """
        nic_data = {
            "device_index": 0,
            "device": "",
            "nic_type": "",
            "ip_addresses": [],
            "cidr": "",
            "mac_address": "",
            "public_ip_address": "",
            "tags": {
                "nic_id": ""
            }
        }
        """

        nic_data = []
        index = 0

        vm_network_interfaces = vm.network_profile.network_interfaces

        if vm_network_interfaces is None:
            vm_network_interfaces = []

        match_network_interfaces = self.get_network_interfaces(
            vm_network_interfaces, network_interfaces
        )

        for vm_nic in match_network_interfaces:
            ip_configurations = self.get_ip_configurations(vm_nic)

            network_data = {
                "device_index": index,
                "cidr": self.get_nic_cidr(ip_configurations, virtual_networks),
                "ip_addresses": self.get_nic_ip_addresses(ip_configurations),
                "mac_address": vm_nic.mac_address,
                "public_ip_address": self.get_nic_public_ip_addresses(
                    ip_configurations, public_ip_addresses
                ),
                "tags": self.get_tags(vm_nic),
            }

            primary_ip = self.get_primary_ip_addresses(
                self.get_ip_configurations(vm_nic)
            )

            index += 1
            nic_data.append(network_data)

        return nic_data, primary_ip

    @staticmethod
    def get_nic_public_ip_addresses(ip_configurations, public_ip_addresses):
        for ip_conf in ip_configurations:
            if getattr(ip_conf, "public_ip_address") and ip_conf.public_ip_address:
                ip_name = ip_conf.public_ip_address.id.split("/")[-1]
                for pub_ip in public_ip_addresses:
                    if ip_name == pub_ip.name:
                        return pub_ip.ip_address

        return None

    @staticmethod
    def get_nic_cidr(ip_configurations, virtual_networks):
        if ip_configurations:
            subnet_name = ip_configurations[0].subnet.id.split("/")[-1]
            for vnet in virtual_networks:
                for subnet in vnet.subnets:
                    if subnet_name == subnet.name:
                        return subnet.address_prefix

        return None

    @staticmethod
    def get_nic_ip_addresses(ip_configurations):
        ip_addresses = []
        for ip_conf in ip_configurations:
            ip_addresses.append(ip_conf.private_ip_address)

        if ip_addresses:
            return ip_addresses

        return None

    @staticmethod
    def get_primary_ip_addresses(ip_configurations):
        result = {}
        for ip_conf in ip_configurations:
            result.update({ip_conf.private_ip_address: ip_conf.primary})

        return result

    @staticmethod
    def get_ip_configurations(vm_nic):
        result = []
        if getattr(vm_nic, "ip_configurations") and vm_nic.ip_configurations:
            for ip in vm_nic.ip_configurations:
                result.append(ip)

        return result

    @staticmethod
    def get_tags(vm_nic):
        return {
            "name": vm_nic.name,
            "etag": vm_nic.etag,
            "enable_accelerated_networking": vm_nic.enable_accelerated_networking,
            "enable_ip_forwarding": vm_nic.enable_ip_forwarding,
        }

    @staticmethod
    def get_network_interfaces(vm_network_interfaces, network_interfaces):
        result = []
        for vm_nic in vm_network_interfaces:
            for nic in network_interfaces:
                if vm_nic.id.split("/")[-1] == nic.name:
                    result.append(nic)
                    break

        return result
