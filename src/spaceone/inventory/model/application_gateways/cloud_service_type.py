import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import ASSET_URL

current_dir = os.path.abspath(os.path.dirname(__file__))

ag_count_by_account_conf = os.path.join(current_dir, 'widget/application_gateways_count_by_account.yaml')
ag_count_by_subscription_conf = os.path.join(current_dir, 'widget/application_gateways_count_by_subscription.yaml')
ag_count_by_location_conf = os.path.join(current_dir, 'widget/application_gateways_count_by_region.yaml')
ag_total_count_conf = os.path.join(current_dir, 'widget/application_gateways_total_count.yaml')

cst_application_gateways = CloudServiceTypeResource()
cst_application_gateways.name = 'Instance'
cst_application_gateways.group = 'ApplicationGateways'
cst_application_gateways.service_code = 'Microsoft.Network/applicationGateways'
cst_application_gateways.labels = ['Networking']
cst_application_gateways.is_major = True
cst_application_gateways.is_primary = True
cst_application_gateways.tags = {
    'spaceone:icon': f'{ASSET_URL}/azure-application-gateways.svg',
}

cst_application_gateways._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Public IP Address', 'data.public_ip_address.ip_address'),
        TextDyField.data_source('Private IP Address', 'data.private_ip_address'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id', options={
            'is_optional': True
        }),
        # is_optional fields - Configuration
        TextDyField.data_source('Capacity', 'data.sku.tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Minimum Instance Count', 'data.autoscale_configuration.min_capacity', options={
            'is_optional': True
        }),
        TextDyField.data_source('Maximum Instance Count', 'data.autoscale_configuration.max_capacity', options={
            'is_optional': True
        }),
        TextDyField.data_source('Enable HTTP2', 'data.enable_http2',  options={
            'is_optional': True
        }),
        # is_optional fields - Firewall
        TextDyField.data_source('Firewall Mode', 'data.web_application_firewall_configuration.firewall_mode', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Max Request Body Size(KB)',
                                'data.web_application_firewall_configuration.max_request_body_size_in_kb', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall File Upload Limit(MB)', 'data.web_application_firewall_configuration.file_upload_limit_in_mb', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Rule Set Type', 'data.web_application_firewall_configuration.rule_set_type',  options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Rule Set Version', 'data.web_application_firewall_configuration.rule_set_version', options={
            'is_optional': True
        }),
        # is_optional fields - Firewall
        TextDyField.data_source('Backend Address Pool Name', 'data.backend_address_pools.name', options={
            'is_optional': True
        }),
        ListDyField.data_source('Backend Address Rule Associated', 'data.backend_address_pools.associated_rules', options={
            'is_optional': True
        }),
        # is_optional fields - HTTP Settings
        TextDyField.data_source('HTTP Backend Name', 'data.backend_http_settings_collection.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('HTTP Backend Port', 'data.backend_http_settings_collection.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('HTTP Backend Protocol', 'data.backend_http_settings_collection.protocol', options={
            'is_optional': True
        }),
        # is_optional fields - SSL settings
        TextDyField.data_source('SSL Profile Name', 'data.ssl_profiles.name', options={
            'is_optional': True
        }),
        ListDyField.data_source('SSL Client Certificates', 'data.ssl_profiles.trusted_client_certificates.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('SSL Policy Type', 'data.ssl_profiles.ssl_policy.policy_type', options={
            'is_optional': True
        }),
        # is_optional fields - Frontend IP Configurations
        TextDyField.data_source('Frontend IP Type', 'data.frontend_ip_configurations.ip_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Frontend IP Configuration Name', 'data.frontend_ip_configurations.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Frontend IP Address', 'data.frontend_ip_configurations.ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Frontend Associated Listeners', 'data.frontend_ip_configurations.associated_listeners', options={
            'is_optional': True
        }),
        # is_optional fields - Listeners
        TextDyField.data_source('HTTP Listener Name', 'data.http_listeners.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('HTTP Listener Protocol', 'data.http_listeners.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('HTTP Listener Port', 'data.http_listeners.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('HTTP Listener Associated Rule', 'data.http_listeners.associated_rules', options={
            'is_optional': True
        }),
        TextDyField.data_source('HTTP Listener Host name', 'data.http_listeners.host_name', options={
            'is_optional': True
        }),
        # is_optional fields - Rules
        TextDyField.data_source('Request Routing Rule Name', 'data.request_routing_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Request Routing Rule Type', 'data.request_routing_rules.rule_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Request Routing Rule Listener', 'data.request_routing_rules.http_listener_name', options={
            'is_optional': True
        }),
        # is_optional fields - Health Probes
        TextDyField.data_source('Health Probes Name', 'data.probes.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Probes Protocol', 'data.probes.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Probes Host', 'data.probes.host', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Probes Path', 'data.probes.path', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Probes Timeout(Seconds)', 'data.probes.timeout', options={
            'is_optional': True
        })

    ],
    search=[
        SearchField.set(name='Subscription ID', key='data.subscription_id'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Public IP Address', key='data.public_ip_address.ip_address'),
        SearchField.set(name='Private IP Address', key='data.private_ip_address'),
        SearchField.set(name='Capacity', key='data.sku.tier'),
        SearchField.set(name='Minimum Instance Count',
                        key='data.autoscale_configuration.min_capacity',
                        data_type='integer'),
        SearchField.set(name='Maximum Instance Count',
                        key='data.autoscale_configuration.max_capacity',
                        data_type='integer'),
        SearchField.set(name='Enable HTTP2',
                        key='data.enable_http2',
                        data_type='boolean'),
        SearchField.set(name='Firewall Mode',
                        key='data.web_application_firewall_configuration.firewall_mode'),
        SearchField.set(name='Firewall Rule Set Type',
                        key='data.web_application_firewall_configuration.rule_set_type'),
        SearchField.set(name='Firewall Rule Set Version',
                        key='data.web_application_firewall_configuration.rule_set_version'),
        SearchField.set(name='Backend Address Pool Name',
                        key='data.backend_address_pools.name'),
        SearchField.set(name='Backend Address Rule Associated',
                        key='data.backend_address_pools.associated_rules'),
        SearchField.set(name='HTTP Backend Name',
                        key='data.backend_http_settings_collection.name'),
        SearchField.set(name='HTTP Backend Port',
                        key='data.backend_http_settings_collection.port'),
        SearchField.set(name='HTTP Backend Protocol',
                        key='data.backend_http_settings_collection.protocol'),
        SearchField.set(name='SSL Profile Name',
                        key='data.ssl_profiles.name'),
        SearchField.set(name='SSL Client Certificates',
                        key='data.ssl_profiles.trusted_client_certificates.id'),
        SearchField.set(name='SSL Policy Type',
                        key='data.ssl_profiles.ssl_policy.policy_type'),
        SearchField.set(name='Frontend IP Type',
                        key='data.frontend_ip_configurations.ip_type'),
        SearchField.set(name='Frontend IP Configuration Name',
                        key='data.frontend_ip_configurations.name'),
        SearchField.set(name='Frontend IP Address',
                        key='data.frontend_ip_configurations.ip_address'),
        SearchField.set(name='Frontend Associated Listeners',
                        key='data.frontend_ip_configurations.associated_listeners'),
        SearchField.set(name='HTTP Listener Name',
                        key='data.http_listeners.name'),
        SearchField.set(name='HTTP Listener Protocol',
                        key='data.http_listeners.protocol'),
        SearchField.set(name='HTTP Listener Port',
                        key='data.http_listeners.port'),
        SearchField.set(name='HTTP Listener Associated Rule',
                        key='data.http_listeners.associated_rules'),
        SearchField.set(name='HTTP Listener Host name',
                        key='data.http_listeners.host_name'),
        SearchField.set(name='Request Routing Rule Name',
                        key='data.request_routing_rules.name'),
        SearchField.set(name='Request Routing Rule Type',
                        key='data.request_routing_rules.rule_type'),
        SearchField.set(name='Request Routing Rule Listener',
                        key='data.request_routing_rules.http_listener_name'),
        SearchField.set(name='Health Probes Name',
                        key='data.probes.name'),
        SearchField.set(name='Health Probes Protocol',
                        key='data.probes.protocol'),
        SearchField.set(name='Health Probes Host',
                        key='data.probes.host'),
        SearchField.set(name='Health Probes Path',
                        key='data.probes.path'),
        SearchField.set(name='Health Probes Timeout(Seconds)',
                        key='data.probes.timeout',
                        data_type='integer'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(ag_count_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(ag_count_by_location_conf)),
        ChartWidget.set(**get_data_from_yaml(ag_count_by_account_conf)),
        CardWidget.set(**get_data_from_yaml(ag_total_count_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_application_gateways}),
]
