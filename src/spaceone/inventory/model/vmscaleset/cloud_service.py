from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.vmscaleset.data import VirtualMachineScaleSet
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
VM_SCALE_SET
'''
# TAB - Default
# TODO : instance termination notification(Configuration Tab), over provisioning, proximity placement group, Termination Notification
#        application health monitoring(Health and repair Tab), Upgrade Policy(Upgrade Policy Tab),
vm_scale_set_info_meta = ItemDynamicLayout.set_fields('VmScaleSet', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('Instances', 'data.instance_count'),
    TextDyField.data_source('Operating System', 'data.virtual_machine_profile.os_profile.operating_system'),
    TextDyField.data_source('Size', 'data.sku.name'),
    TextDyField.data_source('Virtual network/subnet', 'data.virtual_machine_profile.network_profile.primary_vnet'),
    TextDyField.data_source('Host group', 'data.host_group.id'),
    TextDyField.data_source('Ephemeral OS Disk',
                            'data.virtual_machine_profile.storage_profile.os_disk.diff_disk_settings.option.local'),
    TextDyField.data_source('Azure Spot Eviction Policy', 'data.virtual_machine_profile.eviction_policy'),
    TextDyField.data_source('Termination Notification', 'data.virtual_machine_profile.terminate_notification_display'),
    TextDyField.data_source('OverProvisioning', 'data.overprovision'),
    TextDyField.data_source('Proximity Placement Group', 'data.proximity_placement_group_display'),
    TextDyField.data_source('Automatic Repairs', 'data.automatic_repairs_policy.enabled'),
    TextDyField.data_source('Upgrade Policy', 'data.upgrade_policy.mode'),
    TextDyField.data_source('Fault Domains', 'data.platform_fault_domain_count'),

])

# TAB - tags
vm_scale_set_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

# TAB - Instances
# name, computer name, location, status,  provisioning state, fault domain,
#       protection policy, and latest model
vm_scale_set_instance = TableDynamicLayout.set_fields('Instances', 'data.vm_instances', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Computer Name', 'os_profile.computer_name'),
    TextDyField.data_source('Location', 'location'),
    EnumDyField.data_source('Status', 'vm_instance_status_profile.vm_agent.display_status', default_state={
        'safe': ['Ready'],
        'warning':['Not Ready']
    }),
    TextDyField.data_source('Provisioning State', 'provisioning_state'),
    TextDyField.data_source('Protection From Scale-in', 'protection_policy.protect_from_scale_in'),
    TextDyField.data_source('Protection From Scale-set Actions', 'protection_policy.protect_from_scale_set_actions'),
    TextDyField.data_source('Latest Model', 'latest_model_applied'),
    TextDyField.data_source('Virtual Network', 'primary_vnet')
])

# TAB - Networking
# IP Configuration, Network interface, Virtual Network, Accelerated Networking,
#        Inbound /Outbound port rules(x) , Load balancing(x)
vm_scale_set_info_networking = ItemDynamicLayout.set_fields('Networking',
                                                            'data.virtual_machine_profile.network_profile', fields=[
        TextDyField.data_source('Virtual Network', 'primary_vnet'),
    ])

vm_scale_set_info_network_configuration = SimpleTableDynamicLayout.set_fields('Network Configuration',
                                                                              'data.virtual_machine_profile.network_profile.network_interface_configurations',
                                                                              fields=[
                                                                                  TextDyField.data_source('Name',
                                                                                                          'name'),
                                                                                  TextDyField.data_source(
                                                                                      'Network interface',
                                                                                      'enable_accelerated_networking_display'),
                                                                                  TextDyField.data_source(
                                                                                      'Accelerated Networking',
                                                                                      'enable_accelerated_networking_display'),
                                                                                  TextDyField.data_source('Primary',
                                                                                                          'primary'),
                                                                              ])

vm_scale_set_info_ip_configurations = SimpleTableDynamicLayout.set_fields('IP Configurations',
                                                                         'data.virtual_machine_profile.network_profile.network_interface_configurations.ip_configurations',
                                                                          fields=[

                                                                             TextDyField.data_source(
                                                                                 'Public Ip Address Configuration',
                                                                                 'public_ip_address_configuration'),
                                                                             TextDyField.data_source(
                                                                                 'Private IP Address Version',
                                                                                 'private_ip_address_version'),
                                                                         ])

vm_scale_set_info_network = ListDynamicLayout.set_layouts('Networking', layouts=[vm_scale_set_info_networking,
                                                                                 vm_scale_set_info_network_configuration,
                                                                                 vm_scale_set_info_ip_configurations])

# TAB - Scaling
# TODO: Instance Count, Scale-in policy
vm_scale_set_info_scaling = ItemDynamicLayout.set_fields('Scaling', fields=[
    TextDyField.data_source('Instance Count', 'data.instance_count'),
    ListDyField.data_source('Scale-in Policy', 'data.scale_in_policy.rules', options={
        'delimiter': '<br>'
    }),
])

# TAB - Disks OS Disks and Data Disks
#  Image reference, Storage Type, Size, MAX iops, max throughput, encryption, host caching
#      : LUN, Storage Type, Size, MAx iops, max throughput, encryption, host caching
os_disk = ItemDynamicLayout.set_fields('OS Disk', 'data.virtual_machine_profile.storage_profile', fields=[
    TextDyField.data_source('Image Reference', 'image_reference_display'),
    TextDyField.data_source('Storage Account Type', 'os_disk.managed_disk.storage_account_type'),
    SizeField.data_source('Size', 'os_disk.disk_size_gb', options={
        'source_unit': 'GB'
    }),
    TextDyField.data_source('Host Caching', 'os_disk.caching')

])
data_disks = SimpleTableDynamicLayout.set_fields('Data Disks', 'data.virtual_machine_profile.storage_profile.data_disks', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Storage Type', 'managed_disk.storage_type'),
    SizeField.data_source('Size', 'disk_size_gb', options={
        'source_unit': 'GB'
    }),
    TextDyField.data_source('Max IOPS', 'disk_iops_read_write'),
    TextDyField.data_source('MAX Throughput(MBps)', 'disk_m_bps_read_write'),
    TextDyField.data_source('Encryption', 'disk_encryption_set.id'),
    TextDyField.data_source('Host Caching', 'caching'),
    TextDyField.data_source('LUN', 'lun')
])
vm_scale_set_info_disk = ListDynamicLayout.set_layouts('Disks', layouts=[os_disk, data_disks])

# TAB - Operating System
# Operating system, image reference, computer name prefix, administrator username,
#        password authentication, vm agent, enable automatic OS upgrades, custom data and cloud init

vm_scale_set_info_os_profile = ItemDynamicLayout.set_fields('Operating System', fields=[
        TextDyField.data_source('Computer Name Prefix', 'data.virtual_machine_profile.os_profile.computer_name_prefix'),
        TextDyField.data_source('Administrator Username', 'data.virtual_machine_profile.os_profile.admin_username'),
        TextDyField.data_source('Operating System', 'data.virtual_machine_profile.os_profile.operating_system'),
        TextDyField.data_source('VM Agent', 'data.virtual_machine_profile.os_profile.linux_configuration.provision_vm_agent'),
        TextDyField.data_source('Automatic OS Upgrades',
                                'data.upgrade_policy.automatic_os_upgrade_policy.enable_automatic_os_upgrade'),
        TextDyField.data_source('Custom Data', 'data.virtual_machine_profile.os_profile.custom_data')
    ])

vm_scale_set_meta = CloudServiceMeta.set_layouts(
    [vm_scale_set_info_meta, vm_scale_set_info_tags, vm_scale_set_instance, vm_scale_set_info_network,
     vm_scale_set_info_scaling, vm_scale_set_info_disk, vm_scale_set_info_os_profile])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class VmScaleSetResource(ComputeResource):
    cloud_service_type = StringType(default='VmScaleSet')
    data = ModelType(VirtualMachineScaleSet)
    _metadata = ModelType(CloudServiceMeta, default=vm_scale_set_meta, serialized_name='metadata')


class VmScaleSetResponse(CloudServiceResponse):
    resource = PolyModelType(VmScaleSetResource)
