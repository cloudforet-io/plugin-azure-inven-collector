import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

virtualnetwork_count_per_location_conf = os.path.join(current_dir, 'widget/virtualnetwork_count_per_location.yaml')
virtualnetwork_count_per_subscription_conf = os.path.join(current_dir, 'widget/virtualnetwork_count_per_subscription.yaml')
virtualnetwork_subnet_count_per_location_conf = os.path.join(current_dir, 'widget/virtualnetwork_subnet_count_per_location.yaml')
virtualnetwork_subnet_count_per_subscription_conf = os.path.join(current_dir, 'widget/virtualnetwork_subnet_count_per_subscription.yaml')


cst_virtual_network = CloudServiceTypeResource()
cst_virtual_network.name = 'Instance'
cst_virtual_network.group = 'VirtualNetworks'
cst_virtual_network.service_code = 'Microsoft.Network/virtualNetworks'
cst_virtual_network.labels = ['Networking']
cst_virtual_network.is_major = True
cst_virtual_network.is_primary = True
cst_virtual_network.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-virtual-networks.svg',
}

cst_virtual_network._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),

        # is_optional fields - Default
        TextDyField.data_source('Subscription ID', 'account', options={
            'is_optional': True
        }),
        ListDyField.data_source('DNS servers', 'data.dhcp_options.dns_servers', options={
            'is_optional': True
        }),
        TextDyField.data_source('Resource GUID', 'data.resource_guid', options={
            'is_optional': True
        }),
        ListDyField.data_source('Address Space', 'data.address_space.address_prefixes', options={
            'is_optional': True
        }),

        # is_optional fields - Connected Devices
        TextDyField.data_source('Connected Device', 'data.connected_devices.device', options={
            'is_optional': True
        }),
        TextDyField.data_source('Connected Device Type', 'data.connected_devices.type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Connected Subnet', 'data.connected_devices.name', options={
            'is_optional': True
        }),

        # is_optional fields -Subnets
        TextDyField.data_source('Subnet Name', 'data.subnets.name', options={
            'is_optional': True
        }),
        ListDyField.data_source('Subnet IP Prefixes', 'data.subnets.address_prefixes', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Delegated To', 'data.subnets.delegations.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Network Security Group', 'data.subnets.network_security_group.name', options={
            'is_optional': True
        }),

        # is optional fields - Firewall
        TextDyField.data_source('Firewall Name', 'data.azure_firewall.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall IP Address', 'data.azure_firewall.ip_configurations.private_ip_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Firewall Subnet', 'data.azure_firewall.subnet', options={
            'is_optional': True
        }),

        # is_optional fields - Peerings
        TextDyField.data_source('Peering Name', 'data.virtual_network_peerings.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Peer', 'data.virtual_network_peerings.remote_virtual_network.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Peer Gateway Transit', 'data.virtual_network_peerings.allow_gateway_transit', options={
            'is_optional': True
        }),

        # is optional fields - Service Endpoints
        TextDyField.data_source('Service Endpoint', 'data.service_endpoints.service', options={
            'is_optional': True
        }),
        TextDyField.data_source('Service Endpoint Subnet', 'data.service_endpoints.subnet', options={
            'is_optional': True
        }),
        TextDyField.data_source('Service Endpoint Locations', 'data.service_endpoints.locations', options={
            'is_optional': True
        }),

        # is optional fields - Private Endpoints
        TextDyField.data_source('Private Endpoint', 'data.private_endpoints.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Endpoint Subnet', 'data.private_endpoints.subnet', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='DNS servers', key='data.dhcp_options.dns_servers'),
        SearchField.set(name='Resource GUID', key='data.resource_guid'),
        SearchField.set(name='Address Space', key='data.address_space.address_prefixes'),
        SearchField.set(name='Connected Device', key='data.connected_devices.device'),
        SearchField.set(name='Connected Device Type', key='data.connected_devices.type'),
        SearchField.set(name='Connected Subnet', key='data.connected_devices.name'),
        SearchField.set(name='Subnet Name', key='data.subnets.name'),
        SearchField.set(name='Subnet IP Prefixes', key='data.subnets.address_prefixes'),
        SearchField.set(name='Subnet Delegated To', key='data.subnets.delegations.name'),
        SearchField.set(name='Subnet Network Security Group', key='data.subnets.network_security_group.name'),
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(virtualnetwork_count_per_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(virtualnetwork_count_per_location_conf)),
        ChartWidget.set(**get_data_from_yaml(virtualnetwork_subnet_count_per_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(virtualnetwork_subnet_count_per_location_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_virtual_network}),
]
