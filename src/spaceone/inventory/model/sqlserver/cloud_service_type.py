from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_sql_server = CloudServiceTypeResource()
cst_sql_server.name = 'SqlServers'
cst_sql_server.group = 'Sql'
cst_sql_server.service_code = 'Microsoft.Sql/servers'
cst_sql_server.labels = ['Server']
cst_sql_server.is_primary = True
cst_sql_server.is_major = True
cst_sql_server.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-sql-servers.svg',
}

cst_sql_server._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['Ready'],
            'warning': ['Disabled']
        }),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Public Network Access', key='data.public_network_access', data_type='string'),

    ]

)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sql_server}),
]
