import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, \
    ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

'''
Service
'''

web_pubsub_svc_count_by_region_conf = os.path.join(current_dir, 'widget/web_pubsub_svc_count_by_region.yaml')
web_pubsub_svc_count_by_subscription_conf = os.path.join(current_dir, 'widget/web_pubsub_svc_count_by_subscription.yaml')
web_pubsub_svc_total_count_conf = os.path.join(current_dir, 'widget/web_pubsub_svc_total_count.yaml')
web_pubsub_svc_total_unit_count_conf = os.path.join(current_dir, 'widget/web_pubsub_svc_unit_count_by_tier.yaml')
web_pubsub_svc_unit_count_by_tier_conf = os.path.join(current_dir, 'widget/web_pubsub_svc_total_unit_count.yaml')

cst_web_pubsub_svc = CloudServiceTypeResource()
cst_web_pubsub_svc.name = 'Service'
cst_web_pubsub_svc.group = 'WebPubSubService'
cst_web_pubsub_svc.service_code = 'Microsoft.SignalRService/WebPubSub'
cst_web_pubsub_svc.labels = ['Application Integration']
cst_web_pubsub_svc.is_major = True
cst_web_pubsub_svc.is_primary = True
cst_web_pubsub_svc.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-web-pubsub-service.svg',
}

cst_web_pubsub_svc._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Service State', 'data.provisioning_state', default_state={
            'safe': ['Running', 'Succeeded'],
            'warning': ['Creating', 'Updating', 'Deleting', 'Moving', 'Updating'],
            'alert': ['Failed', 'Canceled'],
            'disable': ['Unknown']}),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'account', options={
            'is_optional': True
        }),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Hub count', 'data.web_pubsub_hub_count_display'),
        TextDyField.data_source('SKU', 'data.sku.tier'),
        TextDyField.data_source('Unit', 'data.sku.unit'),
        TextDyField.data_source('Version', 'data.version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Host name', 'data.host_name'),
        TextDyField.data_source('Host name prefix', 'data.host_name_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Public IP', 'data.external_ip'),
        TextDyField.data_source('Public access', 'data.public_network_access'),
        TextDyField.data_source('Public port', 'data.public_port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Server port', 'data.server_port', options={
            'is_optional': True
        }),
        TextDyField.data_source('TLS', 'data.tls.client_cert_enabled', options={
            'is_optional': True
        }),

    ],
    search=[
        SearchField.set('Service State', key='data.provisioning_state'),
        SearchField.set('Subscription Name', key='data.subscription_name'),
        SearchField.set('Subscription ID', key='account'),
        SearchField.set('Resource Group', key='data.resource_group'),
        SearchField.set('Location', key='data.location'),
        SearchField.set('Hub count', key='data.web_pubsub_hub_count_display', data_type='integer'),
        SearchField.set('SKU', key='data.sku.tier'),
        SearchField.set('Unit', key='data.sku.unit', data_type='integer'),
        SearchField.set('Version', key='data.version', data_type='float'),
        SearchField.set('Host name', key='data.host_name'),
        SearchField.set('Host name prefix', key='data.host_name_prefix'),
        SearchField.set('Public IP', key='data.external_ip'),
        SearchField.set('Public access', key='data.public_network_access'),
        SearchField.set('Public port', key='data.public_port'),
        SearchField.set('Server port', key='data.server_port'),
        SearchField.set('TLS', key='data.tls.client_cert_enabled'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(web_pubsub_svc_count_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(web_pubsub_svc_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(web_pubsub_svc_unit_count_by_tier_conf)),
        CardWidget.set(**get_data_from_yaml(web_pubsub_svc_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(web_pubsub_svc_total_unit_count_conf)),
    ]
)

'''
Hub
'''
web_pubsub_hub_count_by_region_conf = os.path.join(current_dir, 'widget/web_pubsub_hub_count_by_region.yaml')
web_pubsub_hub_count_by_resource_group_conf = os.path.join(current_dir, 'widget/web_pubsub_hub_count_by_resource_group.yaml')
web_pubsub_hub_count_by_subscription_conf = os.path.join(current_dir, 'widget/web_pubsub_hub_count_by_subscription.yaml')
web_pubsub_hub_event_handler_total_count_conf = os.path.join(current_dir, 'widget/web_pubsub_hub_event_handler_total_count.yaml')
web_pubsub_hub_total_count_conf = os.path.join(current_dir, 'widget/web_pubsub_hub_total_count.yaml')

cst_web_pubsub_hub = CloudServiceTypeResource()
cst_web_pubsub_hub.name = 'Hub'
cst_web_pubsub_hub.group = 'WebPubSubService'
cst_web_pubsub_hub.service_code = 'Microsoft.SignalRService/WebPubSub/hubs'
cst_web_pubsub_hub.labels = ['Application Integration']
cst_web_pubsub_hub.is_major = True
cst_web_pubsub_hub.is_primary = True
cst_web_pubsub_hub.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-web-pubsub-service.svg',
}

cst_web_pubsub_hub._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Anonymous Connect', 'data.properties.anonymous_connect_policy', default_badge={
            'indigo.500': ['allow'], 'coral.600': ['deny']}),
        TextDyField.data_source('Event Handlers count', 'data.web_pubsub_hub_evnet_handler_count_display'),
        TextDyField.data_source('Web SubSub Service', 'data.web_pubsub_svc_name'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
    ],
    search=[
        SearchField.set('Anonymous Connect', key='data.properties.anonymous_connect_policy'),
        SearchField.set('Event Handlers count', key='data.web_pubsub_hub_evnet_handler_count_display', data_type='integer'),
        SearchField.set('Web SubSub Service', 'data.web_pubsub_svc_name'),
        SearchField.set('Subscription Name', key='data.subscription_name'),
        SearchField.set('Subscription ID', key='account'),
        SearchField.set('Resource Group', key='data.resource_group'),
        SearchField.set('Location', key='data.location'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(web_pubsub_hub_count_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(web_pubsub_hub_count_by_resource_group_conf)),
        ChartWidget.set(**get_data_from_yaml(web_pubsub_hub_count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(web_pubsub_hub_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(web_pubsub_hub_event_handler_total_count_conf))
    ]

)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_web_pubsub_svc}),
    CloudServiceTypeResponse({'resource': cst_web_pubsub_hub}),
]
