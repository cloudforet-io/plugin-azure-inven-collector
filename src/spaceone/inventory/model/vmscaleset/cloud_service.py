from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.vmscaleset.data import VmScaleSet
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
VM_SCALE_SET
'''
# TAB - Default
# TODO : instance termination notification(Configuration Tab), over provisioning, proximity placement group(o),
#        application health monitoring(Health and repair Tab), Upgrade Policy(Upgrade Policy Tab),
vm_scale_set_info_meta = ItemDynamicLayout.set_fields('VmScaleSet', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Resource ID', 'data.id'),
    # TextDyField.data_source('Termination Notification', )
    TextDyField.data_source('OverProvisioning', 'data.overprovision_display'),
    TextDyField.data_source('Proximity Placement Group', 'data.proximity_placement_group_name'),
    TextDyField.data_source('Automatic Repairs', 'data.automatic_repairs_policy_display'),
    TextDyField.data_source('Upgrade Policy', 'data.upgrade_policy.mode')


])

# TAB - tags
vm_scale_set_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

# TAB - Instances
# TODO : name, computer name, status, health state, provisioning state, protection policy, and latest model

# TAB - Networking
# TODO : IP Configuration, NEtwork interface(o), Virtual Network(o), Accelerated Networking,
#        Inbound /Outbound port rules ,Load balancing(Boolean)
vm_scale_set_info_networking = TableDynamicLayout.set_fields('Networking', 'data.network_profile', fields=[
    TextDyField.data_source('IP Configuration', 'network_interface_configurations.ip_configurations.name'),
    TextDyField.data_source('Network Interface', 'network_interface_configurations.name'),
    TextDyField.data_source('Accelerated Networking', 'network_interface_configurations'
                                                      '.enable_accelerated_networking_display'),
    TableDynamicLayout.set_fiels('Load Balancing', 'data.network_profile')

])
# TAB - Scaling

# TAB - Disks OS Disks and Data Disks
# TODO : Image reference, Storage Type, Size, MAX iops, max throughput, encryption, host caching
#      : LUN, Storage Type, Size, MAx iops, max throughput, encryption, host caching

# TAB - Operating System
# TODO : Operating system, image reference, computer name prefix, adminitrator username,
#        password authentication, vm agent, enable automatic OS upgrades(x), custom data and cloud init(x)
vm_scale_set_meta = CloudServiceMeta.set_layouts([vm_scale_set_info_meta, vm_scale_set_info_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class VmScaleSetResource(ComputeResource):
    cloud_service_type = StringType(default='VmScaleSet')
    data = ModelType(VmScaleSet)
    _metadata = ModelType(CloudServiceMeta, default=vm_scale_set_meta, serialized_name='metadata')


class VmScaleSetResponse(CloudServiceResponse):
    resource = PolyModelType(VmScaleSetResource)
