from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.virtualnetwork import VirtualNetworkConnector
from spaceone.inventory.model.virtualnetwork.cloud_service import *
from spaceone.inventory.model.virtualnetwork.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.virtualnetwork.data import *
import time
import ipaddress

class VirtualNetworkManager(AzureManager):
    connector_name = 'VirtualNetworkConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Vnet START **")
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
                - subscription_info
        Response:
            CloudServiceResponse
        """
        secret_data = params['secret_data']
        subscription_info = params['subscription_info']

        vnet_conn: VirtualNetworkConnector = self.locator.get_connector(self.connector_name, **params)
        virtual_networks = []
        vnet_list = vnet_conn.list_all_virtual_networks()

        for vnet in vnet_list:
            vnet_dict = self.convert_nested_dictionary(self, vnet)

            # update vnet_dict
            vnet_dict.update({
                'resource_group': self.get_resource_group_from_id(vnet_dict['id']),  # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })
            if vnet_dict.get('subnets') is not None:
                # Change attached network interfaces objects to id
                self.change_subnet_object_to_ids_list(vnet_dict['subnets'])

                vnet_dict.update({
                  'subnets': self.update_subnet_info(self, vnet_dict['subnets'], vnet_conn, vnet_dict['resource_group'])
                })

                vnet_dict.update({
                    'service_endpoints': self.get_service_endpoints(self, vnet_dict['subnets'])
                })

                vnet_dict.update({
                    'private_endpoints': self.get_private_endpoints(self, vnet_dict['subnets'])
                })

            # If not 'custom dns servers', add default azure dns server dict to vnet
            if vnet_dict.get('dhcp_options') is None:
                dhcp_option_dict = {
                    'dns_servers': ['Azure provided DNS service']
                }
                vnet_dict.update({
                    'dhcp_options': dhcp_option_dict
                })

            '''
            # Get IP Address Range, Count
            if vnet_dict.get('address_space') is not None:
                if vnet_dict['address_space'].get('address_prefixes') is not None:
                    for address_space in vnet_dict['address_space']['address_prefixes']:  # ex. address_space = '10.0.0.0/16'
                        ip = IPNetwork(address_space)
                        # vnet_dict['address_space']['address_count'] = ip.size
            '''

            print(f'[VNET INFO] {vnet_dict}')

            vnet_data = VirtualNetwork(vnet_dict, strict=False)
            vnet_resource = VirtualNetworkResource({
                'data': vnet_data,
                'region_code': vnet_data.location,
                'reference': ReferenceModel(vnet_data.reference()),
                'name': vnet_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(vnet_data['location'])
            virtual_networks.append(VirtualNetworkResponse({'resource': vnet_resource}))

        print(f'** Virtual Network Finished {time.time() - start_time} Seconds **')
        return virtual_networks

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split('/')[4]
        return resource_group

    @staticmethod
    def change_subnet_object_to_ids_list(subnets_dict):
        subnet_id_list = []
        for subnet in subnets_dict:
            subnet_id_list.append(subnet['id'])
            if subnet.get('private_endpoints') is not None:
                for private_endpoint in subnet['private_endpoints']:
                    if private_endpoint.get('network_interfaces') is not None:
                        for ni in private_endpoint['network_interfaces']:
                            if ni.get('network_security_group') is not None:
                                ni['network_interfaces'] = ni['id']
                                ni['subnets'] = subnet_id_list

        return subnet_id_list

    @staticmethod
    def update_subnet_info(self, subnets_dict, vnet_conn, resource_group_name):
        '''
        : subnets_dict = {
            ip_configurations= [
                {
                 'id': '/subscriptions/xxx/resourceGroups/xxx/Microsoft.Network/[DeviceType]/[DeviceName]
                },
                ...
            ]
        }
        :return
            subnets_dict = {
                 connected_devices_list = [
                    {
                        'device' :<str>,
                        'type' :<str>,
                        'ip_address' : <str>,
                        'subnet':<str>
                    }
                ]

                'network_security_group' : {
                    'id' : <str> ,
                    'name' : <str>
                }
            }
                ...

        '''
        connected_devices_list = list()
        for subnet in subnets_dict:
            device_dict = {}
            service_endpoint_list = []

            if subnet.get('ip_configurations') is not None:
                for ip_configuration in subnet['ip_configurations']:
                    device_dict['name'] = subnet['name']
                    device_dict['type'] = ip_configuration['id'].split('/')[7]
                    device_dict['device'] = ip_configuration['id'].split('/')[8]
                    connected_devices_list.append(device_dict)

                subnet['connected_devices_list'] = connected_devices_list

            # Get network security group's name
            if subnet.get('network_security_group') is not None:
                subnet['network_security_group']['name'] = subnet['network_security_group']['id'].split('/')[8]

            # Get Azure firewall information
            if subnet.get('connected_devices_list'):
                for device in subnet['connected_devices_list']:
                    if device['type'] == 'azureFirewalls':  # The subnet which has 'AzureFirewall' is typed as 'azureFirewalls'
                        firewall_obj = vnet_conn.list_all_firewalls(resource_group_name)
                        firewall_list = []
                        for firewall in firewall_obj:
                            firewall_dict = self.convert_nested_dictionary(self, firewall)
                            for ip_configuration in firewall_dict['ip_configurations']:
                                if ip_configuration.get('subnet') is not None:
                                    if subnet['id'] in ip_configuration['subnet']['id']:
                                        firewall_list.append(firewall_dict)

                        subnet['azure_firewall'] = firewall_list

            # Get private endpoints
            if subnet.get('private_endpoints') is not None:
                for private_endpoint in subnet['private_endpoints']:
                    private_endpoint.update({
                        'name': private_endpoint['id'].split('/')[8],
                        'subnet': subnet['name'],
                        'resource_group': private_endpoint['id'].split('/')[4]
                    })

        return subnets_dict

    @staticmethod
    def get_service_endpoints(self, subnets_dict):
        service_endpoint_list = []
        for subnet in subnets_dict:
            # Put subnet name to service endpoints dictionary
            if subnet.get('service_endpoints') is not None:
                for service_endpoint in subnet['service_endpoints']:
                    service_endpoint['subnet'] = subnet['name']
                    service_endpoint_list.append(service_endpoint)

        return service_endpoint_list

    @staticmethod
    def get_private_endpoints(self, subnets_dict):
        private_endpoint_list = []
        for subnet in subnets_dict:
            if subnet.get('private_endpoints') is not None:
                for private_endpoint in subnet['private_endpoints']:
                    private_endpoint_list.append(private_endpoint)

        return private_endpoint_list
