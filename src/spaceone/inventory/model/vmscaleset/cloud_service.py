from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.vmscaleset.data import VmScaleSet
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
VM_SCALE_SET
'''
# TAB - Default
# TODO : instance termination notification(Configuration Tab), over provisioning, proximity placement group, Termination Notification(x)
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
# TODO : name, computer name, location, status(x), health state(x), provisioning state, fault domain,
#       protection policy, and latest model
vm_scale_set_instance = TableDynamicLayout.set_fields('Instances', 'data.vm_instances', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Computer Name', 'os_profile.computer_name'),
    TextDyField.data_source('Location', 'location'),
    TextDyField.data_source('Fault Domain', ''),
    # TextDyField.data_source('Status', ''),
    # TextDyField.data_source('Health State', ''),
    TextDyField.data_source('Provisioning State', 'provisioning_state'),
    TextDyField.data_source('Protection Policy', 'protection_policy'),
    TextDyField.data_source('Latest Model', 'latest_model_applied_display'),
    TextDyField.data_source('Virtual Network', '')
])


# TAB - Networking
# TODO : IP Configuration, Network interface, Virtual Network, Accelerated Networking,
#        Inbound /Outbound port rules , Load balancing(x)
vm_scale_set_info_networking = ItemDynamicLayout.set_fields('Networking', 'data.network_profile', fields=[
    TextDyField.data_source('IP Configuration', 'network_interface_configurations.ip_configurations.name'),
    TextDyField.data_source('Network Interface', 'network_interface_configurations.name'),
    TextDyField.data_source('Virtual Network', 'network_interface_configurations.virtual_network'),
    TextDyField.data_source('Accelerated Networking', 'network_interface_configurations'
                                                      '.enable_accelerated_networking_display')
])
# vm_scale_set_info_networking_port_rules = TableDynamicLayout.set_fields('Inbound/Outbound Port Rules','')
# TAB - Scaling
# TODO: Instance Count, Scale-in policy
vm_scale_set_info_scaling = ItemDynamicLayout.set_fields('Scaling', fields=[
    TextDyField.data_source('Instance Count', 'data.instance_count'),
    TextDyField.data_source('Scale-in Policy', 'data.scale_in_policy.rules[0]'),

])

# TAB - Disks OS Disks and Data Disks
# TODO : Image reference, Storage Type, Size, MAX iops, max throughput, encryption, host caching
#      : LUN, Storage Type, Size, MAx iops, max throughput, encryption, host caching
os_disk = SimpleTableDynamicLayout.set_fields('OS Disk', 'data.storage_profile', fields=[
    TextDyField.data_source('Image Reference', 'image_reference.id'),
    TextDyField.data_source('Storage Type', 'os_disk.managed_disk.storage_account_type'),
    SizeField.data_source('Size', 'os_disk.disk_size_gb', options={
        'source_unit': 'GB'
    }),
    TextDyField.data_source('Host Caching', 'os_disk.caching')

])
data_disks = SimpleTableDynamicLayout.set_fields('Data Disks', 'data.storage_profile', fields=[
    TextDyField.data_source('LUN', 'data_disks.lun'),
    TextDyField.data_source('Storage Type', 'data_disks.managed_disk.storage_account_type'),
    SizeField.data_source('Size', 'data_disks.disk_size_gb', options={
        'source_unit': 'GB'
    }),
    TextDyField.data_source('Max IOPS', 'data_disks.disk_iops_read_write'),
    TextDyField.data_source('MAX Throughput(MBps)', 'data_disks.disk_m_bps_read_write'),
    TextDyField.data_source('Encryption', 'data_disks.disk_encryption_set_display'),
    TextDyField.data_source('Host Caching', 'data_disks.caching')

])
vm_scale_set_info_disk = ListDynamicLayout.set_layouts('Disks', layouts=[os_disk, data_disks])

# TAB - Operating System
# TODO : Operating system, image reference, computer name prefix, administrator username,
#        password authentication, vm agent, enable automatic OS upgrades, custom data and cloud init
vm_scale_set_info_os = ItemDynamicLayout.set_fields('Operating System', fields=[
    TextDyField.data_source('Operating System', 'data.os_profile.operating_system'),
    ListDyField.data_source('Image Reference', 'data.storage_profile.os_disk_spec_list', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('Computer Name Prefix', 'data.os_profile.computer_name_prefix'),
    TextDyField.data_source('Administrator Username', 'data.os_profile.admin_username'),
    TextDyField.data_source('VM Agent', 'data.os_profile.linux_configuration.provision_vm_agent_display'),
    TextDyField.data_source('Automatic OS Upgrades', 'data.upgrade_policy.automatic_os_upgrade_policy'),
    TextDyField.data_source('Custom Data', 'data.os_profile.custom_data')
])

vm_scale_set_meta = CloudServiceMeta.set_layouts([vm_scale_set_info_meta, vm_scale_set_info_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class VmScaleSetResource(ComputeResource):
    cloud_service_type = StringType(default='VmScaleSet')
    data = ModelType(VmScaleSet)
    _metadata = ModelType(CloudServiceMeta, default=vm_scale_set_meta, serialized_name='metadata')


class VmScaleSetResponse(CloudServiceResponse):
    resource = PolyModelType(VmScaleSetResource)
