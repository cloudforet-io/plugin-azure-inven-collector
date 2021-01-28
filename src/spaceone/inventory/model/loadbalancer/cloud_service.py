from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.loadbalancer.data import LoadBalancer
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
LOAD_BALANCER
'''

# TAB - Default
# Resource Group, Location, Subscription, Subscription ID, SKU, Backend pool, Health probe,
# Load balancing rule, NAT Rules, Public IP Addresses, Load Balancing Type
load_balancer_info_meta = ItemDynamicLayout.set_fields('LoadBalancer', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_id'),
    TextDyField.data_source('SKU', 'data.sku.name'),
    TextDyField.data_source('Backend pools', 'data.backend_address_pools_count_display'),
    ListDyField.data_source('Health Probe', 'data.probes_display', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('Load Balancing Rule', 'data.load_balancing_rules_display', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('NAT Rules', 'data.inbound_nat_rules_display', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('Private IP Address', 'data.private_ip_address_display', options={
        'delimiter': '<br>'
    }),
])

# TAB - Frontend IP Configurations
# 1) Name, IP Address, Rules Count, Type, Public IP Address
load_balancer_info_frontend_ip_config = SimpleTableDynamicLayout.set_fields('Frontend IP Configurations',
                                                                      'data.frontend_ip_configurations', fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('IP Address', 'private_ip_address'),
        TextDyField.data_source('IP Version', 'private_ip_address_version'),
    ])


# 2) Used By
load_balancer_info_frontend_ip_config_rules = ItemDynamicLayout.set_fields('Used By', fields=[
    ListDyField.data_source('Used By', 'data.frontend_ip_configurations_used_by_display', options={
        'delimiter': '<br>'
    })
])

# 1 + 2) TAB - Frontend IP Configurations Meta
load_balancer_info_frontend_ip_config_meta = ListDynamicLayout.set_layouts('Frontend IP Configurations',
                                                                           layouts=[
                                                                               load_balancer_info_frontend_ip_config,
                                                                               load_balancer_info_frontend_ip_config_rules])

# TAB - Backend Pools
# 3) Backend pool name, Virtual Network, Private IP Address Version
load_balancer_info_backend_pools = SimpleTableDynamicLayout.set_fields('Backend Pools', 'data.backend_address_pools', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('ID', 'id')
])

# 4) Virtual machine, Load Balancer, Network interface, private IP address
load_balancer_info_backend_pools_vms = SimpleTableDynamicLayout.set_fields('Backend Pools VM information',
                                                                     'data.network_interfaces', fields=[
        TextDyField.data_source('Load Balancer', 'load_balancer_backend_address_pools_name_display'),
        TextDyField.data_source('VM Name', 'virtual_machine_name_display'),
        TextDyField.data_source('Network Interface', 'name'),
        TextDyField.data_source('Private IP Address', 'private_ip_display')
    ])

# 3 + 4) TAB - Backend Pools
load_balancer_info_backend_pools_meta = ListDynamicLayout.set_layouts('Backend Pools',
                                                                      layouts=[
                                                                          load_balancer_info_backend_pools,
                                                                          load_balancer_info_backend_pools_vms])
# TAB - Health Probes
# Name, Protocol, Port
load_balancer_info_health_probes = TableDynamicLayout.set_fields('Health Probes', 'data.probes', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Protocol', 'protocol'),
    TextDyField.data_source('Port', 'port'),
    TextDyField.data_source('Interval', 'interval_in_seconds'),
    TextDyField.data_source('Unhealthy Threshold', 'number_of_probes')
])

# TAB _ Load Balancing Rules
# LB rules Name, Load balancing rule, Health probe -> skip
load_balancer_info_load_balancing_rules = TableDynamicLayout.set_fields('Load Balancing Rules',
                                                                        'data.load_balancing_rules', fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Frontend IP Address', 'frontend_ip_configuration_display'),
        TextDyField.data_source('Protocol', 'protocol'),
        TextDyField.data_source('Frontend Port', 'frontend_port'),
        TextDyField.data_source('Backend Port', 'backend_port'),
        ListDyField.data_source('Backend Pool', 'backend_address_pool_display'),
        TextDyField.data_source('Session Persistence', 'load_distribution_display'),
        TextDyField.data_source('Idle Timeout (minutes)', 'idle_timeout_in_minutes'),
        TextDyField.data_source('Floating IP', 'enable_floating_ip'),
        TextDyField.data_source('TCP Reset', 'enable_tcp_reset'),

    ])

# TAB - Inbound NAT Rules
# Forwards incoming traffic sent to a selected IP address and port combination to a specific virtual machine
# NAT rule Name, IP version, destination, target, service
load_balancer_info_load_balancing_rules = TableDynamicLayout.set_fields('Inbound NAT Rules', 'data.inbound_nat_rules',
                                                                        fields=[
                                                                            TextDyField.data_source('Name', 'name'),
                                                                            TextDyField.data_source('Protocol',
                                                                                                    'protocol'),
                                                                            TextDyField.data_source(
                                                                                'Idle timeout (minutes)',
                                                                                'idle_timeout_in_minutes'),
                                                                            TextDyField.data_source('TCP Reset',
                                                                                                    'enable_tcp_reset'),
                                                                            TextDyField.data_source('Port',
                                                                                                    'frontend_port'),
                                                                            ListDyField.data_source(
                                                                                'Target Virtual Machine', 'target_virtual_machine'),  # *****
                                                                            TextDyField.data_source(
                                                                                'Network IP Configuration',
                                                                                'frontend_ip_configuration_display'),
                                                                            TextDyField.data_source('Port mapping',
                                                                                                    'port_mapping_display'),
                                                                            TextDyField.data_source('Floating IP',
                                                                                                    'enable_floating_ip'),
                                                                            TextDyField.data_source('Target Port',
                                                                                                    'backend_port')
                                                                        ])
# TextDyField.data_source('IP Version', 'frontend_ip_configurations...private_ip_address_version'),
# TextDyField.data_source('Destination', 'private_ip_address'),

# TAB - tags
load_balancer_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

load_balancer_meta = CloudServiceMeta.set_layouts(
    [load_balancer_info_meta, load_balancer_info_frontend_ip_config_meta, load_balancer_info_backend_pools_meta,
     load_balancer_info_health_probes,
     load_balancer_info_load_balancing_rules, load_balancer_info_tags])


class NetworkResource(CloudServiceResource):
    cloud_service_group = StringType(default='Network')


class LoadBalancerResource(NetworkResource):
    cloud_service_type = StringType(default='LoadBalancers')
    data = ModelType(LoadBalancer)
    _metadata = ModelType(CloudServiceMeta, default=load_balancer_meta, serialized_name='metadata')


class LoadBalancerResponse(CloudServiceResponse):
    resource = PolyModelType(LoadBalancerResource)
