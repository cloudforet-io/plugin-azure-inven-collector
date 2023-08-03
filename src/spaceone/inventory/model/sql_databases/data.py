from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, FloatType, DateTimeType
from spaceone.inventory.libs.schema.resource import AzureCloudService


class Sku(Model):
    capacity = IntType(serialize_when_none=False)
    family = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    size = StringType(serialize_when_none=False)
    tier = StringType(serialize_when_none=False)


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
    user_private_link = BooleanType(serialize_when_none=False)
    conflict_logging_retention_in_days = IntType(serialize_when_none=False)
    use_private_link_connection = BooleanType(serialize_when_none=False)
    sku = ModelType(Sku, serialize_when_none=False)
    automatic_sync = BooleanType(serialize_when_none=False)


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
    partner_role = StringType(choices=('Copy', 'NonReadableSecondary', 'Primary', 'Secondary', 'Source'), serialize_when_none=False)
    partner_server = StringType(default='-')
    percent_complete = IntType(serialize_when_none=False)
    replication_mode = StringType(serialize_when_none=False)
    replication_state = StringType(choices=('CATCH_UP', 'PENDING', 'SEEDING', 'SUSPENDED'), serialize_when_none=False)
    role = StringType(choices=('Copy', 'NonReadableSecondary', 'Primary', 'Secondary', 'Source'), serialize_when_none=False)
    start_time = DateTimeType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    link_type = StringType(choices=('GEO', 'NAMED'), serialize_when_none=False)
    replica_state = StringType(serialized_name=False)


class DatabaseBlobAuditingPolicy(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    retention_days = IntType(serialize_when_none=False)
    audit_actions_and_groups = ListType(StringType, serialize_when_none=False)
    is_storage_secondary_key_in_use = BooleanType(serialize_when_none=False)
    is_azure_monitor_target_enabled = BooleanType(serialize_when_none=False)
    queue_delay_ms = IntType(serialize_when_none=False)
    state = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    storage_endpoint = StringType(serialize_when_none=False)
    storage_account_access_key = StringType(serialize_when_none=False)
    storage_account_subscription_id = StringType(serialize_when_none=False)


class SQLDatabase(AzureCloudService):  # Main Class
    name = StringType(serialize_when_none=False)
    id = StringType()
    kind = StringType(serialize_when_none=False)
    location = StringType()
    managed_by = StringType(serialize_when_none=False)
    server_name = StringType(serialize_when_none=False)
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
    database_auditing_settings = ModelType(DatabaseBlobAuditingPolicy, serialize_when_none=False)
    # database_auditing_settings = ListType(ModelType(DatabaseBlobAuditingPolicy, serialize_when_none=False))


    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
