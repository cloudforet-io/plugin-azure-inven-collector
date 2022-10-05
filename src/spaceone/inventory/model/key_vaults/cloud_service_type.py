import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

key_vaults_count_by_account_conf = os.path.join(current_dir, 'widget/key_vaults_count_by_account.yaml')
key_vaults_count_by_region_conf = os.path.join(current_dir, 'widget/key_vaults_count_by_region.yaml')
key_vaults_count_per_subscription_conf = os.path.join(current_dir, 'widget/key_vaults_count_by_subscription.yaml')
key_vaults_total_count_conf = os.path.join(current_dir, 'widget/key_vaults_total_count.yaml.yaml')

cst_key_vaults = CloudServiceTypeResource()
cst_key_vaults.name = 'Instance'
cst_key_vaults.group = 'KeyVaults'
cst_key_vaults.service_code = 'Microsoft.KeyVault/vaults'
cst_key_vaults.labels = ['Security']
cst_key_vaults.is_major = True
cst_key_vaults.is_primary = True
cst_key_vaults.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-key-vault.svg',
}

cst_key_vaults._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Type', 'instance_type'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Subscription ID', 'account'),

        # is_optional fields - Public IP Addresses
        TextDyField.data_source('Public IP Address', 'data.public_ip_addresses.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Vault URI', 'data.properties.vault_uri', options={
            'is_optional': True
        }),
        TextDyField.data_source('SKU (Pricing Tier)', 'data.sku.name', options={
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

        TextDyField.data_source('Private Connection Name', 'data.properties.private_endpoint_connections.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Connection State', 'data.properties.private_endpoint_connections.private_link_service_connection_state.status', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Endpoint ID', 'data.properties.private_endpoint_connections.private_endpoint.id', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Type', key='instance_type'),
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Public IP Address', key='data.public_ip_addresses.name'),
        SearchField.set(name='Vault URI', key='data.properties.vault_uri'),
        SearchField.set(name='SKU (Pricing Tier)', key='data.sku.name'),
        SearchField.set(name='Directory ID', key='data.properties.tenant_id'),
        SearchField.set(name='Soft-delete', key='data.properties.enable_soft_delete'),
        SearchField.set(name='Purge Protection', key='data.properties.enable_purge_protection'),
        SearchField.set(name='Key Name', key='data.keys.name'),
        SearchField.set(name='Key Type', key='data.keys.type'),
        SearchField.set(name='Key Location', key='data.keys.location'),
        SearchField.set(name='Key Status', key='data.keys.attributes.enabled'),
        SearchField.set(name='Key Expiration Date', key='data.keys.attributes.expires'),
        SearchField.set(name='Key Creation Date', key='data.keys.attributes.created'),
        SearchField.set(name='Key URI', key='data.keys.key_uri'),
        SearchField.set(name='Enable for Azure VM Deployment',
                        key='data.properties.enabled_for_deployment',
                        data_type='boolean'),
        SearchField.set(name='Enable for Disk Encryption',
                        key='data.properties.enabled_for_disk_encryption',
                        data_type='boolean'),
        SearchField.set(name='Enable for Template Deployment',
                        key='data.properties.enabled_for_template_deployment',
                        data_type='boolean'),
        SearchField.set(name='Enable RBAC Authorization',
                        key='data.properties.enable_rbac_authorization',
                        data_type='boolean'),
        SearchField.set(name='Private Endpoint Connection Name',
                        key='data.properties.private_endpoint_connections.name'),
        SearchField.set(name='Private Endpoint Connection State',
                        key='data.properties.private_endpoint_connections.private_link_service_connection_state.status'),
        SearchField.set(name='Private Endpoint ID',
                        key='data.properties.private_endpoint_connections.private_endpoint.id'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(key_vaults_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(key_vaults_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(key_vaults_count_per_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(key_vaults_total_count_conf)),

    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_key_vaults}),
]
