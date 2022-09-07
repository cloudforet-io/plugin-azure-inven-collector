import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

nsg_count_per_location_conf = os.path.join(current_dir, 'widget/nsg_count_per_location.yaml')
nsg_count_per_subscription_conf = os.path.join(current_dir, 'widget/nsg_count_per_subscription.yaml')
nsg_inbound_count_per_subscription_conf = os.path.join(current_dir, 'widget/nsg_inbound_count_per_subscription.yaml')
nsg_outbound_count_per_subscription_conf = os.path.join(current_dir, 'widget/nsg_outbound_count_per_subscription.yaml')

cst_network_security_group = CloudServiceTypeResource()
cst_network_security_group.name = 'Instance'
cst_network_security_group.group = 'NetworkSecurityGroups'
cst_network_security_group.service_code = 'Microsoft.Network/networkSecurityGroups'
cst_network_security_group.labels = ['Networking']
cst_network_security_group.is_major = True
cst_network_security_group.is_primary = True
cst_network_security_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-network-security-groups.svg',
}

cst_network_security_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Virtual Machines', 'data.virtual_machines_display'),
        # is_optional fields - Inbound Security Rules
        TextDyField.data_source('Inbound Rule Priority', 'data.inbound_security_rules.priority', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Rule Name', 'data.inbound_security_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Rule Port', 'data.inbound_security_rules.destination_port_range', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Rule Protocol', 'data.inbound_security_rules.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Rule Source', 'data.inbound_security_rules.source_address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Rule Destination', 'data.inbound_security_rules.destination_address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Rule Action', 'data.inbound_security_rules.access', options={
            'is_optional': True
        }),
        # is_optional fields - Outbound Security Rules
        TextDyField.data_source('Outbound Rule Priority', 'data.outbound_security_rules.priority', options={
            'is_optional': True
        }),
        TextDyField.data_source('Outbound Rule Name', 'data.outbound_security_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Outbound Rule Port', 'data.outbound_security_rules.destination_port_range', options={
            'is_optional': True
        }),
        TextDyField.data_source('Outbound Rule Protocol', 'data.outbound_security_rules.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Outbound Rule Source', 'data.outbound_security_rules.source_address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Outbound Rule Destination', 'data.outbound_security_rules.destination_address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Outbound Rule Action', 'data.outbound_security_rules.access', options={
            'is_optional': True
        }),
        # is_optional_field - Network Interfaces
        TextDyField.data_source('Network Interface Name', 'data.network_interfaces.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Network Interface Public IP Address', 'data.network_interfaces.public_ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Network Interface Private IP Address', 'data.network_interfaces.private_ip_address', options={
            'is_optional': True
        }),
        # is_optional field - Subnets
        TextDyField.data_source('Subnet Name', 'data.subnets.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Address Range', 'data.subnets.address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Virtual Network', 'data.subnets.virtual_network', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Virtual Machines', key='data.virtual_machines_display'),
        SearchField.set(name='Inbound Rule Priority', key='data.inbound_security_rules.priority', data_type='integer'),
        SearchField.set(name='Inbound Rule Name', key='data.inbound_security_rules.name'),
        SearchField.set(name='Inbound Rule Port', key='data.inbound_security_rules.destination_port_range'),
        SearchField.set(name='Inbound Rule Protocol', key='data.inbound_security_rules.protocol'),
        SearchField.set(name='Inbound Rule Source', key='data.inbound_security_rules.source_address_prefix'),
        SearchField.set(name='Inbound Rule Destination', key='data.inbound_security_rules.destination_address_prefix'),
        SearchField.set(name='Inbound Rule Action', key='data.inbound_security_rules.access'),
        SearchField.set(name='Outbound Rule Priority', key='data.outbound_security_rules.priority', data_type='integer'),
        SearchField.set(name='Outbound Rule Name', key='data.outbound_security_rules.name'),
        SearchField.set(name='Outbound Rule Port', key='data.outbound_security_rules.destination_port_range'),
        SearchField.set(name='Outbound Rule Protocol', key='data.outbound_security_rules.protocol'),
        SearchField.set(name='Outbound Rule Source', key='data.outbound_security_rules.source_address_prefix'),
        SearchField.set(name='Outbound Rule Destination', key='data.outbound_security_rules.destination_address_prefix'),
        SearchField.set(name='Outbound Rule Action', key='data.outbound_security_rules.access'),
        SearchField.set(name='Network Interface Name', key='data.network_interfaces.name'),
        SearchField.set(name='Network Interface Public IP Address', key='data.network_interfaces.public_ip_address'),
        SearchField.set(name='Network Interface Private IP Address', key='data.network_interfaces.private_ip_address'),
        SearchField.set(name='Subnet Name', key='data.subnets.name'),
        SearchField.set(name='Subnet Address Range', key='data.subnets.address_prefix'),
        SearchField.set(name='Virtual Network', key='data.subnets.virtual_network'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(nsg_count_per_location_conf)),
        ChartWidget.set(**get_data_from_yaml(nsg_count_per_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(nsg_inbound_count_per_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(nsg_outbound_count_per_subscription_conf)),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_network_security_group}),
]
