from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, IntType, DateTimeType, FloatType
from .base import BaseMetaData, BaseResponse, MetaDataView, MetaDataViewSubData, ReferenceModel


class CloudServiceMeta(BaseMetaData):
    @classmethod
    def set(cls):
        sub_data = MetaDataViewSubData()
        return cls({'view': MetaDataView({'sub_data': sub_data})})

    @classmethod
    def set_layouts(cls, layouts=[]):
        sub_data = MetaDataViewSubData({'layouts': layouts})
        return cls({'view': MetaDataView({'sub_data': sub_data})})


class Tags(Model):
    key = StringType()
    value = StringType()


class CloudServiceResource(Model):
    provider = StringType(default="azure")
    cloud_service_type = StringType()
    cloud_service_group = StringType()
    name = StringType(default='')
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    account = StringType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)
    tags = DictType(StringType(), StringType(), serialize_when_none=False)
    data = PolyModelType(Model, default=lambda: {})
    reference = ModelType(ReferenceModel)
    region_code = StringType()
    _metadata = PolyModelType(CloudServiceMeta, serialize_when_none=False, serialized_name='metadata')


class CloudServiceResponse(BaseResponse):
    state = StringType(default='SUCCESS')
    match_rules = DictType(ListType(StringType), default={
        '1': ['reference.resource_id', 'provider', 'cloud_service_type', 'cloud_service_group', 'account']
    })
    resource_type = StringType(default='inventory.CloudService')
    resource = PolyModelType(CloudServiceResource)
