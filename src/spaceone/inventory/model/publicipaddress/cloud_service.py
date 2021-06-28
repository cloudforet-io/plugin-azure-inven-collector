from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.publicipaddress.data import PublicIPAddress

'''
PUBLIC_IP_ADDRESS
'''
# TAB - Default
public_ip_address_meta = ItemDynamicLayout.set_fields('Public IP Address', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('SKU', ''),
    TextDyField.data_source('Tier', ''),
    TextDyField.data_source('IP Address', ''),
    TextDyField.data_source('DNS Name', ''),
    TextDyField.data_source('Associated To', '')
])

# TAB - Configuration
public_ip_address_configuration = ItemDynamicLayout.set_fields('Configuration', fields=[
    TextDyField.data_source('IP Address Assignment', ''),
    TextDyField.data_source('Idle Timeout(Minutes)', ''),
    TextDyField.data_source('DNS Name Label(Optional)', '')
])

# TAB - Alias Record Sets
public_ip_address_alias_record_sets = TableDynamicLayout.set_fields('Alias Record Sets', fields=[
    TextDyField.data_source('Subscription', 'enabled', default_state={
        'safe': [True],
        'warning': [False]
    }),
    TextDyField.data_source('DNS Zone', ''),
    TextDyField.data_source('Name', ''),
    TextDyField.data_source('Type', '')
])
public_ip_address_configuration_meta = ListDynamicLayout.set_layouts('Configuration', layouts=[
                                                                               public_ip_address_alias_record_sets,
    public_ip_address_configuration])

application_gateway_web_app_firewall_exclusions = SimpleTableDynamicLayout.set_fields('Exclusions', 'data.web_application_firewall_configuration.exclusions', fields=[
    TextDyField.data_source('Field', 'match_variable'),
    TextDyField.data_source('Operator', 'selector_match_operator'),
    TextDyField.data_source('Selector', 'selector')
])

public_ip_address_configuration_meta = ListDynamicLayout.set_layouts('Web Application Firewall', layouts=[
                                                                               public_ip_address_alias_record_sets,
                                                                               application_gateway_web_app_firewall_exclusions
                                                                               ])

# TAB - Backend Pools
# Name,Rule Associated, Targets
application_gateway_backend_pools = SimpleTableDynamicLayout.set_fields('Backend Pools', 'data.backend_address_pools', fields=[
    TextDyField.data_source('Name', 'name'),
    ListDyField.data_source('Rule Associated', 'associated_rules'),
    # TextDyField.data_source('Targets', '')
])

# TAB - HTTP Settings
application_gateway_http_settings = SimpleTableDynamicLayout.set_fields('HTTP Settings', 'data.backend_http_settings_collection', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Port', 'port'),
    TextDyField.data_source('Protocol', 'protocol'),
    EnumDyField.data_source('Cookie Based Affinity', 'cookie_based_affinity', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Custom Probe', 'custom_probe')
])

# TAB - SSL Settings
application_gateway_ssl_settings = SimpleTableDynamicLayout.set_fields('SSL Settings', 'data.ssl_profiles', fields=[
    TextDyField.data_source('Name', 'name'),
    ListDyField.data_source('Client Certificates', 'trusted_client_certificates.id'),
    TextDyField.data_source('SSL Policy Type', 'ssl_policy.policy_type'),
])

# TAB - Frontend IP Configurations
application_gateway_frontend_ip_configurations = SimpleTableDynamicLayout.set_fields('Frontend IP Configurations', 'data.frontend_ip_configurations', fields=[
    TextDyField.data_source('Type', 'ip_type'),
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('IP Address', 'ip_address'),
    TextDyField.data_source('Associated Listeners', 'associated_listeners')
])

# TAB - Listeners
application_gateway_listeners = SimpleTableDynamicLayout.set_fields('Listeners', 'data.http_listeners', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Protocol', 'protocol'),
    TextDyField.data_source('Port', 'port'),
    TextDyField.data_source('Associated Rule', 'associated_rules'),
    TextDyField.data_source('Host name', 'host_name')
])

application_gateway_listeners_custom = SimpleTableDynamicLayout.set_fields('Custom Error Configurations', 'data.custom_error_configurations', fields=[
    TextDyField.data_source('Listener Name', 'listener_name'),
    TextDyField.data_source('Status Code', 'status_code'),
    TextDyField.data_source('Custom Error Page URL', 'custom_error_page_url')
])

# 1 + 2) TAB - Listeners
application_gateway_listeners_info = ListDynamicLayout.set_layouts('Listeners', layouts=[
                                                                               application_gateway_listeners,
                                                                               application_gateway_listeners_custom])

# TAB - Rules
application_gateway_rules = SimpleTableDynamicLayout.set_fields('Rules', 'data.request_routing_rules', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Type', 'rule_type'),
    TextDyField.data_source('Listener', 'http_listener_name'),
    ListDyField.data_source('Rule Configuration', 'rule_configuration')
])

# TAB - Rewrites
application_gateway_rewrites = SimpleTableDynamicLayout.set_fields('Rewrites', 'data.rewrite_rule_sets', fields=[
    TextDyField.data_source('Rewrite Sets', 'name'),
    TextDyField.data_source('Type', 'rule_type'),
    TextDyField.data_source('Rules Applied', 'rules_applied'),
    ListDyField.data_source('Rewrite Rule Configuration', 'rewrite_rules_display')
])

# TAB - Health Probes
application_gateway_health_probes = SimpleTableDynamicLayout.set_fields('Health Probes', 'data.probes', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Protocol', 'protocol'),
    TextDyField.data_source('Host', 'host'),
    TextDyField.data_source('Path', 'path'),
    TextDyField.data_source('Timeout(Seconds)', 'timeout')
])

# TAB - tags
virtual_network_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

application_gateway_meta = CloudServiceMeta.set_layouts(
    [public_ip_address_meta, public_ip_address_configuration,
     public_ip_address_configuration_meta, application_gateway_backend_pools, application_gateway_http_settings,
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
