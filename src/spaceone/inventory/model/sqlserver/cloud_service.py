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
# Resource Group, Location, Subscription, Subscription ID, SKU, Backend pool, Health probe,
# Load balancing rule, NAT Rules, Public IP Addresses, Load Balancing Type
sql_servers_info_meta = ItemDynamicLayout.set_fields('SQL Servers', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_id'),
    TextDyField.data_source('SKU', 'data.sku.name'),
    TextDyField.data_source('Backend pools', 'data.backend_address_pools_count_display'),
    ListDyField.data_source('Health Probe', 'data.probes_display', options={
        'delimiter': '<br>'
    })
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
