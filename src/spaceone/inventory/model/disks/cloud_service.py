from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.model.disks.data import Disk
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout,ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
DISK
'''
# TAB - Default
disk_info_meta = ItemDynamicLayout.set_fields('Disks', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Storage Account Type', 'instance_type'),
    SizeField.data_source('Size', 'instance_size'),
    EnumDyField.data_source('Disk State', 'data.disk_state', default_state={
        'safe': ['ActiveSAS', 'ActiveUpload', 'Attached', 'Reserved'],
        'warning':['ReadyToUpload'],
        'available': ['Unattached']
    }),
    TextDyField.data_source('Attached VM', 'data.managed_by'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Resource ID', 'data.id'),
    ListDyField.data_source('Zones', 'data.zones', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('Subscription Name', 'data.subscription_name'),
    TextDyField.data_source('Encryption Type', 'data.encryption.type'),
    TextDyField.data_source('Networking', 'data.network_access_policy_display'),
    DateTimeDyField.data_source('Time Created', 'data.time_created'),
    TextDyField.data_source('Max Shares', 'data.max_shares')

])

# TAB - tags
disk_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

disk_meta = CloudServiceMeta.set_layouts([disk_info_meta, disk_info_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Disks')


class DiskResource(ComputeResource):
    cloud_service_type = StringType(default='Disk')
    data = ModelType(Disk)
    _metadata = ModelType(CloudServiceMeta, default=disk_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class DiskResponse(CloudServiceResponse):
    resource = PolyModelType(DiskResource)
