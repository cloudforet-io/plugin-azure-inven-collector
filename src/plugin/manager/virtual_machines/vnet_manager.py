class VirtualMachineVNetManager:
    def get_vnet_subnet_info(self, nic_name, network_interfaces, virtual_networks):
        '''
        vnet_subnet_dict = {
            "vnet_info": vnet_data,
            "subnet_info": subnet_data
        }
        '''
        vnet_info_dict = {}

        for nic in network_interfaces:
            if nic.name == nic_name:
                vnet_name = nic.ip_configurations[0].subnet.id.split('/')[-3]

        if vnet_name is not None and len(virtual_networks) > 0:
            for vnet in virtual_networks:
                if vnet.name == vnet_name:
                    subnet_info = self.convert_subnet_info(vnet.subnets[0])  # Get attached subnets
                    vnet_info = self.convert_vnet_info(vnet)
                    if subnet_info is not None:
                        vnet_info_dict['subnet_info'] = subnet_info
                    if vnet_info is not None:
                        vnet_info_dict['vnet_info'] = vnet_info

        return vnet_info_dict

    @staticmethod
    def convert_vnet_info(vnet):
        '''
        vnet_data = {
            "vnet_id" = "",
            "vnet_name" = "",
            "cidr" = ""
        }
        '''

        vnet_data = {
            'vnet_id': vnet.id,
            'vnet_name': vnet.name,
            'cidr': vnet.address_space.address_prefixes[0]
        }

        return vnet_data

    @staticmethod
    def convert_subnet_info(subnet):
        '''
        subnet_data = {
            "subnet_name": "",
            "subnet_id": "",
            "cidr": ""
        }
        '''

        subnet_data = {
            'subnet_name': subnet.name,
            'subnet_id': subnet.id,
            'cidr': subnet.address_prefix
        }

        return subnet_data
