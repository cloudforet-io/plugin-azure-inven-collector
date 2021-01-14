from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.vmscaleset import VmScaleSetConnector
from spaceone.inventory.model.vmscaleset.cloud_service import *
from spaceone.inventory.model.vmscaleset.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.vmscaleset.data import *
import time


class VmScaleSetManager(AzureManager):
    connector_name = 'VmScaleSetConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** VmScaleSet START **")
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
                - subscription_info
        Response:
            CloudServiceResponse
        """
        secret_data = params['secret_data']
        subscription_info = params['subscription_info']

        vm_scale_set_conn: VmScaleSetConnector = self.locator.get_connector(self.connector_name, **params)
        vm_scale_sets = []
        for vm_scale_set in vm_scale_set_conn.list_vm_scale_sets():
            # vm_scale_set_dict = self.convert_nested_dictionary(self, self.convert_dictionary(vm_scale_set))
            vm_scale_set_dict = self.convert_nested_dictionary(self, vm_scale_set)
            # update vm_scale_set_dict
            vm_scale_set_dict.update({
                'resource_group': self.get_resource_group_from_id(vm_scale_set_dict['id']),  # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            '''
            hasattr : object 에 name 의 속성이 존재하면 True, 아니면 False
            get(key) : key 가 "없으면" None 리턴 -> key 자체는 있음, 단지 우리 dict 의 value 값이 NoneType 일뿐.. / key 가 없거나 value 자체가 NoneType 인 경우(우리 케이스) 모두 포함함
            '''

            if vm_scale_set_dict.get('proximity_placement_group'):  # key 있으면 -> value 가져옴 -> None 아닌지 검사 / key 없으면 -> None return
                vm_scale_set_dict.update({
                    'proximity_placement_group_display':  self.get_proximity_placement_group_name(vm_scale_set_dict['proximity_placement_group']['id'])
                })

            # Get Instance termination notification display
            if vm_scale_set_dict['virtual_machine_profile'].get('scheduled_events_profile'):
                if vm_scale_set.virtual_machine_profile.scheduled_events_profile.terminate_notification_profile.enable:
                    terminate_notification_display = 'On'
                else:
                    terminate_notification_display = 'Off'
                vm_scale_set_dict.update({
                    'terminate_notification_display': terminate_notification_display
                })

            # Convert disks' sku-dict to string display
            if vm_scale_set_dict['virtual_machine_profile']['storage_profile'].get('image_reference'):
                image_reference_dict = vm_scale_set_dict['virtual_machine_profile']['storage_profile']['image_reference']
                image_reference_str = \
                    str(image_reference_dict['publisher']) + " / " + str(image_reference_dict['offer']) + " / " + str(image_reference_dict['sku']) + " / " + str(image_reference_dict['version'])
                vm_scale_set_dict['virtual_machine_profile']['storage_profile'].update({
                    'image_reference_display': image_reference_str
                })

            # switch storage_account_type to storage_account_type for user-friendly words.
            # (ex.Premium LRS -> Premium SSD, Standard HDD..)
            if vm_scale_set_dict['virtual_machine_profile']['storage_profile'].get('data_disks'):
                for data_disk in vm_scale_set_dict['virtual_machine_profile']['storage_profile']['data_disks']:
                    data_disk['managed_disk'].update({
                        'storage_type': self.get_disk_storage_type(data_disk['managed_disk']['storage_account_type'])
                    })

            # Get VM Profile's operating_system type (Linux or Windows)
            vm_scale_set_dict['virtual_machine_profile']['os_profile'].update({
                'operating_system': self.get_operating_system(vm_scale_set_dict['virtual_machine_profile']['os_profile'])
            })

            # Get VM Profile's primary Vnet
            vmss_vm_network_profile_dict = vm_scale_set_dict['virtual_machine_profile']['network_profile']
            vmss_vm_network_profile_dict.update({
                'primary_vnet': self.get_primary_vnet(vmss_vm_network_profile_dict['network_interface_configurations'])
            })

            # Add vm instances list attached to VMSS
            vm_instances_list = list()
            instance_count = 0
            for vm_instance in vm_scale_set_conn.list_vm_scale_set_vms(vm_scale_set_dict['resource_group'],
                                                                       vm_scale_set_dict['name']):
                instance_count += 1
                vm_scale_set_dict.update({
                    'instance_count': instance_count
                })

                vm_instance_dict = self.get_vm_instance_dict(self, vm_instance, vm_scale_set_conn, vm_scale_set_dict['resource_group'],  vm_scale_set_dict['name'])
                vm_instances_list.append(vm_instance_dict)

            vm_scale_set_dict['vm_instances'] = vm_instances_list

            # switch tags form
            tags = vm_scale_set_dict.get('tags', {})
            vm_scale_set_dict.update({
                'tags': self.convert_tag_format(tags)
            })

            vm_scale_set_data = VirtualMachineScaleSet(vm_scale_set_dict, strict=False)
            vm_scale_set_resource = VmScaleSetResource({
                'data': vm_scale_set_data,
                'region_code': vm_scale_set_data.location,
                'reference': ReferenceModel(vm_scale_set_data.reference())
            })

            # Must set_region_code method for region collection
            self.set_region_code(vm_scale_set_data['location'])
            vm_scale_sets.append(VmScaleSetResponse({'resource': vm_scale_set_resource}))

        print(f'** VmScaleSet Finished {time.time() - start_time} Seconds **')
        return vm_scale_sets

    @staticmethod
    def get_resource_group_from_id(disk_id):
        resource_group = disk_id.split('/')[4].lower()
        return resource_group

    @staticmethod
    def get_proximity_placement_group_name(placement_group_id):
        placement_group_name = placement_group_id.split('/')[8]  # parse placement_group_name from placement_group_id
        return placement_group_name

    @staticmethod
    def get_source_disk_name(source_resource_id):
        source_disk_name = source_resource_id.split('/')[8]  # parse source_disk_name from source_resource_id
        return source_disk_name

    @staticmethod
    def get_disk_storage_type(sku_tier):
        if sku_tier == 'Premium_LRS':
            sku_name = 'Premium SSD'
        elif sku_tier == 'StandardSSD_LRS':
            sku_name = 'Standard SSD'
        elif sku_tier == 'Standard_LRS':
            sku_name = 'Standard HDD'
        else:
            sku_name = 'Ultra SSD'
        return sku_name

    @staticmethod
    def get_operating_system(os_profile_dictionary):
        if os_profile_dictionary['linux_configuration'] is None:
            operating_system = 'Windows'
        else:
            operating_system = 'Linux'
        return operating_system

    @staticmethod
    def get_primary_vnet(network_interface_configurations):
        # 1) Find Primary NIC
        for nic in network_interface_configurations:
            if nic['primary'] is True:
                # 2) Find primary ip configurations
                for ip_configuration in nic['ip_configurations']:
                    if ip_configuration['primary'] is True:
                        vnet_id = ip_configuration['subnet']['id'].split('/')[8]
        return vnet_id

    # Get instances of a virtual machine from a VM scale set
    @staticmethod
    def get_vm_instance_dict(self, vm_instance, vm_instance_conn, resource_group, vm_scale_set_name):
        vm_instance_dict = self.convert_nested_dictionary(self, vm_instance)
        vm_instance_status_dict = self.get_vm_instance_view_dict(self, vm_instance_conn, resource_group, vm_scale_set_name, vm_instance.instance_id)
        vm_instance_dict['vm_instance_status_profile'] = vm_instance_status_dict  # Get instance view of a virtual machine from a VM scale set instance

        # Get Primary Vnet display
        if getattr(vm_instance, 'network_profile_configuration') is not None:
            vm_instance_dict.update({
                'primary_vnet': self.get_primary_vnet(vm_instance_dict['network_profile_configuration']['network_interface_configurations'])
            })

        return vm_instance_dict

    # Get instance view of a virtual machine from a VM scale set instance
    @staticmethod
    def get_vm_instance_view_dict(self, vm_instance_conn, resource_group, vm_scale_set_name, instance_id):
        vm_instance_status_profile = vm_instance_conn.get_vm_scale_set_instance_view(resource_group, vm_scale_set_name, instance_id)
        vm_instance_status_profile_dict = self.convert_nested_dictionary(self, vm_instance_status_profile)

        for status in vm_instance_status_profile_dict['vm_agent']['statuses']:
            status_str = status['display_status']

        vm_instance_status_profile_dict['vm_agent'].update({
                'display_status': status_str
        })

        return vm_instance_status_profile_dict
