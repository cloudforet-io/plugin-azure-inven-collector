import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))


cst_cosmos_db = CloudServiceTypeResource()
cst_cosmos_db.name = 'AzureCosmosDB'
cst_cosmos_db.group = 'Database'
cst_cosmos_db.service_code = 'Microsoft.DocumentDB/databaseAccounts'
cst_cosmos_db.labels = ['Database']
cst_cosmos_db.is_major = False
cst_cosmos_db.is_primary = False
cst_cosmos_db.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-cosmos-db.svg',
}

cst_cosmos_db._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        TextDyField.data_source('Resource ID', 'data.id'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id'),

        # is_optional field
        TextDyField.data_source('Name ', 'data.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Policy', 'data.backup_policy.type', options={
            'is_optional': True
        }),
        ListDyField.data_source('Read Locations', 'data.read_locations.location_name', options={
            'is_optional': True
        }),
        ListDyField.data_source('Write Locations', 'data.write_locations.location_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('URI', 'data.document_endpoint', options={
            'is_optional': True
        }),
        TextDyField.data_source('Capacity Mode', 'data.capability_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Enable Automatic Failover', 'data.enable_automatic_failover',options={
            'is_optional': True
        }),
        TextDyField.data_source('Enable Free Tier', 'data.enable_free_tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Enable Analytical Storage', 'data.enable_analytical_storage', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Policy', 'data.backup_policy.type', options={
            'is_optional': True
        }),
        ListDyField.data_source('CORS', 'data.cors_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Default Consistency', 'data.consistency_policy.default_consistency_level', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Interval (Minutes)',
                                'data.backup_policy.periodic_mode_properties.backup_interval_in_minutes', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Retention (Hours)', 'data.backup_policy.periodic_mode_properties.backup_retention_interval_in_hours', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup storage redundancy', 'data.backup_policy.periodic_mode_properties.additional_properties.backupStorageRedundancy', options={
            'is_optional': True
        }),
        TextDyField.data_source('Enable Public Network Access', 'data.public_network_access', options={
            'is_optional': True
        }),
        ListDyField.data_source('Virtual Networks', 'data.virtual_network_display', options={
            'is_optional': True
        }),
        # is_optional - private endpoint connections
        TextDyField.data_source('Connection Name', 'data.private_endpoint_connections.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Connection State', 'data.private_endpoint_connections.private_link_service_connection_state.status', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Endpoint', 'data.private_endpoint_connections.private_endpoint.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.private_endpoint_connections.private_link_service_connection_state.description', options={
            'is_optional': True
        }),
        # is_optional - cors
        TextDyField.data_source('Connection Name', 'data.cors.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Connection State', 'data.cors.private_link_service_connection_state.status', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Endpoint', 'data.cors.private_endpoint.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.cors.private_link_service_connection_state.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('Database', 'name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Database ID', 'id', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='name', data_type='string'),
        SearchField.set(name='Subscription ID', key='account', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string')
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_cosmos_db}),
]
