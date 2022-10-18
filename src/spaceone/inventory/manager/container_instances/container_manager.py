import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.connector.container_instances import ContainerInstancesConnector
from spaceone.inventory.model.container_instances.cloud_service import *
from spaceone.inventory.model.container_instances.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.container_instances.data import *
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.core.utils import *

_LOGGER = logging.getLogger(__name__)


class ContainerInstancesManager(AzureManager):
    connector_name = 'ContainerInstancesConnector'
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
                    CloudServiceResponse (list) : list of azure container instances data resource information
                    ErrorResourceResponse (list) : list of error resource information
        """

        _LOGGER.debug(f'** Container Instances START **')
        start_time = time.time()
        subscription_info = params['subscription_info']

        container_instances_conn: ContainerInstancesConnector = self.locator.get_connector(self.connector_name, **params)
        container_instances_responses = []
        error_responses = []

        container_instances = container_instances_conn.list_container_groups()
        for container_instance in container_instances:
            container_instance_id = ''
            try:
                container_instance_dict = self.convert_nested_dictionary(container_instance)
                container_instance_id = container_instance_dict['id']

                # if bug fix these code will be deleted
                resource_group_name = self.get_resource_group_from_id(container_instance_id)
                container_group_name = container_instance_dict['name']
                container_instance = container_instances_conn.get_container_groups(resource_group_name=resource_group_name,
                                                              container_group_name=container_group_name)
                container_instance_dict = self.convert_nested_dictionary(container_instance)
                time.sleep(0.2)  # end code

                # Update data info in Container's Raw Data
                for container in container_instance_dict['containers']:
                    _start_time = container['instance_view']['current_state']['start_time']
                    if _start_time is not None:
                        container_instance_dict['start_time'] = datetime_to_iso8601(_start_time)

                container_instance_dict.update({
                    'resource_group': self.get_resource_group_from_id(container_instance_id),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': container_instance_id},
                    'container_count_display': container_instance_dict['containers'].__len__()
                })

                container_instance_data = ContainerInstance(container_instance_dict, strict=False)
                container_instance_resource = ContainerInstanceResource({
                    'name': container_instance_data.name,
                    'account': container_instance_dict['subscription_id'],
                    'data': container_instance_data,
                    'tags': container_instance_dict.get('tags', {}),
                    'region_code': container_instance_data.location,
                    'reference': ReferenceModel(container_instance_data.reference())
                })

                self.set_region_code(container_instance_data['location'])
                container_instances_responses.append(ContainerInstanceResponse({'resource': container_instance_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {container_instance_id} {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'Container', 'ContainerInstances', container_instance_id)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Container Instances Finished {time.time() - start_time} Seconds **')
        return container_instances_responses, error_responses
