import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

ag_count_per_subscription_conf = os.path.join(current_dir, 'widget/application_gateway_count_per_subscription.yaml')
ag_count_per_location_conf = os.path.join(current_dir, 'widget/application_gateway_count_per_location.yaml')

cst_application_gateway = CloudServiceTypeResource()
cst_application_gateway.name = 'ApplicationGateway'
cst_application_gateway.group = 'Network'
cst_application_gateway.service_code = 'Microsoft.Network/applicationGateways'
cst_application_gateway.labels = ['Network']
cst_application_gateway.is_major = False
cst_application_gateway.is_primary = False
cst_application_gateway.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-application-gateways.svg',
}

cst_application_gateway._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Public IP Address', 'data.public_ip_address.ip_address'),
        TextDyField.data_source('Private IP Address', 'data.private_ip_address'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        # is_optional fields - Configuration
        TextDyField.data_source('Capacity ', 'data.sku.tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Minimum Instance Count', 'data.autoscale_configuration.min_capacity', options= {
            'is_optional': True
        }),
        TextDyField.data_source('Maximum Instance Count', 'data.autoscale_configuration.max_capacity', options= {
            'is_optional': True
        }),
        TextDyField.data_source('Enable HTTP2', 'data.enable_http2',  options={
            'is_optional': True
        }),
        # is_optional fields - Firewall
        TextDyField.data_source('Firewall Mode', 'data.web_application_firewall_configuration.firewall_mode', options={
            'is_optional': True
        }),
        TextDyField.data_source('Max Request Body Size(KB)', 'data.web_application_firewall_configuration.max_request_body_size_in_kb', options={
            'is_optional': True
        }),
        TextDyField.data_source('File Upload Limit(MB)', 'data.web_application_firewall_configuration.file_upload_limit_in_mb', options={
            'is_optional': True
        }),
        TextDyField.data_source('Rule Set Type', 'data.web_application_firewall_configuration.rule_set_type',  options={
            'is_optional': True
        }),
        TextDyField.data_source('Rule Set Version', 'data.web_application_firewall_configuration.rule_set_version', options={
            'is_optional': True
        }),
        # is_optional fields - Firewall
        TextDyField.data_source('Backend Pool Name', 'data.backend_address_pools.name', options={
            'is_optional': True
        }),
        ListDyField.data_source('Rule Associated', 'data.backend_address_pools.associated_rules', options={
            'is_optional': True
        }),
        # is_optional fields - HTTP Settings
        TextDyField.data_source('Name', 'data.backend_http_settings_collection.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Port', 'data.backend_http_settings_collection.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Protocol', 'data.backend_http_settings_collection.protocol', options={
            'is_optional': True
        }),
        # is_optional fields - SSL settings
        TextDyField.data_source('SSL Profile Name', 'data.ssl_profiles.name', options={
            'is_optional': True
        }),
        ListDyField.data_source('Client Certificates', 'data.ssl_profiles.trusted_client_certificates.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('SSL Policy Type', 'data.ssl_profiles.ssl_policy.policy_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Type', 'ip_type', options={
            'is_optional': True
        }),
        # is_optional fields - Frontend IP Configurations
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
        TextDyField.data_source('Listener Name', 'data.http_listeners.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Listener Protocol', 'data.http_listeners.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Listener Port', 'data.http_listeners.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Listener Associated Rule', 'data.http_listeners.associated_rules', options={
            'is_optional': True
        }),
        TextDyField.data_source('Listener Host name', 'data.http_listeners.host_name', options={
            'is_optional': True
        }),
        # is_optional fields - Rules
        TextDyField.data_source('Rule Name', 'data.request_routing_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Rule Type', 'data.request_routing_rules.rule_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Rule Listener', 'data.request_routing_rules.http_listener_name', options={
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
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='name', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Public IP Address', key='data.public_ip_address.ip_address', data_type='string'),
        SearchField.set(name='Private IP Address', key='data.private_ip_address', data_type='string')
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(ag_count_per_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(ag_count_per_location_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_application_gateway}),
]
