from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.network_security_group import NetworkSecurityGroupConnector
from spaceone.inventory.model.networksecuritygroup.cloud_service import *
from spaceone.inventory.model.networksecuritygroup.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.networksecuritygroup.data import *
import time
import ipaddress


class NetworkSecurityGroupManager(AzureManager):
    connector_name = 'NetworkSecurityGroupConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Network Security Group START **")
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
        # subscription_info = params['subscription_info']
        subscription_info = {
            'subscription_id': '3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca',
            'subscription_name': 'Azure subscription 1',
            'tenant_id': '35f43e22-0c0b-4ff3-90aa-b2c04ef1054c'
        }
        network_security_group_conn: NetworkSecurityGroupConnector = self.locator.get_connector(self.connector_name,**params)
        network_security_groups = []
        network_security_group_list = network_security_group_conn.list_all_network_security_groups()

        for network_security_group in network_security_group_list:
            network_security_group_dict = self.convert_nested_dictionary(self, network_security_group)

            # update application_gateway_dict
            network_security_group_dict.update({
                'resource_group': self.get_resource_group_from_id(network_security_group_dict['id']),
                # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })
            '''
            if network_security_group_dict.get('frontend_ip_configurations') is not None:
                for frontend_ip_configuration_dict in network_security_group_dict['frontend_ip_configurations']:
                    if frontend_ip_configuration_dict.get('private_ip_address') is not None:
                        network_security_group_dict.update({
                            'private_ip_address': frontend_ip_configuration_dict['private_ip_address']
                        })
                        frontend_ip_configuration_dict.update({
                            'ip_type': 'Private',
                            'ip_address': frontend_ip_configuration_dict['private_ip_address']
                        })
            '''
            print(f'[NETWORK SECURITY GROUP INFO] {network_security_group_dict}')

            network_security_group_data = NetworkSecurityGroup(network_security_group_dict, strict=False)
            network_security_group_resource = NetworkSecurityGroupResource({
                'data': network_security_group_data,
                'region_code': network_security_group_data.location,
                'reference': ReferenceModel(network_security_group_data.reference()),
                'name': network_security_group_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(network_security_group_data['location'])
            network_security_groups.append(NetworkSecurityGroupResponse({'resource': network_security_group_resource}))

        print(f'** Network Security Group Finished {time.time() - start_time} Seconds **')
        return network_security_groups

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split('/')[4]
        return resource_group
