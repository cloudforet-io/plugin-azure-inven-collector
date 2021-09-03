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
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id')
])


# TAB - tags
mysql_servers_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

mysql_servers_meta = CloudServiceMeta.set_layouts(
    [mysql_servers_info_meta, mysql_servers_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='MySQL')


class MySQLServerResource(ComputeResource):
    cloud_service_type = StringType(default='Server')
    data = ModelType(MySQLServer)
    _metadata = ModelType(CloudServiceMeta, default=mysql_servers_meta, serialized_name='metadata')
    name = StringType()


class MySQLServerResponse(CloudServiceResponse):
    resource = PolyModelType(MySQLServerResource)
