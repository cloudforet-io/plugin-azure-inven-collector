from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.networksecuritygroup.data import NetworkSecurityGroup

'''
NETWORK_SECURITY_GROUP
'''
# TAB - Default
network_security_group_info_meta = ItemDynamicLayout.set_fields('Network Security Group', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('Virtual Network', 'data.virtual_network'),
    TextDyField.data_source('Subnet', 'data.subnet'),
    TextDyField.data_source('Frontend public IP Address', 'data.public_ip_address.ip_address'),
    TextDyField.data_source('Frontend private IP Address', 'data.private_ip_address'),
    TextDyField.data_source('Tier', 'data.sku.tier')
])

# TAB - tags
network_security_group_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

network_security_group_meta = CloudServiceMeta.set_layouts(
    [network_security_group_info_meta, network_security_group_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Network')


class NetworkSecurityGroupResource(ComputeResource):
    cloud_service_type = StringType(default='NetworkSecurityGroup')
    data = ModelType(NetworkSecurityGroup)
    _metadata = ModelType(CloudServiceMeta, default=network_security_group_meta, serialized_name='metadata')
    name = StringType()


class NetworkSecurityGroupResponse(CloudServiceResponse):
    resource = PolyModelType(NetworkSecurityGroupResource)
