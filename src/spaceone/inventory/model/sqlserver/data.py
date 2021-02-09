from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType

class Tags(Model):
    key = StringType()
    value = StringType()


class ResourceIdentity(Model):
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    type = StringType(choices=('None', 'SystemAssigned', 'UserAssigned'))


class PrivateEndpointProperty(Model):
    id = StringType()


class PrivateLinkServiceConnectionStateProperty(Model):
    actions_required = StringType(choices=('None', ''), serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(choices=('Approved', 'Disconnected', 'Pending', 'Rejected'), serialize_when_none=False)


class PrivateEndpointConnectionProperties(Model):
    private_endpoint = ModelType(PrivateEndpointProperty, serialize_when_none=False)
    private_link_service_connection_state = ModelType(PrivateLinkServiceConnectionStateProperty, serialize_when_none=False)
    provisioning_state = StringType(choices=('Approving', 'Dropping', 'Failed', 'Ready', 'Rejecting'))


class ServerPrivateEndpointConnection(Model):
    id = StringType(serialize_when_none=False)
    properties = ModelType(PrivateEndpointConnectionProperties)


class ServerAzureADAdministrator(Model):
    id = StringType()
    name = StringType(serialize_when_none=False)
    administrator_type = StringType(choices=('ActiveDirectory', ''), serialize_when_none=False)
    login = StringType(serialize_when_none=False)
    sid = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)


class AutomaticTuningServerOptions(Model):
    actual_state = StringType(choices=('Off', 'On'), serialize_when_none=False)
    desired_state = StringType(choices=('Default', 'Off', 'On'), serialize_when_none=False)
    reason_code = IntType(serialize_when_none=False)
    reason_desc = StringType(choices=('AutoConfigured', 'Default', 'Disabled'), serialize_when_none=False)


class ServerAutomaticTuning(Model):
    name = StringType()
    id = StringType()
    actual_state = StringType(choices=('Auto', 'Custom', 'Unspecified'), serialize_when_none=False)
    desired_state = StringType(choices=('Default', 'Off', 'On'), serialize_when_none=False)
    options = ModelType(AutomaticTuningServerOptions, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ServerBlobAuditingPolicy(Model):
    name = StringType()
    id = StringType()
    audit_actions_and_groups = ListType(StringType, serialize_when_none=False)
    is_azure_monitor_target_enabled = BooleanType(serialize_when_none=False)
    is_storage_secondary_key_in_use = BooleanType(serialize_when_none=False)
    queue_delay_ms = IntType(serialize_when_none=False)
    retention_days = IntType(serialize_when_none=False)
    state = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    storage_account_access_key = StringType(serialize_when_none=False)
    storage_account_subscription_id = StringType(serialize_when_none=False)
    storage_endpoint = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PartnerInfo(Model):
    id = StringType()
    location = StringType()
    replication_role = StringType(choices=('Primary', 'Secondary'), serialize_when_none=False)


class FailoverGroupReadOnlyEndpoint(Model):
    failover_policy = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)


class FailoverGroupReadWriteEndpoint(Model):
    failover_policy = StringType(choices=('Automatic', 'Manual'), serialize_when_none=False)
    failover_with_data_loss_grace_period_minutes = IntType(serialize_when_none=False)


class FailoverGroup(Model):
    name = StringType(serialize_when_none=False)
    id = StringType()
    location = StringType()
    databases = ListType(StringType, serialize_when_none=False)
    partner_servers = ListType(ModelType(PartnerInfo), serialize_when_none=False)
    read_only_endpoint = ModelType(FailoverGroupReadOnlyEndpoint, serialize_when_none=False)
    read_write_endpoint = ModelType(FailoverGroupReadWriteEndpoint, serialize_when_none=False)
    replication_role = StringType(choices=('Primary', 'Secondary'), serialize_when_none=False)
    replication_state = StringType(serialize_when_none=False)
    tags = ListType(ModelType(Tags))
    type = StringType(serialize_when_none=False)


class SqlServer(Model):
    name = StringType()
    id = StringType()
    identity = ModelType(ResourceIdentity, serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    location = StringType()
    type = StringType()
    subscription_id = StringType()
    subscription_name = StringType()
    resource_group = StringType()
    administrator_login = StringType(serialize_when_none=False)
    administrator_login_password = StringType(serialize_when_none=False)
    fully_qualified_domain_name = StringType(serialize_when_none=False)
    minimal_tls_version = StringType(choices=('1.0', '1.1', '1.2'), serialize_when_none=False)
    private_endpoint_connections = ListType(ModelType(ServerPrivateEndpointConnection))
    public_network_access = StringType(choices=('Disabled', 'Enabled'))
    state = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    azure_ad_administrator = ModelType(ServerAzureADAdministrator, serialize_when_none=False)
    server_automatic_tuning = ModelType(ServerAutomaticTuning, serialize_when_none=False)
    server_automatic_tuning_display = BooleanType(serialize_when_none=False)
    server_auditing_settings = ModelType(ServerBlobAuditingPolicy, serialize_when_none=False)
    failover_groups = ModelType(FailoverGroup, serialize_when_none=False)
    tags = ListType(ModelType(Tags))

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }