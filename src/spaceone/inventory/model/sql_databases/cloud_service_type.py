import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

sql_databases_count_by_account_conf = os.path.join(current_dir, 'widget/sql_databases_count_by_account.yaml')
sql_databases_count_by_region_conf = os.path.join(current_dir, 'widget/sql_databases_count_by_region.yaml')
sql_databases_count_by_subscription_conf = os.path.join(current_dir, 'widget/sql_databases_count_by_subscription.yaml')
sql_databases_total_count_conf = os.path.join(current_dir, 'widget/sql_databases_total_count.yaml')

cst_sql_databases = CloudServiceTypeResource()
cst_sql_databases.name = 'Database'
cst_sql_databases.group = 'SQLDatabases'
cst_sql_databases.service_code = 'Microsoft.Sql/servers/databases'
cst_sql_databases.labels = ['Database']
cst_sql_databases.is_major = True
cst_sql_databases.is_primary = True
cst_sql_databases.service_code = 'Microsoft.Sql/servers/databases'
cst_sql_databases.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-sql-databases.svg',
}

cst_sql_databases._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
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
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),

        # is_optional fields - Default
        TextDyField.data_source('Elastic Pool', 'data.elastic_pool_id', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Earliest Restore Point', 'data.earliest_restore_date', options={
            'is_optional': True
        }),
        TextDyField.data_source('Collation', 'data.collation', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Creation Date', 'launched_at', options={
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
        TextDyField.data_source('Data max size', 'instance_size', options={
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
        SearchField.set(name='Database ID', key='data.database_id'),
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Tier', key='instance_type'),
        SearchField.set(name='Server Name', key='data.managed_by'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Replication Partner Server', key='data.replication_link.partner_server'),
        SearchField.set(name='Pricing Tier', key='data.pricing_tier_display'),
        SearchField.set(name='Elastic Pool', key='data.elastic_pool_id'),
        SearchField.set(name='Earliest Restore Point', key='data.earliest_restore_date'),
        SearchField.set(name='Collation', key='data.collation'),
        SearchField.set(name='Server Admin Login', key='data.administrator_login'),
        SearchField.set(name='Service Tier', key='data.service_tier_display'),
        SearchField.set(name='Compute Tier', key='data.compute_tier'),
        SearchField.set(name='Compute Hardware', key='data.sku.family'),
        SearchField.set(name='Licence Type', key='data.license_type'),
        SearchField.set(name='vCores', key='data.current_sku.capacity', data_type='integer'),
        SearchField.set(name='Data max size', key='instance_size', data_type='integer'),
        SearchField.set(name='Zone Redundant', key='data.zone_redundant'),
        SearchField.set(name='Sync Groups', key='data.sync_group_display'),
        SearchField.set(name='Sync Agents', key='data.sync_agent_display'),
        SearchField.set(name='Diagnostic Setting Name', key='data.diagnostic_settings_resource.name'),
        SearchField.set(name='Diagnostic Setting Storage Account', key='data.diagnostic_settings_resource.storage_account_id'),
        SearchField.set(name='Event Hub', key='data.diagnostic_settings_resource.event_hub_name'),
        SearchField.set(name='Log Analytics Workspace', key='data.diagnostic_settings_resource.workspace_id'),
        SearchField.set(name='Creation Date', key='launched_at', data_type='datetime'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(sql_databases_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_databases_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_databases_count_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_databases_total_count_conf))
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sql_databases}),
]
