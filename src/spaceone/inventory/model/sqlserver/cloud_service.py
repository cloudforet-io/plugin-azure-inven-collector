from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.sqlserver.data import SqlServer
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
SQL SERVERS

'''

# TAB - Default
# Resource Group, Status, Location, Subscription, Subscription ID, Server Admin, Firewalls, Active Directory admin, Server name
sql_servers_info_meta = ItemDynamicLayout.set_fields('SQL Servers', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource Group', 'data.name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    EnumDyField.data_source('Status', 'data.state', default_state={
        'safe': ['Ready'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('Server Admin', 'data.administrator_login'),
    TextDyField.data_source('Active Directory Admin', 'data.azure_ad_admin_name'),
    TextDyField.data_source('Server Name', 'data.fully_qualified_domain_name')

])

# TAB - Failover Groups
# Name, Primary Server, Secondary Server, Read/Write Failover Policy, Grace Period (minutes), Database count
sql_server_failover_group = TableDynamicLayout.set_fields('Failover Groups', 'data.failover_groups', fields=[
    TextDyField.data_source('ID', 'id'),
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Primary Server', 'primary_server'),
    TextDyField.data_source('Secondary Server', 'secondary_server'),
    TextDyField.data_source('Read/Write Failover Policy', 'failover_policy_display'),
    TextDyField.data_source('Grace Period (minutes)', 'grace_period_display'),
    # TextDyField.data_source('Database count', ''),
])

# TAB - Active Directory Admin
# Name, Primary Server, Secondary Server, Read/Write Failover Policy, Grace Period (minutes), Database count
sql_servers_active_directory_admin = ItemDynamicLayout.set_fields('Active Directory Admin', fields=[
    TextDyField.data_source('Active Directory admin', 'azure_ad_admin_name')
])

# TAB - SQL Databases
# Database, Status, Pricing tier
sql_servers_databases = TableDynamicLayout.set_fields('Databases', 'data.databases', fields=[
    TextDyField.data_source('Database', 'name'),
    TextDyField.data_source('Status', 'status'),
    TextDyField.data_source('Pricing Tier', 'pricing_tier_display')
])

# TAB - Elastic Pools
# Name, Pricing tier, Per DB settings, of DBs, Storage, unit, avg, peak, average utilization over past hour
sql_servers_databases = TableDynamicLayout.set_fields('Databases', 'data.elastic_pools', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource Group', 'resource_group_display'),
    TextDyField.data_source('Per DB Settings', 'per_db_settings_display'),
    TextDyField.data_source('Pricing Tier', 'pricing_tier_display'),
    TextDyField.data_source('# of DBs', 'number_of_databases'),
    TextDyField.data_source('Unit', 'unit_display'),
    EnumDyField.data_source('Status', 'state', default_state={
        'safe': ['Ready', 'Creating'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Storage[%]', ''),
    TextDyField.data_source('Avg[%]', ''),
    TextDyField.data_source('Peak[%]', ''),
    TextDyField.data_source('Utilization Over Past Hour[%]', ''),
    TextDyField.data_source('Utilization Over Past Hour[%]', ''),
    TextDyField.data_source('Server Name', 'server_name_display'),
    TextDyField.data_source('Resource Configuration', 'pricing_tier_display'),
    TextDyField.data_source('Maximum Storage Size', 'max_size_gb'),
    ListDyField.data_source('Tags', 'tags')

])

# TAB - Deleted Databases
sql_servers_deleted_databases = TableDynamicLayout.set_fields('Deleted Databases', 'data.deleted_databases', fields=[
    TextDyField.data_source('Database', 'database_name'),
    DateTimeDyField.data_source('Deletion Time (UTC)', 'deletion_date'),
    DateTimeDyField.data_source('Creation Time (UTC)', 'creation_date'),
    TextDyField.data_source('Edition Time (UTC)', 'edition')
])

# TAB - Auditing
sql_servers_auditing = TableDynamicLayout.set_fields('Auditing', 'data.deleted_databases', fields=[
    TextDyField.data_source('Database', 'database_name'),
    DateTimeDyField.data_source('Deletion Time (UTC)', 'deletion_date'),
    DateTimeDyField.data_source('Creation Time (UTC)', 'creation_date'),
    TextDyField.data_source('Edition Time (UTC)', 'edition')
])


# TAB - tags
sql_servers_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

sql_servers_meta = CloudServiceMeta.set_layouts(
    [sql_servers_info_meta, sql_servers_info_tags])


class DatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='Sql')


class SqlServerResource(DatabaseResource):
    cloud_service_type = StringType(default='SqlServers')
    data = ModelType(SqlServer)
    _metadata = ModelType(CloudServiceMeta, default=sql_servers_meta, serialized_name='metadata')


class SqlServerResponse(CloudServiceResponse):
    resource = PolyModelType(SqlServerResource)
