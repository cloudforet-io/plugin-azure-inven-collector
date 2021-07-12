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
    TextDyField.data_source('Name', 'data.name', options={
        'is_optional': True
    }),
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
    TextDyField.data_source('Capacity ', 'data.sku.tier', options={
        'is_optional': True
    }),
    # TextDyField.data_source('Capacity Type', ''),
    TextDyField.data_source('Minimum Instance Count', 'data.autoscale_configuration.min_capacity', options= {
        'is_optional': True
    }),
    TextDyField.data_source('Maximum Instance Count', 'data.autoscale_configuration.max_capacity', options= {
        'is_optional': True
    }),
    TextDyField.data_source('Enable HTTP2', 'data.enable_http2',  options={
        'is_optional': True
    })
])

# TAB - Subnets
# Name, IPv4, IPv6, Available Ips, Delegated To, Security Group
application_gateway_web_app_firewall = ItemDynamicLayout.set_fields('Web Application Firewall', 'data.web_application_firewall_configuration', fields=[
    EnumDyField.data_source('Firewall Status Enabled', 'enabled', default_state={
        'safe': [True],
        'warning': [False]
    }),
    TextDyField.data_source('Firewall Mode', 'firewall_mode'),
    EnumDyField.data_source('Inspect Request Body', 'request_body_check', default_state={
        'safe': [True],
        'warning':[False]
    }),
    TextDyField.data_source('Max Request Body Size(KB)', 'max_request_body_size_in_kb',  options={
        'is_optional': True
    }),
    TextDyField.data_source('File Upload Limit(MB)', 'file_upload_limit_in_mb',  options={
        'is_optional': True
    }),
    TextDyField.data_source('Rule Set Type', 'rule_set_type',  options={
        'is_optional': True
    }),
    TextDyField.data_source('Rule Set Version', 'rule_set_version', options={
        'is_optional': True
    })
    # TextDyField.data_source('Advanced Rule Configuration', ''),

])

application_gateway_web_app_firewall_exclusions = SimpleTableDynamicLayout.set_fields('Exclusions', 'data.web_application_firewall_configuration.exclusions', fields=[
    TextDyField.data_source('Field', 'match_variable', options={
        'is_optional': True
    }),
    TextDyField.data_source('Operator', 'selector_match_operator', options={
        'is_optional': True
    }),
    TextDyField.data_source('Selector', 'selector', options={
        'is_optional': True
    })
])

application_gateway_web_app_firewall_meta = ListDynamicLayout.set_layouts('Web Application Firewall', layouts=[
                                                                               application_gateway_web_app_firewall,
                                                                               application_gateway_web_app_firewall_exclusions
                                                                               ])

# TAB - Backend Pools
# Name,Rule Associated, Targets
application_gateway_backend_pools = SimpleTableDynamicLayout.set_fields('Backend Pools', 'data.backend_address_pools', fields=[
    TextDyField.data_source('Name', 'name', options={
        'is_optional': True
    }),
    ListDyField.data_source('Rule Associated', 'associated_rules', options={
        'is_optional': True
    }),
    # TextDyField.data_source('Targets', '')
])

