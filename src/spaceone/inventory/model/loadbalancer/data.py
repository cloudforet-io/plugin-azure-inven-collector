from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType


class Tags(Model):
    key = StringType()
    value = StringType()


class SubResource(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class DdosSettings(Model):
    ddos_custom_policy = ModelType(SubResource, serialize_when_none=False)
    protected_ip = BooleanType(serialize_when_none=False)
    protection_coverage = StringType(choices=('Basic', 'Standard'), serialize_when_none=False)


class ExtendedLocationTypes(Model):
    edge_zone = StringType(serialize_when_none=False)


class ExtendedLocation(Model):
    name = StringType(serialize_when_none=False)
    type = ModelType(ExtendedLocationTypes, serialize_when_none=False)


class TrafficAnalyticsConfigurationProperties(Model):
    enabled = BooleanType(serialize_when_none=False)
    traffic_analytics_interval = IntType(serialize_when_none=False)
    workspace_id = StringType(serialize_when_none=False)
    workspace_region = StringType(serialize_when_none=False)
    workspace_resource_id = StringType(serialize_when_none=False)


class NetworkInterfaceDnsSettings(Model):
    applied_dns_servers = ListType(StringType,serialize_when_none=False)
    dns_servers = ListType(StringType, serialize_when_none=False)
    internal_dns_name_label= StringType(serialize_when_none=False)
    internal_domain_name_suffix = StringType(serialize_when_none=False)
    internal_fqdn = StringType(serialize_when_none=False)


class PublicIPAddressDnsSettings(Model):
    domain_name_label = StringType(serialize_when_none=False)
    fqdn = StringType(serialize_when_none=False)
    reverse_fqdn = StringType(serialize_when_none=False)


class PublicIPAddressSku(Model):
    name = StringType(choices=('Basic', 'Standard'), serialize_when_none=False)
    tier = StringType(choices=('Global', 'Regional'), serialize_when_none=False)


class IpTag(Model):
    ip_tag_type = StringType(serialize_when_none=False)
    tag = StringType(serialize_when_none=False)


class TrafficAnalyticsProperties(Model):
    network_watcher_flow_analytics_configuration = ModelType(TrafficAnalyticsConfigurationProperties, serialize_when_none=False)


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
    location = StringType(serialize_when_none=False)
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


class NetworkInterfaceTapConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class CustomDnsConfigPropertiesFormat(Model):
    fqdn = StringType(serialize_when_none=False)
    ip_addresses = ListType(StringType, serialize_when_none=False)


class NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties(Model):  # belongs to NetworkInterfaceIPConfiguration
    fqdns = ListType(StringType, serialize_when_none=False)
    group_id = StringType(serialize_when_none=False)
    required_member_name = StringType(serialize_when_none=False)


class ApplicationSecurityGroup(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class IPConfigurationProfileRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ListType(StringType(), default=[], serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PrivateLinkServiceConnectionState(Model):
    actions_required = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)


class ServiceAssociationLink(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    allow_delete = BooleanType(serialize_when_none=False)
    link = StringType(serialize_when_none=False)
    linked_resource_type = StringType(serialize_when_none=False)
    locations = ListType(StringType, serialize_when_none=False)
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


class IPConfigurationRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    public_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ListType(StringType(), default=[], serialize_when_none=False)


class Delegation(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    actions = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    service_name = StringType(serialize_when_none=False)


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
    next_hop_type = StringType(choices=('Internet', 'None', 'VirtualAppliance', 'VirtualNetworkGateway', 'VnetLocal'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)


class RouteTable(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    disable_bgp_route_propagation = BooleanType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    routes = ListType(ModelType(Route), serialize_when_none=False)
    subnets = ListType(StringType, default=[], serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ServiceEndpointPolicy(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    service_endpoint_policy_definitions = ListType(ModelType(ServiceEndpointPolicyDefinition), serialize_when_none=False)
    subnets = ListType(StringType, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ServiceEndpointPropertiesFormat(Model):
    locations = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    service = StringType(serialize_when_none=False)


class NetworkSecurityGroupRef(Model):
    id = StringType()
    name = StringType()


class PrivateEndpointRef(Model):
    id = StringType()
    name = StringType()


class IPConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    public_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)


class PublicIPAddress(Model):
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
    ip_tags = ListType(ModelType(IpTag), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    public_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    public_ip_prefix = ModelType(SubResource, serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    sku = ModelType(PublicIPAddressSku, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)


class SubnetRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    address_prefix = StringType(serialize_when_none=False)
    address_prefixes = ListType(StringType, serialize_when_none=False)
    ip_allocations = ListType(ModelType(SubResource, serialize_when_none=False))
    nat_gateway = ModelType(SubResource, serialize_when_none=False)
    private_endpoint_network_policies = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    purpose = StringType(serialize_when_none=False)
    delegations = ListType(ModelType(Delegation), serialize_when_none=False)
    ip_configuration_profiles = ListType(ModelType(IPConfigurationProfileRef), serialize_when_none=False)
    ip_configurations = ListType(ModelType(IPConfigurationRef), serialize_when_none=False)
    network_security_group = ModelType(NetworkSecurityGroupRef, serialize_when_none=False)
    private_endpoints = ListType(ModelType(PrivateEndpointRef), serialize_when_none=False)
    private_link_service_network_policies = StringType(serialize_when_none=False)
    resource_navigation_links = ListType(ModelType(ResourceNavigationLink, serialize_when_none=False))
    route_table = ModelType(RouteTable, serialize_when_none=False)
    service_association_links = ListType(ModelType(ServiceAssociationLink), serialize_when_none=False)
    service_endpoint_policies = ListType(ModelType(ServiceEndpointPolicy), serialize_when_none=False)
    service_endpoints = ListType(ModelType(ServiceEndpointPropertiesFormat), serialize_when_none=False)


class PrivateEndpoint(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    custom_dns_configs = ListType(ModelType(CustomDnsConfigPropertiesFormat), serialize_when_none=False)
    manual_private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    network_interfaces = ListType(ModelType(SubResource), serialize_when_none=False) # 아래에 있음
    private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ModelType(SubnetRef, serialize_when_none=False)  # 아래에 있음
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkInterfaceIPConfiguration(Model):  # ip configuration in a network interface
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    # application_gateway_backend_address_pools = ListType(ModelType(ApplicationGatewayBackendAddressPool), serialize_when_none=False)
    application_security_groups = ListType(ModelType(ApplicationSecurityGroup), serialize_when_none=False)
    # load_balancer_backend_address_pools = ListType(ModelType(BackendAddressPool), serialize_when_none=False)  # 아래에 있음
    # load_balancer_inbound_nat_rules = ListType(ModelType(InboundNatRule), serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    private_link_connection_properties = ModelType(NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties,
                                                   serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = ModelType(PublicIPAddress, serialize_when_none=False)
    subnet = ModelType(SubnetRef, serialize_when_none=False)
    virtual_network_taps = ListType(ModelType(SubResource), serialize_when_none=False)


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
    ip_configurations = ListType(ModelType(NetworkInterfaceIPConfiguration), serialize_when_none=False)  # 아래에 있음
    mac_address = StringType(serialize_when_none=False)
    network_security_group = ModelType(SubResource)
    load_balancer_backend_address_pools_name_display = StringType(serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpoint, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tap_configurations = ListType(ModelType(NetworkInterfaceTapConfiguration), serialize_when_none=False)
    virtual_machine = ModelType(SubResource, serialize_when_none=False)
    virtual_machine_name_display = StringType(serialize_when_none=False, default='-')
    private_ip_display = ListType(StringType, default=[], serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkSecurityGroupRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    default_security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    flow_logs = ListType(ModelType(FlowLog), serialize_when_none=False)
    network_interfaces = ListType(ModelType(NetworkInterface), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    subnet = ListType(StringType(), default=[], serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PrivateEndpointRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    custom_dns_configs = ListType(ModelType(CustomDnsConfigPropertiesFormat), serialize_when_none=False)
    manual_private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    network_interfaces = ListType(ModelType(NetworkInterface), serialize_when_none=False) # 아래에 있음
    private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ListType(StringType(), default=[], serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class IPConfigurationProfile(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ModelType(SubnetRef, serialize_when_none=False)  # 아래에 있음.. 흠
    type = StringType(serialize_when_none=False)


class ApplicationGatewayBackendAddress(Model):
    fqdn = StringType(serialize_when_none=False)
    ip_address = StringType(serialize_when_none=False)


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

################################################################################
################################################################################


class SubnetRef(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    address_prefix = StringType(serialize_when_none=False)
    address_prefixes = ListType(StringType, serialize_when_none=False)
    delegations = ListType(ModelType(Delegation), serialize_when_none=False)
    ip_allocations = ListType(ModelType(SubResource, serialize_when_none=False))
    ip_configuration_profiles = ListType(ModelType(IPConfigurationProfileRef), serialize_when_none=False)
    nat_gateway = ModelType(SubResource, serialize_when_none=False)
    network_security_group = ModelType(NetworkSecurityGroupRef, serialize_when_none=False)
    private_endpoint_network_policies = StringType(serialize_when_none=False)
    private_endpoints = ListType(ModelType(PrivateEndpointRef), serialize_when_none=False)
    private_link_service_network_policies = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    purpose = StringType(serialize_when_none=False)
    resource_navigation_links = ListType(ModelType(ResourceNavigationLink, serialize_when_none=False))
    route_table = ModelType(RouteTable, serialize_when_none=False)
    service_association_links = ListType(ModelType(ServiceAssociationLink), serialize_when_none=False)
    service_endpoint_policies = ListType(ModelType(ServiceEndpointPolicy), serialize_when_none=False)
    service_endpoints = ListType(ModelType(ServiceEndpointPropertiesFormat), serialize_when_none=False)


class InboundNatRule(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    backend_ip_configurations = ListType(ModelType(NetworkInterfaceIPConfiguration), serialize_when_none=False)
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


class Probe(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    interval_in_seconds = IntType(serialize_when_none=False)
    load_balancing_rules = ListType(ModelType(SubResource), serialize_when_none=False)
    number_of_probes = IntType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    protocol = StringType(choices=('Http', 'Tcp', 'Https'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    request_path = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkSecurityGroup(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    default_security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    flow_logs = ListType(ModelType(FlowLog), serialize_when_none=False)
    network_interfaces = ListType(ModelType(NetworkInterface), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    security_rules = ListType(ModelType(SecurityRule), serialize_when_none=False)
    subnets = ListType(ModelType(SubnetRef), serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class PrivateEndpoint(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    custom_dns_configs = ListType(ModelType(CustomDnsConfigPropertiesFormat), serialize_when_none=False)
    manual_private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    network_interfaces = ListType(ModelType(NetworkInterface), serialize_when_none=False) # 아래에 있음
    private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ModelType(SubnetRef, serialize_when_none=False)  # 아래에 있음
    tags = ModelType(Tags, serialize_when_none=False)
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
    public_ip_address = ModelType(PublicIPAddress, serialize_when_none=False)  # 아래에 있음..힝
    public_ip_prefix = ModelType(SubResource, serialize_when_none=False)
    subnet = ModelType(SubnetRef, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)


class VirtualNetworkTap(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    destination_load_balancer_front_end_ip_configuration = ModelType(FrontendIPConfiguration, serialize_when_none=False)
    destination_network_interface_ip_configuration = ModelType(NetworkInterfaceIPConfiguration, serialize_when_none=False)
    destination_port = IntType(serialize_when_none=False)
    network_interface_tap_configurations = ListType(ModelType(NetworkInterfaceTapConfiguration))
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties(Model):  # belongs to NetworkInterfaceIPConfiguration
    fqdns = ListType(StringType, serialize_when_none=False)
    group_id = StringType(serialize_when_none=False)
    required_member_name = StringType(serialize_when_none=False)


class NetworkInterfaceIPConfiguration(Model):  # ip configuration in a network interface
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    # application_gateway_backend_address_pools = ListType(ModelType(ApplicationGatewayBackendAddressPool), serialize_when_none=False)
    application_security_groups = ListType(ModelType(ApplicationSecurityGroup), serialize_when_none=False)
    # load_balancer_backend_address_pools = ListType(ModelType(BackendAddressPool), serialize_when_none=False)  # 아래에 있음
    # load_balancer_inbound_nat_rules = ListType(ModelType(InboundNatRule), serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    private_link_connection_properties = ModelType(NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = ModelType(PublicIPAddress, serialize_when_none=False)
    subnet = ModelType(SubnetRef, serialize_when_none=False)
    virtual_network_taps = ListType(ModelType(VirtualNetworkTap), serialize_when_none=False)


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
    ip_configurations = ListType(ModelType(NetworkInterfaceIPConfiguration), serialize_when_none=False)  # 아래에 있음
    mac_address = StringType(serialize_when_none=False)
    network_security_group = ModelType(SubResource)
    load_balancer_backend_address_pools_name_display = StringType(serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpoint, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tap_configurations = ListType(ModelType(NetworkInterfaceTapConfiguration), serialize_when_none=False)
    virtual_machine = ModelType(SubResource, serialize_when_none=False)
    virtual_machine_name_display = StringType(serialize_when_none=False, default='-')
    private_ip_display = ListType(StringType, serialize_when_none=False, default=[])
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)

class Route(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    address_prefix = StringType(serialize_when_none=False)
    next_hop_ip_address = StringType(serialize_when_none=False)
    next_hop_type = StringType(choices=('Internet', 'None', 'VirtualAppliance', 'VirtualNetworkGateway', 'VnetLocal'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)


class RouteTable(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    disable_bgp_route_propagation = BooleanType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    routes = ListType(ModelType(Route), serialize_when_none=False)
    subnets = ListType(ModelType(SubnetRef), serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class Subnet(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    address_prefix = StringType(serialize_when_none=False)
    address_prefixes = ListType(StringType, serialize_when_none=False)
    delegations = ListType(ModelType(Delegation), serialize_when_none=False)
    ip_allocations = ListType(ModelType(SubResource, serialize_when_none=False))
    ip_configuration_profiles = ListType(ModelType(IPConfigurationProfile), serialize_when_none=False)
    ip_configurations = ListType(ModelType(IPConfiguration), serialize_when_none=False)  # 아래에 있음
    nat_gateway = ModelType(SubResource, serialize_when_none=False)
    network_security_group = ModelType(NetworkSecurityGroup, serialize_when_none=False)
    private_endpoint_network_policies = StringType(serialize_when_none=False)
    private_endpoints = ListType(ModelType(PrivateEndpoint), serialize_when_none=False)
    private_link_service_network_policies = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    purpose = StringType(serialize_when_none=False)
    resource_navigation_links = ListType(ModelType(ResourceNavigationLink, serialize_when_none=False))
    route_table = ModelType(RouteTable, serialize_when_none=False)
    service_association_links = ListType(ModelType(ServiceAssociationLink), serialize_when_none=False)
    service_endpoint_policies = ListType(ModelType(ServiceEndpointPolicy), serialize_when_none=False)
    service_endpoints = ListType(ModelType(ServiceEndpointPropertiesFormat), serialize_when_none=False)


class LoadBalancerBackendAddress(Model):
    name = StringType(serialize_when_none=False)
    ip_address = StringType(serialize_when_none=False)
    load_balancer_frontend_ip_configuration = ModelType(SubResource, serialize_when_none=False)
    network_interface_ip_configuration = ModelType(SubResource, serialize_when_none=False)
    virtual_network = ModelType(SubResource, serialize_when_none=False)


class BackendAddressPoolRef(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    etag = StringType(serialize_when_none=False)


class NetworkInterfaceIPConfiguration(Model):  # ip configuration in a network interface
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    etag = StringType(serialize_when_none=False)
    application_security_groups = ListType(ModelType(ApplicationSecurityGroup), serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    private_link_connection_properties = ModelType(NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = ModelType(PublicIPAddress, serialize_when_none=False)
    subnet = ModelType(Subnet, serialize_when_none=False)
    virtual_network_taps = ListType(ModelType(VirtualNetworkTap), serialize_when_none=False)


class ApplicationGatewayBackendAddressPool(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    backend_addresses = ListType(ModelType(ApplicationGatewayBackendAddress), serialize_when_none=False)
    backend_ip_configurations = ListType(ModelType(NetworkInterfaceIPConfiguration), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class BackendAddressPool(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    backend_ip_configurations = ListType(ModelType(NetworkInterfaceIPConfiguration), serialize_when_none=False)
    load_balancer_backend_addresses = ListType(ModelType(LoadBalancerBackendAddress), serialize_when_none=False)
    load_balancing_rules = ListType(ModelType(SubResource), serialize_when_none=False)
    outbound_rule = ModelType(SubResource, serialize_when_none=False)
    outbound_rules = ListType(ModelType(SubResource), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    vm_ids = ListType(StringType, serialize_when_none=False)


class LoadBalancerSku(Model):
    tier = StringType(choices=('Global', 'Regional'), serialize_when_none=False)
    name = StringType(choices=('Standard', 'Basic'), serialize_when_none=False)


class LoadBalancer(Model):
    name = StringType()
    id = StringType()
    type = StringType()
    subscription_id = StringType()
    subscription_name = StringType()
    resource_group = StringType()
    location = StringType()
    sku = ModelType(LoadBalancerSku, serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    backend_address_pools = ListType(ModelType(BackendAddressPool), serialize_when_none=False)
    backend_address_pools_count_display = StringType(serialize_when_none=False, default='')
    network_interfaces = ListType(ModelType(NetworkInterface), serialize_when_none=False)
    frontend_ip_configurations = ListType(ModelType(FrontendIPConfiguration), serialize_when_none=False)
    frontend_ip_configurations_used_by_display = ListType(StringType, serialize_when_none=False)
    private_ip_address_display = ListType(StringType, serialize_when_none=False)
    inbound_nat_pools = ListType(ModelType(InboundNatPool), serialize_when_none=False)
    inbound_nat_rules = ListType(ModelType(InboundNatRule), serialize_when_none=False)
    inbound_nat_rules_display = ListType(StringType, serialize_when_none=False)
    load_balancing_rules = ListType(ModelType(LoadBalancingRule), serialize_when_none=False)
    load_balancing_rules_display = ListType(StringType, serialize_when_none=False)
    outbound_rules = ListType(ModelType(OutboundRule), serialize_when_none=False)
    probes = ListType(ModelType(Probe), serialize_when_none=False)
    probes_display = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tags = ListType(ModelType(Tags), serialize_when_none=False)
    type = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }