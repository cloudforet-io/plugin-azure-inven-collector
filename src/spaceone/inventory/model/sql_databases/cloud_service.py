from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.model.sqldatabase.data import Database
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

# TAB - Diagnostic Settings
sql_databases_diagnostic_settings = SimpleTableDynamicLayout.set_fields('Diagnostic Settings', 'data.diagnostic_settings_resource', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Storage Account', 'storage_account_id'),
    TextDyField.data_source('Event Hub', 'event_hub_name'),
    TextDyField.data_source('Log Analytics Workspace', 'workspace_id'),
])


# TAB - tags
sql_databases_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

sql_databases_meta = CloudServiceMeta.set_layouts(
    [sql_databases_info_meta, sql_databases_configure, sql_databases_diagnostic_settings, sql_databases_info_tags])


class DatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='Database')


class SqlDatabaseResource(DatabaseResource):
    cloud_service_type = StringType(default='SQLDatabase')
    data = ModelType(Database)
    _metadata = ModelType(CloudServiceMeta, default=sql_databases_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)


class SqlDatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(SqlDatabaseResource)
