from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_sql_database = CloudServiceTypeResource()
cst_sql_database.name = 'SQLDatabase'
cst_sql_database.group = 'Sql'
cst_sql_database.service_code = 'Microsoft.Sql/servers/databases'
cst_sql_database.labels = ['Databases']
cst_sql_database.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-sql-databases.svg',
}

cst_sql_database._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Status', 'data.status'),
        TextDyField.data_source('Replication Role', ''),
        TextDyField.data_source('Server', 'server_name'),
        TextDyField.data_source('Pricing Tier', 'data.pricing_tier_display'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),

    ],
    search=[
        SearchField.set(name='Database ID', key='data.database_id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Tier', key='data.sku.tier', data_type='string'),
        SearchField.set(name='Server Name', key='data.managed_by', data_type='string')

    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sql_database}),
]
