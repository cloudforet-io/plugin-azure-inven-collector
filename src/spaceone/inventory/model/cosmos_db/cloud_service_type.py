import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

cosmosdb_count_by_account_conf = os.path.join(current_dir, 'widget/cosmosdb_count_by_account.yaml')
cosmosdb_count_per_subscription_conf = os.path.join(current_dir, 'widget/cosmosdb_count_by_subscription.yaml')
cosmosdb_count_per_location_conf = os.path.join(current_dir, 'widget/cosmosdb_count_by_region.yaml')
cosmosdb_database_count_per_subscription_conf = os.path.join(current_dir,
                                                             'widget/cosmosdb_database_count_by_subscription.yaml')
cosmosdb_total_count = os.path.join(current_dir, 'widget/cosmosdb_total_count.yaml')

cst_cosmos_db = CloudServiceTypeResource()
cst_cosmos_db.name = 'Instance'
cst_cosmos_db.group = 'CosmosDB'
cst_cosmos_db.service_code = 'Microsoft.DocumentDB/databaseAccounts'
cst_cosmos_db.labels = ['Database']
cst_cosmos_db.is_major = True
cst_cosmos_db.is_primary = True
cst_cosmos_db.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-cosmos-db.svg',
}

cst_cosmos_db._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        TextDyField.data_source('Resource ID', 'data.id'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id'),

        # is_optional field
        TextDyField.data_source('Backup Policy', 'data.backup_policy.type', options={
            'is_optional': True
        }),
        ListDyField.data_source('Read Locations', 'data.read_locations.location_name', options={
            'is_optional': True
        }),
        ListDyField.data_source('Write Locations', 'data.write_locations.location_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Document Endpoint', 'data.document_endpoint', options={
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
        TextDyField.data_source('Private Endpoint Connection Name', 'data.cors.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Endpoint State', 'data.cors.private_link_service_connection_state.status', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Endpoint', 'data.cors.private_endpoint.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('COR Private Link Description', 'data.cors.private_link_service_connection_state.description', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Backup Policy', key='data.backup_policy.type'),
        SearchField.set(name='Read Locations', key='data.read_locations.location_name'),
        SearchField.set(name='Write Locations', key='data.write_locations.location_name'),
        SearchField.set(name='Document Endpoint', key='data.document_endpoint'),
        SearchField.set(name='Capacity Mode', key='data.capability_display'),
        SearchField.set(name='Enable Automatic Failover', key='data.enable_automatic_failover', data_type='boolean'),
        SearchField.set(name='Enable Free Tier', key='data.enable_free_tier', data_type='boolean'),
        SearchField.set(name='Enable Analytical Storage', key='data.enable_analytical_storage', data_type='boolean'),
        SearchField.set(name='Backup Policy', key='data.backup_policy.type'),
        SearchField.set(name='CORS', key='data.cors_display'),
        SearchField.set(name='Default Consistency',
                        key='data.consistency_policy.default_consistency_level'),
        SearchField.set(name='Backup Interval (Minutes)',
                        key='data.backup_policy.periodic_mode_properties.backup_interval_in_minutes',
                        data_type='integer'),
        SearchField.set(name='Backup Retention (Hours)',
                        key='data.backup_policy.periodic_mode_properties.backup_retention_interval_in_hours'),
        SearchField.set(name='Backup storage redundancy',
                        key='data.backup_policy.periodic_mode_properties.additional_properties.backupStorageRedundancy'),
        SearchField.set(name='Enable Public Network Access',
                        key='data.public_network_access'),
        SearchField.set(name='Virtual Networks',
                        key='data.virtual_network_display'),
        SearchField.set(name='Private Endpoint Connection Name',
                        key='data.private_endpoint_connections.name'),
        SearchField.set(name='Private Endpoint State',
                        key='data.private_endpoint_connections.private_link_service_connection_state.status'),
        SearchField.set(name='Private Endpoint Name',
                        key='data.private_endpoint_connections.name'),
        SearchField.set(name='Private Endpoint',
                        key='data.private_endpoint_connections.name'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(cosmosdb_total_count)),
        ChartWidget.set(**get_data_from_yaml(cosmosdb_count_per_location_conf)),
        ChartWidget.set(**get_data_from_yaml(cosmosdb_count_per_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(cosmosdb_database_count_per_subscription_conf)),
        CardWidget.set(**get_data_from_yaml(cosmosdb_total_count)),
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_cosmos_db}),
]
