from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_snapshot = CloudServiceTypeResource()
cst_snapshot.name = 'Snapshot'
cst_snapshot.provider = 'azure'
cst_snapshot.group = 'Compute'
cst_snapshot.labels = ['Compute', 'Storage']
cst_snapshot.is_major = False
cst_snapshot.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-disk-snapshot.svg',
    'spaceone:display_name': 'Snapshots'
}

cst_snapshot._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Source disk', 'data.source_disk_name'),
        TextDyField.data_source('Snapshot type', 'data.incremental_display'),
        DateTimeDyField.data_source('Time created', 'data.time_created'),
        TextDyField.data_source('Source disk size(GiB)', 'data.disk_size_gb'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Storage Account Type', key='data.sku.name', data_type='string'),
        SearchField.set(name='Snapshot Type', key='data.incremental_display', data_type='string'),
        SearchField.set(name='Disk Size(GiB)', key='data.disk_size_gb', data_type='integer'),
        SearchField.set(name='Encryption', key='data.encryption.type_display', data_type='string'),
        SearchField.set(name='Network Access Policy', key='data.network_access_policy', data_type='string'),
        SearchField.set(name='Provisioning State', key='data.provisioning_state', data_type='string'),
        SearchField.set(name='Creation Time', key='data.time_created', data_type='datetime'),
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_snapshot}),
]
