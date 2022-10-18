import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.nat_gateways import NATGatewaysConnector
from spaceone.inventory.model.nat_gateways.cloud_service import *
from spaceone.inventory.model.nat_gateways.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.nat_gateways.data import *

_LOGGER = logging.getLogger(__name__)


class NATGatewaysManager(AzureManager):
    connector_name = 'NATGatewaysConnector'
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
                CloudServiceResponse (dict) : dictionary of azure nat gateway data resource information
                ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug(f'** NAT Gateway START **')
        start_time = time.time()

        subscription_info = params['subscription_info']

        nat_gateway_conn: NATGatewaysConnector = self.locator.get_connector(self.connector_name, **params)
        nat_gateway_responses = []
        error_responses = []

        nat_gateways = nat_gateway_conn.list_all_nat_gateways()

        for nat_gateway in nat_gateways:
            nat_gateway_id = ''

            try:
                nat_gateway_dict = self.convert_nested_dictionary(nat_gateway)
                nat_gateway_id = nat_gateway_dict['id']

                # update application_gateway_dict
                nat_gateway_dict.update({
                    'resource_group': self.get_resource_group_from_id(nat_gateway_id),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': nat_gateway_id}
                })

                if nat_gateway_dict.get('public_ip_addresses') is not None:
                    # Get Count of Public IP Address
                    nat_gateway_dict.update({
                        'public_ip_addresses_count': len(nat_gateway_dict['public_ip_addresses'])
                    })

                    # Get Public IP Address Dictionary
                    if not nat_gateway_dict['public_ip_addresses']:
                        break

                    pip_list = []

                    for pip in nat_gateway_dict['public_ip_addresses']:
                        public_ip_prefixes_id = pip['id']
                        pip_dict = self.get_public_ip_address_dict(nat_gateway_conn, public_ip_prefixes_id)
                        pip_list.append(pip_dict)
                    nat_gateway_dict['public_ip_addresses'] = pip_list

                if nat_gateway_dict.get('public_ip_prefixes') is not None:
                    nat_gateway_dict.update({
                        'public_ip_prefixes_count': len(nat_gateway_dict['public_ip_addresses'])
                    })

                    # Get Public IP Address Dictionary
                    if not nat_gateway_dict['public_ip_prefixes']:
                        break

                    pip_list = []

                    for pip in nat_gateway_dict['public_ip_prefixes']:
                        public_ip_prefixes_id = pip['id']
                        pip_dict = self.get_public_ip_prefixes_dict(nat_gateway_conn, public_ip_prefixes_id)
                        pip_list.append(pip_dict)

                    nat_gateway_dict['public_ip_prefixes'] = pip_list

                if nat_gateway_dict.get('subnets') is not None:
                    nat_gateway_dict.update({
                        'subnets': self.get_subnets(nat_gateway_conn, nat_gateway_dict['subnets'])
                    })

                nat_gateway_data = NatGateway(nat_gateway_dict, strict=False)
                nat_gateway_resource = NatGatewayResource({
                    'data': nat_gateway_data,
                    'tags': nat_gateway_dict.get('tags', {}),
                    'region_code': nat_gateway_data.location,
                    'reference': ReferenceModel(nat_gateway_data.reference()),
                    'name': nat_gateway_data.name,
                    'account': nat_gateway_data.subscription_id,
                    'instance_type': nat_gateway_data.sku.name
                })

                # Must set_region_code method for region collection
                self.set_region_code(nat_gateway_data['location'])
                # _LOGGER.debug(f'[NAT GATEWAYS INFO] {nat_gateway_resource.to_primitive()}')
                nat_gateway_responses.append(NatGatewayResponse({'resource': nat_gateway_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {nat_gateway_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Network', 'NATGateway', nat_gateway_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** NAT Gateway Finished {time.time() - start_time} Seconds **')
        return nat_gateway_responses, error_responses

    def get_public_ip_address_dict(self, nat_gateway_conn, pip_id):
        pip_name = pip_id.split('/')[8]
        resource_group_name = pip_id.split('/')[4]
        pip_obj = nat_gateway_conn.get_public_ip_addresses(resource_group_name=resource_group_name, public_ip_address_name=pip_name)
        pip_dict = self.convert_nested_dictionary(pip_obj)
        return pip_dict

    def get_public_ip_prefixes_dict(self, nat_gateway_conn, pip_id):
        pip_name = pip_id.split('/')[8]
        resource_group_name = pip_id.split('/')[4]
        pip_obj = nat_gateway_conn.get_public_ip_prefixes(resource_group_name=resource_group_name, public_ip_prefixes_name=pip_name)

        pip_dict = self.convert_nested_dictionary(pip_obj)
        return pip_dict

    def get_subnets(self, nat_gateway_conn, subnets):
        subnet_list = []

        for subnet in subnets:
            resource_group_name = subnet['id'].split('/')[4]
            subnet_name = subnet['id'].split('/')[10]
            vnet_name = subnet['id'].split('/')[8]

            subnet_obj = nat_gateway_conn.get_subnet(resource_group_name=resource_group_name, subnet_name=subnet_name, vnet_name=vnet_name)
            subnet_dict = self.convert_nested_dictionary(subnet_obj)
            subnet_dict.update({
                'virtual_network': vnet_name
            })

            subnet_list.append(subnet_dict)

        return subnet_list
