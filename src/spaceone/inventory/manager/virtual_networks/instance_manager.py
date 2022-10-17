import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.virtual_networks import VirtualNetworksConnector
from spaceone.inventory.model.virtual_networks.cloud_service import *
from spaceone.inventory.model.virtual_networks.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.virtual_networks.data import *

_LOGGER = logging.getLogger(__name__)


class VirtualNetworksManager(AzureManager):
    connector_name = 'VirtualNetworksConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        """
            Args:
                params (dict):
                    - 'options' : 'dict'
                    - 'schema' : 'str'
                    - 'secret_data' : 'dict'
                    - 'filter' : 'dict'
                    - 'zones' : 'list'
                    - 'subscription_info' :  'dict'
            Response:
                CloudServiceResponse (list) : dictionary of virtual network data resource information
                ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug("** Vnet START **")
        start_time = time.time()

        secret_data = params['secret_data']
        subscription_info = params['subscription_info']

        vnet_conn: VirtualNetworksConnector = self.locator.get_connector(self.connector_name, **params)
        virtual_network_responses = []
        error_responses = []

        virtual_networks = vnet_conn.list_all_virtual_networks()

        for virtual_network in virtual_networks:
            virtual_network_id = ''

            try:
                vnet_dict = self.convert_nested_dictionary(virtual_network)
                virtual_network_id = vnet_dict['id']

                # update vnet_dict
                vnet_dict.update({
                    'resource_group': self.get_resource_group_from_id(virtual_network_id),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': virtual_network_id}
                })

                if vnet_dict.get('subnets') is not None:
                    subnets = vnet_dict['subnets']
                    resource_group = vnet_dict['resource_group']

                    # Change attached network interfaces objects to id
                    self.change_subnet_object_to_ids_list(subnets)

                    vnet_dict.update({
                        'subnets': self.update_subnet_info(subnets),
                        'service_endpoints': self.get_service_endpoints(subnets),
                        'private_endpoints': self.get_private_endpoints(subnets),
                        'azure_firewall': self.get_azure_firewall(vnet_conn, subnets, resource_group),
                        'connected_devices': self.get_connected_devices(subnets)
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

                vnet_data = VirtualNetwork(vnet_dict, strict=False)
                vnet_resource = VirtualNetworkResource({
                    'data': vnet_data,
                    'region_code': vnet_data.location,
                    'reference': ReferenceModel(vnet_data.reference()),
                    'name': vnet_data.name,
                    'account': vnet_data.subscription_id,
                    'tags': vnet_dict.get('tags', {})
                })

                # Must set_region_code method for region collection
                self.set_region_code(vnet_data['location'])
                # _LOGGER.debug(f'[VNET INFO] {vnet_resource.to_primitive()}')
                virtual_network_responses.append(VirtualNetworkResponse({'resource': vnet_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {virtual_network_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Network', 'VirtualNetwork', virtual_network_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** Virtual Network Finished {time.time() - start_time} Seconds **')
        return virtual_network_responses, error_responses

    def get_azure_firewall(self, vnet_conn, subnet_list, resource_group_name):
        # Get Azure firewall information
        azure_firewall_list = []
        for subnet in subnet_list:
            if subnet.get('connected_devices_list'):
                for device in subnet['connected_devices_list']:
                    if device['type'] == 'azureFirewalls':  # The subnet which has 'AzureFirewall' is typed as 'azureFirewalls'
                        firewall_obj = vnet_conn.list_all_firewalls(resource_group_name)  # List all firewalls in the resource group
                        for firewall in firewall_obj:
                            firewall_dict = self.convert_nested_dictionary(firewall)
                            for ip_configuration in firewall_dict['ip_configurations']:
                                if ip_configuration.get('subnet') is not None:
                                    if subnet['id'] in ip_configuration['subnet']['id']:  # If subnet id matches the firewall's subnet id
                                        firewall_dict['subnet'] = subnet['id'].split('/')[10]
                                        azure_firewall_list.append(firewall_dict)

        return azure_firewall_list

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
    def update_subnet_info(subnet_list):
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

        for subnet in subnet_list:
            # Get network security group's name
            if subnet.get('network_security_group') is not None:
                subnet['network_security_group']['name'] = subnet['network_security_group']['id'].split('/')[8]

            # Get private endpoints
            if subnet.get('private_endpoints') is not None:
                for private_endpoint in subnet['private_endpoints']:
                    private_endpoint.update({
                        'name': private_endpoint['id'].split('/')[8],
                        'subnet': subnet['name'],
                        'resource_group': private_endpoint['id'].split('/')[4]
                    })

        return subnet_list

    @staticmethod
    def get_service_endpoints(subnet_list):
        service_endpoint_list = []
        for subnet in subnet_list:
            # Put subnet name to service endpoints dictionary
            if subnet.get('service_endpoints') is not None:
                for service_endpoint in subnet['service_endpoints']:
                    service_endpoint['subnet'] = subnet['name']
                    service_endpoint_list.append(service_endpoint)

        return service_endpoint_list

    @staticmethod
    def get_private_endpoints(subnet_list):
        private_endpoint_list = []
        for subnet in subnet_list:
            if subnet.get('private_endpoints') is not None:
                for private_endpoint in subnet['private_endpoints']:
                    private_endpoint_list.append(private_endpoint)

        return private_endpoint_list

    @staticmethod
    def get_connected_devices(subnet_list):
        connected_devices_list = []
        for subnet in subnet_list:
            device_dict = {}

            if subnet.get('ip_configurations') is not None:
                for ip_configuration in subnet['ip_configurations']:
                    device_dict['name'] = subnet['name']
                    device_dict['type'] = ip_configuration['id'].split('/')[7]
                    device_dict['device'] = ip_configuration['id'].split('/')[8]
                    connected_devices_list.append(device_dict)

        return connected_devices_list
