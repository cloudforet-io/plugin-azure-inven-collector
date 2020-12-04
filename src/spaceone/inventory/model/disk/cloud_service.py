from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.disk.data import Disk
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
DISK
'''
disk_info_meta = ItemDynamicLayout.set_fields('Disk', fields=[
    # TODO: Fill out to Dynamic Item Field Tab
    TextDyField.data_source('ID', 'data.id'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Attached VM', 'data.ManagedBy'),
    TextDyField.data_source('Zone', 'data.zones'),
    TextDyField.data_source('Name', 'data.skuTier'),

    # TextDyField.data_source('Storage account type', 'data.type'),
    TextDyField.data_source('Size(GiB)', 'data.diskSizeGB'),
    TextDyField.data_source('State', 'data.diskState'),
    TextDyField.data_source('Owner', 'data.managedBy'),
    TextDyField.data_source('Resource Group', 'data.resourceGroup'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Type', 'data.type')
])

disk_meta = CloudServiceMeta.set_layouts([disk_info_meta, ])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class DiskResource(ComputeResource):
    cloud_service_type = StringType(default='Disk')
    data = ModelType(Disk)
    _metadata = ModelType(CloudServiceMeta, default=disk_meta, serialized_name='metadata')


class DiskResponse(CloudServiceResponse):
    resource = PolyModelType(DiskResource)
