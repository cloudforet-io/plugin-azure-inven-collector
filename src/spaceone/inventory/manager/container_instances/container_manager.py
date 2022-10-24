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
                container_instance = container_instances_conn.get_container_groups(
                    resource_group_name=resource_group_name,
                    container_group_name=container_group_name)
                container_instance_dict = self.convert_nested_dictionary(container_instance)
                time.sleep(0.2)  # end code

                # Update data info in Container Instance's Raw Data
                _gpu_count_display = 0
                _memory_size_display = 0.0

                for container in container_instance_dict['containers']:
                    container_instance_dict['start_time'] = self.convert_start_time_iso861_to_datetime(container)
                    _gpu_count_display += self.get_gpu_count_display(container)
                    _memory_size_display += container['resources']['requests']['memory_in_gb']

                # Set detail volume info for container
                if container_instance_dict['volumes'] is not None:
                    for volume in container_instance_dict['volumes']:
                        self.set_volumes_detail_info(volume, container_instance_dict['containers'])

                    # Set Container Instance volume type and volume count
                    self.set_container_instance_volume_type(container_instance_dict['volumes'])
                    container_instance_dict['volume_count_display'] = len(container_instance_dict['volumes'])

                container_instance_dict.update({
                    'resource_group': self.get_resource_group_from_id(container_instance_id),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': container_instance_id},
                    'container_count_display': len(container_instance_dict['containers']),
                    'gpu_count_display': _gpu_count_display,
                    'memory_size_display': _memory_size_display
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
                container_instances_responses.append(
                    ContainerInstanceResponse({'resource': container_instance_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {container_instance_id} {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'Container', 'ContainerInstances',
                                                                       container_instance_id)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Container Instances Finished {time.time() - start_time} Seconds **')
        return container_instances_responses, error_responses

    @staticmethod
    def set_container_instance_volume_type(volumes):
        for volume in volumes:
            if volume.get('git_repo') is not None:
                volume['volume_type'] = 'Git repo'
            elif volume.get('azure_file') is not None:
                volume['volume_type'] = 'Azure file'
            elif volume.get('empty_dir') is not None:
                volume['volume_type'] = 'Empty directory'
            elif volume.get('secret') is not None:
                volume['volume_type'] = 'Secret'

    @staticmethod
    def set_volumes_detail_info(volume, containers):
        for container in containers:
            if container['volume_mounts'] is not None:
                volume_mounts = container['volume_mounts']
                container['volume_mount_count_display'] = len(volume_mounts)
                for volume_mount in volume_mounts:
                    if volume_mount['name'] == volume['name']:
                        volume.update({
                            'mount_path': volume_mount['mount_path'],
                            'container_name': container['name']
                        })
                        return

    @staticmethod
    def convert_start_time_iso861_to_datetime(container):
        _start_time = None
        if container['instance_view'] is not None:
            _start_time = container['instance_view']['current_state']['start_time']
            if _start_time is not None:
                _start_time = datetime_to_iso8601(_start_time)
        return _start_time

    @staticmethod
    def get_gpu_count_display(container):
        _gpu_count = 0
        if container['resources']['requests']['gpu'] is not None:
            _gpu_count = container['resources']['requests']['gpu']['count']
        return _gpu_count


