from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_storage_account = CloudServiceTypeResource()
cst_storage_account.name = 'StorageAccount'
cst_storage_account.group = 'Storage'
cst_storage_account.service_code = 'Microsoft.Storage/storageAccounts'
cst_storage_account.labels = ['Storage']
cst_storage_account.is_major = False
cst_storage_account.is_primary = False
cst_storage_account.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-service-accounts.svg',
}

cst_storage_account._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Type', 'data.type'),
        TextDyField.data_source('Kind', 'data.type'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('State of Primary', 'data.status_of_primary', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Tier', 'data.sku.tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Tier', 'data.access_tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Replication', 'data.sku.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Account Kind', 'data.kind', options={
            'is_optional': True
        }),
        TextDyField.data_source('Provisioning State', 'data.provisioning_state', options={
            'is_optional': True
        }),
        TextDyField.data_source('Is Public', 'data.allow_blob_public_access', options={
            'is_optional': True
        }),
        TextDyField.data_source('Virtual Network', 'data.network_rule_set.virtual_networks', options={
            'is_optional': True
        }),
        ListDyField.data_source('Firewall Address Range', 'data.network_rule_set.firewall_address_range', options={
            'is_optional': True
        }),
        ListDyField.data_source('Resource Instances', 'data.network_rule_set.resource_access_rules_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Exceptions', 'data.network_rule_set.bypass', options={
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
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Name', key='data.type', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string')
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_storage_account}),
]
