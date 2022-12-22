import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import ASSET_URL

current_dir = os.path.abspath(os.path.dirname(__file__))
load_balancers_backendpool_vm_count_by_region_conf = os.path.join(current_dir, 'widget/load_balancers_backendpool_vm_count_by_region.yaml')
load_balancers_count_by_account_conf = os.path.join(current_dir, 'widget/load_balancers_count_by_account.yaml')
load_balancers_count_by_region_conf = os.path.join(current_dir, 'widget/load_balancers_count_by_region.yaml')
load_balancers_count_by_subscription_conf = os.path.join(current_dir, 'widget/load_balancers_count_by_subscription.yaml')
load_balancers_total_count_conf = os.path.join(current_dir, 'widget/load_balancers_total_count.yaml')

cst_load_balancers = CloudServiceTypeResource()
cst_load_balancers.name = 'Instance'
cst_load_balancers.group = 'LoadBalancers'
cst_load_balancers.service_code = 'Microsoft.Network/loadBalancers'
cst_load_balancers.labels = ['Networking']
cst_load_balancers.is_major = True
cst_load_balancers.is_primary = True
cst_load_balancers.tags = {
    'spaceone:icon': f'{ASSET_URL}/azure-loadbalancers.svg',
}

cst_load_balancers._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('SKU', 'instance_type', options={
            'is_optional': True
        }),
        ListDyField.data_source('Health Probe', 'data.probes_display', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Load Balancing Rule', 'data.load_balancing_rules_display', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('NAT Rules', 'data.inbound_nat_rules_display', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Private IP Address', 'data.private_ip_address_display', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        # is_optional fields- Frontend IP Configurations
        TextDyField.data_source('Frontend Name', 'data.frontend_ip_configurations.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Frontend IP Address', 'data.frontend_ip_configurations.private_ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Frontend IP Version', 'data.frontend_ip_configurations.private_ip_address_version', options={
            'is_optional': True
        }),
        ListDyField.data_source('Frontend IP Used By', 'data.frontend_ip_configurations_used_by_display', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        # is_optional fields- Backend Pools
        TextDyField.data_source('Backend Pool Name', 'data.backend_address_pools.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backend Pool ID', 'data.backend_address_pools.id', options={
            'is_optional': True
        }),
        # is_optional fields - Health Probes
        TextDyField.data_source('Health Probe Name', 'data.probes.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Probes Protocol', 'data.probes.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Probes Port', 'data.probes.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Probes Interval', 'data.probes.interval_in_seconds', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Probes Unhealthy Threshold', 'data.probes.number_of_probes', options={
            'is_optional': True
        }),
        # is_optional fields - Load Balancing Rules
        TextDyField.data_source('LB Rule Name', 'data.load_balancing_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('LB Rule Frontend IP Address', 'data.load_balancing_rules.frontend_ip_configuration_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('LB Rule Protocol', 'data.load_balancing_rules.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('LB Rule Frontend Port', 'data.load_balancing_rules.frontend_port', options={
            'is_optional': True
        }),
        TextDyField.data_source('LB Rule Backend Port', 'data.load_balancing_rules.backend_port', options={
            'is_optional': True
        }),
        ListDyField.data_source('LB Rule Backend Pool', 'data.load_balancing_rules.backend_address_pool_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('LB Rule Session Persistence', 'data.load_balancing_rules.load_distribution_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('LB Rule Idle Timeout (minutes)', 'data.load_balancing_rules.idle_timeout_in_minutes', options={
            'is_optional': True
        }),
        TextDyField.data_source('LB Rule Floating IP', 'data.load_balancing_rules.enable_floating_ip', options={
            'is_optional': True
        }),
        TextDyField.data_source('LB Rule TCP Reset', 'data.load_balancing_rules.enable_tcp_reset', options={
            'is_optional': True
        }),
        # is_optional fields - Inbound NAT Rules
        TextDyField.data_source('Inbound NAT Rules Name', 'data.inbound_nat_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound NAT Rule Protocol', 'data.inbound_nat_rules.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound NAT Rule Idle timeout (minutes)', 'data.inbound_nat_rules.idle_timeout_in_minutes', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound NAT Rule TCP Reset', 'data.inbound_nat_rules.enable_tcp_reset', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound NAT Rule Port', 'data.inbound_nat_rules.frontend_port', options={
            'is_optional': True
        }),
        ListDyField.data_source('Inbound NAT Rule Target Virtual Machine', 'data.inbound_nat_rules.target_virtual_machine', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound NAT Rule Network IP Configuration', 'data.inbound_nat_rules.frontend_ip_configuration_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound NAT Rule Port mapping', 'data.inbound_nat_rules.port_mapping_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound NAT Rule Floating IP', 'data.inbound_nat_rules.enable_floating_ip', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound NAT Rule Target Port', 'data.inbound_nat_rules.backend_port', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Load Balancer Type', key='instance_type'),
        SearchField.set(name='SKU', key='instance_type'),
        SearchField.set(name='Health Probe', key='data.probes_display'),
        SearchField.set(name='Load Balancing Rule', key='data.load_balancing_rules_display'),
        SearchField.set(name='NAT Rules', key='data.inbound_nat_rules_display'),
        SearchField.set(name='Private IP Address', key='data.private_ip_address_display'),
        SearchField.set(name='Frontend Name', key='data.frontend_ip_configurations.name'),
        SearchField.set(name='Frontend IP Address', key='data.frontend_ip_configurations.private_ip_address'),
        SearchField.set(name='Frontend IP Version', key='data.frontend_ip_configurations.private_ip_address_version'),
        SearchField.set(name='Frontend IP Used By', key='data.frontend_ip_configurations_used_by_display'),
        SearchField.set(name='Backend Pool Name', key='data.backend_address_pools.name'),
        SearchField.set(name='Backend Pool ID', key='data.backend_address_pools.id'),
        SearchField.set(name='Health Probe Name', key='data.probes.name'),
        SearchField.set(name='Health Probes Protocol', key='data.probes.protocol'),
        SearchField.set(name='Health Probes Port', key='data.probes.port', data_type='integer'),
        SearchField.set(name='Health Probes Interval', key='data.probes.interval_in_seconds', data_type='integer'),
        SearchField.set(name='Health Probes Unhealthy Threshold', key='data.probes.number_of_probes'),
        SearchField.set(name='LB Rule Name', key='data.load_balancing_rules.name'),
        SearchField.set(name='LB Rule Frontend IP Address', key='data.load_balancing_rules.frontend_ip_configuration_display'),
        SearchField.set(name='LB Rule Protocol', key='data.load_balancing_rules.protocol'),
        SearchField.set(name='LB Rule Frontend Port', key='data.load_balancing_rules.frontend_port', data_type='integer'),
        SearchField.set(name='LB Rule Backend Port', key='data.load_balancing_rules.backend_port', data_type='integer'),
        SearchField.set(name='LB Rule Backend Pool', key='data.load_balancing_rules.backend_address_pool_display'),
        SearchField.set(name='LB Rule Session Persistence', key='data.load_balancing_rules.load_distribution_display'),
        SearchField.set(name='LB Rule Idle Timeout (minutes)', key='data.load_balancing_rules.idle_timeout_in_minutes', data_type='integer'),
        SearchField.set(name='LB Rule Floating IP', key='data.load_balancing_rules.enable_floating_ip'),
        SearchField.set(name='LB Rule TCP Reset', key='data.load_balancing_rules.enable_tcp_reset'),
        SearchField.set(name='Inbound NAT Rules Name', key='data.inbound_nat_rules.name'),
        SearchField.set(name='Inbound NAT Rule Protocol', key='data.inbound_nat_rules.protocol'),
        SearchField.set(name='Inbound NAT Rule Idle timeout (minutes)', key='data.inbound_nat_rules.idle_timeout_in_minutes', data_type='integer'),
        SearchField.set(name='Inbound NAT Rule TCP Reset', key='data.load_balancing_rules.enable_tcp_reset'),
        SearchField.set(name='Inbound NAT Rule Port', key='data.inbound_nat_rules.frontend_port', data_type='integer'),
        SearchField.set(name='Inbound NAT Rule Target Virtual Machine', key='data.inbound_nat_rules.target_virtual_machine'),
        SearchField.set(name='Inbound NAT Rule Network IP Configuration', key='data.inbound_nat_rules.frontend_ip_configuration_display'),
        SearchField.set(name='Inbound NAT Rule Port mapping', key='data.inbound_nat_rules.port_mapping_display'),
        SearchField.set(name='Inbound NAT Rule Floating IP', key='data.inbound_nat_rules.enable_floating_ip'),
        SearchField.set(name='Inbound NAT Rule Target Port', key='data.inbound_nat_rules.backend_port', data_type='integer'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(load_balancers_backendpool_vm_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(load_balancers_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(load_balancers_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(load_balancers_count_by_subscription_conf)),
        CardWidget.set(**get_data_from_yaml(load_balancers_total_count_conf)),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_load_balancers}),
]
