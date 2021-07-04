from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, NumberType, DateTimeType, \
    TimestampType, UTCDateTimeType, TimedeltaType, FloatType


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


class NetworkSecurityGroup(Model):
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


class PrivateLinkServiceConnectionState(Model):
    actions_required = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)


class PrivateLinkServiceConnectionState(Model):
    actions_required = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)


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
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    dns_settings = ModelType(NetworkInterfaceDnsSettings, serialize_when_none=False)
    dscp_configuration = ModelType(SubResource, serialize_when_none=False)
    enable_accelerated_networking = BooleanType(serialize_when_none=False)
    enable_ip_forwarding = BooleanType(serialize_when_none=False)
    hosted_workloads = ListType(StringType, serialize_when_none=False)
    ip_configurations = ListType(ModelType(NetworkInterfaceIPConfiguration), serialize_when_none=False)
    mac_address = StringType(serialize_when_none=False)
    migration_phase = StringType(choices=('Abort', 'Commit', 'Committed', 'None', 'Prepare'), serialize_when_none=False)
    nic_type = StringType(choices=('Elastic', 'Standard'), serialize_when_none=False)
    network_security_group = ModelType(NetworkSecurityGroup, serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpointRef, serialize_when_none=False)
    private_link_service = ModelType(PrivateLinkService, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tap_configurations = ListType(ModelType(NetworkInterfaceTapConfiguration), serialize_when_none=False)
    virtual_machine = ModelType(SubResource, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkSecurityGroup(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(default='-', serialize_when_none=False)
    default_security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    flow_logs = ListType(ModelType(FlowLog), serialize_when_none=False)
    network_interfaces = ListType(ModelType(NetworkInterface), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    subnets = ListType(StringType, serialize_when_none=False)  # Change to Subnet IDs
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
