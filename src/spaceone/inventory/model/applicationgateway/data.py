from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, NumberType, DateTimeType, \
    TimestampType, UTCDateTimeType, TimedeltaType, FloatType


class Tags(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class SubResource(Model):
    id = StringType()


class ApplicationGatewayAuthenticationCertificate(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    data = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayAutoscaleConfiguration(Model):
    max_capacity = IntType(serialize_when_none=False)
    min_capacity = IntType(serialize_when_none=False)


class ManagedServiceIdentity(Model):
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    type = StringType(choices=('None', 'SystemAssigned', 'SystemAssigned, UserAssigned', 'UserAssigned'), serialize_when_none=False)
    user_assigned_identities = StringType(serialize_when_none=False)


class ApplicationGatewayBackendAddress(Model):
    fqdn = StringType(serialize_when_none=False)
    ip_address = StringType(serialize_when_none=False)


###### Firewall Classes ######
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


class AzureFirewallIPConfiguration(Model):
    etag = StringType()
    id = StringType()
    name = StringType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = ModelType(SubResource, serialize_when_none=False)
    subnet = ModelType(SubResource, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class AzureFirewallPublicIPAddress(Model):
    address = StringType(serialize_when_none=False)


class HubPublicIPAddresses(Model):
    address = ListType(ModelType(AzureFirewallPublicIPAddress), serialize_when_none=False)
    count = IntType(serialize_when_none=False)


class HubIPAddresses(Model):
    private_ip_address = StringType(serialize_when_none=False)
    public_ips = ModelType(HubPublicIPAddresses, serialize_when_none=False)


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


class AzureFirewallNatRuleCollection(Model):
    etag = StringType()
    id = StringType()
    name = StringType(serialize_when_none=False)
    action = StringType(choices=('Dnat', 'Snat'), serialize_when_none=False)
    priority = IntType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    rules = ListType(ModelType(AzureFirewallNatRule), serialize_when_none=False)


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


class NetworkInterfaceIPConfigurationPrivateLinkConnectionProperties(Model):
    fqdns = ListType(StringType, serialize_when_none=False)
    group_id = StringType(serialize_when_none=False)
    required_member_name = StringType(serialize_when_none=False)


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
    public_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = StringType(serialize_when_none=False)  # Change to PublicIPAddress ID
    subnet = StringType(serialize_when_none=False)


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


class RetentionPolicyParameters(Model):
    days = IntType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)


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


class CustomDnsConfigPropertiesFormat(Model):
    fqdn = StringType(serialize_when_none=False)
    ip_addresses = ListType(StringType, serialize_when_none=False)


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


class PrivateEndpoint(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    location = ModelType(ExtendedLocation, serialize_when_none=False)
    extended_location = ModelType(ExtendedLocation, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    custom_dns_configs = ListType(ModelType(CustomDnsConfigPropertiesFormat), serialize_when_none=False)
    manual_private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection),
                                                       serialize_when_none=False)
    network_interfaces = ListType(StringType, serialize_when_none=False)  # Change to network interface ids
    private_link_service_connections = ListType(ModelType(PrivateLinkServiceConnection), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


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


class ServiceEndpointPropertiesFormat(Model):
    locations = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    service = StringType(serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)


class Subnet(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType()
    name = StringType(serialize_when_none=False)
    address_prefix = StringType(serialize_when_none=False)
    address_prefixes = ListType(StringType, serialize_when_none=False)
    application_gateway_ip_configurations = ListType(StringType, serialize_when_none=False) # Change to ip configurations id
    delegations = ListType(ModelType(Delegation), serialize_when_none=False)
    ip_allocations = ListType(ModelType(SubResource), serialize_when_none=False)
    ip_configuration_profiles = ListType(ModelType(IPConfigurationProfile), serialize_when_none=False)
    ip_configurations = ListType(ModelType(IPConfiguration), serialize_when_none=False)
    azure_firewall = ListType(ModelType(AzureFirewall), serialize_when_none=False)
    nat_gateway = ModelType(SubResource, serialize_when_none=False)
    network_security_group = ModelType(NetworkSecurityGroup, serialize_when_none=False)
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


class FrontendIPConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    inbound_nat_pools = ListType(ModelType(SubResource), serialize_when_none=False)
    inbound_nat_rules = ListType(ModelType(SubResource), serialize_when_none=False)
    load_balancing_rules = ListType(ModelType(SubResource), serialize_when_none=False)
    outbound_rules = ListType(ModelType(SubResource), serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = ModelType(PublicIPAddress, serialize_when_none=False)
    public_ip_prefix = ModelType(SubResource, serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)  # Change to Subnet ID
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)


class VirtualNetworkTap(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    destination_load_balancer_front_end_ip_configuration = ModelType(FrontendIPConfiguration, serialize_when_none=False)
    destination_network_interface_ip_configuration = StringType(serialize_when_none=False) # Change to networkinterface ip configuration
    destination_port = IntType(serialize_when_none=False)
    network_interface_tap_configurations = ListType(StringType,serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    tags = ListType(ModelType(Tags))
    type = StringType(serialize_when_none=False)


class NetworkInterfaceIPConfiguration(Model):  # ip configuration in a network interface
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    application_gateway_backend_address_pools = ListType(StringType, serialize_when_none=False)  # Change to ApplicationGatewayBackendAddressPool's ID
    application_security_groups = ListType(ModelType(ApplicationSecurityGroup), serialize_when_none=False)
    load_balancer_backend_address_pools = ListType(StringType, serialize_when_none=False)  # Change to backend address pools id
    load_balancer_inbound_nat_rules = ListType(StringType, serialize_when_none=False)  # Change to inbound NAT rules id
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
    associated_rules = ListType(StringType, serialize_when_none=False)


class ApplicationGatewayConnectionDraining(Model):
    drain_timeout_in_sec = IntType(serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)


class ApplicationGatewayBackendHttpSettings(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    affinity_cookie_name = StringType(serialize_when_none=False)
    authentication_certificates = ListType(ModelType(SubResource), serialize_when_none=False)
    connection_draining = ModelType(ApplicationGatewayConnectionDraining, serialize_when_none=False)
    cookie_based_affinity = StringType(choices=('Disabled', 'Enabled'), serialize_when_none=False)
    host_name = StringType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    pick_host_name_from_backend_address = BooleanType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    probe = ModelType(SubResource, serialize_when_none=False)
    probe_enabled = BooleanType(serialize_when_none=False)
    custom_probe = StringType(serialize_when_none=False)
    protocol = StringType(choices=('Http', 'Https'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    request_timeout = IntType(serialize_when_none=False)
    trusted_root_certificates = ListType(ModelType(SubResource), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayCustomError(Model):
    listener_name = StringType(serialize_when_none=False)
    custom_error_page_url = StringType(serialize_when_none=False)
    status_code = StringType(choices=('HttpStatus403', 'HttpStatus502'))


class ApplicationGatewayFrontendIPConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(default='-', serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_allocation_method = StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    private_link_configuration = ModelType(SubResource, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_ip_address = ModelType(SubResource, serialize_when_none=False)
    ip_type = StringType(choices=('Public', 'Private'), serialize_when_none=False)
    ip_address = StringType(serialize_when_none=False)
    associated_listener = StringType(default='-')
    subnet = ModelType(SubResource, serialize_when_none=False)


class ApplicationGatewayFrontendPort(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayIPConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ModelType(SubResource, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayHttpListener(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    custom_error_configurations = ListType(ModelType(ApplicationGatewayCustomError), serialize_when_none=False)
    firewall_policy = ModelType(SubResource)
    frontend_ip_configuration = ModelType(SubResource)
    frontend_port = ModelType(SubResource)
    port = IntType(serialize_when_none=False)
    host_name = StringType(default='-')
    host_names = ListType(StringType, serialize_when_none=False)
    protocol = StringType(choices=('Http', 'Https'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    require_server_name_indication = BooleanType(serialize_when_none=False)
    ssl_certificate = ModelType(SubResource, serialize_when_none=False)
    ssl_profile = ModelType(SubResource, serialize_when_none=False)
    associated_rules = ListType(StringType, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayPrivateEndpointConnection(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    link_identifier = StringType(serialize_when_none=False)
    private_endpoint = ModelType(PrivateEndpoint, serialize_when_none=False)
    private_link_service_connection_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayPrivateLinkIpConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    private_ip_allocation_method =  StringType(choices=('Dynamic', 'Static'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    subnet = ModelType(SubResource, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayPrivateLinkConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    ip_configurations = ListType(ModelType(ApplicationGatewayPrivateLinkIpConfiguration), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayProbeHealthResponseMatch(Model):
    body = StringType(serialize_when_none=False)
    status_codes = ListType(StringType, serialize_when_none=False)


class ApplicationGatewayProbe(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    host = StringType(serialize_when_none=False)
    interval = IntType(serialize_when_none=False)
    match = ModelType(ApplicationGatewayProbeHealthResponseMatch, serialize_when_none=False)
    min_servers = IntType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    pick_host_name_from_backend_http_settings = BooleanType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    protocol = StringType(choices=('Http', 'Https'), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    timeout = IntType(serialize_when_none=False)
    unhealthy_threshold = IntType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayRedirectConfiguration(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(default='-', serialize_when_none=False)
    include_path = BooleanType(serialize_when_none=False)
    include_query_string = BooleanType(serialize_when_none=False)
    path_rules = ListType(ModelType(SubResource), serialize_when_none=False)
    redirect_type = StringType(choices=('Found', 'Permanent', 'SeeOther', 'Temporary'), serialize_when_none=False)
    request_routing_rules = ListType(ModelType(SubResource), serialize_when_none=False)
    target_listener = ModelType(SubResource, serialize_when_none=False)
    target_url = StringType(serialize_when_none=False)
    url_path_maps = ListType(ModelType(SubResource), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayRequestRoutingRule(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    backend_address_pool = ModelType(SubResource, serialize_when_none=False)
    backend_http_settings = ModelType(SubResource, serialize_when_none=False)
    http_listener = ModelType(SubResource, serialize_when_none=False)
    http_listener_name = StringType(default='-')
    priority = IntType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    redirect_configuration = ModelType(SubResource, serialize_when_none=False)
    rewrite_rule_set = ModelType(SubResource, serialize_when_none=False)
    rule_type = StringType(choices=('Basic', 'PathBasedRouting'), serialize_when_none=False)
    url_path_map = ModelType(SubResource, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayHeaderConfiguration(Model):
    header_name = StringType(serialize_when_none=False)
    header_value = StringType(serialize_when_none=False)


class ApplicationGatewayUrlConfiguration(Model):
    modified_path = StringType(serialize_when_none=False)
    modified_query_string = StringType(serialize_when_none=False)
    reroute = BooleanType(serialize_when_none=False)


class ApplicationGatewayRewriteRuleActionSet(Model):
    request_header_configurations = ListType(ModelType(ApplicationGatewayHeaderConfiguration), serialize_when_none=False)
    response_header_configurations = ListType(ModelType(ApplicationGatewayHeaderConfiguration), serialize_when_none=False)
    url_configuration = ModelType(ApplicationGatewayUrlConfiguration, serialize_when_none=False)


class ApplicationGatewayRewriteRuleCondition(Model):
    ignore_case = BooleanType(serialize_when_none=False)
    negate = BooleanType(serialize_when_none=False)
    pattern = StringType(serialize_when_none=False)
    variable = StringType(serialize_when_none=False)


class ApplicationGatewayRewriteRule(Model):
    action_set = ModelType(ApplicationGatewayRewriteRuleActionSet, serialize_when_none=False)
    conditions = ListType(ModelType(ApplicationGatewayRewriteRuleCondition), serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    rule_sequence = IntType(serialize_when_none=False)


class ApplicationGatewayRewriteRuleSet(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    rewrite_rules = ListType(ModelType(ApplicationGatewayRewriteRule), serialize_when_none=False)
    rewrite_rules_display = ListType(StringType, serialize_when_none=False)
    rules_applied = ListType(StringType, serialize_when_none=False)


class ApplicationGatewaySku(Model):
    capacity = IntType(serialize_when_none=False)
    name = StringType(choices=('Standard_Large', 'Standard_Medium', 'Standard_Small', 'Standard_v2', 'WAF_Large', 'WAF_Medium', 'WAF_v2'), serialize_when_none=False)
    tier = StringType(choices=('Standard', 'Standard_v2', 'WAF', 'WAF_v2'), serialize_when_none=False)


class ApplicationGatewaySslCertificate(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    data = StringType(serialize_when_none=False)
    key_vault_secret_id = StringType(serialize_when_none=False)
    password = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    public_cert_data = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewaySslPolicy(Model):
    cipher_suites = ListType(StringType, serialize_when_none=False)
    disabled_ssl_protocols = ListType(StringType, serialize_when_none=False)
    min_protocol_version = StringType(choices=('TLSv1_0', 'TLSv1_1', 'TLSv1_2'), serialize_when_none=False)
    policy_name = StringType(choices=('AppGwSslPolicy20150501', 'AppGwSslPolicy20170401', 'AppGwSslPolicy20170401S'), serialize_when_none=False)
    policy_type = StringType(choices=('Custom', 'Predefined'), serialize_when_none=False)


class ApplicationGatewayClientAuthConfiguration(Model):
    verify_client_cert_issuer_dn = BooleanType(serialize_when_none=False)


class ApplicationGatewaySslProfile(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    client_auth_configuration = ModelType(ApplicationGatewayClientAuthConfiguration, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    ssl_policy = ModelType(ApplicationGatewaySslPolicy, serialize_when_none=False)
    trusted_client_certificates = ListType(ModelType(SubResource), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayTrustedClientCertificate(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    data = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayTrustedRootCertificate(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    data = StringType(serialize_when_none=False)
    key_vault_secret_id = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayPathRule(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    backend_address_pool = ModelType(SubResource, serialize_when_none=False)
    backend_http_settings = ModelType(SubResource, serialize_when_none=False)
    firewall_policy = ModelType(SubResource, serialize_when_none=False)
    paths = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    redirect_configuration = ModelType(SubResource, serialize_when_none=False)
    rewrite_rule_set = ModelType(SubResource, serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayUrlPathMap(Model):
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    default_backend_address_pool = ModelType(SubResource, serialize_when_none=False)
    default_backend_http_settings = ModelType(SubResource, serialize_when_none=False)
    default_redirect_configuration = ModelType(SubResource, serialize_when_none=False)
    default_rewrite_rule_set = ModelType(SubResource, serialize_when_none=False)
    path_rules = ListType(ModelType(ApplicationGatewayPathRule), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ApplicationGatewayFirewallExclusion(Model):
    match_variable = StringType(serialize_when_none=False)
    selector = StringType(serialize_when_none=False)
    selector_match_operator = StringType(serialize_when_none=False)


class ApplicationGatewayFirewallDisabledRuleGroup(Model):
    rule_group_name = StringType(serialize_when_none=False)
    rules = ListType(IntType, serialize_when_none=False)


class ApplicationGatewayWebApplicationFirewallConfiguration(Model):
    disabled_rule_groups = ListType(ModelType(ApplicationGatewayFirewallDisabledRuleGroup), serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)
    exclusions = ListType(ModelType(ApplicationGatewayFirewallExclusion), serialize_when_none=False)
    file_upload_limit_in_mb = IntType(serialize_when_none=False)
    firewall_mode = StringType(choices=('Detection', 'Prevention'), serialize_when_none=False)
    max_request_body_size = IntType(serialize_when_none=False)
    max_request_body_size_in_kb = IntType(serialize_when_none=False)
    request_body_check = BooleanType(serialize_when_none=False)
    rule_set_type = StringType(serialize_when_none=False)
    rule_set_version = StringType(serialize_when_none=False)


class ApplicationGateway(Model):  # Main Class
    etag = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    identity = ModelType(ManagedServiceIdentity, serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(default='-', serialize_when_none=False)
    authentication_certificates = ListType(ModelType(ApplicationGatewayAuthenticationCertificate), serialize_when_none=False)
    autoscale_configuration = ModelType(ApplicationGatewayAutoscaleConfiguration, serialize_when_none=False)
    backend_address_pools = ListType(ModelType(ApplicationGatewayBackendAddressPool), serialize_when_none=False)
    backend_http_settings_collection = ListType(ModelType(ApplicationGatewayBackendHttpSettings), serialize_when_none=False)
    custom_error_configurations = ListType(ModelType(ApplicationGatewayCustomError), serialize_when_none=False)
    enable_fips = BooleanType(serialize_when_none=False)
    enable_http2 = BooleanType(serialize_when_none=False)
    firewall_policy = ModelType(SubResource, serialize_when_none=False)
    force_firewall_policy_association = BooleanType(serialize_when_none=False)
    frontend_ip_configurations = ListType(ModelType(ApplicationGatewayFrontendIPConfiguration), serialize_when_none=False)
    frontend_ports = ListType(ModelType(ApplicationGatewayFrontendPort), serialize_when_none=False)
    gateway_ip_configurations = ListType(ModelType(ApplicationGatewayIPConfiguration), serialize_when_none=False)
    http_listeners = ListType(ModelType(ApplicationGatewayHttpListener), serialize_when_none=False)
    operational_state = StringType(choices=('Running', 'Starting', 'Stopped', 'Stopping'), serialize_when_none=False)
    private_endpoint_connections = ListType(ModelType(ApplicationGatewayPrivateEndpointConnection), serialize_when_none=False)
    private_link_configurations = ListType(ModelType(ApplicationGatewayPrivateLinkConfiguration), serialize_when_none=False)
    probes = ListType(ModelType(ApplicationGatewayProbe), serialize_when_none=False)
    provisioning_state = StringType(choices=('Deleting', 'Failed', 'Succeeded', 'Updating'), serialize_when_none=False)
    redirect_configurations = ListType(ModelType(ApplicationGatewayRedirectConfiguration), serialize_when_none=False)
    request_routing_rules = ListType(ModelType(ApplicationGatewayRequestRoutingRule), serialize_when_none=False)
    resource_guid = StringType(serialize_when_none=False)
    rewrite_rule_sets = ListType(ModelType(ApplicationGatewayRewriteRuleSet), serialize_when_none=False)
    sku = ModelType(ApplicationGatewaySku, serialize_when_none=False)
    ssl_certificates = ListType(ModelType(ApplicationGatewaySslCertificate), serialize_when_none=False)
    ssl_policy = ModelType(ApplicationGatewaySslPolicy, serialize_when_none=False)
    ssl_profiles = ListType(ModelType(ApplicationGatewaySslProfile), serialize_when_none=False)
    trusted_client_certificates = ListType(ModelType(ApplicationGatewayTrustedClientCertificate), serialize_when_none=False)
    trusted_root_certificates = ListType(ModelType(ApplicationGatewayTrustedRootCertificate), serialize_when_none=False)
    url_path_maps = ListType(ModelType(ApplicationGatewayUrlPathMap), serialize_when_none=False)
    web_application_firewall_configuration = ModelType(ApplicationGatewayWebApplicationFirewallConfiguration, serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
    subscription_id = StringType(serialize_when_none=False)
    subscription_name = StringType(serialize_when_none=False)
    private_ip_address = StringType(serialize_when_none=False)
    public_ip_address = ModelType(PublicIPAddress, serialize_when_none=False)
    virtual_network = StringType(serialize_when_none=False)
    subnet = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
