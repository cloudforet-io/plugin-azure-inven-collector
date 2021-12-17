import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))


cst_postgre_sql_server = CloudServiceTypeResource()
cst_postgre_sql_server.name = 'PostgreSQLServer'
cst_postgre_sql_server.group = 'Database'
cst_postgre_sql_server.service_code = 'Microsoft.DBforPostgreSQL/servers'
cst_postgre_sql_server.labels = ['Database']
cst_postgre_sql_server.is_primary = False
cst_postgre_sql_server.is_major = False
cst_postgre_sql_server.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-sql-postgresql-server.svg',
}

cst_postgre_sql_server._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Type', 'instance_type'),
        EnumDyField.data_source('Status', 'data.user_visible_state', default_state={
            'safe': ['Ready'],
            'warning': ['Disabled', 'Dropping', 'Inaccessible']
        }),
        TextDyField.data_source('Resource Group', 'data.resource_group', options={
            'is_optional': True
        }),
        TextDyField.data_source('Location', 'data.location', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subscription', 'data.subscription_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subscription ID', 'account', options={
            'is_optional': True
        }),

        # is_optional fields - Default
        TextDyField.data_source('Resource ID', 'data.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Server Name', 'data.fully_qualified_domain_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Admin Username', 'data.administrator_login', options={
            'is_optional': True
        }),
        TextDyField.data_source('PostgreSQL Version', 'data.version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Configuration Tier', 'instance_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Configuration Name', 'data.sku.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Configuration Capacity', 'data.sku.capacity', options={
            'is_optional': True
        }),
        TextDyField.data_source('SSL Enforce Status', 'data.ssl_enforcement', options={
            'is_optional': True
        }),
        TextDyField.data_source('Public Network Access', 'data.public_network_access', options={
            'is_optional': True
        }),
        TextDyField.data_source('SSL Enforcement', 'data.ssl_enforcement', options={
            'is_optional': True
        }),
        TextDyField.data_source('TLS Setting', 'data.minimal_tls_version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Rule Name', 'data.firewall_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Start IP', 'data.firewall_rules.start_ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('End IP', 'data.firewall_rules.end_ip_address', options={
            'is_optional': True
        }),

        # VNet Rules
        TextDyField.data_source('Rule Name', 'data.virtual_network_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Virtual Network', 'data.virtual_network_rules.virtual_network_name_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet', 'data.virtual_network_rules.subnet_name', options={
            'is_optional': True
        }),

        # Replicas
        TextDyField.data_source('Replicas Name', 'data.replicas.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Location', 'data.replicas.location', options={
            'is_optional': True
        }),
        TextDyField.data_source('Master Server Name', 'data.replicas.master_server_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Active Directory Name', 'data.server_administrators.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Login', 'data.server_administrators.login', options={
            'is_optional': True
        }),
        TextDyField.data_source('SID', 'data.server_administrators.sid', options={
            'is_optional': True
        }),
        TextDyField.data_source('Tenant ID', 'data.server_administrators.tenant_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Compute Generation', 'data.sku.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Compute Tier', 'instance_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('vCore', 'data.sku.capacity', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Retention Period (Days)', 'data.storage_profile.backup_retention_days', options={
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
    CloudServiceTypeResponse({'resource': cst_postgre_sql_server}),
]
