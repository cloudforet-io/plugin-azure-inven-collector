from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_application_gateway = CloudServiceTypeResource()
cst_application_gateway.name = 'ApplicationGateway'
cst_application_gateway.group = 'Network'
cst_application_gateway.service_code = 'Microsoft.Network/applicationGateways'
cst_application_gateway.labels = ['Network']
cst_application_gateway.is_major = False
cst_application_gateway.is_primary = False
cst_application_gateway.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-application-gateways.svg',
}

cst_application_gateway._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Public IP Address', 'data.public_ip_address.ip_address'),
        TextDyField.data_source('Private IP Address', 'data.private_ip_address'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        # is_optional fields
        TextDyField.data_source('Capacity ', 'data.sku.tier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Minimum Instance Count', 'data.autoscale_configuration.min_capacity', options= {
            'is_optional': True
        }),
        TextDyField.data_source('Maximum Instance Count', 'data.autoscale_configuration.max_capacity', options= {
            'is_optional': True
        }),
        TextDyField.data_source('Enable HTTP2', 'data.enable_http2',  options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Mode', 'data.web_application_firewall_configuration.firewall_mode', options={
            'is_optional': True
        }),
        TextDyField.data_source('Max Request Body Size(KB)', 'data.web_application_firewall_configuration.max_request_body_size_in_kb', options={
            'is_optional': True
        }),
        TextDyField.data_source('File Upload Limit(MB)', 'data.web_application_firewall_configuration.file_upload_limit_in_mb', options={
            'is_optional': True
        }),


    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Public IP Address', key='data.public_ip_address.ip_address', data_type='string'),
        SearchField.set(name='Private IP Address', key='data.private_ip_address', data_type='string')
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_application_gateway}),
]
