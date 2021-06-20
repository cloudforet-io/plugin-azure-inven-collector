from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.application_gateway import ApplicationGatewayConnector
from spaceone.inventory.model.applicationgateway.cloud_service import *
from spaceone.inventory.model.applicationgateway.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.applicationgateway.data import *
import time
import ipaddress


class ApplicationGatewayManager(AzureManager):
    connector_name = 'ApplicationGatewayConnector'
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
        
        application_gateway_conn: ApplicationGatewayConnector = self.locator.get_connector(self.connector_name,
                                                                                           **params)
        application_gateways = []
        application_gateways_list = application_gateway_conn.list_all_application_gateways()

        for application_gateway in application_gateways_list:
            application_gateway_dict = self.convert_nested_dictionary(self, application_gateway)

            # update application_gateway_dict
            application_gateway_dict.update({
                'resource_group': self.get_resource_group_from_id(application_gateway_dict['id']),
                # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            if application_gateway_dict.get('frontend_ip_configurations') is not None:
                for frontend_ip_configuration in application_gateway_dict['frontend_ip_configurations']:
                    if frontend_ip_configuration.get('private_ip_address') is not None:
                        application_gateway_dict.update({
                            'private_ip_address': frontend_ip_configuration['private_ip_address']
                        })
                    elif frontend_ip_configuration.get('public_ip_address') is not None:
                        public_ip_address_name = frontend_ip_configuration['public_ip_address']['id'].split('/')[8]
                        application_gateway_dict.update({
                            'public_ip_address': self.get_public_ip_address(self, application_gateway_conn, application_gateway_dict['resource_group'], public_ip_address_name)
                        })

            if application_gateway_dict.get('gateway_ip_configurations') is not None:
                for ip_configuration in application_gateway_dict['gateway_ip_configurations']:
                    application_gateway_dict.update({
                        'virtual_network': ip_configuration.get('subnet')['id'].split('/')[8],
                        'subnet': ip_configuration.get('subnet')['id'].split('/')[10]
                    })
            '''
            if application_gateway_dict.get('subnets') is not None:
                # Change attached network interfaces objects to id
                self.change_subnet_object_to_ids_list(application_gateway_dict['subnets'])
            '''
            print(f'[APPLICATION GATEWAYS INFO] {application_gateway_dict}')

            application_gateway_data = ApplicationGateway(application_gateway_dict, strict=False)
            application_gateway_resource = ApplicationGatewayResource({
                'data': application_gateway_data,
                'region_code': application_gateway_data.location,
                'reference': ReferenceModel(application_gateway_data.reference()),
                'name': application_gateway_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(application_gateway_data['location'])
            application_gateways.append(ApplicationGatewayResponse({'resource': application_gateway_resource}))

        print(f'** Application Gateway Finished {time.time() - start_time} Seconds **')
        return application_gateways

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split('/')[4]
        return resource_group

    @staticmethod
    def get_public_ip_address(self, application_gateway_conn, resource_group_name, pip_name):
        public_ip_address_obj = application_gateway_conn.get_public_ip_addresses(resource_group_name, pip_name)
        public_ip_address_dict = self.convert_nested_dictionary(self, public_ip_address_obj)

        print(f'[Public IP Address]{public_ip_address_dict}')

        return public_ip_address_dict
