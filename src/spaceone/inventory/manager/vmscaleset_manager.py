from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.vmscaleset import VmScaleSetConnector
from spaceone.inventory.model.vmscaleset.cloud_service import *
from spaceone.inventory.model.vmscaleset.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.connector.subscription import SubscriptionConnector
from spaceone.inventory.model.vmscaleset.data import *
from datetime import datetime
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
            vm_scale_set_dict = self.convert_dictionary_recursive(self, self.convert_dictionary(vm_scale_set))
            # update vm_scale_set_dict
            vm_scale_set_dict.update({
                'resource_group': self.get_resource_group_from_id(vm_scale_set_dict['id']), # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            if hasattr(vm_scale_set, 'proximity_placement_group'):  # get proximity placement group name from proximity_group_id
                vm_scale_set_dict.update({
                    'proximity_placement_group_display':  self.get_proximity_placement_group_name(vm_scale_set_dict['proximity_placement_group']['id'])
                })

            if hasattr(vm_scale_set, 'automatic_repairs_policy'):
                vm_scale_set_dict.update({
                    'automatic_repairs_policy_display': self.get_automatic_repairs_policy_display(vm_scale_set.automatic_repairs_policy)
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

                vm_instance_dict = self.get_vm_instance_dict(self, vm_instance)
                vm_instances_list.append(vm_instance_dict)

            vm_scale_set_dict['vm_instances'] = vm_instances_list

            # switch tags form
            tags = vm_scale_set_dict.get('tags', {})
            vm_scale_set_dict.update({
                'tags': self.convert_tag_format(tags)
            })

            print("vm_scale_set_dict")
            print(vm_scale_set_dict)

            vm_scale_set_data = VirtualMachineScaleSet(vm_scale_set_dict, strict=False)
            vm_scale_set_resource = VmScaleSetResource({
                'data': vm_scale_set_data,
                'region_code': vm_scale_set_data.location,
                'reference': ReferenceModel(vm_scale_set_data.reference())
            })

            # Must set_region_code method for region collection
            self.set_region_code(vm_scale_set_data['location'])
            # vm_scale_sets.append(VmScaleSetResource({'resource': vm_scale_set_resource})) ;;;;;;;;아나
            vm_scale_sets.append(vm_scale_set_resource)

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
    def get_automatic_repairs_policy_display(automatic_repair_policy):
        if automatic_repair_policy is True:
            automatic_repairs_policy_display = 'Enabled'
        else:
            automatic_repairs_policy_display = 'Disabled'
        return automatic_repairs_policy_display

    # get instance dictionary
    @staticmethod
    def get_vm_instance_dict(self, vm_instances):
        vm_instances_dict = self.convert_dictionary_recursive(self, self.convert_dictionary(vm_instances))
        return vm_instances_dict
