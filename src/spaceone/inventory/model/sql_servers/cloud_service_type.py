import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

sql_databases_count_by_server_conf = os.path.join(current_dir, 'widget/sql_databases_count_by_server.yaml')
sql_databases_count_by_subscription_conf = os.path.join(current_dir, 'widget/sql_databases_count_per_subscription.yaml')
sql_databases_count_by_tier_conf = os.path.join(current_dir, 'widget/sql_databases_count_by_tier.yaml')
sql_servers_count_by_account_conf = os.path.join(current_dir, 'widget/sql_servers_count_by_account.yaml')
sql_servers_count_by_region_conf = os.path.join(current_dir, 'widget/sql_servers_count_by_region.yaml')
sql_servers_count_by_subscription_conf = os.path.join(current_dir, 'widget/sql_servers_count_per_subscription.yaml')
sql_servers_failover_count_by_region_conf = os.path.join(current_dir, 'widget/sql_servers_failover_count_by_region.yaml')
sql_servers_failover_count_by_server_conf = os.path.join(current_dir, 'widget/sql_servers_failover_count_by_server.yaml')
sql_servers_total_count_conf = os.path.join(current_dir, 'widget/sql_servers_total_count.yaml')


cst_sql_servers = CloudServiceTypeResource()
cst_sql_servers.name = 'Server'
cst_sql_servers.group = 'SQLServers'
cst_sql_servers.service_code = 'Microsoft.Sql/servers'
cst_sql_servers.labels = ['Database']
cst_sql_servers.is_primary = True
cst_sql_servers.is_major = True
cst_sql_servers.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-sql-servers.svg',
}

cst_sql_servers._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['Ready'],
            'warning': ['Disabled']
        }),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),

        # is_optional fields - Default
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
        TextDyField.data_source('Failover Group Name', 'data.failover_groups.name', options={
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
        TextDyField.data_source('Deleted Databases Edition Time (UTC)', 'data.deleted_databases.edition', options={
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
        TextDyField.data_source('Encryption URI', 'data.encryption_protectors.uri', options={
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
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Server Admin', key='data.administrator_login'),
        SearchField.set(name='Active Directory Admin', key='data.azure_ad_admin_name'),
        SearchField.set(name='Server Name', key='data.fully_qualified_domain_name'),
        SearchField.set(name='Failover Group ID', key='data.failover_groups.id'),
        SearchField.set(name='Failover Group Name', key='data.failover_groups.name'),
        SearchField.set(name='Failover Groups Primary Server', key='data.failover_groups.primary_server'),
        SearchField.set(name='Failover Groups Secondary Server', key='data.failover_groups.secondary_server'),
        SearchField.set(name='Read/Write Failover Policy', key='data.failover_groups.failover_policy_display'),
        SearchField.set(name='Grace Period (minutes)', key='data.failover_groups.grace_period_display', data_type='integer'),
        SearchField.set(name='Backup Database', key='data.databases.name'),
        SearchField.set(name='Backup Earliest PITR Restore Point (UTC)', key='data.databases.earliest_restore_date', data_type='datetime'),
        SearchField.set(name='Backup Available LTR backups', key='data.databases.long_term_retention_backup_resource_id'),
        SearchField.set(name='Active Directory Admin', key='data.azure_ad_admin_name'),
        SearchField.set(name='Elastic Pool Name', key='data.elastic_pools.name'),
        SearchField.set(name='Elastic Pool Resource Group', key='data.elastic_pools.resource_group_display'),
        SearchField.set(name='Per DB Settings', key='data.elastic_pools.per_db_settings_display'),
        SearchField.set(name='Pricing Tier', key='data.elastic_pools.pricing_tier_display'),
        SearchField.set(name='Number of DBs', key='data.elastic_pools.number_of_databases', data_type='integer'),
        SearchField.set(name='Elastic Pool Unit', key='data.elastic_pools.unit_display'),
        SearchField.set(name='Elastic Pool Server Name', key='data.elastic_pools.server_name_display'),
        SearchField.set(name='Elastic Pool Resource Configuration', key='data.elastic_pools.pricing_tier_display'),
        SearchField.set(name='Elastic Pool Maximum Storage Size', key='data.elastic_pools.max_size_gb'),
        SearchField.set(name='Deleted Database', key='data.deleted_databases.database_name'),
        SearchField.set(name='Deletion Time (UTC)', key='data.deleted_databases.deletion_date', data_type='datetime'),
        SearchField.set(name='Deleted Databases Creation Time (UTC)', key='data.deleted_databases.creation_date', data_type='datetime'),
        SearchField.set(name='Deleted Databases Edition Time (UTC)', key='data.deleted_databases.edition', data_type='datetime'),
        SearchField.set(name='Audit Log Destination', key='data.server_auditing_settings.storage_endpoint'),
        SearchField.set(name='Audit Storage Account ID', key='data.server_auditing_settings.storage_account_subscription_id'),
        SearchField.set(name='Minimum TLS Version', key='data.minimal_tls_version'),
        SearchField.set(name='Connection Policy', key='data.server_auditing_settings.name'),
        SearchField.set(name='Allow Azure Services and Resources to Access this server', key='data.server_auditing_settings.is_azure_monitor_target_enabled'),
        SearchField.set(name='Firewall Rule Name', key='data.firewall_rules.name'),
        SearchField.set(name='Firewall Start IP', key='data.firewall_rules.start_ip_address'),
        SearchField.set(name='Firewall End IP', key='data.firewall_rules.end_ip_address'),
        SearchField.set(name='Private Endpoint Connection ID', key='data.private_endpoint_connections.connection_id'),
        SearchField.set(name='Private Endpoint State', key='data.private_endpoint_connections.status'),
        SearchField.set(name='Private Endpoint Name', key='data.private_endpoint_connections.private_endpoint_name'),
        SearchField.set(name='Request / Response Message', key='data.private_endpoint_connections.description'),
        SearchField.set(name='Transparent Data Encryption', key='data.encryption_protectors.kind'),
        SearchField.set(name='Encryption Key', key='data.encryption_protectors.server_key_name'),
        SearchField.set(name='Encryption Key Type', key='data.encryption_protectors.server_key_type'),
        SearchField.set(name='Encryption URI', key='data.encryption_protectors.uri'),
        SearchField.set(name='Tuning Type', key='data.server_automatic_tuning.options.tuning_type'),
        SearchField.set(name='Tuning Desired State', key='data.server_automatic_tuning.options.desired_state'),
        SearchField.set(name='Tuning Current State', key='data.server_automatic_tuning.options.actual_state'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(sql_servers_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_servers_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_servers_count_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_servers_failover_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_servers_failover_count_by_server_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_databases_count_by_server_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_databases_count_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_databases_count_by_tier_conf)),
        ChartWidget.set(**get_data_from_yaml(sql_servers_total_count_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sql_servers}),
]
