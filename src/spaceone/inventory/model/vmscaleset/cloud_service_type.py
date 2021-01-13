from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_vm_scale_set = CloudServiceTypeResource()
cst_vm_scale_set.name = 'VmScaleSet'
cst_vm_scale_set.group = 'Compute'
cst_vm_scale_set.service_code = 'Microsoft.Compute/virtualMachineScaleSets'
cst_vm_scale_set.labels = ['Compute', 'Storage']
cst_vm_scale_set.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-vm-scale-set.svg',
}

cst_vm_scale_set._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        # TextDyField.data_source('Status', 'data.'), (x)
        TextDyField.data_source('Instances', 'data.instance_count'),
        TextDyField.data_source('Azure Spot Eviction Policy', 'data.virtual_machine_profile.eviction_policy'),
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
    CloudServiceTypeResponse({'resource': cst_vm_scale_set}),
]
