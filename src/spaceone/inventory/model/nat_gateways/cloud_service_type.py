import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

nat_gateways_count_by_account_conf = os.path.join(current_dir, 'widget/nat_gateways_count_by_account.yaml')
nat_gateways_count_by_region_conf = os.path.join(current_dir, 'widget/nat_gateways_count_by_region.yaml')
nat_gateways_count_by_subscription_conf = os.path.join(current_dir, 'widget/nat_gateways_count_by_subscription.yaml')
nat_gateways_total_count_conf = os.path.join(current_dir, 'widget/nat_gateways_total_count.yaml')

cst_nat_gateways = CloudServiceTypeResource()
cst_nat_gateways.name = 'Instance'
cst_nat_gateways.group = 'NATGateways'
cst_nat_gateways.service_code = 'Microsoft.Network/natGateways'
cst_nat_gateways.labels = ['Networking']
cst_nat_gateways.is_major = True
cst_nat_gateways.is_primary = True
cst_nat_gateways.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-nat.svg',
}

cst_nat_gateways._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Subnets (count)', 'data.subnets_count'),
        TextDyField.data_source('Public IP Addresses (count)', 'data.public_ip_prefixes_count'),
        TextDyField.data_source('Public IP Prefixes (count)', 'data.public_ip_prefixes_count'),
        # is_optional fields - Public IP Addresses
        TextDyField.data_source('Public IP Name', 'data.public_ip_addresses.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Public IP Address', 'data.public_ip_addresses.ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Public DNS Name', 'data.public_ip_addresses.dns_settings.domain_name_label', options={
            'is_optional': True
        }),
        # is_optional fields - Public IP Prefixes
        TextDyField.data_source('Public IP Prefix Name', 'data.public_ip_prefixes.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Public IP Prefix', 'data.public_ip_prefixes.ip_prefix', options={
            'is_optional': True
        }),
        # is_optional fields - Subnets
        TextDyField.data_source('Subnet Name', 'data.subnets.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Addresses', 'data.subnets.address_prefixes', options={
            'is_optional': True
        }),
        TextDyField.data_source('Virtual Network', 'data.subnets.virtual_network', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Public IP Name', key='data.public_ip_addresses.name'),
        SearchField.set(name='Public IP Address', key='data.public_ip_addresses.ip_address'),
        SearchField.set(name='Public DNS Name', key='data.public_ip_addresses.dns_settings.domain_name_label'),
        SearchField.set(name='Public IP Prefix Name', key='data.public_ip_prefixes.name'),
        SearchField.set(name='Public IP Prefix', key='data.public_ip_prefixes.ip_prefix'),
        SearchField.set(name='Subnet Name', key='data.subnets.name'),
        SearchField.set(name='Subnet Addresses', key='data.subnets.address_prefixes'),
        SearchField.set(name='Virtual Network', key='data.subnets.virtual_network')
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(nat_gateways_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(nat_gateways_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(nat_gateways_count_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(nat_gateways_total_count_conf))
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_nat_gateways}),
]
