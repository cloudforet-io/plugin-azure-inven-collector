from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType
from spaceone.inventory.libs.schema.resource import AzureCloudService


class Tags(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class SubResource(Model):
    id = StringType()


class ExtendedLocation(Model):
    name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class DdosSettings(Model):
    ddos_custom_policy = ModelType(SubResource, serialize_when_none=False)
    protected_ip = BooleanType(serialize_when_none=False)
    protection_coverage = StringType(choices=('Basic', 'Standard'), serialize_when_none=False)


class PublicIPAddressDnsSettings(Model):
    domain_name_label = StringType(default='-')
    fqdn = StringType(serialize_when_none=False)
    reverse_fqdn = StringType(serialize_when_none=False)


class NetworkInterface(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    dscp_configuration = ModelType(SubResource, serialize_when_none=False)
    enable_accelerated_networking = BooleanType(serialize_when_none=False)
    enable_ip_forwarding = BooleanType(serialize_when_none=False)
    migration_phase = StringType(choices=('Abort', 'Commit', 'Committed', 'None', 'Prepare'), serialize_when_none=False)
    nic_type = StringType(choices=('Elastic', 'Standard'), serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    virtual_machine = ModelType(SubResource, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class IPConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = StringType(serialize_when_none=False)
    network_interface = ModelType(NetworkInterface, serialize_when_none=False)


class IpTag(Model):
    ip_tag_type = StringType(serialize_when_none=False)
    tag = StringType(serialize_when_none=False)


class NatGatewaySku(Model):
    name = StringType(choices=('Standard', None), serialize_when_none=False)


class NatGateway(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    idle_timeout_in_minutes = IntType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_addresses = ListType(ModelType(SubResource), serialize_when_none=False)
    public_ip_prefixes = ListType(ModelType(SubResource), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    subnets = ListType(ModelType(SubResource), serialize_when_none=False)
    sku = ModelType(NatGatewaySku, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)


class PublicIPAddressSku(Model):
    name = StringType(choices=('Basic', 'Standard'), serialize_when_none=False)
    tier = StringType(choices=('Global', 'Regional'), serialize_when_none=False)


class PublicIPAddress(AzureCloudService):  # Main Class
    etag = StringType(serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    ddos_settings = ModelType(DdosSettings, serialize_when_none=False)
    dns_settings = ModelType(PublicIPAddressDnsSettings, serialize_when_none=False)
    idle_timeout_in_minutes = IntType(serialize_when_none=False)
    ip_address = StringType(serialize_when_none=False)
    ip_configuration = ModelType(IPConfiguration, serialize_when_none=False)
    associated_to = StringType(serialize_when_none=False)
    ip_tags = ListType(ModelType(IpTag), serialize_when_none=False)
    # linked_public_ip_address = ModelType(PublicIPAddress, serialize_when_none=False)
    migration_phase = StringType(choices=('Abort', 'Commit', 'Committed', 'None', 'Prepare'), serialize_when_none=False)
    nat_gateway = ModelType(NatGateway, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    public_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    public_ip_prefix = ModelType(SubResource, serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    sku = ModelType(PublicIPAddressSku, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
