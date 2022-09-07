from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.nat_gateways.data import NatGateway

'''
NAT GATEWAY
'''
# TAB - Default
nat_gateway_info_meta = ItemDynamicLayout.set_fields('NAT Gateway', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
    TextDyField.data_source('Subnets', 'data.subnets_count'),
    TextDyField.data_source('Public IP Addresses', 'data.public_ip_addresses_count'),
    TextDyField.data_source('Public IP Prefixes', 'data.public_ip_prefixes_count'),
    TextDyField.data_source('Idle Timeout (minutes)', 'data.idle_timeout_in_minutes'),
])

# TAB - Outbound IP
nat_gateway_outbound_ip_public_ip_addresses = SimpleTableDynamicLayout.set_fields('Public IP Addresses', 'data.public_ip_addresses', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('IP Address', 'ip_address'),
    TextDyField.data_source('DNS Name', 'dns_settings.domain_name_label')
])

nat_gateway_outbound_ip_public_ip_prefixes = SimpleTableDynamicLayout.set_fields('Public IP Prefixes', 'data.public_ip_prefixes', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('IP Prefix', 'ip_prefix')
])
nat_gateway_outbound_ip_info = ListDynamicLayout.set_layouts('Outbound IP', layouts=[nat_gateway_outbound_ip_public_ip_addresses, nat_gateway_outbound_ip_public_ip_prefixes])

nat_gateway_subnets = SimpleTableDynamicLayout.set_fields('Subnets', 'data.subnets', fields=[
    TextDyField.data_source('Subnet Name', 'name'),
    TextDyField.data_source('Subnet Address ', 'address_prefix'),
    TextDyField.data_source('Subnet Addresses', 'address_prefixes'),
    TextDyField.data_source('Virtual Network', 'virtual_network'),
    EnumDyField.data_source('Private Endpoint Network Policies', 'private_endpoint_network_policies', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    EnumDyField.data_source('Private Link Service Network Policies', 'private_link_service_network_policies', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    })
])

# TAB - tags
nat_gateway_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

nat_gateway_meta = CloudServiceMeta.set_layouts(
    [nat_gateway_info_meta, nat_gateway_outbound_ip_info, nat_gateway_subnets, nat_gateway_tags])


class NetworkResource(CloudServiceResource):
    cloud_service_group = StringType(default='NATGateways')


class NatGatewayResource(NetworkResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(NatGateway)
    _metadata = ModelType(CloudServiceMeta, default=nat_gateway_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)


class NatGatewayResponse(CloudServiceResponse):
    resource = PolyModelType(NatGatewayResource)
