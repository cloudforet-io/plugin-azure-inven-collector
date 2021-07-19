from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.nat_gateway import NATGatewayConnector
from spaceone.inventory.model.natgateway.cloud_service import *
from spaceone.inventory.model.natgateway.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.natgateway.data import *
import time
import ipaddress


class NATGatewayManager(AzureManager):
    connector_name = 'NATGatewayConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** NAT Gateway START **")
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

        nat_gateway_conn: NATGatewayConnector = self.locator.get_connector(self.connector_name, **params)
        nat_gateways = []
        nat_gateways_list = nat_gateway_conn.list_all_nat_gateways()

        for nat_gateway in nat_gateways_list:
            nat_gateway_dict = self.convert_nested_dictionary(self, nat_gateway)
            print(f'[NAT Gateway]{nat_gateway_dict}')
            # update application_gateway_dict
            nat_gateway_dict.update({
                'resource_group': self.get_resource_group_from_id(nat_gateway_dict['id']),
                # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })
            if nat_gateway_dict.get('public_ip_addresses') is not None:
                # Get Count of Public IP Address
                try:
                    nat_gateway_dict.update({
                        'public_ip_addresses_count': len(nat_gateway_dict['public_ip_addresses'])
                    })
                except Exception as e:
                    print(f'[ERROR]: Azure NAT Gateway Manager]: Get Public IP Addresses Count: {e}')

                # Get Public IP Address Dictionary
                try:
                    if not nat_gateway_dict['public_ip_addresses']:
                        break

                    pip_list = []

                    for pip in nat_gateway_dict['public_ip_addresses']:
                        public_ip_prefixes_id = pip['id']
                        pip_dict = self.get_public_ip_address_dict(self, nat_gateway_conn, public_ip_prefixes_id)
                        pip_list.append(pip_dict)

                    nat_gateway_dict['public_ip_addresses'] = pip_list

                except Exception as e:
                    print(f'[ERROR: Azure NAT Gateway Manager Get Public IP Addresses Dictionary]: {e}')

            if nat_gateway_dict.get('public_ip_prefixes') is not None:
                try:
                    nat_gateway_dict.update({
                        'public_ip_prefixes_count':  len(nat_gateway_dict['public_ip_addresses'])
                    })
                except Exception as e:
                    print(f'[ERROR: Azure NAT Gateway Manager Get Public IP Prefixes Count]: {e}')

                # Get Public IP Address Dictionary
                try:
                    if not nat_gateway_dict['public_ip_prefixes']:
                        break

                    pip_list = []

                    for pip in nat_gateway_dict['public_ip_prefixes']:
                        public_ip_prefixes_id = pip['id']
                        pip_dict = self.get_public_ip_prefixes_dict(self, nat_gateway_conn, public_ip_prefixes_id)
                        pip_list.append(pip_dict)

                    nat_gateway_dict['public_ip_prefixes'] = pip_list

                except Exception as e:
                    print(f'[ERROR: Azure NAT Gateway Manager Get Public IP Prefixes Dictionary]: {e}')

            if nat_gateway_dict.get('subnets') is not None:
                try:
                    nat_gateway_dict.update({
                        'subnets': self.get_subnets(self, nat_gateway_conn, nat_gateway_dict['subnets'])
                    })
                except Exception as e:
                    print(f'[ERROR: Azure NAT Gateway Manager Get Subnet]: {e}')

            print(f'[NAT GATEWAYS INFO] {nat_gateway_dict}')

            nat_gateway_data = NatGateway(nat_gateway_dict, strict=False)
            application_gateway_resource = NatGatewayResource({
                'data': nat_gateway_data,
                'region_code': nat_gateway_data.location,
                'reference': ReferenceModel(nat_gateway_data.reference()),
                'name': nat_gateway_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(nat_gateway_data['location'])
            nat_gateways.append(NatGatewayResponse({'resource': application_gateway_resource}))

        print(f'** NAT Gateway Finished {time.time() - start_time} Seconds **')
        return nat_gateways

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split('/')[4]
        return resource_group

    @staticmethod
    def get_public_ip_address_dict(self, nat_gateway_conn, pip_id):
        try:
            pip_name = pip_id.split('/')[8]
            resource_group_name = pip_id.split('/')[4]
            pip_obj = nat_gateway_conn.get_public_ip_addresses(resource_group_name=resource_group_name, public_ip_address_name=pip_name)

            pip_dict = self.convert_nested_dictionary(self, pip_obj)
            return pip_dict

        except Exception as e:
            print(f'[ERROR: Azure NAT Gateway Manager Get Public IP Addresses Dictionary]: {e}')

    @staticmethod
    def get_public_ip_prefixes_dict(self, nat_gateway_conn, pip_id):
        try:
            pip_name = pip_id.split('/')[8]
            resource_group_name = pip_id.split('/')[4]
            pip_obj = nat_gateway_conn.get_public_ip_prefixes(resource_group_name=resource_group_name, public_ip_prefixes_name=pip_name)

            pip_dict = self.convert_nested_dictionary(self, pip_obj)
            return pip_dict

        except Exception as e:
            print(f'[ERROR: Azure NAT Gateway Manager Get Public IP Prefixes Dictionary]: {e}')

    @staticmethod
    def get_subnets(self, nat_gateway_conn, subnets):
        subnet_list = []
        try:
            for subnet in subnets:
                resource_group_name = subnet['id'].split('/')[4]
                subnet_name = subnet['id'].split('/')[10]
                vnet_name = subnet['id'].split('/')[8]

                subnet_obj = nat_gateway_conn.get_subnet(resource_group_name=resource_group_name, subnet_name=subnet_name, vnet_name=vnet_name)
                subnet_dict = self.convert_nested_dictionary(self, subnet_obj)
                subnet_dict.update({
                    'virtual_network': vnet_name
                })

                subnet_list.append(subnet_dict)

            return subnet_list

        except Exception as e:
            print(f'[ERROR: Azure NAT Gateway Manager Get Subnets]: {e}')
