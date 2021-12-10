from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_key_vault = CloudServiceTypeResource()
cst_key_vault.name = 'KeyVault'
cst_key_vault.group = 'KeyVault'
cst_key_vault.service_code = 'Microsoft.KeyVault/vaults'
cst_key_vault.labels = ['KeyVault']
cst_key_vault.is_major = False
cst_key_vault.is_primary = False
cst_key_vault.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-key-vault.svg',
}

cst_key_vault._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Type', 'instance_type'),
        TextDyField.data_source('Resource ID', 'data.id'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'account'),

        # is_optional fields - Public IP Addresses
        TextDyField.data_source('Name', 'data.public_ip_addresses.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Vault URI', 'data.properties.vault_uri', options={
            'is_optional': True
        }),
        TextDyField.data_source('Sku (Pricing Tier)', 'data.sku.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Directory ID', 'data.properties.tenant_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Soft-delete', 'data.properties.enable_soft_delete', options={
            'is_optional': True
        }),
        TextDyField.data_source('Purge Protection', 'data.properties.enable_purge_protection', options={
            'is_optional': True
        }),

        TextDyField.data_source('Key Name', 'data.keys.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key Type', 'data.keys.type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key Location', 'data.keys.location', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key Status', 'data.keys.attributes.enabled', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Key Expiration Date', 'data.keys.attributes.expires', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Key Creation Date', 'data.keys.attributes.created', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key URI', 'data.keys.key_uri', options={
            'is_optional': True
        }),

        TextDyField.data_source('Enable for Azure VM Deployment', 'data.properties.enabled_for_deployment', options={
            'is_optional': True
        }),
        TextDyField.data_source('Enable for Disk Encryption', 'data.properties.enabled_for_disk_encryption', options={
            'is_optional': True
        }),
        TextDyField.data_source('Enable for Template Deployment', 'data.properties.enabled_for_template_deployment', options={
            'is_optional': True
        }),
        TextDyField.data_source('Enable RBAC Authorization', 'data.properties.enable_rbac_authorization', options={
            'is_optional': True
        }),

        TextDyField.data_source('Connection Name', 'data.properties.private_endpoint_connections.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Connection State', 'data.properties.private_endpoint_connections.private_link_service_connection_state.status', options={
            'is_optional': True
        }),

        TextDyField.data_source('Private Endpoint', 'data.properties.private_endpoint_connections.private_endpoint.id', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='name', data_type='string'),
        SearchField.set(name='Type', key='instance_type', data_type='string'),
        SearchField.set(name='Subscription ID', key='account', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string')
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_key_vault}),
]
