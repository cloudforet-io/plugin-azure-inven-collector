from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, DateTimeType, DictType, FloatType
from spaceone.inventory.libs.schema.resource import AzureCloudService


class SubResource(Model):
    id = StringType()


class ExtendedLocation(Model):
    name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PrivateLinkServiceConnectionState(Model):
    actions_required = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)


class PrivateEndpointRef(Model):
    id = StringType(serialize_when_none=False)
    '''
    etag = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    custom_dns_configs = ListType(ModelType(CustomDnsConfigPropertiesFormat), serialize_when_none=False)
    manual_private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection),
                                                       serialize_when_none=False)
    network_interfaces = ListType(StringType(), serialize_when_none=False)  # Change to network interfaces id
    private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)  # Change to subnet ID
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    '''


class PrivateEndpointConnection(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType()
    name = StringType(serialize_when_none=False)
    link_identifier = StringType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpointRef)
    private_link_service_connection_state = ModelType(PrivateLinkServiceConnectionState, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ServiceEndpointPolicyDefinition(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    service = StringType(serialize_when_none=False)
    service_resources = ListType(StringType)


class UserAssignedIdentity(Model):
    client_id = StringType(serialize_when_none=False)
    principal_id = StringType(serialize_when_none=False)


class Identity(Model):
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    type = StringType(choices=('None', 'SystemAssigned', 'SystemAssigned,UserAssigned', 'UserAssigned'), serialize_when_none=False)
    user_assigned_identities = DictType(StringType, ModelType(UserAssignedIdentity), serialize_when_none=False)


class ActiveDirectoryProperties(Model):
    azure_storage_s_id = StringType(serialize_when_none=False)
    domain_guid = StringType(serialize_when_none=False)
    domain_name = StringType(serialize_when_none=False)
    domain_s_id = StringType(serialize_when_none=False)
    forest_name = StringType(serialize_when_none=False)
    net_bios_domain_name = StringType(serialize_when_none=False)


class AzureFilesIdentityBasedAuthentication(Model):
    active_directory_properties = ModelType(ActiveDirectoryProperties, serialize_when_none=False)
    default_share_permission = StringType(choices=('None', 'StorageFileDataSmbShareContributor', 'StorageFileDataSmbShareElevatedContributor', 'StorageFileDataSmbShareOwner', 'StorageFileDataSmbShareReader'), serialize_when_none=False)
    directory_service_options = StringType(choices=('AADDS', 'AD', 'None'), serialize_when_none=False)


class BlobRestoreRange(Model):
    end_range = StringType(serialize_when_none=False)
    start_range = StringType(serialize_when_none=False)


class BlobRestoreParameters(Model):
    blob_ranges = ListType(ModelType(BlobRestoreRange), serialize_when_none=False)
    time_to_restore = StringType(serialize_when_none=False)


class BlobRestoreStatus(Model):
    failure_reason = StringType(serialize_when_none=False)
    parameters = ModelType(BlobRestoreParameters, serialize_when_none=False)
    restore_id = StringType(serialize_when_none=False)
    status = StringType(choices=('Complete', 'Failed', 'InProgress'), serialize_when_none=False)


class CustomDomain(Model):
    name = StringType(serialize_when_none=False)
    use_sub_domain_name = BooleanType(serialize_when_none=False)


class EncryptionIdentity(Model):
    user_assigned_identity = StringType(serialize_when_none=False)


class KeyVaultProperties(Model):
    current_versioned_key_identifier = StringType(serialize_when_none=False)
    key_name = StringType(serialize_when_none=False)
    key_vault_uri = StringType(serialize_when_none=False)
    key_version = StringType(serialize_when_none=False)
    last_key_rotation_timestamp = DateTimeType(serialize_when_none=False)


class EncryptionService(Model):
    enabled = BooleanType(serialize_when_none=False)
    key_type = StringType(choices=('Account', 'Service'), serialize_when_none=False)
    last_enabled_time = DateTimeType(serialize_when_none=False)


class EncryptionServices(Model):
    blob = ModelType(EncryptionService, serialize_when_none=False)
    file = ModelType(EncryptionService, serialize_when_none=False)
    queue = ModelType(EncryptionService, serialize_when_none=False)
    table = ModelType(EncryptionService, serialize_when_none=False)


class Encryption(Model):
    identity = ModelType(EncryptionIdentity, serialize_when_none=False)
    key_source = StringType(choices=('Microsoft.Keyvault', 'Microsoft.Storage'))
    key_vault_properties = ModelType(KeyVaultProperties, serialize_when_none=False)
    require_infrastructure_encryption = BooleanType(serialize_when_none=False)
    services = ModelType(EncryptionServices, serialize_when_none=False)


class GeoReplicationStats(Model):
    can_failover = BooleanType(serialize_when_none=False)
    last_sync_time = StringType(serialize_when_none=False)
    status = StringType(choices=('Bootstrap', 'Live', 'Unavailable'), serialize_when_none=False)


class KeyCreationTime(Model):
    key1 = DateTimeType(serialize_when_none=False)
    key2 = DateTimeType(serialize_when_none=False)


class KeyPolicy(Model):
    key_expiration_period_in_days = IntType(serialize_when_none=False)


class IPRule(Model):
    action = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class ResourceAccessRule(Model):
    resource_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)


class VirtualNetworkRule(Model):
    action = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    state = StringType(choices=('Deprovisioning', 'Failed', 'NetworkSourceDeleted', 'Provisioning', 'Succeeded'), serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class NetworkRuleSet(Model):
    bypass = StringType(choices=('AzureServices', 'Logging', 'Metrics', 'None'), serialize_when_none=False)
    default_action = StringType(choices=('Allow', 'Deny'), serialize_when_none=False)
    is_public_access_allowed = BooleanType(serialize_when_none=False)
    firewall_address_range = ListType(StringType, serialize_when_none=False)
    ip_rules = ListType(ModelType(IPRule), serialize_when_none=False)
    resource_access_rules = ListType(ModelType(ResourceAccessRule), serialize_when_none=False)
    resource_access_rules_display = ListType(StringType, serialize_when_none=False)
    virtual_network_rules = ListType(ModelType(VirtualNetworkRule), serialize_when_none=False)
    virtual_networks = ListType(StringType, serialize_when_none=False)


class StorageAccountInternetEndpoints(Model):
    blob = StringType(serialize_when_none=False)
    dfs = StringType(serialize_when_none=False)
    file = StringType(serialize_when_none=False)
    web = StringType(serialize_when_none=False)


class StorageAccountMicrosoftEndpoints(Model):
    blob = StringType(serialize_when_none=False)
    dfs = StringType(serialize_when_none=False)
    file = StringType(serialize_when_none=False)
    web = StringType(serialize_when_none=False)
    queue = StringType(serialize_when_none=False)
    table = StringType(serialize_when_none=False)


class Endpoints(Model):
    blob = StringType(serialize_when_none=False)
    dfs = StringType(serialize_when_none=False)
    file = StringType(serialize_when_none=False)
    internet_endpoints = ModelType(StorageAccountInternetEndpoints, serialize_when_none=False)
    microsoft_endpoints = ModelType(StorageAccountMicrosoftEndpoints, serialize_when_none=False)
    queue = StringType(serialize_when_none=False)
    table = StringType(serialize_when_none=False)
    web = StringType(serialize_when_none=False)


class RoutingPreference(Model):
    publish_internet_endpoints = BooleanType(serialize_when_none=False)
    publish_microsoft_endpoints = BooleanType(serialize_when_none=False)
    routing_choice = StringType(choices=('InternetRouting', 'MicrosoftRouting'), serialize_when_none=False)


class SasPolicy(Model):
    expiration_action = StringType(serialize_when_none=False)
    sas_expiration_period = StringType(serialize_when_none=False)


class Sku(Model):
    name = StringType(choices=('Premium_LRS', 'Premium_ZRS', 'Standard_GRS', 'Standard_GZRS', 'Standard_LRS',
                               'Standard_RAGRS', 'Standard_RAGZRS', 'Standard_ZRS'), serialize_when_none=False)
    tier = StringType(choices=('Premium', 'Standard'), serialize_when_none=False)


class ContainerItem(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    etag = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    deleted = BooleanType(serialize_when_none=False)
    deleted_time = DateTimeType(serialize_when_none=False)
    remaining_retention_days = IntType(serialize_when_none=False)
    public_access = StringType(serialize_when_none=False)
    last_modified_time = DateTimeType(serialize_when_none=False)
    lease_state = StringType(serialize_when_none=False)
    lease_status = StringType(choices=['LOCKED', 'UNLOCKED'])
    lease_duration = StringType(choices=['FIXED', 'INFINITE'])
    # metadata = DictType(StringType)
    default_encryption_scope = StringType(serialize_when_none=False)


class StorageAccount(AzureCloudService):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(default='-', serialize_when_none=False)
    container_item = ListType(ModelType(ContainerItem), serialize_when_none=False)
    identity = ModelType(Identity, serialize_when_none=False)
    is_public = StringType(serialize_when_none=False)
    access_tier = StringType(choices=('Cool', 'Hot'), serialize_when_none=False)
    allow_blob_public_access = BooleanType(serialize_when_none=False)
    allow_cross_tenant_replication = BooleanType(serialize_when_none=False)
    allow_shared_key_access = BooleanType(serialize_when_none=False)
    azure_files_identity_based_authentication = ModelType(AzureFilesIdentityBasedAuthentication,
                                                          serialize_when_none=False)
    blob_range_status = ModelType(BlobRestoreStatus, serialize_when_none=False)
    creation_time = DateTimeType(serialize_when_none=False)
    custom_domain = ModelType(CustomDomain, serialize_when_none=False)
    encryption = ModelType(Encryption, serialize_when_none=False)
    failover_in_progress = BooleanType(serialize_when_none=False)
    geo_replication_stats = ModelType(GeoReplicationStats, serialize_when_none=False)
    is_hns_enabled = BooleanType(serialize_when_none=False)
    is_nfs_v3_enabled = BooleanType(serialize_when_none=False)
    key_creation_time = ModelType(KeyCreationTime, serialize_when_none=False)
    key_policy = ModelType(KeyPolicy, serialize_when_none=False)
    large_file_shares_state = StringType(choices=('Enabled', 'Disabled'), serialize_when_none=False)
    last_geo_failover_time = StringType(serialize_when_none=False)
    minimum_tls_version = StringType(choices=('TLS1_0', 'TLS1_1', 'TLS1_2'), serialize_when_none=False)
    network_rule_set = ModelType(NetworkRuleSet, serialize_when_none=False)
    primary_endpoints = ModelType(Endpoints, serialize_when_none=False)
    primary_location = StringType(serialize_when_none=False)
    private_endpoint_connections = ListType(ModelType(PrivateEndpointConnection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Creating', 'ResolvingDNS', 'Succeeded'), serialize_when_none=False)
    routing_preference = ModelType(RoutingPreference, serialize_when_none=False)
    routing_preference_display = StringType(default='Microsoft network routing')
    sas_policy = ModelType(SasPolicy, serialize_when_none=False)
    secondary_endpoints = ModelType(Endpoints, serialize_when_none=False)
    secondary_location = StringType(default='-')
    status_of_primary = StringType(choices=('available', 'unavailable'), serialize_when_none=False)
    status_of_secondary = StringType(choices=('available', 'unavailable'), serialize_when_none=False)
    supports_https_traffic_only = BooleanType(serialize_when_none=False)
    sku = ModelType(Sku, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    blob_size_display = FloatType(default=0.0)
    blob_count_display = IntType(default=0)
    container_count_display = IntType(default=0)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
