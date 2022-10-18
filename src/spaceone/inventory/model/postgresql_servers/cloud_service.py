from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.model.postgresql_servers.data import PostgreSQLServer
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, \
    ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
POSTGRESQL SERVERS
'''

# TAB - Default
postgresql_servers_info_meta = ItemDynamicLayout.set_fields('PostgreSQL Servers', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Resource ID', 'data.id'),
    EnumDyField.data_source('Status', 'data.user_visible_state', default_state={
        'safe': ['Ready'],
        'warning': ['Disabled', 'Dropping', 'Inaccessible']
    }),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
    TextDyField.data_source('Server Name', 'data.fully_qualified_domain_name'),
    TextDyField.data_source('Admin Username', 'data.administrator_login'),
    TextDyField.data_source('PostgreSQL Version', 'data.version'),
    TextDyField.data_source('Performance Configuration Tier', 'data.sku.tier'),
    TextDyField.data_source('Performance Configuration Name', 'data.sku.name'),
    TextDyField.data_source('Performance Configuration Capacity', 'data.sku.capacity'),
    EnumDyField.data_source('SSL Enforce Status', 'data.ssl_enforcement', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    })
])

# TAB - Connection Security
postgresql_server_connection_security_default = ItemDynamicLayout.set_fields('Connection Security', fields=[
    EnumDyField.data_source('Public Network Access', 'data.public_network_access', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    EnumDyField.data_source('SSL Enforcement', 'data.ssl_enforcement', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('TLS Setting', 'data.minimal_tls_version'),

])

postgresql_server_firewall_rules = SimpleTableDynamicLayout.set_fields('Firewall Rules', 'data.firewall_rules', fields=[
    TextDyField.data_source('Firewall Rule Name', 'name'),
    TextDyField.data_source('Start IP', 'start_ip_address'),
    TextDyField.data_source('End IP', 'end_ip_address')
])

# TAB - VNet Rules
postgresql_server_vnet_rules = SimpleTableDynamicLayout.set_fields('VNET Rules', 'data.virtual_network_rules', fields=[
    TextDyField.data_source('Rule Name', 'name'),
    TextDyField.data_source('Virtual Network', 'virtual_network_name_display'),
    TextDyField.data_source('Subnet', 'subnet_name'),
    EnumDyField.data_source('Endpoint Status', 'state', default_state={
        'safe': ['Ready', 'InProgress'],
        'warning': ['Deleting', 'Initializing', 'Unknown']
    })
])

# 1 + 2 + 3) TAB - Connection Security Meta
postgresql_servers_connection_security = ListDynamicLayout.set_layouts('Connection Security', layouts=[
                                                                               postgresql_server_connection_security_default,
                                                                               postgresql_server_firewall_rules, postgresql_server_vnet_rules])

# TAB - Replicas
postgresql_servers_replication = SimpleTableDynamicLayout.set_fields('Replicas', 'data.replicas', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Location', 'location'),
    EnumDyField.data_source('Status', 'user_visible_state', default_state={
        'safe': ['Ready'],
        'warning': ['Disabled', 'Dropping', 'Inaccessible']
    }),
    TextDyField.data_source('Master Server Name', 'master_server_name')
])

# TAB - Server Admin
postgresql_servers_server_admin = SimpleTableDynamicLayout.set_fields('Active Directory Admin', 'data.server_administrators', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Login', 'login'),
    TextDyField.data_source('SID', 'sid'),
    TextDyField.data_source('Tenant ID', 'tenant_id')
])

# TAB - Pricing Tier
postgresql_servers_pricing_tier = ItemDynamicLayout.set_fields('Pricing Tier', fields=[
    TextDyField.data_source('Compute Generation', 'data.sku.name'),
    TextDyField.data_source('vCore', 'data.sku.capacity'),
    EnumDyField.data_source('Storage Auto Grow', 'data.storage_profile.storage_autogrow', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Backup Retention Period (Days)', 'data.storage_profile.backup_retention_days')
])

# TAB - Postgresql server - tags
postgresql_servers_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])


postgresql_servers_meta = CloudServiceMeta.set_layouts(
    [postgresql_servers_info_meta, postgresql_servers_connection_security, postgresql_servers_replication,
     postgresql_servers_server_admin, postgresql_servers_pricing_tier, postgresql_servers_tags])


class DatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='PostgreSQLServers')


class PostgreSQLServerResource(DatabaseResource):
    cloud_service_type = StringType(default='Server')
    data = ModelType(PostgreSQLServer)
    _metadata = ModelType(CloudServiceMeta, default=postgresql_servers_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class PostgreSQLServerResponse(CloudServiceResponse):
    resource = PolyModelType(PostgreSQLServerResource)
