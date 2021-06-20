from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.applicationgateway.data import ApplicationGateway

'''
APPLICATION_GATEWAY
'''
# TAB - Default
application_gateway_info_meta = ItemDynamicLayout.set_fields('Application Gateway', fields=[
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

# TAB - Configuration
application_gateway_configuration = ItemDynamicLayout.set_fields('Configuration', fields=[
    TextDyField.data_source('Capacity ', 'data.sku.tier'),
    TextDyField.data_source('Capacity Type', ''), # TODO
    TextDyField.data_source('Minimum Instance Count', 'autoscale_configuration.min_capacity'),
    TextDyField.data_source('Maximum Instance Count', 'autoscale_configuration.max_capacity'),
    TextDyField.data_source('Enable HTTP2', 'enable_http2')
])

# TAB - Subnets
# Name, IPv4, IPv6, Available Ips, Delegated To, Security Group
application_gateway_web_app_firewall = ItemDynamicLayout.set_fields('Web Application Firewall', 'data.web_application_firewall_configuration', fields=[
    EnumDyField.data_source('Firewall Status Enabled', 'enabled', default_state={
        'safe':['True'],
        'warning': ['False']
    }),
    TextDyField.data_source('Firewall Mode', 'firewall_mode'),
    ListDyField.data_source('IP Address Prefixes', 'address_prefixes'),
    TextDyField.data_source('Global Parameters', ''),
    TextDyField.data_source('Max Request Body Size(KB)', 'max_request_body_size_in_kb'),
    TextDyField.data_source('File Upload Limit(MB)', 'file_upload_limit_in_mb'),
    TextDyField.data_source('Rule Set Type', 'rule_set_type'),
    TextDyField.data_source('Rule Set Version', 'rule_set_version'),
    TextDyField.data_source('Advanced Rule Configuration', ''),

])

application_gateway_web_app_firewall_exclusions = SimpleTableDynamicLayout.set_fields('Exclusions', 'data.web_application_firewall_configuration.exclusions', fields=[
    TextDyField.data_source('Field', 'match_variable'),
    TextDyField.data_source('Operator', 'selector_match_operator'),
    TextDyField.data_source('Selector', 'selector')
])

application_gateway_web_app_firewall_meta = ListDynamicLayout.set_layouts('Web Application Firewall',
                                                                           layouts=[
                                                                               application_gateway_web_app_firewall,
                                                                               application_gateway_web_app_firewall_exclusions
                                                                               ])

# TAB - Peerings
# Name, Peering Status, Peer, Gateway Transit
virtual_network_peerings = SimpleTableDynamicLayout.set_fields('Peerings', 'data.virtual_network_peerings', fields=[
    TextDyField.data_source('Name', 'name'),
    EnumDyField.data_source('Peering Status', 'peering_state', default_state={
        'safe': ['Connected'],
        'warning': ['Disconnected', 'Initiated']
    }),
    TextDyField.data_source('Peer', 'remote_virtual_network.id'),
    TextDyField.data_source('Gateway Transit', 'allow_gateway_transit')
])

virtual_network_service_endpoints = SimpleTableDynamicLayout.set_fields('Service Endpoints', 'data.service_endpoints', fields=[
    TextDyField.data_source('Service', 'service'),
    TextDyField.data_source('Subnet', 'subnet'),
    EnumDyField.data_source('Status', 'provisioning_state', default_state={
        'safe': ['Succeeded'],
        'warning': ['Failed', 'Deleting', 'Updating']
    }),
    TextDyField.data_source('Locations', 'locations')
])

# TAB - Private Endpoints
virtual_network_private_endpoints = SimpleTableDynamicLayout.set_fields('Private Endpoints', 'data.private_endpoints', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Subnet', 'subnet'),
    TextDyField.data_source('Resource Group', 'resource_group')
])

# TAB - tags
virtual_network_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

application_gateway_meta = CloudServiceMeta.set_layouts(
    [application_gateway_info_meta, application_gateway_configuration,
     application_gateway_web_app_firewall, virtual_network_peerings, virtual_network_service_endpoints, virtual_network_private_endpoints, virtual_network_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Network')


class ApplicationGatewayResource(ComputeResource):
    cloud_service_type = StringType(default='ApplicationGateway')
    data = ModelType(ApplicationGateway)
    _metadata = ModelType(CloudServiceMeta, default=application_gateway_meta, serialized_name='metadata')
    name = StringType()


class ApplicationGatewayResponse(CloudServiceResponse):
    resource = PolyModelType(ApplicationGatewayResource)
