import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))


cst_public_ip_address = CloudServiceTypeResource()
cst_public_ip_address.name = 'PublicIPAddress'
cst_public_ip_address.group = 'Network'
cst_public_ip_address.service_code = 'Microsoft.Network/publicIPAddresses'
cst_public_ip_address.labels = ['Network']
cst_public_ip_address.is_major = False
cst_public_ip_address.is_primary = False
cst_public_ip_address.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-public-ip-address.svg',
}

cst_public_ip_address._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        TextDyField.data_source('Associated To', 'data.associated_to'),

        # is_optional fields - Default
        TextDyField.data_source('Subscription ID', 'account', options={
            'is_optional': True
        }),
        TextDyField.data_source('SKU', 'instance_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Tier', 'data.sku.tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('IP Address', 'data.ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('DNS Name', 'data.dns_settings.fqdn', options={
            'is_optional': True
        }),

        # is_optional fields - Configuration
        TextDyField.data_source('IP Address Assignment', 'data.public_ip_allocation_method', options={
            'is_optional': True
        }),
        TextDyField.data_source('Idle Timeout(Minutes)', 'data.idle_timeout_in_minutes', options={
            'is_optional': True
        }),
        TextDyField.data_source('DNS Name Label(Optional)', 'data.dns_settings.domain_name_label', options={
            'is_optional': True
        })

    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='name', data_type='string'),
        SearchField.set(name='Subscription ID', key='account', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string')
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_public_ip_address}),
]
