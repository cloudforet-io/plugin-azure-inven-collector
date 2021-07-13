from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_network_security_group = CloudServiceTypeResource()
cst_network_security_group.name = 'NetworkSecurityGroup'
cst_network_security_group.group = 'Network'
cst_network_security_group.service_code = 'Microsoft.Network/networkSecurityGroups'
cst_network_security_group.labels = ['Network']
cst_network_security_group.is_major = False
cst_network_security_group.is_primary = False
cst_network_security_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-network-security-groups.svg',
}

cst_network_security_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription ID', 'data.subscription_id'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Virtual Machines', 'data.virtual_machines_display'),
        # is_optional fields - Inbound Security Rules
        TextDyField.data_source('Inbound Security Rule Priority', 'data.inbound_security_rules.priority', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Security Rule Name', 'data.inbound_security_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Security Rule Port', 'data.inbound_security_rules.destination_port_range', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Security Rule Protocol', 'data.inbound_security_rules.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Security Rule Source', 'data.inbound_security_rules.source_address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Security Rule Destination', 'data.inbound_security_rules.destination_address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Inbound Security Rule Action', 'data.inbound_security_rules.access', options={
            'is_optional': True
        }),
        # is_optional fields - Outbound Security Rules
        TextDyField.data_source('Priority', 'data.outbound_security_rules.priority', options={
            'is_optional': True
        }),
        TextDyField.data_source('Name', 'data.outbound_security_rules.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Port', 'data.outbound_security_rules.destination_port_range', options={
            'is_optional': True
        }),
        TextDyField.data_source('Protocol', 'data.outbound_security_rules.protocol', options={
            'is_optional': True
        }),
        TextDyField.data_source('Source', 'data.outbound_security_rules.source_address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Destination', 'data.outbound_security_rules.destination_address_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Action', 'data.outbound_security_rules.access', options={
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
        SearchField.set(name='ID', key='data.id', data_type='string'),
        SearchField.set(name='Name', key='data.name', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Virtual Machines', key='data.virtual_machines_display', data_type='string')
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_network_security_group}),
]
