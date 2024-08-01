import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class VMScaleSetsConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get("secret_data"))

    def list_vm_scale_sets(self):
        return self.compute_client.virtual_machine_scale_sets.list_all()

    def list_vm_scale_set_vms(self, resource_group, vm_scale_set_name):
        return self.compute_client.virtual_machine_scale_set_vms.list(
            resource_group, vm_scale_set_name
        )

    def get_vm_scale_set_instance_view(
            self, resource_group, vm_scale_set_name, instance_id
    ):
        return self.compute_client.virtual_machine_scale_set_vms.get_instance_view(
            resource_group_name=resource_group,
            vm_scale_set_name=vm_scale_set_name,
            instance_id="0",
        )

    def list_vm_scale_set_instance_view(
            self, resource_group, vm_scale_set_name, instance_id
    ):
        return self.compute_client.virtual_machine_scale_set_vms.list(
            resource_group_name=resource_group,
            vm_scale_set_name=vm_scale_set_name,
            instance_id=instance_id,
        )

    def list_auto_scale_settings(self, resource_group):
        return self.monitor_client.autoscale_settings.list_by_resource_group(
            resource_group_name=resource_group
        )
