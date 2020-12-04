from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.disk.data import Disk
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
DISK
'''
disk_info_meta = ItemDynamicLayout.set_fields('Disk', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Storage Account Type', 'data.sku.name'),
    TextDyField.data_source('Size(GiB)', 'data.disk_size_gb'),
    TextDyField.data_source('Attached VM', 'data.managed_by'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    ListDyField.data_source('Zones', 'data.zones', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
])

# 예제일뿐..
disk_info_lock = TableDynamicLayout.set_fields('Locks', 'data.locks', fields=[
    TextDyField.data_source('Lock Name', 'name'),
    TextDyField.data_source('Lock Type', 'type'),
    TextDyField.data_source('Lock Scope', 'scope'),
    ListDyField.data_source('Lock Notes', 'notes', options={
        'delimiter': '<br>'
    }),
])

disk_meta = CloudServiceMeta.set_layouts([disk_info_meta, disk_info_lock])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class DiskResource(ComputeResource):
    cloud_service_type = StringType(default='Disk')
    data = ModelType(Disk)
    _metadata = ModelType(CloudServiceMeta, default=disk_meta, serialized_name='metadata')


class DiskResponse(CloudServiceResponse):
    resource = PolyModelType(DiskResource)
