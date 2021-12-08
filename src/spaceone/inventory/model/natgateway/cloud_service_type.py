from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_nat_gateway = CloudServiceTypeResource()
cst_nat_gateway.name = 'NATGateway'
cst_nat_gateway.group = 'Network'
cst_nat_gateway.service_code = 'Microsoft.Network/natGateways'
cst_nat_gateway.labels = ['Network']
cst_nat_gateway.is_major = False
cst_nat_gateway.is_primary = False
cst_nat_gateway.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-nat.svg',
}

cst_nat_gateway._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Resource ID', 'data.id'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Subnets', 'data.subnets_count'),
        TextDyField.data_source('Public IP Addresses', 'data.public_ip_prefixes_count'),
        TextDyField.data_source('Public IP Prefixes', 'data.public_ip_prefixes_count'),

        # is_optional fields - Public IP Addresses
        TextDyField.data_source('Name', 'data.public_ip_addresses.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('IP Address', 'data.public_ip_addresses.ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('DNS Name', 'data.public_ip_addresses.dns_settings.domain_name_label', options={
            'is_optional': True
        }),

        # is_optional fields - Public IP Prefixes
        TextDyField.data_source('Name', 'data.public_ip_prefixes.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('IP Prefix', 'data.public_ip_prefixes.ip_prefix', options={
            'is_optional': True
        }),

        # is_optional fields - Subnets
        TextDyField.data_source('Subnet Name', 'data.subnets.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Address ', 'data.subnets.address_prefix', options={
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
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='name', data_type='string'),
        SearchField.set(name='Subscription ID', key='account', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string')
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_nat_gateway}),
]
