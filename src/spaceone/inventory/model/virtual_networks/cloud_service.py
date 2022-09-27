from schematics.types import ModelType, StringType, PolyModelType, DateTimeType, FloatType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.virtual_networks.data import VirtualNetwork

'''
VIRTUAL_NETWORK
'''
# TAB - Default
virtual_network_info_meta = ItemDynamicLayout.set_fields('Virtual Network', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
    ListDyField.data_source('DNS servers', 'data.dhcp_options.dns_servers'),
    EnumDyField.data_source('DDoS Protection Standard', 'data.enable_ddos_protection', default_state={
        'safe': ['True'],
        'warning': ['False']
    }),
    TextDyField.data_source('Resource GUID', 'data.resource_guid'),
    ListDyField.data_source('Address Space', 'data.address_space.address_prefixes')
])


'''
# TAB - Address Space - 
# Address space, Address range, Address count
virtual_network_address_space = ItemDynamicLayout.set_fields('Address Space', 'data.address_space', fields=[
    ListDyField.data_source('Address Space', 'address_prefixes'),
    TextDyField.data_source('Address Range', ''),
    TextDyField.data_source('Address Count', '')
])
'''

# TAB - Connected Devices
virtual_network_connected_devices = SimpleTableDynamicLayout.set_fields('Connected Devices', 'data.connected_devices', fields=[
    TextDyField.data_source('Device', 'device'),
    TextDyField.data_source('Type', 'type'),
    # TextDyField.data_source('IP Address', ''),
    TextDyField.data_source('Subnet', 'name')  # TODO : 210713
])

# TAB - Subnets
# Name, IPv4, IPv6, Available Ips, Delegated To, Security Group
virtual_network_subnets = SimpleTableDynamicLayout.set_fields('Subnets', 'data.subnets', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('IP Address Prefix', 'address_prefix'),
    ListDyField.data_source('IP Address Prefixes', 'address_prefixes'),
    TextDyField.data_source('Delegated To', 'delegations.name'),
    TextDyField.data_source('Security Group', 'network_security_group.name')
])


# TAB - Firewall
# Name, IP Address, Subnet
virtual_network_firewall = SimpleTableDynamicLayout.set_fields('Firewall', 'data.azure_firewall', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('IP Address', 'ip_configurations.private_ip_address'),
    TextDyField.data_source('Subnet', 'subnet')
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

virtual_network_meta = CloudServiceMeta.set_layouts(
    [virtual_network_info_meta, virtual_network_connected_devices,
     virtual_network_subnets, virtual_network_firewall, virtual_network_peerings, virtual_network_service_endpoints, virtual_network_private_endpoints, virtual_network_tags])


class NetworkResource(CloudServiceResource):
    cloud_service_group = StringType(default='VirtualNetworks')


class VirtualNetworkResource(NetworkResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(VirtualNetwork)
    _metadata = ModelType(CloudServiceMeta, default=virtual_network_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)


class VirtualNetworkResponse(CloudServiceResponse):
    resource = PolyModelType(VirtualNetworkResource)
