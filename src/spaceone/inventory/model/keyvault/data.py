from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, NumberType, DateTimeType, \
    TimestampType, UTCDateTimeType, TimedeltaType, FloatType


class Tags(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class SubResource(Model):
    id = StringType()


class Permissions(Model):
    certificates = ListType(StringType, serialize_when_none=False)
    keys = ListType(StringType, serialize_when_none=False)
    secrets = ListType(StringType, serialize_when_none=False)
    storage = ListType(StringType, serialize_when_none=False)


class AccessPolicyEntry(Model):
    application_id = StringType(serialize_when_none=False)
    object_id = StringType(serialize_when_none=False)
    permissions = ModelType(Permissions, serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)


class IPRule(Model):
    value = StringType(serialize_when_none=False)


class VirtualNetworkRule(Model):
    ip = StringType(serialize_when_none=False)
    ignore_missing_vnet_service_endpoint = BooleanType(serialize_when_none=False)


class NetworkRuleSet(Model):
    bypass = StringType(choices=('AzureServices', 'None'), serialize_when_none=False)
    default_action = StringType(choices=('Allow', 'Deny'), serialize_when_none=False)
    ip_rules = ListType(ModelType(IPRule), serialize_when_none=False)
    virtual_network_rules = ListType(ModelType(VirtualNetworkRule), serialize_when_none=False)


class PrivateEndpoint(Model):
    id = StringType(serialize_when_none=False)


class PrivateLinkServiceConnectionState(Model):
    actions_required = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(choices=('Approved', 'Disconnected', 'Pending', 'Rejected'), serialize_when_none=False)


class PrivateEndpointConnectionItem(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpoint, serialize_when_none=False)
    private_link_service_connection_state = ModelType(PrivateLinkServiceConnectionState, serialize_when_none=False)
    provisioning_state = StringType(choices=('Creating', 'Deleting', 'Disconnected', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)


class Sku(Model):
    family = StringType(serialize_when_none=False)
    name = StringType(choices=('premium', 'standard'), serialize_when_none=False)


class SecretAttributes(Model):
    created = DateTimeType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)
    exp = DateTimeType(serialize_when_none=False)
    nbf = DateTimeType(serialize_when_none=False)
    recoverable_days = IntType(serialize_when_none=False)
    recovery_level = StringType(choices=('CustomizedRecoverable', 'CustomizedRecoverable+ProtectedSubscription',
                                         'CustomizedRecoverable+Purgeable', 'Purgeable', 'Recoverable', 'Recoverable+ProtectedSubscription',
                                         'Recoverable+Purgeable'), serialize_when_none=False)
    updated = DateTimeType(serialize_when_none=False)


class ResourceId(Model):
    source_id = StringType(serialize_when_none=False)
    vault_url = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)


class VaultId(Model):
    resource_id = ModelType(ResourceId, serialize_when_none=False)


class SecretItem(Model):
    _attributes = ModelType(SecretAttributes, serialize_when_none=False)
    _content_type = StringType(serialize_when_none=False)
    _id = StringType(serialize_when_none=False)
    _managed = BooleanType(serialize_when_none=False)
    _tags = ModelType(Tags, serialize_when_none=False)
    _vault_id = ModelType(VaultId, serialize_when_none=False)


class CertificateAttributes(Model):
    created = DateTimeType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)
    exp = DateTimeType(serialize_when_none=False)
    nbf = DateTimeType(serialize_when_none=False)
    recoverable_days = IntType(serialize_when_none=False)
    recovery_level = StringType(choices=('CustomizedRecoverable', 'CustomizedRecoverable+ProtectedSubscription',
                                         'CustomizedRecoverable+Purgeable', 'Purgeable', 'Recoverable',
                                         'Recoverable+ProtectedSubscription',
                                         'Recoverable+Purgeable'), serialize_when_none=False)
    updated = DateTimeType(serialize_when_none=False)


class CertificateItem(Model):
    _attributes = ModelType(CertificateAttributes, serialize_when_none=False)
    _id = StringType(serialize_when_none=False)
    _content_type = StringType(serialize_when_none=False)
    _tags = ModelType(Tags, serialize_when_none=False)
    _vault_id = ModelType(VaultId, serialize_when_none=False)


class VaultProperties(Model):
    access_policies = ListType(ModelType(AccessPolicyEntry), serialize_when_none=False)
    create_mode = StringType(choices=('default', 'recover'), serialize_when_none=False)
    enable_purge_protection = BooleanType(default=False, serialize_when_none=False)
    enable_purge_protection_str = StringType(serialize_when_none=False, default='Disabled')
    enable_rbac_authorization = BooleanType(serialize_when_none=False)
    enable_soft_delete = BooleanType(serialize_when_none=False)
    enabled_for_deployment = BooleanType(serialize_when_none=False)
    enabled_for_disk_encryption = BooleanType(serialize_when_none=False)
    enabled_for_template_deployment = BooleanType(serialize_when_none=False)
    hsm_pool_resource_id = StringType(serialize_when_none=False)
    network_acls = ModelType(NetworkRuleSet, serialize_when_none=False)
    private_endpoint_connections = ListType(ModelType(PrivateEndpointConnectionItem), serialize_when_none=False)
    provisioning_state = StringType(choices=('RegisteringDns', 'Succeeded'), serialize_when_none=False)
    sku = ModelType(Sku, serialize_when_none=False)
    soft_delete_retention_in_days = IntType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    vault_uri = StringType(serialize_when_none=False)


class KeyAttributes(Model):
    created = DateTimeType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)
    exp = DateTimeType(serialize_when_none=False)
    nbf = DateTimeType(serialize_when_none=False)
    recoverable_days = IntType(serialize_when_none=False)
    recovery_level = StringType(choices=('CustomizedRecoverable', 'CustomizedRecoverable+ProtectedSubscription',
                                         'CustomizedRecoverable+Purgeable', 'Purgeable', 'Recoverable',
                                         'Recoverable+ProtectedSubscription',
                                         'Recoverable+Purgeable'), serialize_when_none=False)
    updated = DateTimeType(serialize_when_none=False)


class KeyItem(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    key_uri = StringType(serialize_when_none=False)
    attributes = ModelType(KeyAttributes, serialize_when_none=False)
    kid = StringType(serialize_when_none=False)
    managed = BooleanType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)


class KeyVault(Model):  # Main class
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    subscription_id = StringType(serialize_when_none=False)
    subscription_name = StringType(serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    properties = ModelType(VaultProperties, serialize_when_none=False)
    keys = ListType(ModelType(KeyItem), serialize_when_none=False)
    secrets = ListType(ModelType(SecretItem), serialize_when_none=False)
    certificates = ListType(ModelType(CertificateItem), serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
