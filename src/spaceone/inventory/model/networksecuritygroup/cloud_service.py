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

])

# TAB - Inbound Security Rules
network_security_group_inbound_security_rules = TableDynamicLayout.set_fields('Inbound Security Rules', 'data.inbound_security_rules', fields=[
    TextDyField.data_source('Priority', 'priority'),
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Port', 'destination_port_range'),
    TextDyField.data_source('Protocol', 'protocol'),
    TextDyField.data_source('Source', 'source_address_prefix'),
    TextDyField.data_source('Destination', 'destination_address_prefix'),
    TextDyField.data_source('Action', 'access')
])

# TAB - Outbound Security Rules
network_security_group_outbound_security_rules = TableDynamicLayout.set_fields('Outbound Security Rules', 'data.outbound_security_rules', fields=[
    TextDyField.data_source('Priority', 'priority'),
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Port', 'destination_port_range'),
    TextDyField.data_source('Protocol', 'protocol'),
    TextDyField.data_source('Source', 'source_address_prefix'),
    TextDyField.data_source('Destination', 'destination_address_prefix'),
    TextDyField.data_source('Action', 'access')
])

# TAB - Network Interfaces
network_security_group_network_interfaces = TableDynamicLayout.set_fields('Network Interfaces', 'data.network_interfaces', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Public IP Address', 'public_ip_address'),
    TextDyField.data_source('Private IP Address', 'private_ip_address'),
    TextDyField.data_source('Virtual Machine', 'virtual_machine_display')
])

# TAB - Subnets
network_subnets = TableDynamicLayout.set_fields('Subnets', 'data.subnets', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Address Range', ''),
    TextDyField.data_source('Virtual Network', '')
])

# TAB - tags
network_security_group_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

network_security_group_meta = CloudServiceMeta.set_layouts(
    [network_security_group_info_meta, network_security_group_inbound_security_rules, network_security_group_outbound_security_rules,
     network_security_group_network_interfaces, network_subnets, network_security_group_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Network')


class NetworkSecurityGroupResource(ComputeResource):
    cloud_service_type = StringType(default='NetworkSecurityGroup')
    data = ModelType(NetworkSecurityGroup)
    _metadata = ModelType(CloudServiceMeta, default=network_security_group_meta, serialized_name='metadata')
    name = StringType()


class NetworkSecurityGroupResponse(CloudServiceResponse):
    resource = PolyModelType(NetworkSecurityGroupResource)
