from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.cosmos_db.data import DatabaseAccountGetResults

'''
COSMOS DB
'''
# TAB - Default
cosmos_db_info_meta = ItemDynamicLayout.set_fields('Cosmos DB', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('Backup Policy', 'data.backup_policy.type'),
    ListDyField.data_source('Read Locations', 'data.read_locations.location_name'),
    ListDyField.data_source('Write Locations', 'data.write_locations.location_name'),
    TextDyField.data_source('URI', 'data.document_endpoint'),
    EnumDyField.data_source('Public Network Access', 'data.public_network_access', default_state={
        'safe': ['Enabled'],
        'warning':['Disabled']
    }),
    TextDyField.data_source('Capacity Mode', 'data.capability_display'),
])

# TAB - Features
cosmos_db_features = ItemDynamicLayout.set_fields('Features', fields=[
    EnumDyField.data_source('Enable Automatic Failover', 'data.enable_automatic_failover', default_state={
        'safe': [True],
        'warning':[False]
    }),
    EnumDyField.data_source('Enable Free Tier', 'data.enable_free_tier', default_state={
        'safe': [True],
        'warning':[False]
    }),
    EnumDyField.data_source('Enable Analytical Storage', 'data.enable_analytical_storage', default_state={
        'safe': [True],
        'warning':[False]
    }),
    TextDyField.data_source('Backup Policy', 'data.backup_policy.type'),
    ListDyField.data_source('CORS', 'data.cors_display')
])

# TAB - Default Consistency
cosmos_db_default_consistency = ItemDynamicLayout.set_fields('Default Consistency', fields=[
    TextDyField.data_source('Default Consistency', 'data.consistency_policy.default_consistency_level')
])

# TAB - Features
cosmos_db_backup = ItemDynamicLayout.set_fields('Backup & Restore', fields=[
    TextDyField.data_source('Backup Interval (Minutes)', 'data.backup_policy.periodic_mode_properties.backup_interval_in_minutes'),
    TextDyField.data_source('Backup Retention (Hours)', 'data.backup_policy.periodic_mode_properties.backup_retention_interval_in_hours'),
    TextDyField.data_source('Backup storage redundancy', 'data.backup_policy.periodic_mode_properties.additional_properties.backupStorageRedundancy'),
])

# TAB - Firewall and Virtual Networks
cosmos_db_virtual_network = ItemDynamicLayout.set_fields('Firewall and Virtual Networks', fields=[
    TextDyField.data_source('Enable Public Network Access', 'data.public_network_access'),
    ListDyField.data_source('Virtual Networks', 'data.virtual_network_display')
])

# TAB - Private Endpoint Connections
cosmos_db_private_endpoint = TableDynamicLayout.set_fields('Private Endpoint Connections', 'data.private_endpoint_connections', fields=[
    TextDyField.data_source('Connection Name', 'name'),
    TextDyField.data_source('Connection State', 'private_link_service_connection_state.status'),
    TextDyField.data_source('Private Endpoint', 'private_endpoint.name'),
    TextDyField.data_source('Description', 'private_link_service_connection_state.description')
])

# TAB - Cors
cosmos_db_cors = TableDynamicLayout.set_fields('Cors', 'data.cors', fields=[
    TextDyField.data_source('Connection Name', 'name'),
    TextDyField.data_source('Connection State', 'private_link_service_connection_state.status'),
    TextDyField.data_source('Private Endpoint', 'private_endpoint.name'),
    TextDyField.data_source('Description', 'private_link_service_connection_state.description')
])

# TAB - Keys
cosmos_db_keys = ItemDynamicLayout.set_fields('Keys', 'data.keys', fields=[
    TextDyField.data_source('Primary Readonly Master Key', 'primary_readonly_master_key'),
    TextDyField.data_source('Secondary Readonly Master Key', 'secondary_readonly_master_key'),
    TextDyField.data_source('Primary Master Key', 'primary_master_key'),
    TextDyField.data_source('Primary Master Key', 'secondary_master_key')
])

# TAB - Database
cosmos_db_database = SimpleTableDynamicLayout.set_fields('Database', 'data.sql_databases', fields=[
    TextDyField.data_source('Database', 'name'),
    TextDyField.data_source('ID', 'id')
])

cosmos_db_meta = CloudServiceMeta.set_layouts(
    [cosmos_db_info_meta, cosmos_db_features, cosmos_db_default_consistency, cosmos_db_backup,
     cosmos_db_virtual_network, cosmos_db_private_endpoint, cosmos_db_cors, cosmos_db_database])


class DatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='CosmosDB')


class CosmosDBResource(DatabaseResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(DatabaseAccountGetResults)
    _metadata = ModelType(CloudServiceMeta, default=cosmos_db_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)


class CosmosDBResponse(CloudServiceResponse):
    resource = PolyModelType(CosmosDBResource)
