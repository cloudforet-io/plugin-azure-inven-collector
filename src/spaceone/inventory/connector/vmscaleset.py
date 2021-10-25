import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *

__all__ = ['VmScaleSetConnector']
_LOGGER = logging.getLogger(__name__)


class VmScaleSetConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_vm_scale_sets(self):
        try:
            return self.compute_client.virtual_machine_scale_sets.list_all()
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR(field='VM Scale Sets'))

    def list_vm_scale_set_vms(self, resource_group, vm_scale_set_name):
        try:
            return self.compute_client.virtual_machine_scale_set_vms.list(resource_group, vm_scale_set_name)
        except ConnectionError:
            raise ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='VM Scale Sets VMs')

    def get_vm_scale_set_instance_view(self, resource_group, vm_scale_set_name, instance_id):
        try:
            return self.compute_client.virtual_machine_scale_set_vms.get_instance_view(resource_group_name=resource_group, vm_scale_set_name=vm_scale_set_name, instance_id=instance_id)
        except ConnectionError:
            _LOGGER.error(ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='VM Scale Sets Instance View'))

    def list_auto_scale_settings(self, resource_group):
        try:
            return self.monitor_client.autoscale_settings.list_by_resource_group(resource_group_name=resource_group)
        except ConnectionError:
            raise ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='VM Scale Sets Autoscale Settings')
