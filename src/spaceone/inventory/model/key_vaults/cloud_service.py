from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.keyvault.data import KeyVault

'''
KEY_VAULT
'''
# TAB - Default
key_vault_info_meta = ItemDynamicLayout.set_fields('Key Vault', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
    TextDyField.data_source('Vault URI', 'data.properties.vault_uri'),
    TextDyField.data_source('Sku (Pricing Tier)', 'instance_type'),
    TextDyField.data_source('Directory ID', 'data.properties.tenant_id'),
    # TextDyField.data_source('Directory Name', 'data.'),
    TextDyField.data_source('Soft-delete', 'data.properties.enable_soft_delete'),
    TextDyField.data_source('Purge Protection', 'data.properties.enable_purge_protection_str'),
])

# TAB - Keys
key_vault_keys = SimpleTableDynamicLayout.set_fields('Keys', 'data.keys', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Type', 'instance_type'),
    TextDyField.data_source('Location', 'location'),
    TextDyField.data_source('Status', 'attributes.enabled'),
    DateTimeDyField.data_source('Expiration Date', 'attributes.expires'),
    DateTimeDyField.data_source('Creation Date', 'attributes.created'),
    TextDyField.data_source('Key URI', 'key_uri')
])


# TAB - Secrets
key_vault_secrets = SimpleTableDynamicLayout.set_fields('Secrets', 'data.secrets', fields=[
    TextDyField.data_source('ID', '_id'),
    TextDyField.data_source('Type', '_content_type'),
    TextDyField.data_source('Status', '_attributes.enabled'),
    DateTimeDyField.data_source('Updated Date', '_attributes.updated'),
    DateTimeDyField.data_source('Creation Date', '_attributes.created'),
    TextDyField.data_source('Recoverable Days', '_attributes.recoverable_days')
])


# TAB - Certificates
key_vault_certificates = SimpleTableDynamicLayout.set_fields('Certificates', 'data.certificates', fields=[
    TextDyField.data_source('ID', '_id'),
    TextDyField.data_source('Status', '_attributes.enabled'),
    DateTimeDyField.data_source('Updated Date', '_attributes.updated'),
    DateTimeDyField.data_source('Creation Date', '_attributes.created'),
    TextDyField.data_source('Recoverable Days', '_attributes.recoverable_days')

])

# TAB - Access Policies
key_vault_access_policies = ItemDynamicLayout.set_fields('Access Policies', fields=[
    TextDyField.data_source('Enable for Azure VM Deployment', 'data.properties.enabled_for_deployment'),
    TextDyField.data_source('Enable for Disk Encryption', 'data.properties.enabled_for_disk_encryption'),
    TextDyField.data_source('Enable for Template Deployment', 'data.properties.enabled_for_template_deployment'),
    TextDyField.data_source('Enable RBAC Authorization', 'data.properties.enable_rbac_authorization')
])


# TAB - Networking
key_vault_networking = SimpleTableDynamicLayout.set_fields('Private Endpoint Connections', 'data.properties.private_endpoint_connections', fields=[
    TextDyField.data_source('Connection Name', 'name'),
    TextDyField.data_source('Connection State', 'private_link_service_connection_state.status'),
    EnumDyField.data_source('Provisioning State', 'provisioning_state', default_state={
        'safe': ['Succeeded', 'RegisteringDns']
    }),
    TextDyField.data_source('Private Endpoint', 'private_endpoint.id'),
])

# TAB - tags
key_vault_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

key_vault_meta = CloudServiceMeta.set_layouts(
    [key_vault_info_meta, key_vault_keys, key_vault_secrets, key_vault_certificates, key_vault_access_policies, key_vault_networking, key_vault_tags])


class KeyVaultResource(CloudServiceResource):
    cloud_service_group = StringType(default='KeyVault')
    cloud_service_type = StringType(default='KeyVault')
    data = ModelType(KeyVault)
    _metadata = ModelType(CloudServiceMeta, default=key_vault_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)


class KeyVaultResponse(CloudServiceResponse):
    resource = PolyModelType(KeyVaultResource)
