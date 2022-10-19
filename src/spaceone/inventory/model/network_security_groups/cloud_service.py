from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.network_security_groups.data import NetworkSecurityGroup

'''
NETWORK_SECURITY_GROUP
'''
# TAB - Default
network_security_group_info_meta = ItemDynamicLayout.set_fields('Network Security Group', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account')
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
    TextDyField.data_source('Address Range', 'address_prefix'),
    TextDyField.data_source('Virtual Network', 'virtual_network')
])

network_security_group_meta = CloudServiceMeta.set_layouts(
    [network_security_group_info_meta, network_security_group_inbound_security_rules, network_subnets,
     network_security_group_outbound_security_rules, network_security_group_network_interfaces])


class NetworkResource(CloudServiceResource):
    cloud_service_group = StringType(default='NetworkSecurityGroups')


class NetworkSecurityGroupResource(NetworkResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(NetworkSecurityGroup)
    _metadata = ModelType(CloudServiceMeta, default=network_security_group_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class NetworkSecurityGroupResponse(CloudServiceResponse):
    resource = PolyModelType(NetworkSecurityGroupResource)
