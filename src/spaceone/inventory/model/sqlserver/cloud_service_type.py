import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))


cst_sql_server = CloudServiceTypeResource()
cst_sql_server.name = 'SQLServer'
cst_sql_server.group = 'Database'
cst_sql_server.service_code = 'Microsoft.Sql/servers'
cst_sql_server.labels = ['Database']
cst_sql_server.is_primary = True
cst_sql_server.is_major = True
cst_sql_server.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-sql-servers.svg',
}

cst_sql_server._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['Ready'],
            'warning': ['Disabled']
        }),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),

        # is_optional fields - Default
        TextDyField.data_source('Resource ID', 'data.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subscription ID', 'account', options={
            'is_optional': True
        }),
        TextDyField.data_source('Server Admin', 'data.administrator_login', options={
            'is_optional': True
        }),
        TextDyField.data_source('Active Directory Admin', 'data.azure_ad_admin_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Server Name', 'data.fully_qualified_domain_name', options={
            'is_optional': True
        }),

        # is_optional fields - Failover Groups
        TextDyField.data_source('Failover Group ID', 'data.failover_groups.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Failover Group', 'data.failover_groups.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Failover Groups Primary Server', 'data.failover_groups.primary_server', options={
            'is_optional': True
        }),
        TextDyField.data_source('Failover Groups Secondary Server', 'data.failover_groups.secondary_server', options={
            'is_optional': True
        }),
        TextDyField.data_source('Read/Write Failover Policy', 'data.failover_groups.failover_policy_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Grace Period (minutes)', 'data.failover_groups.grace_period_display', options={
            'is_optional': True
        }),
        # is_optional fields - Backups
        TextDyField.data_source('Backup Database', 'data.databases.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Earliest PITR Restore Point (UTC)', 'data.databases.earliest_restore_date', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Available LTR backups', 'data.databases.long_term_retention_backup_resource_id', options={
            'is_optional': True
        }),

        # is_optional fields - Active Directory Admin
        TextDyField.data_source('Active Directory Admin', 'data.azure_ad_admin_name', options={
            'is_optional': True
        }),

        # is_optional fields - Elastic Pools
        TextDyField.data_source('Elastic Pool Name', 'data.elastic_pools.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Elastic Pool Resource Group', 'data.elastic_pools.resource_group_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Per DB Settings', 'data.elastic_pools.per_db_settings_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Pricing Tier', 'data.elastic_pools.pricing_tier_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('# of DBs', 'data.elastic_pools.number_of_databases', options={
            'is_optional': True
        }),
        TextDyField.data_source('Elastic Pool Unit', 'data.elastic_pools.unit_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Elastic Pool Server Name', 'data.elastic_pools.server_name_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Elastic Pool Resource Configuration', 'data.elastic_pools.pricing_tier_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Elastic Pool Maximum Storage Size', 'data.elastic_pools.max_size_gb', options={
            'is_optional': True
        }),

        # is_optional fields - Deleted Databases
        TextDyField.data_source('Deleted Database', 'data.deleted_databases.database_name', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Deletion Time (UTC)', 'data.deleted_databases.deletion_date', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Deleted Databases Creation Time (UTC)', 'data.deleted_databases.creation_date', options={
            'is_optional': True
        }),
        TextDyField.data_source(' Deleted Databases Edition Time (UTC)', 'data.deleted_databases.edition', options={
            'is_optional': True
        }),

        # is_optional fields - Auditing
        TextDyField.data_source('Audit Log Destination', 'data.server_auditing_settings.storage_endpoint', options={
            'is_optional': True
        }),
        TextDyField.data_source('Audit Storage Account ID', 'data.server_auditing_settings.storage_account_subscription_id', options={
            'is_optional': True
        }),

        # is_optional fields - Firewalls and Vnets
        TextDyField.data_source('Minimum TLS Version', 'data.minimal_tls_version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Connection Policy', 'data.server_auditing_settings.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Allow Azure Services and Resources to Access this server',
                                'data.server_auditing_settings.is_azure_monitor_target_enabled', options={
            'is_optional': True
        }),

        # is_optional fields - Firewall Rules
        TextDyField.data_source('Firewall Rule Name', 'data.firewall_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Start IP', 'data.firewall_rules.start_ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall End IP', 'data.firewall_rules.end_ip_address', options={
            'is_optional': True
        }),

        # is_optional fields - Private Endpoint Connections
        TextDyField.data_source('Private Endpoint Connection ID', 'data.private_endpoint_connections.connection_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Endpoint State', 'data.private_endpoint_connections.status', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Endpoint Name', 'data.private_endpoint_connections.private_endpoint_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Request / Response Message', 'data.private_endpoint_connections.description', options={
            'is_optional': True
        }),

        # is_optional fields - Transparent Data Encryption
        TextDyField.data_source('Transparent Data Encryption', 'data.encryption_protectors.kind', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encryption Key', 'data.encryption_protectors.server_key_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encryption Key Type', 'data.encryption_protectors.server_key_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encryption Uri', 'data.encryption_protectors.uri', options={
            'is_optional': True
        }),

        # is_optional fields - Automatic Tuning
        TextDyField.data_source('Tuning Type', 'data.server_automatic_tuning.options.tuning_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Tuning Desired State', 'data.server_automatic_tuning.options.desired_state', options={
            'is_optional': True
        }),
        TextDyField.data_source('Tuning Current State', 'data.server_automatic_tuning.options.actual_state', options={
            'is_optional': True
        })
    ],


    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='name', data_type='string'),
        SearchField.set(name='Subscription ID', key='account', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Public Network Access', key='data.public_network_access', data_type='string'),

    ]

)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sql_server}),
]
