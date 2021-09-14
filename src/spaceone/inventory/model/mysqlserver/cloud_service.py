from schematics.types import ModelType, StringType, PolyModelType
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.mysqlserver.data import MySQLServer
'''
MYSQL SERVERS
'''

# TAB - Default
mysql_servers_info_meta = ItemDynamicLayout.set_fields('MySQL Server', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Server Name', 'data.fully_qualified_domain_name'),
    TextDyField.data_source('Type', 'data.type'),
    EnumDyField.data_source('Status', 'data.user_visible_state', default_state={
        'safe': ['Ready'],
        'warning': ['Dropping'],
        'disable': ['Disabled', 'Inaccessible']
    }),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('Server Admin Login Name', 'data.administrator_login'),
    TextDyField.data_source('MySQL Version', 'data.version'),
    TextDyField.data_source('Performance Configuration (Tier)', 'data.sku.tier'),
    TextDyField.data_source('Performance Configuration (Name)', 'data.sku.name'),
    TextDyField.data_source('SSL Enforce Status', 'data.ssl_enforcement'),
])


# TAB - Connection Security
mysql_servers_firewall_rules = TableDynamicLayout.set_fields('Firewall Rules', 'data.firewall_rules', fields=[
    TextDyField.data_source('Firewall Rule Name', 'name'),
    TextDyField.data_source('Start IP', 'start_ip_address'),
    TextDyField.data_source('End IP', 'end_ip_address')
])
mysql_servers_ssl_tls = ItemDynamicLayout.set_fields('MySQL Server', fields=[
    TextDyField.data_source('Allow Access To Azure Services', 'data.allow_azure_services_access'),
    TextDyField.data_source('Enforce SSL Connection', 'data.ssl_enforcement'),
    TextDyField.data_source('Minimum TLS Version', 'data.minimal_tls_version')
])
# 1 + 2) TAB - Connection Security Meta
mysql_servers_connection_security = ListDynamicLayout.set_layouts('Connection Security', layouts=[
                                                                               mysql_servers_firewall_rules,
                                                                               mysql_servers_ssl_tls])


mysql_servers_parameters = TableDynamicLayout.set_fields('MySQL Parameters', fields=[
    TextDyField.data_source('Allow Access To Azure Services', 'data.allow_azure_services_access'),
    TextDyField.data_source('Enforce SSL Connection', 'data.ssl_enforcement'),
    TextDyField.data_source('Minimum TLS Version', 'data.minimal_tls_version')
])

mysql_servers_pricing_tiers = ItemDynamicLayout.set_fields('Pricing Tier', fields=[
    TextDyField.data_source('Tier', 'data.sku.tier'),
    TextDyField.data_source('Compute Generation', 'data.sku.family'),
    TextDyField.data_source('vCore', 'data.sku.capacity'),
    TextDyField.data_source('Storage', 'data.storage_profile.storage_gb'),
    EnumDyField.data_source('Storage Auto-Growth', 'data.storage_profile.storage_autogrow', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    EnumDyField.data_source('Geo Redundant Backup', 'data.storage_profile.geo_redundant_backup', default_state={
        'safe': ['Enabled'],
        'warning': ['Disabled']
    }),
    TextDyField.data_source('Backup Retention Period', 'data.storage_profile.backup_retention_days'),
])

# TAB - tags
mysql_servers_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

mysql_servers_meta = CloudServiceMeta.set_layouts(
    [mysql_servers_info_meta, mysql_servers_connection_security, mysql_servers_parameters, mysql_servers_pricing_tiers, mysql_servers_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='MySQL')


class MySQLServerResource(ComputeResource):
    cloud_service_type = StringType(default='Server')
    data = ModelType(MySQLServer)
    _metadata = ModelType(CloudServiceMeta, default=mysql_servers_meta, serialized_name='metadata')
    name = StringType()


class MySQLServerResponse(CloudServiceResponse):
    resource = PolyModelType(MySQLServerResource)
