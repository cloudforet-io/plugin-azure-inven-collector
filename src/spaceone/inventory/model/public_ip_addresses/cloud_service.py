from schematics.types import ModelType, StringType, PolyModelType, DateTimeType, FloatType

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    ListDyField, SizeField, StateItemDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.model.public_ip_addresses.data import PublicIPAddress

'''
PUBLIC_IP_ADDRESS
'''
# TAB - Default
public_ip_address_meta = ItemDynamicLayout.set_fields('Public IP Address', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
    TextDyField.data_source('SKU', 'instance_type'),
    TextDyField.data_source('Tier', 'data.sku.tier'),
    TextDyField.data_source('IP Address', 'data.ip_address'),
    TextDyField.data_source('DNS Name', 'data.dns_settings.fqdn'),
    TextDyField.data_source('Associated To', 'data.associated_to')
    # TextDyField.data_source('Routing Preference', ''),

])

# TAB - Configuration
public_ip_address_configuration = ItemDynamicLayout.set_fields('Configuration', fields=[
    TextDyField.data_source('IP Address Assignment', 'data.public_ip_allocation_method'),
    TextDyField.data_source('Idle Timeout(Minutes)', 'data.idle_timeout_in_minutes'),
    TextDyField.data_source('DNS Name Label(Optional)', 'data.dns_settings.domain_name_label')
])

# TAB - Alias Record Sets TODO: Find Alias information API
public_ip_address_alias_record_sets = TableDynamicLayout.set_fields('Alias Record Sets', fields=[
    TextDyField.data_source('Subscription', ''),
    TextDyField.data_source('DNS Zone', ''),
    TextDyField.data_source('Name', ''),
    TextDyField.data_source('Type', ''),
    TextDyField.data_source('TTL', '')
])

# TAB - tags
virtual_network_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

public_addresses_meta = CloudServiceMeta.set_layouts([public_ip_address_meta, public_ip_address_configuration])


class NetworkResource(CloudServiceResource):
    cloud_service_group = StringType(default='PublicIPAddresses')


class PublicIPAddressResource(NetworkResource):
    cloud_service_type = StringType(default='IPAddress')
    data = ModelType(PublicIPAddress)
    _metadata = ModelType(CloudServiceMeta, default=public_addresses_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class PublicIPAddressResponse(CloudServiceResponse):
    resource = PolyModelType(PublicIPAddressResource)
