import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

storage_account_count_per_location_conf = os.path.join(current_dir, 'widget/storage_account_count_per_location.yaml')
storage_account_count_per_subscription_conf = os.path.join(current_dir, 'widget/storage_account_count_per_subscription.yaml')

cst_storage_account = CloudServiceTypeResource()
cst_storage_account.name = 'StorageAccount'
cst_storage_account.group = 'Storage'
cst_storage_account.service_code = 'Microsoft.Storage/storageAccounts'
cst_storage_account.labels = ['Storage']
cst_storage_account.is_major = False
cst_storage_account.is_primary = True
cst_storage_account.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-service-accounts.svg',
}

cst_storage_account._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Type', 'data.type'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('State of Primary', 'data.status_of_primary', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Tier', 'instance_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Tier', 'data.access_tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Replication', 'data.sku.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Kind of Account', 'data.kind', options={
            'is_optional': True
        }),
        TextDyField.data_source('Provisioning State', 'data.provisioning_state', options={
            'is_optional': True
        }),
        TextDyField.data_source('Is Public', 'data.allow_blob_public_access', options={
            'is_optional': True
        }),
        TextDyField.data_source('Virtual Network', 'data.network_acls.virtual_networks', options={
            'is_optional': True
        }),
        ListDyField.data_source('Firewall Address Range', 'data.network_acls.firewall_address_range', options={
            'is_optional': True
        }),
        ListDyField.data_source('Resource Instances', 'data.network_acls.resource_access_rules_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Exceptions', 'data.network_acls.bypass', options={
            'is_optional': True
        }),
        TextDyField.data_source('Routing Preference', 'data.routing_preference_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Publish Microsoft Endpoints', 'data.routing_preference.publish_microsoft_endpoints', options={
            'is_optional': True
        }),
        TextDyField.data_source('Publish Internet Endpoints', 'data.routing_preference.publish_internet_endpoints', options={
            'is_optional': True
        }),
        TextDyField.data_source('Blob', 'data.primary_endpoints.blob', options={
            'is_optional': True
        }),
        TextDyField.data_source('Queue', 'data.primary_endpoints.queue', options={
            'is_optional': True
        }),
        TextDyField.data_source('Table', 'data.primary_endpoints.table', options={
            'is_optional': True
        }),
        TextDyField.data_source('File', 'data.primary_endpoints.file', options={
            'is_optional': True
        }),
        TextDyField.data_source('Web', 'data.primary_endpoints.web', options={
            'is_optional': True
        }),
        TextDyField.data_source('DFS', 'data.primary_endpoints.dfs', options={
            'is_optional': True
        }),
        TextDyField.data_source('Microsoft Endpoints', 'data.routing_preference.publish_microsoft_endpoints', options={
            'is_optional': True
        }),
        TextDyField.data_source('Internet Endpoints', 'data.routing_preference.publish_internet_endpoints', options={
            'is_optional': True
        }),
        TextDyField.data_source('Container Name', 'data.container_item.name', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Container Last Modified', 'data.container_item.last_modified_time', options={
            'is_optional': True
        }),
        TextDyField.data_source('Container Public Access Level', 'data.container_item.public_access', options={
            'is_optional': True
        }),
        TextDyField.data_source('Container Lease State', 'data.container_item.lease_state', options={
            'is_optional': True
        }),
        TextDyField.data_source('Primary Location', 'data.primary_location', options={
            'is_optional': True
        }),
        TextDyField.data_source('Secondary Location', 'data.secondary_location', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Type', key='data.type'),
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='State of Primary', key='data.status_of_primary'),
        SearchField.set(name='Performance Tier', key='instance_type'),
        SearchField.set(name='Access Tier', key='data.access_tier'),
        SearchField.set(name='Replication', key='data.sku.name'),
        SearchField.set(name='Kind of Account', key='data.kind'),
        SearchField.set(name='Provisioning State', key='data.provisioning_state'),
        SearchField.set(name='Is Public', key='data.allow_blob_public_access', data_type='boolean'),
        SearchField.set(name='Virtual Network', key='data.network_acls.virtual_networks'),
        SearchField.set(name='Firewall Address Range', key='data.network_acls.firewall_address_range'),
        SearchField.set(name='Resource Instances', key='data.network_acls.resource_access_rules_display'),
        SearchField.set(name='Exceptions', key='data.network_acls.bypass'),
        SearchField.set(name='Routing Preference', key='data.routing_preference_display'),
        SearchField.set(name='Publish Microsoft Endpoints', key='data.routing_preference.publish_microsoft_endpoints'),
        SearchField.set(name='Publish Internet Endpoints', key='data.routing_preference.publish_internet_endpoints'),
        SearchField.set(name='Blob', key='data.primary_endpoints.blob'),
        SearchField.set(name='Queue', key='data.primary_endpoints.queue'),
        SearchField.set(name='Table', key='data.primary_endpoints.table'),
        SearchField.set(name='File', key='data.primary_endpoints.file'),
        SearchField.set(name='Web', key='data.primary_endpoints.web'),
        SearchField.set(name='DFS', key='data.primary_endpoints.dfs'),
        SearchField.set(name='Microsoft Endpoints', key='data.routing_preference.publish_microsoft_endpoints'),
        SearchField.set(name='Internet Endpoints', key='data.routing_preference.publish_internet_endpoints'),
        SearchField.set(name='Container Name', key='data.container_item.name'),
        SearchField.set(name='Container Last Modified', key='data.container_item.last_modified_time', data_type='datetime'),
        SearchField.set(name='Container Public Access Level', key='data.container_item.public_access'),
        SearchField.set(name='Container Lease State', key='data.container_item.lease_state'),
        SearchField.set(name='Primary Location', key='data.primary_location'),
        SearchField.set(name='Secondary Location', key='data.secondary_location'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(storage_account_count_per_location_conf)),
        ChartWidget.set(**get_data_from_yaml(storage_account_count_per_subscription_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_storage_account}),
]
