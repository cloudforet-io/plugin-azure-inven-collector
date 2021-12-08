from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, NumberType, DateTimeType, \
    TimestampType, UTCDateTimeType, TimedeltaType, FloatType


class Tags(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class SubResource(Model):
    id = StringType()


class ApiProperties(Model):
    server_version = StringType(serialize_when_none=False)


class ManagedServiceIdentity(Model):
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    type = StringType(choices=('None', 'SystemAssigned', 'SystemAssigned, UserAssigned', 'UserAssigned'), serialize_when_none=False)
    user_assigned_identities = StringType(serialize_when_none=False)


class PeriodicModeProperties(Model):
    backup_interval_in_minutes = IntType(serialize_when_none=False)
    backup_retention_interval_in_hours = IntType(serialize_when_none=False)
    backup_storage_redundancy = StringType(choices=('Geo', 'Local', 'Zone'), serialize_when_none=False)


class PeriodicModeBackupPolicy(Model):
    periodic_mode_properties = ModelType(PeriodicModeProperties, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Capability(Model):
    name = StringType(serialize_when_none=False)


class ConsistencyPolicy(Model):
    default_consistency_level = StringType(choices=('BoundedStaleness', 'ConsistentPrefix', 'Eventual', 'Session', 'Strong'), serialize_when_none=False)
    max_interval_in_seconds = IntType(serialize_when_none=False)
    max_staleness_prefix = IntType(serialize_when_none=False)


class CorsPolicy(Model):
    allowed_headers = StringType(serialize_when_none=False)
    allowed_methods = StringType(serialize_when_none=False)
    allowed_origins = StringType(serialize_when_none=False)
    exposed_headers = StringType(serialize_when_none=False)
    max_age_in_seconds = IntType(serialize_when_none=False)


class FailoverPolicy(Model):
    failover_priority = IntType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location_name = StringType(serialize_when_none=False)


class IpAddressOrRange(Model):
    ip_address_or_range = StringType(serialize_when_none=False)


class Location(Model):
    document_endpoint = StringType(serialize_when_none=False)
    failover_priority = IntType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    is_zone_redundant = BooleanType(serialize_when_none=False)
    location_name = StringType(serialize_when_none=False)
    provisioning_state = StringType(serialize_when_none=False)


class PrivateEndpointProperty(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class PrivateLinkServiceConnectionStateProperty(Model):
    actions_required = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)


class PrivateEndpointConnection(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    group_id = StringType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpointProperty, serialize_when_none=False)
    private_link_service_connection_state = ModelType(PrivateLinkServiceConnectionStateProperty, serialize_when_none=False)
    provisioning_state = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class DatabaseRestoreResource(Model):
    collection_names = ListType(StringType, serialize_when_none=False)
    database_name = StringType(serialize_when_none=False)


class RestoreMode(Model):
    point_in_time = StringType(serialize_when_none=False)


class RestoreParameters(Model):
    databases_to_restore = ListType(ModelType(DatabaseRestoreResource), serialize_when_none=False)
    restore_mode = ModelType(RestoreMode, serialize_when_none=False)
    restore_source = StringType(serialize_when_none=False)
    restore_timestamp_in_utc = UTCDateTimeType(serialize_when_none=False)


class VirtualNetworkRule(Model):
    id = StringType(serialize_when_none=False)
    ignore_missing_v_net_service_endpoint = BooleanType(serialize_when_none=False)


class SystemData(Model):
    created_at = DateTimeType(serialize_when_none=False)
    created_by = StringType(serialize_when_none=False)
    created_by_type = StringType(choices=('Application', 'Key', 'ManagedIdentity', 'User'), serialize_when_none=False)
    last_modified_at = DateTimeType(serialize_when_none=False)
    last_modified_by = StringType(serialize_when_none=False)
    last_modified_by_type = StringType(choices=('Application', 'Key', 'ManagedIdentity', 'User'), serialize_when_none=False)


class DatabaseAccountListKeysResult(Model):
    primary_master_key = StringType(serialize_when_none=False)
    primary_readonly_master_key = StringType(serialize_when_none=False)
    secondary_master_key = StringType(serialize_when_none=False)
    secondary_readonly_master_key = StringType(serialize_when_none=False)


class SqlDatabaseGetResults(Model):
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    tags = ModelType(Tags)
    type = StringType(serialize_when_none=False)


class DatabaseAccountGetResults(Model):  # Main Class
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    identity = ModelType(ManagedServiceIdentity, serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    kind = StringType(choices=('GlobalDocumentDB', 'MongoDB', 'Parse'), serialize_when_none=False)
    name = StringType(default='-', serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
    subscription_id = StringType(serialize_when_none=False)
    subscription_name = StringType(serialize_when_none=False)
    api_properties = ModelType(ApiProperties, serialize_when_none=False)
    backup_policy = ModelType(PeriodicModeBackupPolicy, serialize_when_none=False)
    capabilities = ListType(ModelType(Capability), serialize_when_none=False)
    capability_display = StringType(serialize_when_none=False)
    connector_offer = StringType(serialize_when_none=False)
    consistency_policy = ModelType(ConsistencyPolicy, serialize_when_none=False)
    cors = ListType(ModelType(CorsPolicy), serialize_when_none=False)
    cors_display = ListType(StringType, serialize_when_none=False)
    create_mode = StringType(choices=('Default', 'Restore'), serialize_when_none=False)
    database_account_offer_type = StringType(serialize_when_none=False)
    default_identity = StringType(serialize_when_none=False)
    disable_key_based_metadata_write_access = BooleanType(serialize_when_none=False)
    document_endpoint = StringType(serialize_when_none=False)
    enable_analytical_storage = BooleanType(serialize_when_none=False)
    enable_automatic_failover = BooleanType(serialize_when_none=False)
    enable_cassandra_connector = BooleanType(serialize_when_none=False)
    enable_free_tier = BooleanType(serialize_when_none=False)
    enable_multiple_write_locations = BooleanType(serialize_when_none=False)
    failover_policies = ListType(ModelType(FailoverPolicy), serialize_when_none=False)
    instance_id = StringType(serialize_when_none=False)
    ip_rules = ListType(ModelType(IpAddressOrRange), serialize_when_none=False)
    is_virtual_network_filter_enabled = BooleanType(serialize_when_none=False)
    key_vault_key_uri = BooleanType(serialize_when_none=False)
    keys = ModelType(DatabaseAccountListKeysResult, serialize_when_none=False)
    locations = ListType(ModelType(Location), serialize_when_none=False)
    network_acl_bypass = StringType(choices=('AzureServices', 'None'), serialize_when_none=False)
    network_acl_bypass_resource_ids = ListType(StringType, serialize_when_none=False)
    private_endpoint_connections = ListType(ModelType(PrivateEndpointConnection), serialize_when_none=False)
    provisioning_state = StringType(serialize_when_none=False)
    public_network_access = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    read_locations = ListType(ModelType(Location), serialize_when_none=False)
    restore_parameters = ModelType(RestoreParameters, serialize_when_none=False)
    virtual_network_rules = ListType(ModelType(VirtualNetworkRule), serialize_when_none=False)
    virtual_network_display = ListType(StringType, serialize_when_none=False)
    sql_databases = ListType(ModelType(SqlDatabaseGetResults), serialize_when_none=False)
    write_locations = ListType(ModelType(Location), serialize_when_none=False)
    system_data = ModelType(SystemData, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    account = StringType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
