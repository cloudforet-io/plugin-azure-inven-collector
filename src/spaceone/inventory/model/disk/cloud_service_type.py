from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_disk = CloudServiceTypeResource()
cst_disk.name = 'Disk'
cst_disk.provider = 'azure'
cst_disk.group = 'Compute'
cst_disk.labels = ['Compute', 'Storage']
cst_disk.is_major = True
cst_disk.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-disk.svg',
    'spaceone:display_name': 'Disk'
}

cst_disk._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Storage Account Type', 'data.sku.name'),
        SizeField.data_source('Size', 'data.disk_size_gb'),
        EnumDyField.data_source('Disk State', 'data.disk_state', default_state={
            'safe': ['ActiveSAS', 'ActiveUpload', 'Attached', 'Reserved'],
            'warning': ['ReadyToUpload'],
            'available': ['Unattached']
        }),
        TextDyField.data_source('Owner', 'data.managed_by'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Tier', key='data.tier', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Zone', key='data.zones', data_type='string'),
        SearchField.set(name='Storage Account Type', key='data.sku.name', data_type='string'),
        SearchField.set(name ='Disk Size', key = 'data.disk_size_gb', data_type='integer'),
        SearchField.set(name='Disk IOPS', key='data.disk_iops_read_write', data_type='integer'),
        SearchField.set(name='OS Type', key='data.os_type', data_type='string'),
        SearchField.set(name='Provisioning State', key='data.provisioning_state', data_type='string'),
        SearchField.set(name='Creation Time', key='data.time_created', data_type='datetime'),
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_disk})
]
