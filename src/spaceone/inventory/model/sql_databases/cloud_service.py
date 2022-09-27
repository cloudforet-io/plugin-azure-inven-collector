from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.model.sql_databases.data import *
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
SQL DATABASES
'''

# TAB - Default
# Resource Group, Location, Subscription, Subscription ID, SKU, Backend pool, Health probe,
# Load balancing rule, NAT Rules, Public IP Addresses, Load Balancing Type
sql_databases_info_meta = ItemDynamicLayout.set_fields('SQL Databases', fields=[
    TextDyField.data_source('Database Name', 'name'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['Online', 'Creating', 'Copying', 'Creating', 'OnlineChangingDwPerformanceTiers', 'Restoring',
                 'Resuming', 'Scaling', 'Standby'],
        'warning': ['AutoClosed', 'Inaccessible', 'Offline', 'OfflineChangingDwPerformanceTiers', 'OfflineSecondary',
                    'Pausing', 'Recovering', 'RecoveryPending', 'Suspect'],
        'disable': ['Disabled', 'Paused', 'Shutdown'],
        'alert': ['EmergencyMode']
    }),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription ID', 'account'),
    TextDyField.data_source('Server Name', 'data.server_name'),
    TextDyField.data_source('Elastic Pool', 'data.elastic_pool_id'),
    TextDyField.data_source('Pricing Tier', 'data.pricing_tier_display'),
    DateTimeDyField.data_source('Earliest Restore Point', 'data.earliest_restore_date'),
    TextDyField.data_source('Collation', 'data.collation'),
    DateTimeDyField.data_source('Creation Date', 'launched_at'),
    TextDyField.data_source('Server Admin Login', 'data.administrator_login'),

])

# TAB - Configure
sql_databases_configure = ItemDynamicLayout.set_fields('Configure', fields=[
    TextDyField.data_source('Service Tier', 'data.service_tier_display'),
    TextDyField.data_source('Compute Tier', 'data.compute_tier'),
    TextDyField.data_source('Compute Hardware', 'data.sku.family'),
    TextDyField.data_source('Licence Type', 'data.license_type'),
    TextDyField.data_source('vCores', 'data.current_sku.capacity'),
    TextDyField.data_source('Data max size', 'instance_size'),
    TextDyField.data_source('Zone Redundant', 'data.zone_redundant'),
    ListDyField.data_source('Sync Groups', 'data.sync_group_display'),
    ListDyField.data_source('Sync Agents', 'data.sync_agent_display'),
    TextDyField.data_source('Collation', 'data.collation'),
    DateTimeDyField.data_source('Creation Date', 'data.creation_date')
])


# TAB - Backups
# Database, Earliest PITR restore point (UTC), Available LTR backups
sql_databases_backups = TableDynamicLayout.set_fields('Backups', 'data', fields=[
    TextDyField.data_source('Database', 'name'),
    TextDyField.data_source('Earliest PITR Restore Point (UTC)', 'earliest_restore_date'),
    TextDyField.data_source('Available LTR backups', 'long_term_retention_backup_resource_id'),
])

# TAB - Replication
sql_databases_replication = TableDynamicLayout.set_fields('Replicas', 'data.replication_link', fields=[
    TextDyField.data_source('Name', 'partner_database'),
    TextDyField.data_source('linkType', 'link_type'),
    TextDyField.data_source('Region', 'partner_location'),
    TextDyField.data_source('Replica state', 'replica_state'),
])

# TAB - Maintenance
sql_databases_maintenance = ItemDynamicLayout.set_fields('Maintenance', 'data', fields=[

])

# TAB - Sync to other databases - Sync database
sql_databases_sync_to_other_databases_sync_database = TableDynamicLayout.set_fields('Sync Group', 'data.sync_group', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Status', 'sync_state'),
    TextDyField.data_source('Use private link', 'use_private_link_connection'),
    TextDyField.data_source('Automatic Sync', 'automatic_sync'),
    TextDyField.data_source('Conflict Resolution', 'conflict_resolution_policy'),
    TextDyField.data_source('Interval', 'interval')

])
# TAB - Sync to other databases - Sync Agent
sql_databases_sync_to_other_databases_sync_agent = TableDynamicLayout.set_fields('Sync Agent', 'data.sync_agent', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Status', 'state'),
    TextDyField.data_source('version', 'version')
])

# TAB - Sync to other databases
sql_databases_sync_to_other_databases_info = ListDynamicLayout.set_layouts('Sync to other databases', layouts=[
    sql_databases_sync_to_other_databases_sync_database, sql_databases_sync_to_other_databases_sync_agent
])

# TAB - Auditing
sql_servers_auditing = ItemDynamicLayout.set_fields('Auditing', 'data.database_auditing_settings', fields=[
    EnumDyField.data_source('Enable SQL Auditing', 'state', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Audit Log Destination', 'storage_endpoint'),
    TextDyField.data_source('Storage Account ID', 'storage_account_subscription_id'),
    TextDyField.data_source('Retention days', 'retention_days'),
    TextDyField.data_source('Secondary Storage access key used', 'is_storage_secondary_key_in_use'),
    TextDyField.data_source('Storage Authentication Type', 'storage_account_access_key')
])

# TAB


# TAB - Diagnostic Settings
sql_databases_diagnostic_settings = SimpleTableDynamicLayout.set_fields('Diagnostic Settings', 'data.diagnostic_settings_resource', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Storage Account', 'storage_account_id'),
    TextDyField.data_source('Event Hub', 'event_hub_name'),
    TextDyField.data_source('Log Analytics Workspace', 'workspace_id'),
])


# TAB - tags
sql_databases_info_tags = TableDynamicLayout.set_fields('Tags', 'data', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

sql_databases_meta = CloudServiceMeta.set_layouts(
    [sql_databases_info_meta, sql_databases_configure, sql_databases_diagnostic_settings, sql_databases_backups,
     sql_databases_replication, sql_databases_sync_to_other_databases_info, sql_databases_info_tags])


class DatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='SQLDatabases')


class SQLDatabaseResource(DatabaseResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(SQLDatabase)
    _metadata = ModelType(CloudServiceMeta, default=sql_databases_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)


class SQLDatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(SQLDatabaseResource)
