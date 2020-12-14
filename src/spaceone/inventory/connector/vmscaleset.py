import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['VmScaleSetConnector']
_LOGGER = logging.getLogger(__name__)


class VmScaleSetConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_vm_scale_sets(self):
        return self.compute_client.virtual_machine_scale_sets.list_all()

    def list_vm_scale_set_vms(self):
        return self.compute_client.virtual_machine_scale_set_vms_list()
