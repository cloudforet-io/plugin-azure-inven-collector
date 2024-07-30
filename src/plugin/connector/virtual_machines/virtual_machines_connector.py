import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class VirtualMachinesConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_resource_groups(self):
        return self.resource_client.resource_groups.list()

    def list_tenants(self):
        return self.subscription_client.tenants.list()

    def list_vms_in_rg(self, resource_group_name, **query):
        return list(self.compute_client.virtual_machines.list(resource_group_name=resource_group_name, **query))

    def list_all_vms(self, **query):
        return list(self.compute_client.virtual_machines.list_all(**query))

    def get_vm(self, resource_group_name, vm_name):
        return self.compute_client.virtual_machines.get(resource_group_name, vm_name, expand='instanceView')

    # todo : deprecated
    def list_virtual_machine_sizes(self, location):
        return self.compute_client.virtual_machine_sizes.list(location=location)

    def list_resources_in_rg(self, resource_group_name):
        return self.resource_client.resources.list_by_resource_group(resource_group_name=resource_group_name)

    def list_network_interfaces(self):
        return self.network_client.network_interfaces.list_all()

    def list_network_interfaces_in_rg(self, resource_group_name):
        return self.network_client.network_interfaces.list(resource_group_name)

    def list_disks(self):
        return self.compute_client.disks.list()

    def list_virtual_networks(self):
        return self.network_client.virtual_networks.list_all()

    def list_virtual_networks_in_rg(self, resource_group_name):
        return self.network_client.virtual_networks.list(resource_group_name)

    def list_public_ip_addresses(self):
        return self.network_client.public_ip_addresses.list_all()

    def list_public_ip_addresses_in_rg(self, resource_group_name):
        return self.network_client.public_ip_addresses.list(resource_group_name)

    def list_load_balancers(self):
        return self.network_client.load_balancers.list_all()

    def list_load_balancers_in_rg(self, resource_group_name):
        return self.network_client.load_balancers.list(resource_group_name)

    def list_load_balancer_network_interfaces_in_rg(self, resource_group_name, lb_name):
        return self.network_client.load_balancer_network_interfaces.list(resource_group_name, lb_name)

    def list_network_security_groups(self):
        return self.network_client.network_security_groups.list_all()

    def list_network_security_groups_in_rg(self, resource_group_name):
        return self.network_client.network_security_groups.list(resource_group_name)

    def get_subscription_info(self, subscription_id):
        return self.subscription_client.subscriptions.get(subscription_id)

    def list_scale_set_vms(self, resource_group_name, scale_set_name):
        return self.compute_client.virtual_machine_scale_set_vms.list(resource_group_name, scale_set_name)

    def list_virtual_machine_scale_sets_in_rg(self, resource_group_name):
        return self.compute_client.virtual_machine_scale_sets.list(resource_group_name)

    def list_skus(self):
        return self.compute_client.resource_skus.list()