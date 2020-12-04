from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_disk = CloudServiceTypeResource()
cst_disk.name = 'Disk'
cst_disk.provider = 'azure'
cst_disk.group = 'Compute'
cst_disk.labels = ['Compute', 'Storage']
cst_disk.is_major = True
cst_disk.tags = {
    # TODO: Fill out to display Icon
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-disk.svg',
    'spaceone:display_name': 'Disk'
}

cst_disk._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        # TODO: Fill out to Dynamic Table
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Storage account type', 'data.type'),
        TextDyField.data_source('Size(GiB)', 'data.diskSizeGB'),
        TextDyField.data_source('State', 'data.diskState'),
        TextDyField.data_source('Owner', 'data.managedBy'),
        TextDyField.data_source('Resource Group', 'data.resourceGroup'),
        TextDyField.data_source('Location', 'data.location')

        #TextDyField.data_source('Subscription', 'data.')

    ],
    search=[
        # TODO: Fill out to Search Meta
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resourceGroup', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string')
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_disk}),
]
