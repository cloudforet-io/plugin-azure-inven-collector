from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.storageaccount.data import StorageAccount

'''
STORAGE_ACCOUNT
'''
# TAB - Default
storage_account_info_meta = ItemDynamicLayout.set_fields('Storage Account', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'data.subscription_id'),
    TextDyField.data_source('State of Primary', 'data.status_of_primary'),
    TextDyField.data_source('Performance Tier', 'data.sku.tier'),
    TextDyField.data_source('Access Tier', 'data.access_tier'),
    TextDyField.data_source('Replication', 'data.sku.name'),
    TextDyField.data_source('Account Kind', 'data.kind'),
    TextDyField.data_source('Provisioning State', 'data.provisioning_state'),
    DateTimeDyField.data_source('Created', 'data.creation_time')
])

# TAB - Networking
storage_group_networking = ItemDynamicLayout.set_fields('Networking', fields=[
    TextDyField.data_source('Is Public', 'allow_blob_public_access'),
    TextDyField.data_source('Virtual Network', 'data.network_rule_set.virtual_network_rules.name'),
    ListDyField.data_source('Firewall Address Range', 'data.network_rule_set.firewall_address_range'),
    ListDyField.data_source('Resource Instances', 'data.network_rule_set.resource_access_rules_display'),
    TextDyField.data_source('Exceptions', 'data.network_rule_set.bypass'),
    TextDyField.data_source('Routing Preference', 'data.routing_preference_display'),
    TextDyField.data_source('Publish Microsoft Endpoints', 'data.routing_preference.publish_microsoft_endpoints'),
    TextDyField.data_source('Publish Internet Endpoints', 'data.routing_preference.publish_internet_endpoints')
])

# TAB - Endpoints
storage_account_primary_endpoints = ItemDynamicLayout.set_fields('Primary Endpoints', fields=[
    TextDyField.data_source('Blob', 'data.primary_endpoints.'),
    TextDyField.data_source('Queue', 'data.primary_endpoints..blob'),
    TextDyField.data_source('Table', 'data.primary_endpoints.table'),
    TextDyField.data_source('File', 'data.primary_endpoints.file'),
    TextDyField.data_source('Web', 'data.primary_endpoints.web'),
    TextDyField.data_source('DFS', 'data.primary_endpoints.dfs'),
    TextDyField.data_source('Microsoft Endpoints', 'data.routing_preference.publish_microsoft_endpoints'),
    TextDyField.data_source('Internet Endpoints', 'data.routing_preference.publish_internet_endpoints')
])

# TAB - Containers
storage_account_containers = TableDynamicLayout.set_fields('Containers', 'data.container_item', fields=[
    TextDyField.data_source('Name', 'name'),
    DateTimeDyField.data_source('Last Modified', 'last_modified_time'),
    TextDyField.data_source('Public Access Level', 'public_access'),
    TextDyField.data_source('Lease State', 'lease_state')
])

# TAB - Encryption
storage_account_encryption = ItemDynamicLayout.set_fields('Encryption', 'data.encryption', fields=[
    TextDyField.data_source('Key Source', 'key_source'),
    TextDyField.data_source('Key Vault URI', 'key_vault_properties.key_vault_uri')
])


# TAB - Geo-Replication
storage_account_geo_replication = TableDynamicLayout.set_fields('Geo-Replication', fields=[
    TextDyField.data_source('Primary Location', 'primary_location'),
    EnumDyField.data_source('Status of Primary', 'status_of_primary', default_state={
        'safe': ['available'],
        'warning': ['unavailable']
    }),
    TextDyField.data_source('Secondary Location', 'secondary_location'),
    EnumDyField.data_source('Status of Secondary', 'status_of_secondary', default_state={
        'safe': ['available'],
        'warning': ['unavailable']
    })
])

# TAB - tags
network_security_group_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

storage_account_meta = CloudServiceMeta.set_layouts(
    [storage_account_info_meta, storage_group_networking, storage_account_encryption, storage_account_geo_replication, network_security_group_tags])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Storage')


class StorageAccountResource(ComputeResource):
    cloud_service_type = StringType(default='StorageAccount')
    data = ModelType(StorageAccount)
    _metadata = ModelType(CloudServiceMeta, default=storage_account_meta, serialized_name='metadata')
    name = StringType()


class StorageAccountResponse(CloudServiceResponse):
    resource = PolyModelType(StorageAccountResource)
