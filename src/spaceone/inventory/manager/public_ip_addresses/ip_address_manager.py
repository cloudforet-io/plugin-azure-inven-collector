import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.public_ip_addresses import PublicIPAddressesConnector
from spaceone.inventory.model.public_ip_addresses.cloud_service import *
from spaceone.inventory.model.public_ip_addresses.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.public_ip_addresses.data import *

_LOGGER = logging.getLogger(__name__)


class PublicIPAddressesManager(AzureManager):
    connector_name = 'PublicIPAddressesConnector'
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
                CloudServiceResponse (list) : dictionary of azure public ip address data resource information
                ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug("** Public IP Address START **")
        start_time = time.time()

        subscription_info = params['subscription_info']

        public_ip_address_conn: PublicIPAddressesConnector = self.locator.get_connector(self.connector_name,**params)
        public_ip_address_responses = []
        error_responses = []

        public_ip_addresses_list = public_ip_address_conn.list_all_public_ip_addresses()

        for public_ip_address in public_ip_addresses_list:
            public_ip_address_id = ''

            try:
                public_ip_address_dict = self.convert_nested_dictionary(public_ip_address)
                public_ip_address_id = public_ip_address_dict['id']

                # update application_gateway_dict
                public_ip_address_dict.update({
                    'resource_group': self.get_resource_group_from_id(public_ip_address_id),
                    # parse resource_group from ID
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': public_ip_address_id}
                })

                if public_ip_address_dict.get('ip_configuration') is not None:
                    associated_to = public_ip_address_dict['ip_configuration']['id'].split('/')[8]
                    if associated_to:
                        public_ip_address_dict.update({
                            'associated_to': associated_to
                        })

                public_ip_address_data = PublicIPAddress(public_ip_address_dict, strict=False)
                public_ip_address_resource = PublicIPAddressResource({
                    'data': public_ip_address_data,
                    'tags': public_ip_address_dict.get('tags', {}),
                    'region_code': public_ip_address_data.location,
                    'reference': ReferenceModel(public_ip_address_data.reference()),
                    'name': public_ip_address_data.name,
                    'account': public_ip_address_data.subscription_id,
                    'instance_type': public_ip_address_data.sku.name
                })

                # Must set_region_code method for region collection
                self.set_region_code(public_ip_address_data['location'])
                # _LOGGER.debug(f'[PUBLIC IP ADDRESS INFO IN PIP MANAGER] {public_ip_address_resource.to_primitive()}')
                public_ip_address_responses.append(PublicIPAddressResponse({'resource': public_ip_address_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {public_ip_address_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Network', 'PublicIPAddress', public_ip_address_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** Public IP Address Finished {time.time() - start_time} Seconds **')
        return public_ip_address_responses, error_responses