# TAB - HTTP Settings
application_gateway_http_settings = SimpleTableDynamicLayout.set_fields('HTTP Settings', 'data.backend_http_settings_collection', fields=[
    TextDyField.data_source('Name', 'name', options={
        'is_optional': True
    }),
    TextDyField.data_source('Port', 'port', options={
        'is_optional': True
    }),
    TextDyField.data_source('Protocol', 'protocol', options={
        'is_optional': True
    }),
    EnumDyField.data_source('Cookie Based Affinity', 'cookie_based_affinity', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Custom Probe', 'custom_probe')
])

# TAB - SSL Settings
application_gateway_ssl_settings = SimpleTableDynamicLayout.set_fields('SSL Settings', 'data.ssl_profiles', fields=[
    TextDyField.data_source('Name', 'name', options={
        'is_optional': True
    }),
    ListDyField.data_source('Client Certificates', 'trusted_client_certificates.id', options={
        'is_optional': True
    }),
    TextDyField.data_source('SSL Policy Type', 'ssl_policy.policy_type', options={
        'is_optional': True
    }),
])

# TAB - Frontend IP Configurations
application_gateway_frontend_ip_configurations = SimpleTableDynamicLayout.set_fields('Frontend IP Configurations', 'data.frontend_ip_configurations', fields=[
    TextDyField.data_source('Type', 'ip_type', options={
        'is_optional': True
    }),
    TextDyField.data_source('Name', 'name', options={
        'is_optional': True
    }),
    TextDyField.data_source('IP Address', 'ip_address', options={
        'is_optional': True
    }),
    TextDyField.data_source('Associated Listeners', 'associated_listeners', options={
        'is_optional': True
    })
])

# TAB - Listeners
application_gateway_listeners = SimpleTableDynamicLayout.set_fields('Listeners', 'data.http_listeners', fields=[
    TextDyField.data_source('Name', 'name', options={
        'is_optional': True
    }),
    TextDyField.data_source('Protocol', 'protocol', options={
        'is_optional': True
    }),
    TextDyField.data_source('Port', 'port', options={
        'is_optional': True
    }),
    TextDyField.data_source('Associated Rule', 'associated_rules', options={
        'is_optional': True
    }),
    TextDyField.data_source('Host name', 'host_name', options={
        'is_optional': True
    })
])

application_gateway_listeners_custom = SimpleTableDynamicLayout.set_fields('Custom Error Configurations', 'data.custom_error_configurations', fields=[
    TextDyField.data_source('Listener Name', 'listener_name', options={
        'is_optional': True
    }),
    TextDyField.data_source('Status Code', 'status_code', options={
        'is_optional': True
    }),
    TextDyField.data_source('Custom Error Page URL', 'custom_error_page_url', options={
        'is_optional': True
    })
])

# 1 + 2) TAB - Listeners
application_gateway_listeners_info = ListDynamicLayout.set_layouts('Listeners', layouts=[
                                                                               application_gateway_listeners,
                                                                               application_gateway_listeners_custom])

# TAB - Rules
application_gateway_rules = SimpleTableDynamicLayout.set_fields('Rules', 'data.request_routing_rules', fields=[
    TextDyField.data_source('Name', 'name', options={
        'is_optional': True
    }),
    TextDyField.data_source('Type', 'rule_type', options={
        'is_optional': True
    }),
    TextDyField.data_source('Listener', 'http_listener_name', options={
        'is_optional': True
    }),
    ListDyField.data_source('Rule Configuration', 'rule_configuration')
])

# TAB - Rewrites
application_gateway_rewrites = SimpleTableDynamicLayout.set_fields('Rewrites', 'data.rewrite_rule_sets', fields=[
    TextDyField.data_source('Rewrite Sets', 'name', options={
        'is_optional': True
    }),
    TextDyField.data_source('Type', 'rule_type', options={
        'is_optional': True
    }),
    TextDyField.data_source('Rules Applied', 'rules_applied', options={
        'is_optional': True
    }),
    ListDyField.data_source('Rewrite Rule Configuration', 'rewrite_rules_display', options={
        'is_optional': True
    })
])

# TAB - Health Probes
application_gateway_health_probes = SimpleTableDynamicLayout.set_fields('Health Probes', 'data.probes', fields=[
    TextDyField.data_source('Name', 'name', options={
        'is_optional': True
    }),
    TextDyField.data_source('Protocol', 'protocol', options={
        'is_optional': True
    }),
    TextDyField.data_source('Host', 'host', options={
        'is_optional': True
    }),
    TextDyField.data_source('Path', 'path', options={
        'is_optional': True
    }),
    TextDyField.data_source('Timeout(Seconds)', 'timeout', options={
        'is_optional': True
    })
])

# TAB - tags
virtual_network_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

application_gateway_meta = CloudServiceMeta.set_layouts(
    [application_gateway_info_meta, application_gateway_configuration,
     application_gateway_web_app_firewall_meta, application_gateway_backend_pools, application_gateway_http_settings,
     application_gateway_frontend_ip_configurations, application_gateway_rules, application_gateway_listeners_info,
     application_gateway_rewrites, application_gateway_health_probes])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Network')


class ApplicationGatewayResource(ComputeResource):
    cloud_service_type = StringType(default='ApplicationGateway')
    data = ModelType(ApplicationGateway)
    _metadata = ModelType(CloudServiceMeta, default=application_gateway_meta, serialized_name='metadata')
    name = StringType()


class ApplicationGatewayResponse(CloudServiceResponse):
    resource = PolyModelType(ApplicationGatewayResource)
