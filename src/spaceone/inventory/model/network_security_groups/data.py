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


class ApplicationSecurityGroup(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class SecurityRule(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    access = StringType(choices=('Allow', 'Deny'), serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    destination_address_prefix = StringType(serialize_when_none=False)
    destination_address_prefixes = ListType(StringType, serialize_when_none=False)
    destination_application_security_groups = ListType(ModelType(ApplicationSecurityGroup), serialize_when_none=False)
    destination_port_range = StringType(serialize_when_none=False)
    destination_port_ranges = ListType(StringType, serialize_when_none=False)
    direction = StringType(choices=('Inbound', 'Outbound'), serialize_when_none=False)
    priority = IntType(serialize_when_none=False)
    protocol = StringType(choices=('*', 'Ah', 'Esp', 'Icmp', 'Tcp', 'Udp'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    source_address_prefix = StringType(serialize_when_none=False)
    source_address_prefixes = ListType(StringType, serialize_when_none=False)
    source_application_security_groups = ListType(ModelType(ApplicationSecurityGroup), serialize_when_none=False)
    source_port_range = StringType(serialize_when_none=False)
    source_port_ranges = ListType(StringType, serialize_when_none=False)


class TrafficAnalyticsConfigurationProperties(Model):
    enabled = BooleanType(serialize_when_none=False)
    traffic_analytics_interval = IntType(serialize_when_none=False)
    workspace_id = StringType(serialize_when_none=False)
    workspace_region = StringType(serialize_when_none=False)
    workspace_resource_id = StringType(serialize_when_none=False)


class TrafficAnalyticsProperties(Model):
    network_watcher_flow_analytics_configuration = ModelType(TrafficAnalyticsConfigurationProperties,
                                                             serialize_when_none=False)


class FlowLogFormatType(Model):
    json = StringType(serialize_when_none=False)


class FlowLogFormatParameters(Model):
    type = ModelType(FlowLogFormatType, serialize_when_none=False)
    version = IntType(serialize_when_none=False)


class RetentionPolicyParameters(Model):
    days = IntType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)


class FlowLog(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    enable = BooleanType(serialize_when_none=False)
    flow_analytics_configuration = ModelType(TrafficAnalyticsProperties, serialize_when_none=False)
    format = ModelType(FlowLogFormatParameters, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    retention_policy = ModelType(RetentionPolicyParameters, serialize_when_none=False)
    storage_id = StringType(serialize_when_none=False)
    target_resource_guid = StringType(serialize_when_none=False)
    target_resource_id = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkInterfaceDnsSettings(Model):
    applied_dns_servers = ListType(StringType, serialize_when_none=False)
    dns_servers = ListType(StringType, serialize_when_none=False)
    internal_dns_name_label = StringType(serialize_when_none=False)
    internal_domain_name_suffix = StringType(serialize_when_none=False)
    internal_fqdn = StringType(serialize_when_none=False)


class NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties(Model):
    fqdns = ListType(StringType, serialize_when_none=False)
    group_id = StringType(serialize_when_none=False)
    required_member_name = StringType(serialize_when_none=False)


class PublicIPAddressSku(Model):
    name = StringType(choices=('Basic', 'Standard'), serialize_when_none=False)
    tier = StringType(choices=('Global', 'Regional'), serialize_when_none=False)


class IpTag(Model):
    ip_tag_type = StringType(serialize_when_none=False)
    tag = StringType(serialize_when_none=False)


class DdosSettings(Model):
    ddos_custom_policy = ModelType(SubResource, serialize_when_none=False)
    protected_ip = BooleanType(serialize_when_none=False)
    protection_coverage = StringType(choices=('Basic', 'Standard'), serialize_when_none=False)


class PublicIPAddressDnsSettings(Model):
    domain_name_label = StringType(serialize_when_none=False)
    fqdn = StringType(serialize_when_none=False)
    reverse_fqdn = StringType(serialize_when_none=False)


class IPConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = StringType(serialize_when_none=False)  # Change to Public IP Address's ID
    subnet = StringType(serialize_when_none=False)


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


class PublicIPAddress(Model):
    etag = StringType(serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    ddos_settings = ModelType(DdosSettings, serialize_when_none=False)
    dns_settings = ModelType(PublicIPAddressDnsSettings, serialize_when_none=False)
    idle_timeout_in_minutes = IntType(serialize_when_none=False)
    ip_address = StringType(serialize_when_none=False)
    ip_configuration = ModelType(IPConfiguration, serialize_when_none=False)
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
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)


class NetworkInterfaceIPConfiguration(Model):  # ip configuration in a network interface
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    application_security_groups = ListType(ModelType(ApplicationSecurityGroup), serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    private_link_connection_properties = ModelType(NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties,
                                                   serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = ModelType(PublicIPAddress, serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)  # Change to Subnet ID
    virtual_network_taps = ListType(ModelType(SubResource), serialize_when_none=False)


class NetworkSecurityGroupRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(default='-', serialize_when_none=False)
    default_security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    flow_logs = ListType(ModelType(FlowLog), serialize_when_none=False)
    network_interfaces = StringType(serialize_when_none=False)  # Change to Network interfaces' Id
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    subnets = ListType(StringType, serialize_when_none=False)  # Change to Subnet IDs
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PrivateLinkServiceConnectionState(Model):
    actions_required = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)


class PrivateLinkServiceConnection(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    group_ids = ListType(StringType, serialize_when_none=False)
    private_link_service_connection_state = ModelType(PrivateLinkServiceConnectionState, serialize_when_none=False)
    private_link_service_id = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    request_message = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class CustomDnsConfigPropertiesFormat(Model):
    fqdn = StringType(serialize_when_none=False)
    ip_addresses = ListType(StringType, serialize_when_none=False)


class PrivateEndpointRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
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


class AutoApproval(Model):
    subscriptions = ListType(StringType, serialize_when_none=False)


class PrivateLinkServiceIpConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)  # Change to Subnet ID
    type = StringType(serialize_when_none=False)


class InboundNatPool(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    backend_port = IntType(serialize_when_none=False)
    enable_floating_ip = BooleanType(serialize_when_none=False)
    enable_tcp_reset = BooleanType(serialize_when_none=False)
    frontend_ip_configuration = ModelType(SubResource, serialize_when_none=False)
    frontend_port_range_end = IntType(serialize_when_none=False)
    frontend_port_range_start = IntType(serialize_when_none=False)
    idle_timeout_in_minutes = IntType(serialize_when_none=False)
    protocol = StringType(choices=('All', 'Tcp', 'Udp'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationSecurityGroupRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkInterfaceIPConfigurationRef(Model):  # ip configuration in a network interface
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    application_security_groups = ListType(ModelType(ApplicationSecurityGroupRef), serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    private_link_connection_properties = ModelType(NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties,
                                                   serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = StringType(default='', serialize_when_none=False)  # Change Public IP Address to id
    subnet = StringType(default='', serialize_when_none=False)  # Change Subnet to id
    virtual_network_taps = ListType(ModelType(SubResource), serialize_when_none=False)


class InboundNatRule(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    backend_ip_configurations = ListType(ModelType(NetworkInterfaceIPConfigurationRef), serialize_when_none=False)
    target_virtual_machine = ListType(StringType, serialize_when_none=False)
    backend_port = IntType(serialize_when_none=False)
    enable_floating_ip = BooleanType(serialize_when_none=False)
    enable_tcp_reset = BooleanType(serialize_when_none=False)
    frontend_ip_configuration = ModelType(SubResource, serialize_when_none=False)
    frontend_ip_configuration_display = StringType(serialize_when_none=False)
    frontend_port = IntType(serialize_when_none=False)
    port_mapping_display = StringType(serialize_when_none=False)
    idle_timeout_in_minutes = IntType(serialize_when_none=False)
    protocol = StringType(choices=('All', 'Tcp', 'Udp'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class LoadBalancingRule(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    backend_address_pool = ModelType(SubResource, serialize_when_none=False)
    backend_address_pool_display = StringType(serialize_when_none=False)
    backend_port = IntType(serialize_when_none=False)
    disable_outbound_s_nat = BooleanType(serialize_when_none=False)
    enable_floating_ip = BooleanType(serialize_when_none=False)
    enable_tcp_reset = BooleanType(serialize_when_none=False)
    frontend_ip_configuration = ModelType(SubResource, serialize_when_none=False)
    frontend_ip_configuration_display = StringType(serialize_when_none=False)
    frontend_port = IntType(serialize_when_none=False)
    idle_timeout_in_minutes = IntType(serialize_when_none=False)
    load_distribution = StringType(choices=('Default', 'SourceIP', 'SourceIPProtocol'), serialize_when_none=False)
    load_distribution_display = StringType(serialize_when_none=False)
    probe = ModelType(SubResource, serialize_when_none=False)
    protocol = StringType(choices=('All', 'Tcp', 'Udp'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class OutboundRule(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    allocated_outbound_ports = IntType(serialize_when_none=False)
    backend_address_pool = ModelType(SubResource, serialize_when_none=False)
    enable_tcp_reset = BooleanType(serialize_when_none=False)
    frontend_ip_configurations = ListType(ModelType(SubResource), serialize_when_none=False)
    idle_timeout_in_minutes = IntType(serialize_when_none=False)
    protocol = StringType(choices=('All', 'Tcp', 'Udp'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class FrontendIPConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    inbound_nat_pools = ListType(ModelType(InboundNatPool), serialize_when_none=False)
    inbound_nat_rules = ListType(ModelType(InboundNatRule), serialize_when_none=False)
    load_balancing_rules = ListType(ModelType(LoadBalancingRule), serialize_when_none=False)
    outbound_rules = ListType(ModelType(OutboundRule), serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = StringType(serialize_when_none=False)
    public_ip_prefix = ModelType(SubResource, serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)  # Change to Subnet ID
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)


class PrivateEndpointConnection(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType()
    name = StringType(serialize_when_none=False)
    link_identifier = StringType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpointRef)
    private_link_service_connection_state = ModelType(PrivateLinkServiceConnectionState, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Visibility(Model):
    subscriptions = ListType(StringType, serialize_when_none=False)


class PrivateLinkService(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType()
    name = StringType(serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    alias = StringType(serialize_when_none=False)
    auto_approval = ModelType(AutoApproval, serialize_when_none=False)
    enable_proxy_protocol = BooleanType(serialize_when_none=False)
    fqdns = ListType(StringType, serialize_when_none=False)
    ip_configurations = ListType(ModelType(PrivateLinkServiceIpConfiguration), serialize_when_none=False)
    loadBalancer_frontend_ip_configurations = ListType(ModelType(FrontendIPConfiguration), serialize_when_none=False)
    network_interfaces = ListType(StringType, serialize_when_none=False)  # Change to network interfaces' id
    private_endpoint_connections = ListType(ModelType(PrivateEndpointConnection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    visibility = ModelType(Visibility, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkInterfaceTapConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkInterface(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    dns_settings = ModelType(NetworkInterfaceDnsSettings, serialize_when_none=False)
    dscp_configuration = ModelType(SubResource, serialize_when_none=False)
    enable_accelerated_networking = BooleanType(serialize_when_none=False)
    enable_ip_forwarding = BooleanType(serialize_when_none=False)
    hosted_workloads = ListType(StringType, serialize_when_none=False)
    ip_configurations = ListType(ModelType(NetworkInterfaceIPConfiguration), serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    public_ip_address = StringType(serialize_when_none=False)
    mac_address = StringType(serialize_when_none=False)
    migration_phase = StringType(choices=('Abort', 'Commit', 'Committed', 'None', 'Prepare'), serialize_when_none=False)
    nic_type = StringType(choices=('Elastic', 'Standard'), serialize_when_none=False)
    network_security_group = ModelType(NetworkSecurityGroupRef, serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpointRef, serialize_when_none=False)
    private_link_service = ModelType(PrivateLinkService, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tap_configurations = ListType(ModelType(NetworkInterfaceTapConfiguration), serialize_when_none=False)
    virtual_machine = ModelType(SubResource, serialize_when_none=False)
    virtual_machine_display = StringType(default='-')
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


### Subnet Class ###
class ServiceEndpointPropertiesFormat(Model):
    locations = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    service = StringType(serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)


class ApplicationGatewayIPConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ModelType(SubResource, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Delegation(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType()
    name = StringType(default='-', serialize_when_none=False)
    actions = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    service_name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class IPConfigurationProfile(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)  # Change to Subnet ID
    type = StringType(serialize_when_none=False)


class AzureFirewallRCAction(Model):
    type = StringType(choices=('Allow', 'Deny'), serialize_when_none=False)


class AzureFirewallApplicationRuleProtocol(Model):
    port = IntType(serialize_when_none=False)
    protocol_type = StringType(choices=('Http', 'Https', 'Mssql'), serialize_when_none=False)


class AzureFirewallApplicationRule(Model):
    description = StringType(serialize_when_none=False)
    fqdn_tags = ListType(StringType, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    protocols = ListType(ModelType(AzureFirewallApplicationRuleProtocol), serialize_when_none=False)
    source_addresses = ListType(StringType, serialize_when_none=False)
    source_ip_groups = ListType(StringType, serialize_when_none=False)
    target_fqdns = ListType(StringType, serialize_when_none=False)


class AzureFirewallApplicationRuleCollection(Model):
    etag = StringType()
    id = StringType()
    name = StringType(serialize_when_none=False)
    action = ModelType(AzureFirewallRCAction, serialize_when_none=False)
    priority = IntType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    rules = ListType(ModelType(AzureFirewallApplicationRule), serialize_when_none=False)


class AzureFirewallPublicIPAddress(Model):
    address = StringType(serialize_when_none=False)


class HubPublicIPAddresses(Model):
    address = ListType(ModelType(AzureFirewallPublicIPAddress), serialize_when_none=False)
    count = IntType(serialize_when_none=False)


class HubIPAddresses(Model):
    private_ip_address = StringType(serialize_when_none=False)
    public_ips = ModelType(HubPublicIPAddresses, serialize_when_none=False)


class AzureFirewallIPConfiguration(Model):
    etag = StringType()
    id = StringType()
    name = StringType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = ModelType(SubResource, serialize_when_none=False)
    subnet = ModelType(SubResource, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class AzureFirewallIpGroups(Model):
    change_number = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)


class AzureFirewallNatRule(Model):
    description = StringType(serialize_when_none=False)
    destination_addresses = ListType(StringType, serialize_when_none=False)
    destination_ports = ListType(StringType, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    protocols = ListType(StringType, serialize_when_none=False)
    source_addresses = ListType(StringType, serialize_when_none=False)
    source_ip_groups = ListType(StringType, serialize_when_none=False)
    translated_address = StringType(serialize_when_none=False)
    translated_fqdn = StringType(serialize_when_none=False)
    translated_port = StringType(serialize_when_none=False)


class AzureFirewallNatRuleCollection(Model):
    etag = StringType()
    id = StringType()
    name = StringType(serialize_when_none=False)
    action = StringType(choices=('Dnat', 'Snat'), serialize_when_none=False)
    priority = IntType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    rules = ListType(ModelType(AzureFirewallNatRule), serialize_when_none=False)


class AzureFirewallNetworkRule(Model):
    description = StringType(serialize_when_none=False)
    destination_addresses = ListType(StringType, serialize_when_none=False)
    destination_ports = ListType(StringType, serialize_when_none=False)
    destination_fqdns = ListType(StringType, serialize_when_none=False)
    destination_ip_groups = ListType(StringType, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    protocols = ListType(StringType, serialize_when_none=False)
    source_addresses = ListType(StringType, serialize_when_none=False)
    source_ip_groups = ListType(StringType, serialize_when_none=False)
    translated_address = StringType(serialize_when_none=False)
    translated_fqdn = StringType(serialize_when_none=False)
    translated_port = StringType(serialize_when_none=False)


class AzureFirewallNetworkRuleCollection(Model):
    etag = StringType()
    id = StringType()
    name = StringType(serialize_when_none=False)
    action = ModelType(AzureFirewallRCAction, serialize_when_none=False)
    priority = IntType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    rules = ListType(ModelType(AzureFirewallNetworkRule), serialize_when_none=False)


class AzureFirewallSku(Model):
    name = StringType(choices=('AZFW_Hub', 'AZFW_VNet'), serialize_when_none=False)
    tier = StringType(choices=('Premium', 'Standard'), serialize_when_none=False)


class AzureFirewall(Model):
    etag = StringType()
    id = StringType()
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)
    application_rule_collections = ListType(ModelType(AzureFirewallApplicationRuleCollection), serialize_when_none=False)
    firewall_policy = ModelType(SubResource, serialize_when_none=False)
    hub_ip_addresses = ModelType(HubIPAddresses, serialize_when_none=False)
    ip_configurations = ListType(ModelType(AzureFirewallIPConfiguration), serialize_when_none=False)
    ip_groups = ListType(ModelType(AzureFirewallIpGroups), serialize_when_none=False)
    management_ip_configuration = ModelType(AzureFirewallIPConfiguration, serialize_when_none=False)
    nat_rule_collections = ListType(ModelType(AzureFirewallNatRuleCollection), serialize_when_none=False)
    network_rule_collections = ListType(ModelType(AzureFirewallNetworkRuleCollection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    sku = ModelType(AzureFirewallSku, serialize_when_none=False)
    threat_intel_mode = StringType(choices=('Alert', 'Deny', 'Off'), serialize_when_none=False)
    virtual_hub = ModelType(SubResource, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)


class ResourceNavigationLink(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    link = StringType(serialize_when_none=False)
    linked_resource_type = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Route(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    address_prefix = StringType(serialize_when_none=False)
    next_hop_ip_address = StringType(serialize_when_none=False)
    next_hop_type = StringType(choices=('Internet', 'None', 'VirtualAppliance', 'VirtualNetworkGateway', 'VnetLocal'),
                               serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)


class RouteTable(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    disable_bgp_route_propagation = BooleanType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    routes = ListType(ModelType(Route), serialize_when_none=False)
    subnets = ListType(StringType, default=[], serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PrivateEndpoint(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    custom_dns_configs = ListType(ModelType(CustomDnsConfigPropertiesFormat), serialize_when_none=False)
    manual_private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection),
                                                       serialize_when_none=False)
    network_interfaces = ListType(ModelType(NetworkInterface), serialize_when_none=False)
    private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ServiceAssociationLink(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    allow_delete = BooleanType(serialize_when_none=False)
    link = StringType(serialize_when_none=False)
    linked_resource_type = StringType(serialize_when_none=False)
    locations = ListType(ModelType(ExtendedLocation), serialize_when_none=False)
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


class ServiceEndpointPolicy(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    service_endpoint_policy_definitions = ListType(ModelType(ServiceEndpointPolicyDefinition),
                                                   serialize_when_none=False)
    subnets = ListType(StringType, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Subnet(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType()
    virtual_network = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    address_prefix = StringType(serialize_when_none=False)
    address_prefixes = ListType(StringType, serialize_when_none=False)
    application_gateway_ip_configurations = ModelType(ApplicationGatewayIPConfiguration, serialize_when_none=False)
    delegations = ListType(ModelType(Delegation), serialize_when_none=False)
    ip_allocations = ListType(ModelType(SubResource), serialize_when_none=False)
    ip_configuration_profiles = ListType(ModelType(IPConfigurationProfile), serialize_when_none=False)
    ip_configurations = ListType(ModelType(IPConfiguration), serialize_when_none=False)
    azure_firewall = ListType(ModelType(AzureFirewall), serialize_when_none=False)
    nat_gateway = ModelType(SubResource, serialize_when_none=False)
    network_security_group = ModelType(NetworkSecurityGroupRef, serialize_when_none=False)
    private_endpoint_network_policies = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    private_endpoints = ListType(ModelType(PrivateEndpoint), serialize_when_none=False)
    private_link_service_network_policies = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    purpose = StringType(serialize_when_none=False)
    resource_navigation_links = ListType(ModelType(ResourceNavigationLink, serialize_when_none=False))
    route_table = ModelType(RouteTable, serialize_when_none=False)
    service_association_links = ListType(ModelType(ServiceAssociationLink), serialize_when_none=False)
    service_endpoint_policies = ListType(ModelType(ServiceEndpointPolicy), serialize_when_none=False)
    service_endpoints = ListType(ModelType(ServiceEndpointPropertiesFormat), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkSecurityGroup(AzureCloudService):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(default='-', serialize_when_none=False)
    default_security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    inbound_security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    outbound_security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    flow_logs = ListType(ModelType(FlowLog), serialize_when_none=False)
    network_interfaces = ListType(ModelType(NetworkInterface), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    subnets = ListType(ModelType(Subnet), serialize_when_none=False)
    virtual_machines_display = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
