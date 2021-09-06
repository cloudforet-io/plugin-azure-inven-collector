from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_mysql_server = CloudServiceTypeResource()
cst_mysql_server.name = 'Server'
cst_mysql_server.group = 'MySQL'
cst_mysql_server.service_code = 'Microsoft.DBforMySQL/servers'
cst_mysql_server.labels = ['MySQLServer']
cst_mysql_server.is_major = False
cst_mysql_server.is_primary = False
cst_mysql_server.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-mysql-servers.svg',
}

cst_mysql_server._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Type', 'data.type'),
        TextDyField.data_source('Status', 'data.user_visible_state'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id'),

        # is_optional fields - MySQL # TODO
        TextDyField.data_source('Name', 'data.name', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Type', key='data.type', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string')
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_mysql_server}),
]
