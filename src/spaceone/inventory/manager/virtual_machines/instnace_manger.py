import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.connector.virtual_machines import VirtualMachinesConnector
from spaceone.inventory.manager.virtual_machines import VirtualMachineDiskManager, VirtualMachineLoadBalancerManager,\
    VirtualMachineNetworkSecurityGroupManager, VirtualMachineNICManager, \
    VirtualMachineVmManager, VirtualMachineVMScaleSetManager, VirtualMachineVNetManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.virtual_machines.data import *
from spaceone.inventory.libs.schema.resource import ErrorResourceResponse, CloudServiceResourceResponse, AzureMonitorModel
from spaceone.core.utils import *
from spaceone.inventory.model.virtual_machines.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.virtual_machines.cloud_service import *

_LOGGER = logging.getLogger(__name__)


class VirtualMachinesManager(AzureManager):
    connector_name = 'VirtualMachinesConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    # refactoring
    def collect_cloud_service(self, params):
        '''
            Args:
                params (dict):
                    - 'options' : 'dict'
                    - 'schema' : 'str'
                    - 'secret_data' : 'dict'
                    - 'filter' : 'dict'
                    - 'zones' : 'list'
                    - 'subscription_info' :  'dict'
            Response:
                CloudServiceResponse (list) : dictionary of azure vm scale set data resource information
                ErrorResourceResponse (list) : list of error resource information
        '''

        _LOGGER.debug("** VirtualMachine START **")
        start_time = time.time()

        servers = []
        errors = []

        azure_vm_connector: VirtualMachinesConnector = self.locator.get_connector(self.connector_name, **params)
        azure_vm_connector.set_connect(params['secret_data'])

        # call all managers
        vm_manager: VirtualMachineVmManager = VirtualMachineVmManager(params, azure_vm_connector=azure_vm_connector)
        disk_manager: VirtualMachineDiskManager = VirtualMachineDiskManager(params,
                                                                            azure_vm_connector=azure_vm_connector)
        load_balancer_manager: VirtualMachineLoadBalancerManager = \
            VirtualMachineLoadBalancerManager(params, azure_vm_connector=azure_vm_connector)
        network_security_group_manager: VirtualMachineNetworkSecurityGroupManager = \
            VirtualMachineNetworkSecurityGroupManager(params, azure_vm_connector=azure_vm_connector)
        nic_manager: VirtualMachineNICManager = VirtualMachineNICManager(params, azure_vm_connector=azure_vm_connector)
        # vmss_manager: AzureVMScaleSetManager = AzureVMScaleSetManager(params, azure_vm_connector=azure_vm_connector)
        vnet_manager: VirtualMachineVNetManager = VirtualMachineVNetManager(params,
                                                                            azure_vm_connector=azure_vm_connector)

        vms = list(azure_vm_connector.list_all_vms())
        resource_groups = list(azure_vm_connector.list_resource_groups())
        load_balancers = list(azure_vm_connector.list_load_balancers())
        network_security_groups = list(azure_vm_connector.list_network_security_groups())
        network_interfaces = list(azure_vm_connector.list_network_interfaces())
        disks = list(azure_vm_connector.list_disks())
        public_ip_addresses = list(azure_vm_connector.list_public_ip_addresses())
        virtual_networks = list(azure_vm_connector.list_virtual_networks())
        skus = list(azure_vm_connector.list_skus())

        subscription_id = params['secret_data'].get('subscription_id')
        subscription_info = azure_vm_connector.get_subscription_info(subscription_id)
        subscription_data = {
            'subscription_id': subscription_info.subscription_id,
            'subscription_name': subscription_info.display_name,
            'tenant_id': subscription_info.tenant_id
        }

        for vm in vms:
            try:
                vnet_data = None
                subnet_data = None
                lb_vos = []
                resource_group, resource_group_name = self.get_resource_info_in_vm(vm, resource_groups)
                skus_dict = self.get_skus_resource(skus)

                disk_vos = disk_manager.get_disk_info(vm, disks)
                nic_vos, primary_ip = nic_manager.get_nic_info(vm, network_interfaces, public_ip_addresses,
                                                               virtual_networks)

                vm_resource = vm_manager.get_vm_info(vm, disk_vos, nic_vos, resource_group, subscription_id,
                                                     network_security_groups, primary_ip, skus_dict)

                if load_balancers is not None:
                    lb_vos = load_balancer_manager.get_load_balancer_info(vm, load_balancers, public_ip_addresses)

                nsg_vos = network_security_group_manager.get_network_security_group_info(vm, network_security_groups,
                                                                                         network_interfaces)

                nic_name = vm.network_profile.network_interfaces[0].id.split('/')[-1]

                if nic_name is not None:
                    vnet_subnet_dict = vnet_manager.get_vnet_subnet_info(nic_name, network_interfaces, virtual_networks)

                    if vnet_subnet_dict.get('vnet_info'):
                        vnet_data = vnet_subnet_dict['vnet_info']

                    if vnet_subnet_dict.get('subnet_info'):
                        subnet_data = vnet_subnet_dict['subnet_info']

                vm_resource.update({
                    'tags': self.get_tags(vm.tags)
                })

                resource_id = f'/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_resource["name"]}'

                vm_resource['data'].update({
                    'load_balancer': lb_vos,
                    'security_group': nsg_vos,
                    'vnet': vnet_data,
                    'subnet': subnet_data,
                    'subscription': Subscription(subscription_data, strict=False),
                    'azure_monitor': AzureMonitorModel({
                        'resource_id': resource_id
                    }, strict=False),
                    'activity_log': ActivityLog({
                        'resource_uri': resource_id
                    }, strict=False)
                })

                vm_resource['data']['compute']['account'] = subscription_data['subscription_name']
                vm_resource.update({
                    'reference': ReferenceModel({
                        'resource_id': vm_resource['data']['compute']['instance_id'],
                        'external_link': f"https://portal.azure.com/#@.onmicrosoft.com/resource/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_resource['data']['compute']['instance_name']}/overview"
                    }),
                    'account': subscription_data['subscription_id'],
                    'instance_type': vm_resource['data']['compute']['instance_type'],
                    'launched_at': datetime_to_iso8601(vm_resource['data']['compute']['launched_at']),
                    'tags': vm.tags
                })

                self.set_region_code(vm_resource['region_code'])

                vm_resource_vo = VirtualMachineResource(vm_resource, strict=False)
                servers.append(VirtualMachineResponse({'resource': vm_resource_vo}))
            except Exception as e:
                _LOGGER.error(f'[list_instances] [{vm.id}] {e}')

                if type(e) is dict:
                    error_resource_response = ErrorResourceResponse({'message': json.dumps(e)})
                else:
                    error_resource_response = ErrorResourceResponse({'message': str(e), 'resource': {'resource_id': vm.id}})

                errors.append(error_resource_response)

        _LOGGER.debug(f'** VirtualMachine Finished {time.time() - start_time} Seconds **')
        return servers, errors

    @staticmethod
    def get_tags(tags):
        tags_result = []
        if tags:
            for k, v in tags.items():
                tags_result.append({
                    'key': k,
                    'value': v
                })

        return tags_result

    @staticmethod
    def get_resource_info_in_vm(vm, resource_groups):
        for rg in resource_groups:
            vm_info = vm.id.split('/')
            for info in vm_info:
                if info == rg.name.upper():
                    resource_group = rg
                    resource_group_name = rg.name
                    return resource_group, resource_group_name

    @staticmethod
    def get_resources_in_resource_group(resources, resource_group_name):
        infos = []
        for resource in resources:
            id_info = resource.id.split('/')
            for info in id_info:
                if info == resource_group_name.upper():
                    infos.append(resource)
        return infos

    @staticmethod
    def get_skus_resource(skus):
        skus_dict = {}
        for sku in skus:
            if sku.resource_type == 'virtualMachines':
                location = sku.locations[0]
                if location not in skus_dict:
                    skus_dict[location] = []
                info = {}
                # get sku information for discriminating instance type
                info.update({
                    'resource_type': sku.resource_type,
                    'name': sku.name,
                    'tier': sku.tier,
                    'size': sku.size,
                    'family': sku.family,
                })

                # get cpu and memory information
                for capa in sku.capabilities:
                    if capa.name == 'vCPUs':
                        info['core'] = capa.value
                    elif capa.name == 'MemoryGB':
                        info['memory'] = capa.value
                skus_dict[location].append(info)

        return skus_dict
