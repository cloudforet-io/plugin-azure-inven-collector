from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, FloatType, DateTimeType


class Tags(Model):
    key = StringType()
    value = StringType()


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
    last_sync_time = StringType(serialize_when_none=False)
    schema = ModelType(SyncGroupSchema, serialize_when_none=False)
    sync_database_id = StringType(serialize_when_none=False)
    sync_state = StringType(choices=('Error', 'Good', 'NotReady', 'Progressing', 'Warning'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Sku(Model):
    capacity = IntType(serialize_when_none=False)
    family = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    size = StringType(serialize_when_none=False)
    tier = StringType(serialize_when_none=False)


class SqlDatabase(Model):
    name = StringType(serialize_when_none=False)
    id = StringType()
    kind = StringType(serialize_when_none=False)
    location = StringType()
    managed_by = StringType(serialize_when_none=False)
    server_name = StringType(serialize_when_none=False)
    subscription_id = StringType(serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
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
    long_term_retention_backup_resource_id = StringType(serialize_when_none=False)
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
    sync_group = ListType(ModelType(SyncGroup))
    sku = ModelType(Sku, serialize_when_none=False)
    pricing_tier_display = StringType(default='-')
    compute_tier = StringType(serialize_when_none=False)
    tags = (ModelType(Tags))
    type = StringType(serialize_when_none=False)