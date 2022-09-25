from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.model.sql_servers.data import SQLServer
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
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Resource ID', 'data.id'),
    EnumDyField.data_source('Status', 'data.state', default_state={
        'safe': ['Ready'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
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

# TAB - Backups
# Database, Earliest PITR restore point (UTC), Available LTR backups
sql_server_backups = TableDynamicLayout.set_fields('Backups', 'data.databases', fields=[
    TextDyField.data_source('Database', 'name'),
    TextDyField.data_source('Earliest PITR Restore Point (UTC)', 'earliest_restore_date'),
    TextDyField.data_source('Available LTR backups', 'long_term_retention_backup_resource_id'),
])

# TAB - Active Directory Admin
# Active Directory Admin
sql_servers_active_directory_admin = ItemDynamicLayout.set_fields('Active Directory Admin', fields=[
    TextDyField.data_source('Active Directory Admin', 'data.azure_ad_admin_name')
])

# TAB - SQL Databases - Default
sql_servers_databases = TableDynamicLayout.set_fields('Databases', 'data.databases', fields=[
    TextDyField.data_source('Database', 'name'),
    TextDyField.data_source('Resource ID', 'id'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['Online', 'Creating', 'Copying', 'Creating', 'OnlineChangingDwPerformanceTiers', 'Restoring', 'Resuming', 'Scaling', 'Standby'],
        'warning': ['AutoClosed', 'Inaccessible', 'Offline', 'OfflineChangingDwPerformanceTiers', 'OfflineSecondary',  'Pausing', 'Recovering', 'RecoveryPending',  'Suspect'],
        'disable':['Disabled', 'Paused', 'Shutdown'],
        'alert': ['EmergencyMode']
    }),
    TextDyField.data_source('Resource Group', 'resource_group'),
    TextDyField.data_source('Subscription ID', 'subscription_id'),
    TextDyField.data_source('Location', 'location'),
    TextDyField.data_source('Server Name', 'server_name'),
    TextDyField.data_source('Elastic Pool', ''),
    # TextDyField.data_source('Connection Strings', ''),
    TextDyField.data_source('Pricing Tier', 'pricing_tier_display'),
    TextDyField.data_source('Earliest Restore Point', 'earliest_restore_date'),
])

# TAB - SQL Databases - Configure
sql_servers_databases_configure = TableDynamicLayout.set_fields('Databases Configure', 'data.databases', fields=[
    TextDyField.data_source('Service Tier', 'service_tier_display'),
    TextDyField.data_source('Compute Tier', 'compute_tier'),
    TextDyField.data_source('Compute Hardware', 'sku.family'),
    TextDyField.data_source('License Type', 'license_type'),
    TextDyField.data_source('vCores', 'sku.capacity'),
    TextDyField.data_source('Data Max Size', 'max_size_gb'),
    TextDyField.data_source('Zone Redundant', 'zone_redundant'),
    ListDyField.data_source('Sync Groups', 'sync_group_display'),
    ListDyField.data_source('Sync Agents', 'sync_agent_display'),
    TextDyField.data_source('Collation', 'collation'),
    DateTimeDyField.data_source('Creation Date', 'creation_date'),
    # TextDyField.data_source('Server Admin Login', '')   # Remove: DB is already under the specific server
    # TextDyField.data_source('Active Directory Login', ''),  # Remove: DB is already under the specific server

])

# TAB - SQL Databases - tags
sql_databases_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

# TAB - Dynamic Data Masking : "Masking rules: + Tab "Recommended fields to mask"  # TODO: confirm!!
sql_servers_databases_info = ListDynamicLayout.set_layouts('SQL Databases',
                                                           layouts=[sql_servers_databases,
                                                                    sql_servers_databases_configure,
                                                                    sql_databases_info_tags])

# TAB - Elastic Pools
# Name, Pricing tier, Per DB settings, of DBs, Storage, unit, avg, peak, average utilization over past hour
sql_servers_elastic_pools = TableDynamicLayout.set_fields('Elastic Pools', 'data.elastic_pools', fields=[
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
    # TextDyField.data_source('Storage[%]', ''),
    # TextDyField.data_source('Avg[%]', ''),
    # TextDyField.data_source('Peak[%]', ''),
    # TextDyField.data_source('Utilization Over Past Hour[%]', ''),
    # TextDyField.data_source('Utilization Over Past Hour[%]', ''),
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
sql_servers_auditing = ItemDynamicLayout.set_fields('Auditing', 'data.server_auditing_settings', fields=[
    EnumDyField.data_source('Enable SQL Auditing', 'state', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Audit Log Destination', 'storage_endpoint'),
    TextDyField.data_source('Storage Account ID', 'storage_account_subscription_id'),
])

# TAB - Firewalls and Virtual Networks
sql_servers_network = ItemDynamicLayout.set_fields('Network', fields=[
    EnumDyField.data_source('Public Network access', 'data.public_network_access', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Minimum TLS Version', 'data.minimal_tls_version'),
    TextDyField.data_source('Connection Policy', 'data.server_auditing_settings.name'),
    TextDyField.data_source('Allow Azure Services and Resources to Access this server',
                            'data.server_auditing_settings.is_azure_monitor_target_enabled')

])
sql_servers_firewall_rules = TableDynamicLayout.set_fields('Firewall Rules', 'data.firewall_rules', fields=[
    TextDyField.data_source('Rule Name', 'name'),
    TextDyField.data_source('Start IP', 'start_ip_address'),
    TextDyField.data_source('End IP', 'end_ip_address')
])

sql_servers_virtual_network_rules = TableDynamicLayout.set_fields('Virtual Network Rules', 'data.virtual_network_rules',
                                                                  fields=[
                                                                      TextDyField.data_source('Rule Name', 'name'),
                                                                      TextDyField.data_source('Virtual Network',
                                                                                              'virtual_network_name_display'),
                                                                      TextDyField.data_source('Subnet ID',
                                                                                              'virtual_network_subnet_id'),
                                                                      # TextDyField.data_source('Address Range', ''),
                                                                      # TextDyField.data_source('Endpoint Status', ''),
                                                                      TextDyField.data_source('Resource Group',
                                                                                              'resource_group'),
                                                                      TextDyField.data_source('Subscription',
                                                                                              'subscription_id'),
                                                                      EnumDyField.data_source('State', 'state',
                                                                                              default_state={
                                                                                                  'safe': ['Ready',
                                                                                                           'InProgress',
                                                                                                           'Initializing'],
                                                                                                  'warning': [
                                                                                                      'Deleting',
                                                                                                      'Unknown']
                                                                                              })
                                                                  ])

sql_servers_firewalls_and_vn = ListDynamicLayout.set_layouts('Firewalls and Network',
                                                             layouts=[sql_servers_network, sql_servers_firewall_rules,
                                                                      sql_servers_virtual_network_rules])

# TAB - Private Endpoint Connections
sql_servers_private_endpoint_connections = TableDynamicLayout.set_fields('Private Endpoint Connections',
                                                                         'data.private_endpoint_connections', fields=[
        TextDyField.data_source('Connection ID', 'connection_id'),
        TextDyField.data_source('State', 'status'),
        TextDyField.data_source('Private Endpoint Name', 'private_endpoint_name'),
        TextDyField.data_source('Request / Response Message', 'description')
])

# TAB - Transparent Data Encryption
sql_servers_transparent_data_encryption = TableDynamicLayout.set_fields('Transparent Data Encryption',
                                                                        'data.encryption_protectors', fields=[
    TextDyField.data_source('Transparent Data Encryption', 'kind'),
    TextDyField.data_source('Key', 'server_key_name'),
    TextDyField.data_source('Key Type', 'server_key_type'),
    TextDyField.data_source('Uri', 'uri')
])

# TAB - Automatic Tuning
sql_servers_automatic_tuning_options = TableDynamicLayout.set_fields('Tuning Options',
                                                                     'data.server_automatic_tuning.options', fields=[
        TextDyField.data_source('Tuning Type', 'tuning_type'),
        TextDyField.data_source('Desired State', 'desired_state'),
        TextDyField.data_source('Current State', 'actual_state'),
])


# TAB - tags
sql_servers_info_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

# TAB - SQL Databases
sql_servers_meta = CloudServiceMeta.set_layouts(
    [sql_servers_info_meta, sql_server_failover_group, sql_server_backups, sql_servers_active_directory_admin, sql_servers_databases_info,
     sql_servers_elastic_pools,
     sql_servers_deleted_databases, sql_servers_auditing, sql_servers_network, sql_servers_transparent_data_encryption, sql_servers_automatic_tuning_options,
     sql_servers_firewalls_and_vn,
     sql_servers_private_endpoint_connections, sql_servers_info_tags])


class DatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='SQLServers')


class SQLServerResource(DatabaseResource):
    cloud_service_type = StringType(default='Server')
    data = ModelType(SQLServer)
    _metadata = ModelType(CloudServiceMeta, default=sql_servers_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)


class SQLServerResponse(CloudServiceResponse):
    resource = PolyModelType(SQLServerResource)
