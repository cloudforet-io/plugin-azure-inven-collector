import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

public_ip_address_count_per_location_conf = os.path.join(current_dir, 'widget/public_ip_address_count_by_location.yaml')
public_ip_address_count_per_subscription_conf = os.path.join(current_dir,
                                                             'widget/public_ip_address_count_by_subscription.yaml')


cst_public_ip_address = CloudServiceTypeResource()
cst_public_ip_address.name = 'IPAddress'
cst_public_ip_address.group = 'PublicIPAddresses'
cst_public_ip_address.service_code = 'Microsoft.Network/publicIPAddresses'
cst_public_ip_address.labels = ['Networking']
cst_public_ip_address.is_major = True
cst_public_ip_address.is_primary = True
cst_public_ip_address.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-public-ip-address.svg',
}

cst_public_ip_address._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
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
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='SKU', key='instance_type'),
        SearchField.set(name='Tier', key='data.sku.tier'),
        SearchField.set(name='IP Address', key='data.ip_address'),
        SearchField.set(name='DNS Name', key='data.dns_settings.fqdn'),
        SearchField.set(name='IP Address Assignment', key='data.public_ip_allocation_method'),
        SearchField.set(name='Idle Timeout(Minutes)', key='data.idle_timeout_in_minutes', data_type='integer'),
        SearchField.set(name='DNS Name Label(Optional)', key='data.dns_settings.domain_name_label'),
        SearchField.set(name='Associated To', key='data.associated_to')
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(public_ip_address_count_per_location_conf)),
        ChartWidget.set(**get_data_from_yaml(public_ip_address_count_per_subscription_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_public_ip_address}),
]
