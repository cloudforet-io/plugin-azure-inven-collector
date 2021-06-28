from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.public_ip_address import PublicIPAddressConnector
from spaceone.inventory.model.publicipaddress.cloud_service import *
from spaceone.inventory.model.publicipaddress.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.publicipaddress.data import *
import json
import time
import ipaddress


class PublicIPAddressManager(AzureManager):
    connector_name = 'PublicIPAddressConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Public IP Address START **")
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

        public_ip_address_conn: PublicIPAddressConnector = self.locator.get_connector(self.connector_name,**params)
        public_ip_addresses = []
        public_ip_addresses_list = public_ip_address_conn.list_all_public_ip_addresses()

        for public_ip_address in public_ip_addresses_list:
            # print(f'[public_ip_address_json]{public_ip_address_json}')
            public_ip_address_dict = self.convert_nested_dictionary(self, public_ip_address)

            # update application_gateway_dict
            public_ip_address_dict.update({
                'resource_group': self.get_resource_group_from_id(public_ip_address_dict['id']),
                # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            # print(f'[PUBLIC IP ADDRESS INFO] {public_ip_address_dict}')

            public_ip_address_data = PublicIPAddress(public_ip_address_dict, strict=False)
            public_ip_address_resource = PublicIPAddressResource({
                'data': public_ip_address_data,
                'region_code': public_ip_address_data.location,
                'reference': ReferenceModel(public_ip_address_data.reference()),
                'name': public_ip_address_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(public_ip_address_data['location'])
            public_ip_addresses.append(PublicIPAddressResponse({'resource': public_ip_address_resource}))

        print(f'** Public IP Address Finished {time.time() - start_time} Seconds **')
        return public_ip_addresses

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split('/')[4]
        return resource_group
