from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, FloatType, DateTimeType
from spaceone.inventory.libs.schema.resource import AzureCloudService, AzureTags


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
    private_link_service_connection_state = ModelType(PrivateLinkServiceConnectionStateProperty,
                                                      serialize_when_none=False)
    provisioning_state = StringType(choices=('Approving', 'Dropping', 'Failed', 'Ready', 'Rejecting'))


class ServerPrivateEndpointConnection(Model):
    id = StringType(serialize_when_none=False)
    connection_id = StringType(serialize_when_none=False)
    private_endpoint_name = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
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
    tuning_type = StringType(choices=('createIndex', 'dropIndex', 'forceLastGoodPlan'), serialize_when_none=False)


class ServerAutomaticTuning(Model):
    name = StringType()
    id = StringType()
    actual_state = StringType(choices=('Auto', 'Custom', 'Unspecified'), serialize_when_none=False)
    desired_state = StringType(choices=('Default', 'Off', 'On'), serialize_when_none=False)
    options = ListType(ModelType(AutomaticTuningServerOptions, serialize_when_none=False))
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
    storage_endpoint = StringType(default='-')
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
    primary_server = StringType(serialize_when_none=False)
    secondary_server = StringType(serialize_when_none=False)
    read_only_endpoint = ModelType(FailoverGroupReadOnlyEndpoint, serialize_when_none=False)
    read_write_endpoint = ModelType(FailoverGroupReadWriteEndpoint, serialize_when_none=False)
    replication_role = StringType(choices=('Primary', 'Secondary'), serialize_when_none=False)
    replication_state = StringType(serialize_when_none=False)
    failover_policy_display = StringType(serialize_when_none=False)
    grace_period_display = StringType(serialize_when_none=False)
    tags = ListType(ModelType(AzureTags))
    type = StringType(serialize_when_none=False)


class SyncGroupSchemaColumn(Model):
    data_size = StringType(serialize_when_none=False)
    data_type = StringType(serialize_when_none=False)
    quoted_name = StringType(serialize_when_none=False)


class SyncGroupSchemaTable(Model):
    columns = ListType(ModelType(SyncGroupSchemaColumn), serialize_when_none=False)
    quoted_name = StringType(serialize_when_none=False)


class SyncGroupSchema(Model):
    master_sync_member_name = StringType(serialize_when_none=False)
    tables = ListType(ModelType(SyncGroupSchemaTable), serialize_when_none=False)


