from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, DateTimeType
from spaceone.inventory.libs.schema.resource import AzureCloudService


# SkuResource
class SkuResource(Model):
    name = StringType(serialize_when_none=False)
    tier = StringType(serialize_when_none=False)
    size = StringType(serialize_when_none=False)
    family = StringType(serialize_when_none=False)
    capacity = IntType(serialize_when_none=False)


# ManagedIdentity

# ManagedIdentity - UserAssignedIdentityProperty
class UserAssignedIdentityProperty(Model):
    principal_id = StringType(serialize_when_none=False)
    client_id = StringType(serialize_when_none=False)


class ManagedIdentity(Model):
    type = StringType(serialize_when_none=False)
    user_assigned_identities = ModelType(UserAssignedIdentityProperty)
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)


# SystemData
class SystemData(Model):
    created_by = StringType(serialize_when_none=False)
    created_by_type = StringType(serialize_when_none=False)
    created_at = DateTimeType(serialize_when_none=False)
    last_modified_by = StringType(serialize_when_none=False)
    last_modified_by_type = StringType(serialize_when_none=False)
    last_modified_at = DateTimeType(serialize_when_none=False)


# PrivateEndpointConnection

# PrivateEndpointConnection - PrivateEndpoint
class PrivateEndpoint(Model):
    id = StringType(serialize_when_none=False)
    private_endpoint_name_display = StringType(serialize_when_none=False)


# PrivateEndpointConnection - PrivateLinkServiceConnectionState
class PrivateLinkServiceConnectionState(Model):
    status = StringType(choices=('Approved', 'Disconnected', 'Pending', 'Rejected'))
    description = StringType(serialize_when_none=False)
    actions_required = StringType(serialize_when_none=False)


class PrivateEndpointConnection(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    system_data = ModelType(SystemData, serialize_when_none=False)
    provisioning_state = StringType(choices=('Canceled', 'Creating', 'Deleting', 'Failed', 'Moving', 'Running',
                                             'Succeeded', 'Unknown', 'Updating'))
    private_endpoint = ModelType(PrivateEndpoint)
    group_ids = ListType(StringType, serialize_when_none=False)
    private_link_service_connection_state = ModelType(PrivateLinkServiceConnectionState)


# SharedPrivateLinkResource
class SharedPrivateLinkResource(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    system_data = ModelType(SystemData)
    group_id = StringType(serialize_when_none=False)
    private_link_resource_id = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Canceled', 'Creating', 'Deleting', 'Failed', 'Moving', 'Running',
                                             'Succeeded', 'Unknown', 'Updating'))
    request_message = StringType(serialize_when_none=False)
    status = StringType(choices=('Approved', 'Disconnected', 'Pending', 'Rejected'))


# WebPubSubTlsSettings
class WebPubSubTlsSettings(Model):
    client_cert_enabled = BooleanType(default=True)


# LiveTraceConfiguration

# LiveTraceConfiguration - LiveTraceCategory
class LiveTraceCategory(Model):
    name = StringType(serialize_when_none=False)
    enabled = StringType(serialize_when_none=False)


class LiveTraceConfiguration(Model):
    enabled = StringType(serialize_when_none=False)
    categories = ListType(ModelType(LiveTraceCategory), serialize_when_none=False)


# ResourceLogConfiguration

# ResourceLogConfiguration - ResourceLogCategory
class ResourceLogCategory(Model):
    name = StringType(serialize_when_none=False)
    enabled = StringType(serialize_when_none=False)


class ResourceLogConfiguration(Model):
    categories = ListType(ModelType(ResourceLogCategory), serialize_when_none=False)


# WebPubSubNetworkACLs

# WebPubSubNetworkACLs - NetworkACL
class NetworkACL(Model):
    allow = ListType(StringType, serialize_when_none=False)
    deny = ListType(StringType, serialize_when_none=False)


# WebPubSubNetworkACLs - PrivateEndpointACL
class PrivateEndpointACL(Model):
    allow = ListType(StringType, serialize_when_none=False)
    deny = ListType(StringType, serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class WebPubSubNetworkACLs(Model):
    default_action = StringType(serialize_when_none=False)
    public_network = ModelType(NetworkACL)
    private_endpoints = ListType(ModelType(PrivateEndpointACL), serialize_when_none=False)


# WebPubSubHub

# WebPubSubHub- WebPubSubNetworkACLs- UpstreamAuthSettings - ManagedIdentitySettings
class ManagedIdentitySettings(Model):
    resource = StringType(serialize_when_none=False)


# WebPubSubHub- WebPubSubNetworkACLs- UpstreamAuthSettings
class UpstreamAuthSettings(Model):
    type = StringType(serialize_when_none=False)
    managed_identity = ModelType(ManagedIdentitySettings)


# WebPubSubHub - WebPubSubHubProperties - EventHandler
class EventHandler(Model):
    url_template = StringType(serialize_when_none=False)
    user_event_pattern = StringType(serialize_when_none=False)
    system_events = ListType(StringType, serialize_when_none=False)
    auth = ModelType(UpstreamAuthSettings)


# WebPubSubHub - WebPubSubHubProperties
class WebPubSubHubProperties(Model):
    event_handlers = ListType(ModelType(EventHandler))
    anonymous_connect_policy = StringType(default='deny', choices=('allow', 'deny'))


class WebPubSubHub(AzureCloudService):
    id = StringType()
    name = StringType()
    location = StringType()
    type = StringType(serialize_when_none=False)
    system_data = ModelType(SystemData)
    properties = ModelType(WebPubSubHubProperties)
    web_pubsub_svc_name = StringType(serialize_when_none=False)
    web_pubsub_hub_evnet_handler_count_display = IntType(default=0)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }


# CustomDomain
class CustomDomain(Model):
    pass


# WebPubSubKeys
class WebPubSubKey(Model):
    primary_key = StringType(serialize_when_none=False)
    primary_connection_string = StringType(serialize_when_none=False)
    secondary_key = StringType(serialize_when_none=False)
    secondary_connection_string = StringType(serialize_when_none=False)


class WebPubSubService(AzureCloudService):  # Main Class
    id = StringType()
    name = StringType()
    location = StringType()
    sku = ModelType(SkuResource, serialize_when_none=False)
    identity = ModelType(ManagedIdentity, serialize_when_none=False)
    system_data = ModelType(SystemData, serialize_when_none=False)
    provisioning_state = StringType(choices=('Canceled', 'Creating', 'Deleting', 'Failed', 'Moving', 'Running',
                                             'Succeeded', 'Unknown', 'Updating'))
    external_ip = StringType(serialize_when_none=False)
    host_name = StringType(serialize_when_none=False)
    public_port = StringType(serialize_when_none=False)
    server_port = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    private_endpoint_connections = ListType(ModelType(PrivateEndpointConnection))
    shared_private_link_resources = ListType(ModelType(SharedPrivateLinkResource))
    tls = ModelType(WebPubSubTlsSettings)
    host_name_prefix = StringType(serialize_when_none=False)
    live_trace_configuration = ModelType(LiveTraceConfiguration)
    resource_log_configuration = ModelType(ResourceLogConfiguration)
    network_ac_ls = ModelType(WebPubSubNetworkACLs)
    public_network_access = StringType(default='Enabled')
    disable_local_auth = BooleanType(default=False)
    disable_aad_auth = BooleanType(default=False)
    web_pubsub_hubs = ListType(ModelType(WebPubSubHub))
    web_pubsub_hub_count_display = IntType(default=0)
    custom_domains = ListType(ModelType(CustomDomain))  # not yet supported
    web_pubsub_key = ModelType(WebPubSubKey)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
