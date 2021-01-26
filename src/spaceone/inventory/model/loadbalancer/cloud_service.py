from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.loadbalancer.data import LoadBalancer
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
LOAD_BALANCER
'''
# TAB - Default
# TODO : Resource Group, Location, Subscription, Subscription ID, SKU, Backend pool, Health probe,
#      : Load balancing rule, NAT Rules, Public IP Addresses, Load Balancing Type
load_balancer_info_meta = ItemDynamicLayout.set_fields('LoadBalancer', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource ID', 'data.id'),
])

# TAB - tags
load_balancer_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

# TAB - Frontend IP Confiuguration
# TODO : Name, IP Address, Rules Count, Type, Public IP Address

# TAB - Backend Pools
# TODO : Backendpool name, Virtual machine, VM status, Network interface, private IP address, availability zone

# TAB - Health Probes
# TODO : Name, Protocol, Port, Used By

# TAB _ Load Balancing Rules
# TODO : lb rules Name, Load balancing rule, Backend pool, Health probe

# TAB - Inbound NAT Rules
# TODO : NAT rule Name, IP version, destination, target, service

load_balancer_meta = CloudServiceMeta.set_layouts(
    [load_balancer_info_meta, load_balancer_info_tags])



class NetworkResource(CloudServiceResource):
    cloud_service_group = StringType(default='Network')


class LoadBalancerResource(NetworkResource):
    cloud_service_type = StringType(default='LoadBalancer')
    data = ModelType(LoadBalancer)
    _metadata = ModelType(CloudServiceMeta, default=load_balancer_meta, serialized_name='metadata')


class LoadBalancerResponse(CloudServiceResponse):
    resource = PolyModelType(LoadBalancerResource)