class SyncGroup(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    conflict_resolution_policy = StringType(choices=('HubWin', 'MemberWin'), serialize_when_none=False)
    hub_database_password = StringType(serialize_when_none=False)
    hub_database_user_name = StringType(serialize_when_none=False)
    interval = IntType(serialize_when_none=False)
    last_sync_time = DateTimeType(serialize_when_none=False)
    schema = ModelType(SyncGroupSchema, serialize_when_none=False)
    sync_database_id = StringType(serialize_when_none=False)
    sync_state = StringType(choices=('Error', 'Good', 'NotReady', 'Progressing', 'Warning'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class SyncAgent(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    expiry_time = DateTimeType(serialize_when_none=False)
    is_up_to_date = BooleanType(serialize_when_none=False)
    last_alive_time = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    state = StringType(choices=('NeverConnected', 'Offline', 'Online'), serialize_when_none=False)
    sync_database_id = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class RetentionPolicy(Model):
    days = IntType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)


class LogSettings(Model):
    category = StringType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)
    retention_policy = ModelType(RetentionPolicy)


class MetricSettings(Model):
    category = StringType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)
    retention_policy = ModelType(RetentionPolicy)
    time_grain = StringType(serialize_when_none=False)


class DiagnosticSettingsResource(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    event_hub_authorization_rule_id = StringType(serialize_when_none=False)
    event_hub_name = StringType(serialize_when_none=False)
    log_analytics_destination_type = StringType(serialize_when_none=False)
    logs = ListType(ModelType(LogSettings), serialize_when_none=False)
    metrics = ListType(ModelType(MetricSettings), serialize_when_none=False)
    service_bus_rule_id = StringType(serialize_when_none=False)
    storage_account_id = StringType(serialize_when_none=False)
    workspace_id = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ReplicationLink(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    is_termination_allowed = BooleanType(serialize_when_none=False)
    partner_database = StringType(serialize_when_none=False)
    partner_location = StringType(serialize_when_none=False)
    partner_role = StringType(choices=('Copy', 'NonReadableSecondary', 'Primary', 'Secondary', 'Source'),
                              serialize_when_none=False)
    partner_server = StringType(default='-')
    percent_complete = IntType(serialize_when_none=False)
    replication_mode = StringType(serialize_when_none=False)
    replication_state = StringType(choices=('CATCH_UP', 'PENDING', 'SEEDING', 'SUSPENDED'), serialize_when_none=False)
    role = StringType(choices=('Copy', 'NonReadableSecondary', 'Primary', 'Secondary', 'Source'),
                      serialize_when_none=False)
    start_time = DateTimeType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Sku(Model):
    capacity = IntType(serialize_when_none=False)
    family = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    size = StringType(serialize_when_none=False)
    tier = StringType(serialize_when_none=False)


class Database(Model):
    name = StringType(serialize_when_none=False)
    id = StringType()
    kind = StringType(serialize_when_none=False)
    location = StringType()
    managed_by = StringType(serialize_when_none=False)
    server_name = StringType(serialize_when_none=False)
    subscription_id = StringType(serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)

    administrator_login = StringType(default='-')
    auto_pause_delay = IntType(serialize_when_none=False)
    catalog_collation = StringType(choices=('DATABASE_DEFAULT', 'SQL_Latin1_General_CP1_CI_AS'),
                                   serialize_when_none=False)
    collation = StringType(serialize_when_none=False)
    create_mode = StringType(choices=(
        'Copy', 'Default', 'OnlineSecondary', 'PointInTimeRestore', 'Recovery', 'Restore', 'RestoreExternalBackup',
        'RestoreExternalBackupSecondary', 'RestoreLongTermRetentionBackup', 'Secondary'), serialize_when_none=False)
    creation_date = DateTimeType(serialize_when_none=False)
    current_service_objective_name = StringType(serialize_when_none=False)
    current_sku = ModelType(Sku, serialize_when_none=False)
    database_id = StringType(serialize_when_none=False)
    default_secondary_location = StringType(serialize_when_none=False)
    earliest_restore_date = DateTimeType(serialize_when_none=False)
    elastic_pool_id = StringType(serialize_when_none=False)
    failover_group_id = StringType(serialize_when_none=False)
    high_availability_replica_count = IntType(serialize_when_none=False)
    license_type = StringType(choices=('BasePrice', 'LicenseIncluded'), serialize_when_none=False)
    long_term_retention_backup_resource_id = StringType(default='-')
    maintenance_configuration_id = StringType(serialize_when_none=False)
    max_log_size_bytes = IntType(serialize_when_none=False)
    max_size_bytes = IntType(serialize_when_none=False)
    max_size_gb = FloatType(serialize_when_none=False)
    min_capacity = FloatType(serialize_when_none=False)
    paused_date = DateTimeType(serialize_when_none=False)
    read_scale = StringType(choices=('Disabled', 'Enabled'), default='Disabled')
    recoverable_database_id = StringType(serialize_when_none=False)
    recovery_services_recovery_point_id = StringType(serialize_when_none=False)
    requested_service_objective_name = StringType(serialize_when_none=False)
    restorable_dropped_database_id = StringType(serialize_when_none=False)
    restore_point_in_time = StringType(serialize_when_none=False)
    resumed_date = DateTimeType(serialize_when_none=False)
    sample_name = StringType(choices=('AdventureWorksLT', 'WideWorldImportersFull', 'WideWorldImportersStd'),
                             serialize_when_none=False)
    secondary_type = StringType(choices=('Geo', 'Named'), serialize_when_none=False)
    source_database_deletion_date = StringType(serialize_when_none=False)
    source_database_id = StringType(serialize_when_none=False)
    status = StringType(choices=(
        'AutoClosed', 'Copying', 'Creating', 'Disabled', 'EmergencyMode', 'Inaccessible', 'Offline',
        'OfflineChangingDwPerformanceTiers', 'OfflineSecondary', 'Online',
        'OnlineChangingDwPerformanceTiers', 'Paused', 'Pausing', 'Recovering', 'RecoveryPending', 'Restoring',
        'Resuming', 'Scaling', 'Shutdown', 'Standby', 'Suspect'), serialize_when_none=False)
    storage_account_type = StringType(choices=('GRS', 'LRS', 'ZRS'), serialize_when_none=False)
    zone_redundant = BooleanType(serialize_when_none=False)
    diagnostic_settings_resource = ListType(ModelType(DiagnosticSettingsResource), serialize_when_none=False)
    replication_link = ListType(ModelType(ReplicationLink), serialize_when_none=False)
    sync_group = ListType(ModelType(SyncGroup), serialize_when_none=False)
    sync_agent = ListType(ModelType(SyncAgent), serialize_when_none=False)
    sync_group_display = ListType(StringType, serialize_when_none=False)
    sync_agent_display = ListType(StringType, serialize_when_none=False)
    sku = ModelType(Sku, serialize_when_none=False)
    pricing_tier_display = StringType(default='-')
    service_tier_display = StringType(default='-')
    compute_tier = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ElasticPoolPerDatabaseSettings(Model):
    max_capacity = FloatType(serialize_when_none=False)
    min_capacity = FloatType(serialize_when_none=False)


class ElasticPool(Model):
    name = StringType(serialize_when_none=False)
    id = StringType()
    kind = StringType(serialize_when_none=False)
    location = StringType()
    creation_date = DateTimeType(serialize_when_none=False)
    license_type = StringType(choices=('BasePrice', 'LicenseIncluded'), default='BasePrice')
    maintenance_configuration_id = StringType(serialize_when_none=False)
    max_size_bytes = IntType(serialize_when_none=False)
    max_size_gb = FloatType(serialize_when_none=False, default=0)
    per_database_settings = ModelType(ElasticPoolPerDatabaseSettings, serialize_when_none=False)
    state = StringType(choices=('Creating', 'Disabled', 'Ready'), serialize_when_none=False)
    zone_redundant = BooleanType(serialize_when_none=False)
    sku = ModelType(Sku)
    per_db_settings_display = StringType(serialize_when_none=False)
    pricing_tier_display = StringType(serialize_when_none=False)
    databases = ListType(ModelType(Database))
    number_of_databases = IntType(serialize_when_none=False, default=0)
    unit_display = StringType(serialize_when_none=False),
    server_name_display = StringType(serialize_when_none=False)
    resource_group_display = StringType(serialize_when_none=False)
    tags = ModelType(AzureTags)
    type = StringType(serialize_when_none=False)


class EncryptionProtector(Model):
    id = StringType()
    kind = StringType(serialize_when_none=False)
    location = StringType()
    name = StringType()
    server_key_name = StringType(serialize_when_none=False)
    server_key_type = StringType(choices=('AzureKeyVault', 'ServiceManaged'), default='ServiceManaged')
    subregion = StringType(serialize_when_none=False)
    thumbprint = StringType(serialize_when_none=False)
    uri = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class RestorableDroppedDatabase(Model):
    name = StringType(serialize_when_none=False)
    id = StringType()
    location = StringType()
    creation_date = DateTimeType(serialize_when_none=False)
    database_name = StringType(serialize_when_none=False)
    deletion_date = DateTimeType(serialize_when_none=False)
    earliest_restore_date = DateTimeType(serialize_when_none=False)
    edition = StringType(serialize_when_none=False)
    elastic_pool_name = StringType(default='-')
    max_size_bytes = StringType(serialize_when_none=False)
    service_level_objective = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class VirtualNetworkRule(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    subscription_id = StringType(serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
    ignore_missing_vnet_service_endpoint = BooleanType(serialize_when_none=False)
    state = StringType(choices=('Deleting', 'InProgress', 'Initializing', 'Ready', 'Unknown'),
                       serialize_when_none=False)
    virtual_network_subnet_id = StringType(serialize_when_none=False)
    virtual_network_name_display = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class FirewallRule(Model):
    id = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    end_ip_address = StringType(serialize_when_none=False)
    start_ip_address = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class SQLServer(AzureCloudService):
    name = StringType()
    id = StringType()
    identity = ModelType(ResourceIdentity, serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    location = StringType()
    type = StringType()
    administrator_login = StringType(serialize_when_none=False)
    azure_ad_admin_name = StringType(default='Not configured')
    administrator_login_password = StringType(serialize_when_none=False)
    encryption_protectors = ListType(ModelType(EncryptionProtector), serialize_when_none=False)
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
    failover_groups = ListType(ModelType(FailoverGroup), serialize_when_none=False)
    databases = ListType(ModelType(Database), serialize_when_none=False)
    elastic_pools = ListType(ModelType(ElasticPool), serialize_when_none=False)
    deleted_databases = ListType(ModelType(RestorableDroppedDatabase), serialize_when_none=False)
    virtual_network_rules = ListType(ModelType(VirtualNetworkRule), serialize_when_none=False)
    firewall_rules = ListType(ModelType(FirewallRule), serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
