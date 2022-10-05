import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

mysql_servers_count_by_account_conf = os.path.join(current_dir, 'widget/mysql_servers_count_by_account.yaml')
mysql_servers_count_by_region_conf = os.path.join(current_dir, 'widget/mysql_servers_count_by_region.yaml')
mysql_servers_count_by_subscription_conf = os.path.join(current_dir, 'widget/mysql_servers_count_by_subscription.yaml')
mysql_servers_count_by_tier_conf = os.path.join(current_dir, 'widget/mysql_servers_count_by_tier.yaml')
mysql_servers_total_count_conf = os.path.join(current_dir, 'widget/mysql_servers_total_count.yaml')


cst_mysql_servers = CloudServiceTypeResource()
cst_mysql_servers.name = 'Server'
cst_mysql_servers.group = 'MySQLServers'
cst_mysql_servers.service_code = 'Microsoft.DBforMySQL/servers'
cst_mysql_servers.labels = ['Database']
cst_mysql_servers.is_major = True
cst_mysql_servers.is_primary = True
cst_mysql_servers.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-mysql-servers.svg',
}

cst_mysql_servers._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Type', 'instance_type'),
        EnumDyField.data_source('Status', 'data.user_visible_state', default_state={
            'safe': ['Ready'],
            'warning': ['Dropping'],
            'disable': ['Disabled', 'Inaccessible']
        }),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Server Admin Login Name', 'data.administrator_login', options={
            'is_optional': True
        }),
        TextDyField.data_source('MySQL Version', 'data.version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Configuration (Tier)', 'instance_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Configuration (Name)', 'data.sku.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('SSL Enforce Status', 'data.ssl_enforcement', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Rule Name', 'data.firewall_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Rule Start IP', 'data.firewall_rules.start_ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Rule End IP', 'data.firewall_rules.end_ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Allow Access To Azure Services', 'data.allow_azure_services_access', options={
            'is_optional': True
        }),
        TextDyField.data_source('Enforce SSL Connection', 'data.ssl_enforcement', options={
            'is_optional': True
        }),
        TextDyField.data_source('Minimum TLS Version', 'data.minimal_tls_version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Compute Generation', 'data.sku.family', options={
            'is_optional': True
        }),
        TextDyField.data_source('vCore', 'data.sku.capacity', options={
            'is_optional': True
        }),
        TextDyField.data_source('Storage', 'data.storage_profile.storage_gb', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Retention Period', 'data.storage_profile.backup_retention_days', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Type', key='instance_type'),
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Server Admin Login Name', key='data.administrator_login'),
        SearchField.set(name='MySQL Version', key='data.version'),
        SearchField.set(name='Performance Configuration (Tier)', key='instance_type'),
        SearchField.set(name='Performance Configuration (Name)', key='data.sku.name'),
        SearchField.set(name='SSL Enforce Status', key='data.ssl_enforcement'),
        SearchField.set(name='Firewall Rule Name', key='data.firewall_rules.name'),
        SearchField.set(name='Firewall Rule Start IP', key='data.firewall_rules.start_ip_address'),
        SearchField.set(name='Firewall Rule End IP', key='data.firewall_rules.end_ip_address'),
        SearchField.set(name='Allow Access To Azure Services', key='data.allow_azure_services_access'),
        SearchField.set(name='Enforce SSL Connection', key='data.ssl_enforcement'),
        SearchField.set(name='Minimum TLS Version', key='data.minimal_tls_version'),
        SearchField.set(name='Compute Generation', key='data.sku.family'),
        SearchField.set(name='vCore', key='data.sku.capacity', data_type='integer'),
        SearchField.set(name='Storage', key='data.storage_profile.storage_gb', data_type='integer'),
        SearchField.set(name='Backup Retention Period', key='data.storage_profile.backup_retention_days'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(mysql_servers_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(mysql_servers_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(mysql_servers_count_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(mysql_servers_count_by_tier_conf)),
        ChartWidget.set(**get_data_from_yaml(mysql_servers_total_count_conf)),

    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_mysql_servers}),
]
