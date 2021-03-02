from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.sqldatabase.data import SqlDatabase
from spaceone.inventory.model.sqlserver.data import SqlServer
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
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Status', 'data.status'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('Server Name', 'data.sku.name'),
    TextDyField.data_source('Elastic Pool', 'data.elastic_pool_id'),
    TextDyField.data_source('Pricing Tier', 'data.pricing_tier_display'),
    DateTimeDyField.data_source('Earliest Restore Point', 'data.earliest_restore_date'),
    TextDyField.data_source('Collation', 'data.collation'),
    DateTimeDyField.data_source('Creation Date', 'data.creation_date'),
    TextDyField.data_source('Server Admin Login', 'data.administrator_login'),


])

# TAB - Configure
sql_databases_configure = ItemDynamicLayout.set_fields('Configure', fields=[
    TextDyField.data_source('Pricing Tier', 'data.sku.tier'),
    TextDyField.data_source('Compute Tier', 'data.compute_tier'),
    TextDyField.data_source('Compute Hardware', 'data.sku.name'),
    TextDyField.data_source('Licence Type', 'data.license_type'),
    TextDyField.data_source('vCores', 'data.current_sku.capacity'),
    TextDyField.data_source('Data max size', 'data.max_size_gb'),
])

# TAB - Geo-Replication TODO : create_mode : None (if create_mode is secondary : Find Region and list all..)
# TAB - Connection Strings TODO : No API
# TAB - Sync To Other Databases
sql_databases_sync_group = ItemDynamicLayout.set_fields('Sync Group', 'data.sync_group', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Status', 'sync_state')
])
sql_databases_sync_agent = ItemDynamicLayout.set_fields('Sync Agent', fields=[
    TextDyField.data_source('Name', ''),
    TextDyField.data_source('Status', '')
])
sql_databases_sync = CloudServiceMeta.set_layouts(
    [sql_databases_sync_group, sql_databases_sync_agent])

# TAB - Connection Strings TODO : Server-Level.. Skip?

# TAB - 

# TAB - tags
sql_databases_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

sql_databases_meta = CloudServiceMeta.set_layouts(
    [sql_databases_info_meta, sql_databases_info_tags])


class DatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='Sql')


class SqlDatabaseResource(DatabaseResource):
    cloud_service_type = StringType(default='Sqldatabases')
    data = ModelType(SqlDatabase)
    _metadata = ModelType(CloudServiceMeta, default=sql_databases_meta, serialized_name='metadata')


class SqlDatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(SqlDatabaseResource)
