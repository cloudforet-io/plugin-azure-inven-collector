from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_virtual_network = CloudServiceTypeResource()
cst_virtual_network.name = 'VirtualNetwork'
cst_virtual_network.group = 'Network'
cst_virtual_network.service_code = 'Microsoft.Network/virtualNetworks'
cst_virtual_network.labels = ['Network']
cst_virtual_network.is_major = True
cst_virtual_network.is_primary = True
cst_virtual_network.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-virtual-networks.svg',
}

cst_virtual_network._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name')
    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_virtual_network}),
]
