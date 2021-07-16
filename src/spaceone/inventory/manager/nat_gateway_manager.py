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
            # if nat_gateway_dict.get('public_ip_addresses') is not None:

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
