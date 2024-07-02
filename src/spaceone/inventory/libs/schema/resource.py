from schematics import Model
from schematics.types import StringType, DictType, ListType, ModelType, PolyModelType
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource
from spaceone.inventory.libs.schema.region import RegionResource


class ErrorResource(Model):
    resource_type = StringType(default="inventory.CloudService")
    provider = StringType(default="azure")
    cloud_service_group = StringType(default="")
    cloud_service_type = StringType(default="")
    resource_id = StringType(serialize_when_none=False)


class ResourceResponse(Model):
    state = StringType()
    message = StringType(default="")
    resource_type = StringType()
    match_rules = DictType(ListType(StringType), serialize_when_none=False)
    resource = DictType(StringType, default={})


class CloudServiceResourceResponse(ResourceResponse):
    state = StringType(default="SUCCESS")
    resource_type = StringType(default="inventory.CloudService")
    match_rules = DictType(
        ListType(StringType),
        default={
            "1": [
                "reference.resource_id",
                "provider",
                "cloud_service_type",
                "cloud_service_group",
            ]
        },
    )
    resource = PolyModelType(CloudServiceTypeResource)


class RegionResourceResponse(ResourceResponse):
    state = StringType(default="SUCCESS")
    resource_type = StringType(default="inventory.Region")
    match_rules = DictType(
        ListType(StringType), default={"1": ["region_code", "provider"]}
    )
    resource = PolyModelType(RegionResource)


class CloudServiceTypeResourceResponse(ResourceResponse):
    state = StringType(default="SUCCESS")
    resource_type = StringType(default="inventory.CloudServiceType")
    match_rules = DictType(
        ListType(StringType), default={"1": ["name", "group", "provider"]}
    )
    resource = PolyModelType(CloudServiceTypeResource)


class ErrorResourceResponse(ResourceResponse):
    state = StringType(default="FAILURE")
    resource_type = StringType(default="inventory.ErrorResource")
    resource = ModelType(ErrorResource, default={})


class AzureMonitorModel(Model):
    resource_id = StringType()


class AzureTags(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class AzureCloudService(Model):
    tenant_id = StringType(serialized_name=False)
    subscription_id = StringType(serialize_when_none=False)
    subscription_name = StringType(serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
    azure_monitor = ModelType(AzureMonitorModel, serialize_when_none=False)
