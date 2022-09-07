from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType
from spaceone.inventory.libs.schema.resource import AzureCloudService


class Tags(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class SubResource(Model):
    id = StringType()


class ResourceIdentity(Model):
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PrivateEndpointProperty(Model):
    id = StringType(serialize_when_none=False)


class ServerPrivateLinkServiceConnectionStateProperty(Model):
    actions_required = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(choices=('Approved', 'Disconnected', 'Pending', 'Rejected'), serialize_when_none=False)


class ServerPrivateEndpointConnectionProperties(Model):
    private_endpoint = ModelType(PrivateEndpointProperty, serialize_when_none=False)
    private_link_service_connection_state = ModelType(ServerPrivateLinkServiceConnectionStateProperty, serialize_when_none=False)
    provisioning_state = StringType(choices=('Approving', 'Dropping', 'Failed', 'Ready', 'Rejecting'), serialize_when_none=False)


class ServerPrivateEndpointConnection(Model):
    id = StringType(serialize_when_none=False)
    properties = ModelType(ServerPrivateEndpointConnectionProperties, serialize_when_none=False)


class StorageProfile(Model):
    backup_retention_days = IntType(serialize_when_none=False)
    geo_redundant_backup = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    storage_autogrow = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    storage_mb = IntType(serialize_when_none=False)
    storage_gb = IntType(serialize_when_none=False)


class Sku(Model):
    capacity = IntType(serialize_when_none=False)
    family = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    size = StringType(serialize_when_none=False)
    tier = StringType(choices=('Basic', 'GeneralPurpose', 'MemoryOptimized'), serialize_when_none=False)


class FirewallRule(Model):
    id = StringType()
    name = StringType(serialize_when_none=False)
    end_ip_address = StringType(serialize_when_none=False)
    start_ip_address = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class MySQLServer(AzureCloudService):  # Main class
    id = StringType()
    identity = ModelType(ResourceIdentity, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    administrator_login = StringType(serialize_when_none=False)
    byok_enforcement = StringType(serialize_when_none=False)
    earliest_restore_date = DateTimeType(serialize_when_none=False)
    firewall_rules = ListType(ModelType(FirewallRule), serialize_when_none=False)
    allow_azure_services_access = BooleanType(default=True, serialize_when_none=False)
    fully_qualified_domain_name = StringType(serialize_when_none=False)
    infrastructure_encryption = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    master_server_id = StringType(serialize_when_none=False)
    minimal_tls_version = StringType(choices=('TLS1_0', 'TLS1_1', 'TLS1_2', 'TLSEnforcementDisabled'), serialize_when_none=False)
    private_endpoint_connections = ListType(ModelType(ServerPrivateEndpointConnection), serialize_when_none=False)
    public_network_access = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    replica_capacity = IntType(serialize_when_none=False)
    replication_role = StringType(serialize_when_none=False)
    ssl_enforcement = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    storage_profile = ModelType(StorageProfile, serialize_when_none=False)
    user_visible_state = StringType(choices=('Disabled', 'Dropping', 'Inaccessible', 'Ready'), serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    sku = ModelType(Sku, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
