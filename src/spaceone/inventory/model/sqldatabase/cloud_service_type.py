from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_sql_database = CloudServiceTypeResource()
cst_sql_database.name = 'SQLDatabase'
cst_sql_database.group = 'SQL'
cst_sql_database.service_code = 'Microsoft.Sql/servers/databases'
cst_sql_database.labels = ['Database']
cst_sql_database.is_major = False
cst_sql_database.is_primary = False
cst_sql_database.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-sql-databases.svg',
}

cst_sql_database._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Database Name', 'data.name'),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['Online', 'Creating', 'Copying', 'Creating', 'OnlineChangingDwPerformanceTiers', 'Restoring',
                     'Resuming', 'Scaling', 'Standby'],
            'warning': ['AutoClosed', 'Inaccessible', 'Offline', 'OfflineChangingDwPerformanceTiers',
                        'OfflineSecondary',
                        'Pausing', 'Recovering', 'RecoveryPending', 'Suspect'],
            'disable': ['Disabled', 'Paused', 'Shutdown'],
            'alert': ['EmergencyMode']
        }),
        TextDyField.data_source('Replication Partner Server', 'data.replication_link.partner_server'),
        TextDyField.data_source('Server', 'data.server_name'),
        TextDyField.data_source('Pricing Tier', 'data.pricing_tier_display'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),

        # is_optional fields - Default
        TextDyField.data_source('Resource ID', 'data.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Server Name', 'data.server_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Elastic Pool', 'data.elastic_pool_id', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Earliest Restore Point', 'data.earliest_restore_date', options={
            'is_optional': True
        }),
        TextDyField.data_source('Collation', 'data.collation', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Creation Date', 'data.creation_date', options={
            'is_optional': True
        }),
        TextDyField.data_source('Server Admin Login', 'data.administrator_login', options={
            'is_optional': True
        }),

        # is_optional fields - Configure
        TextDyField.data_source('Service Tier', 'data.service_tier_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Compute Tier', 'data.compute_tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Compute Hardware', 'data.sku.family', options={
            'is_optional': True
        }),
        TextDyField.data_source('Licence Type', 'data.license_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('vCores', 'data.current_sku.capacity', options={
            'is_optional': True
        }),
        TextDyField.data_source('Data max size', 'data.max_size_gb', options={
            'is_optional': True
        }),
        TextDyField.data_source('Zone Redundant', 'data.zone_redundant', options={
            'is_optional': True
        }),
        ListDyField.data_source('Sync Groups', 'data.sync_group_display', options={
            'is_optional': True
        }),
        ListDyField.data_source('Sync Agents', 'data.sync_agent_display', options={
            'is_optional': True
        }),

        # is_optional fields - Diagnostic Settings
        TextDyField.data_source('Diagnostic Setting Name', 'data.diagnostic_settings_resource.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Diagnostic Setting Storage Account', 'data.diagnostic_settings_resource.storage_account_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Event Hub', 'data.diagnostic_settings_resource.event_hub_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Log Analytics Workspace', 'data.diagnostic_settings_resource.workspace_id', options={
            'is_optional': True
        })

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


CLOUD_SERVICE_TYPES_SQL_DB = [
    CloudServiceTypeResponse({'resource': cst_sql_database}),
]
