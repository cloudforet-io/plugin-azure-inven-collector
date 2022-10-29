from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType
from spaceone.inventory.model.web_pubsub_service.data import WebPubSubService, WebPubSubHub
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Web PubSub Service
'''

# TAB - Web PubSub Service
web_pubsub_svc_info_meta = ItemDynamicLayout.set_fields('Web PubSub Service', fields=[
    TextDyField.data_source('Name', 'name'),
    EnumDyField.data_source('Service State', 'data.provisioning_state', default_state={
        'safe': ['Running', 'Succeeded'],
        'warning': ['Creating', 'Updating', 'Deleting', 'Moving', 'Updating'],
        'alert': ['Failed', 'Canceled'],
        'disable': ['Unknown']}),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
    TextDyField.data_source('Region', 'data.location'),
    TextDyField.data_source('Hub count', 'data.web_pubsub_hub_count_display'),
    TextDyField.data_source('SKU', 'data.sku.tier'),
    TextDyField.data_source('Unit', 'data.sku.unit'),
    TextDyField.data_source('Version', 'data.version'),
    TextDyField.data_source('Host name', 'data.host_name'),
    TextDyField.data_source('Host name prefix', 'data.host_name_prefix'),
    TextDyField.data_source('Public IP', 'data.external_ip'),
    TextDyField.data_source('Public access', 'data.public_network_access'),
    TextDyField.data_source('Public port', 'data.public_port'),
    TextDyField.data_source('Server port', 'data.server_port'),
    TextDyField.data_source('Disable add auth', 'data.disable_aad_auth'),
    TextDyField.data_source('Disable local auth', 'data.disable_local_auth'),
    TextDyField.data_source('TLS', 'data.tls.client_cert_enabled'),
])

# TAB - Keys
web_pubsub_svc_keys_info = ItemDynamicLayout.set_fields('Keys', fields=[
    TextDyField.data_source('Host name', 'data.host_name'),
    TextDyField.data_source('Access Key', 'data.disable_local_auth'),
    TextDyField.data_source('Primary Key', 'data.web_pubsub_key.primary_key'),
    TextDyField.data_source('Primary Connection string', 'data.web_pubsub_key.primary_connection_string'),
    TextDyField.data_source('Secondary Key', 'data.web_pubsub_key.secondary_key'),
    TextDyField.data_source('Secondary Connection string', 'data.web_pubsub_key.secondary_connection_string'),
])

# TAB - Hub
web_pubsub_svc_hubs_info = TableDynamicLayout.set_fields('Hubs', root_path='data.web_pubsub_hubs', fields=[
    TextDyField.data_source('Hub name', 'name'),
    EnumDyField.data_source('Anonymous Connect', 'properties.anonymous_connect_policy', default_badge={
        'indigo.500': ['allow'], 'coral.600': ['deny']
    }),
    ListDyField.data_source('Event Handlers', 'properties.event_handlers.url_template', options={'delimiter': '<br>'})
])

# TAB - Public access
web_pubsub_svc_public_access_info = ItemDynamicLayout.set_fields('Public access', fields=[
    EnumDyField.data_source('Public network access', 'data.public_network_access', default_badge={
        'indigo.500': ['Enabled'], 'coral.600': ['Disabled']
    })
])

# TAB - Private access
private_endpoint_connections_private_access = TableDynamicLayout.set_fields('Private endpoint connections', root_path='data.private_endpoint_connections', fields=[
    TextDyField.data_source('Connection name', 'name'),
    EnumDyField.data_source('Connection state', 'private_link_service_connection_state.status', default_state={
        'safe': ['Approved'],
        'warning': ['Pending'],
        'alert': ['Disconnected', 'Rejected'],
        'disable': []}),
    TextDyField.data_source('Private Endpoint', 'private_endpoint.private_endpoint_name_display'),
    TextDyField.data_source('Description', 'private_link_service_connection_state.status'),
    ListDyField.data_source('Group ids', 'group_ids', options={'delimiter': '<br>'}),
    TextDyField.data_source('Provisioning state', 'provisioning_state')
])
shared_private_endpoints_private_access = TableDynamicLayout.set_fields('Shared private endpoints', root_path='data.shared_private_link_resources', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Private link resource ID', 'private_link_resource_id'),
    TextDyField.data_source('Group ID', 'group_id'),
    EnumDyField.data_source('Connection state', 'status', efault_state={
        'safe': ['Approved'],
        'warning': ['Pending'],
        'alert': ['Disconnected', 'Rejected'],
        'disable': []}),
    TextDyField.data_source('Description', 'request_message'),
    TextDyField.data_source('Provisioning state', 'provisioning_state')
])

web_pubsub_svc_private_access_info = ListDynamicLayout.set_layouts('Private access', layouts=[
   private_endpoint_connections_private_access, shared_private_endpoints_private_access])

# TAB - Access control rules
default_action_access_control_rules = ItemDynamicLayout.set_fields('Default action', fields=[
    EnumDyField.data_source('Default action', 'data.network_ac_ls.default_action', default_badge={
        'indigo.500': ['Allow'], 'coral.600': ['Deny']})
])

public_network_access_control_rules = ItemDynamicLayout.set_fields('Public network', fields=[
    ListDyField.data_source('Allow', 'data.public_network.allow', options={'delimiter': ','})
])

private_endpoint_connections_access_control_rules = TableDynamicLayout.set_fields('Private endpoint connections',
                                                                                  root_path='data.network_ac_ls.private_endpoints' ,fields=[
        TextDyField.data_source('Connection name', 'name'),
        ListDyField.data_source('Allow', 'allow',  options={'delimiter': ','})
    ])

web_pubsub_svc_access_control_rules_info = ListDynamicLayout.set_layouts(' Access control rules', layouts=[
    default_action_access_control_rules, default_action_access_control_rules,
    private_endpoint_connections_access_control_rules
])

# TAB - System data
web_pub_sub_svc_system_data_info = ItemDynamicLayout.set_fields('System data', root_path='data.system_data', fields=[
    DateTimeDyField.data_source('Created at', 'created_at'),
    TextDyField.data_source('Created by', 'created_by'),
    TextDyField.data_source('Created by type', 'created_by_type'),
    DateTimeDyField.data_source('Last modified at', 'last_modified_at'),
    TextDyField.data_source('Last modified by', 'last_modified_by'),
    TextDyField.data_source('Last modified by type', 'last_modified_by_type'),
    DateTimeDyField.data_source('Created at', 'system_data.created_at')
])

# TAB - Custom domain is not yet supported

web_pubsub_service_meta = CloudServiceMeta.set_layouts(
    [web_pubsub_svc_info_meta, web_pubsub_svc_keys_info, web_pubsub_svc_hubs_info, web_pubsub_svc_public_access_info,
     web_pubsub_svc_private_access_info, web_pubsub_svc_access_control_rules_info, web_pub_sub_svc_system_data_info])


class ApplicationIntegrationResource(CloudServiceResource):
    cloud_service_group = StringType(default='WebPubSubService')


class WebPubSubServiceResource(ApplicationIntegrationResource):
    cloud_service_type = StringType(default='Service')
    data = ModelType(WebPubSubService)
    _metadata = ModelType(CloudServiceMeta, default=web_pubsub_service_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class WebPubSubServiceResponse(CloudServiceResponse):
    resource = PolyModelType(WebPubSubServiceResource)


'''
Web PubSub Hub
'''

# TAB - Web PubSub Hub
web_pubsub_hub_info_meta = ItemDynamicLayout.set_fields('Web PubSub Hub', fields=[
    TextDyField.data_source('Hub name', 'name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
    TextDyField.data_source('Region', 'data.location'),
    EnumDyField.data_source('Anonymous Connect', 'data.properties.anonymous_connect_policy', default_badge={
        'indigo.500': ['allow'], 'coral.600': ['deny']
    }),
    TextDyField.data_source('EventHandler count', 'web_pubsub_hub_evnet_handler_count_display')
])

# TAB - Event Handlers
web_pubsub_hub_event_handlers_info = TableDynamicLayout.set_fields('Event Handlers', root_path='data.properties', fields=[
    TextDyField.data_source('Url template', 'url_template'),
    TextDyField.data_source('User events', 'user_event_pattern'),
    ListDyField.data_source('System events', 'system_events', options={'delimiter': ','}),
    TextDyField.data_source('Authentication', 'auth.type')
])

# TAB - System data
web_pubsub_hub_system_data_info = ItemDynamicLayout.set_fields('System data', root_path='data.system_data', fields=[
    DateTimeDyField.data_source('Created at', 'created_at'),
    TextDyField.data_source('Created by', 'created_by'),
    TextDyField.data_source('Created by type', 'created_by_type'),
    DateTimeDyField.data_source('Last modified at', 'last_modified_at'),
    TextDyField.data_source('Last modified by', 'last_modified_by'),
    TextDyField.data_source('Last modified by type', 'last_modified_by_type'),
    DateTimeDyField.data_source('Created at', 'system_data.created_at')
])

web_pubsub_hub_meta = CloudServiceMeta.set_layouts(
    [web_pubsub_hub_info_meta, web_pubsub_hub_event_handlers_info, web_pubsub_hub_event_handlers_info,
     web_pubsub_hub_system_data_info])


class WebPubSubHubResource(ApplicationIntegrationResource):
    cloud_service_type = StringType(default='Hub')
    data = ModelType(WebPubSubHub)
    _metadata = ModelType(CloudServiceMeta, default=web_pubsub_hub_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class WebPubSubHubResponse(CloudServiceResponse):
    resource = PolyModelType(WebPubSubHubResource)
