class VirtualMachineNetworkSecurityGroupManager:
    def get_network_security_group_info(
        self, vm, network_security_groups, network_interfaces
    ):
        """
        nsg_data = {
            "protocol" = "",
            "remote" = "",
            "remote_cidr" = "",
            "remote_id" = "",
            "security_group_name" = "",
            "security_group_id" = "",
            "description" = "",
            "direction" = "inbound" | "outbound",
            "port_range_min" = 0,
            "port_range_max" = 0,
            "port" = "",
            "priority" = 0
        }
        """

        nsg_data = []

        network_security_groups_data = []

        if (
            getattr(vm.network_profile, "network_interfaces")
            and vm.network_profile.network_interfaces
        ):
            vm_network_interfaces = vm.network_profile.network_interfaces
        else:
            vm_network_interfaces = []

        match_network_security_groups = self.get_network_security_group_from_nic(
            vm_network_interfaces, network_interfaces, network_security_groups
        )
        for network_security_group in match_network_security_groups:
            sg_id = network_security_group.id

            security_rules = network_security_group.security_rules
            security_data = self.get_nsg_security_rules(security_rules, sg_id)
            network_security_groups_data.extend(security_data)

            default_security_rules = network_security_group.default_security_rules
            default_security_data = self.get_nsg_security_rules(
                default_security_rules, sg_id
            )
            network_security_groups_data.extend(default_security_data)

        for nsg in network_security_groups_data:
            nsg_data.append(nsg)

        return nsg_data

    def get_nsg_security_rules(self, security_rules, sg_id):
        result = []
        for s_rule in security_rules:
            security_rule_data = {
                "protocol": self.get_nsg_protocol(s_rule.protocol),
                "remote_id": s_rule.id,
                "security_group_name": s_rule.id.split("/")[-3],
                "description": s_rule.description,
                "direction": s_rule.direction.lower(),
                "priority": s_rule.priority,
                "security_group_id": sg_id,
                "action": s_rule.access.lower(),
            }

            remote_data = self.get_nsg_remote(s_rule)
            security_rule_data.update(remote_data)
            port_data = self.get_nsg_port(s_rule)
            security_rule_data.update(port_data)

            result.append(security_rule_data)

        return result

    @staticmethod
    def get_nsg_protocol(protocol):
        if protocol == "*":
            return "ALL"
        return protocol

    @staticmethod
    def get_network_security_group_from_nic(
        vm_network_interfaces, network_interfaces, network_security_groups
    ):
        nsgs = []
        for vm_nic in vm_network_interfaces:
            vm_nic_name = vm_nic.id.split("/")[-1]
            for nic in network_interfaces:
                if vm_nic_name == nic.name:
                    if (
                        getattr(nic, "network_security_group")
                        and nic.network_security_group
                    ):
                        nsg_name = nic.network_security_group.id.split("/")[-1]
                        for nsg in network_security_groups:
                            if nsg.name == nsg_name:
                                nsgs.append(nsg)
                                break
                        break

        return nsgs

    @staticmethod
    def get_nsg_remote(s_rule):
        remote_result = {}
        if s_rule.source_address_prefix is not None:
            if "/" in s_rule.source_address_prefix:
                remote_result.update(
                    {
                        "remote": s_rule.source_address_prefix,
                        "remote_cidr": s_rule.source_address_prefix,
                    }
                )
            elif s_rule.source_address_prefix == "*":
                remote_result.update({"remote": "*", "remote_cidr": "*"})
            else:
                remote_result.update({"remote": s_rule.source_address_prefix})

        else:
            address_prefixes = s_rule.source_address_prefixes
            remote = ""

            if address_prefixes:
                for prfx in address_prefixes:
                    remote += prfx
                    remote += ", "

                remote = remote[:-2]

                remote_result.update({"remote": remote, "remote_cidr": remote})

        if len(remote_result) > 0:
            return remote_result

        return None

    @staticmethod
    def get_nsg_port(s_rule):
        port_result = {}

        if (
            getattr(s_rule, "destination_port_range")
            and s_rule.destination_port_range is not None
        ):
            if "-" in s_rule.destination_port_range:
                port_min = s_rule.destination_port_range.split("-")[0]
                port_max = s_rule.destination_port_range.split("-")[1]
                port_result.update(
                    {
                        "port_range_min": port_min,
                        "port_range_max": port_max,
                        "port": s_rule.destination_port_range,
                    }
                )
            elif s_rule.destination_port_range == "*":
                port_result.update(
                    {"port_range_min": 0, "port_range_max": 0, "port": "*"}
                )
            else:
                port_result.update(
                    {
                        "port_range_min": s_rule.destination_port_range,
                        "port_range_max": s_rule.destination_port_range,
                        "port": s_rule.destination_port_range,
                    }
                )
        else:
            if (
                getattr(s_rule, "destination_port_ranges")
                and s_rule.destination_port_ranges
            ):
                port_ranges = s_rule.destination_port_ranges
                if not port_ranges:
                    port_ranges = []

                port_min = 0
                port_max = 0
                all_port = ""
                ports = []

                for port in port_ranges:
                    if "-" in port:  # ex. ['33-55']
                        for i in port.split("-"):
                            ports.append(i)
                    else:  # ex. ['8080']
                        ports.append(port)

                    ports = list(map(int, ports))  # Change to int list

                    if ports:
                        port_min = min(ports)
                        port_max = max(ports)

                    all_port = ", ".join(map(str, ports))  # Update string

                port_result.update(
                    {
                        "port_range_min": port_min,
                        "port_range_max": port_max,
                        "port": all_port,
                    }
                )

        if len(port_result) > 0:
            return port_result

        return None