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
