from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_load_balancer = CloudServiceTypeResource()
cst_load_balancer.name = 'LoadBalancer'
cst_load_balancer.group = 'Network'
cst_load_balancer.service_code = 'Microsoft.Network/loadBalancers'
cst_load_balancer.labels = ['Network']
cst_load_balancer.is_major = True
cst_load_balancer.is_primary = True
cst_load_balancer.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-loadbalancers.svg',
}

cst_load_balancer._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        # is_optional fields- Default
        TextDyField.data_source('Resource ID', 'data.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('SKU', 'data.sku.name', options={
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
        TextDyField.data_source('Load Balancing Rule Name', 'data.load_balancing_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Rule Frontend IP Address', 'data.load_balancing_rules.frontend_ip_configuration_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Rule Protocol', 'data.load_balancing_rules.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Rule Frontend Port', 'data.load_balancing_rules.frontend_port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Rule Backend Port', 'data.load_balancing_rules.backend_port', options={
            'is_optional': True
        }),
        ListDyField.data_source('Load Balancing Rule Backend Pool', 'data.load_balancing_rules.backend_address_pool_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Rule Session Persistence', 'data.load_balancing_rules.load_distribution_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Rule Idle Timeout (minutes)', 'data.load_balancing_rules.idle_timeout_in_minutes', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Rule Floating IP', 'data.load_balancing_rules.enable_floating_ip', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Rule TCP Reset', 'data.load_balancing_rules.enable_tcp_reset', options={
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
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Load Balancer Type', key='data.sku.name', data_type='string'),


    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_load_balancer}),
]
