from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.loadbalncer import LoadBalancerConnector
from spaceone.inventory.model.loadbalancer.cloud_service import *
from spaceone.inventory.model.loadbalancer.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.loadbalancer.data import *
import time


class LoadBalancerManager(AzureManager):
    connector_name = 'LoadBalancerConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** LoadBalancer START **")
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

        load_balancer_conn: LoadBalancerConnector = self.locator.get_connector(self.connector_name, **params)
        load_balancers = []
        for load_balancer in load_balancer_conn.list_load_balancers():
            load_balancer_dict = self.convert_nested_dictionary(self, load_balancer)
            # update vm_scale_set_dict
            load_balancer_dict.update({
                'resource_group': self.get_resource_group_from_id(load_balancer_dict['id']),  # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            # switch tags form
            tags = load_balancer_dict.get('tags', {})
            load_balancer_dict.update({
                'tags': self.convert_tag_format(tags)
            })

            print("load_balancer_dict")
            print(load_balancer_dict)

            load_balancer_data = LoadBalancer(load_balancer_dict, strict=False)
            load_balancer_resource = LoadBalancerResource({
                'data': load_balancer_data,
                'region_code': load_balancer_data.location,
                'reference': ReferenceModel(load_balancer_data.reference())
            })

            # Must set_region_code method for region collection
            self.set_region_code(load_balancer_data['location'])
            load_balancers.append(LoadBalancerResponse({'resource': load_balancer_resource}))

        print(f'** LoadBalancer Finished {time.time() - start_time} Seconds **')
        return load_balancers

    @staticmethod
    def get_resource_group_from_id(disk_id):
        resource_group = disk_id.split('/')[4].lower()
        return resource_group

