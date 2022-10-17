import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.vm_scale_sets import VmScaleSetsConnector
from spaceone.inventory.model.vm_scale_sets.cloud_service import *
from spaceone.inventory.model.vm_scale_sets.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.vm_scale_sets.data import *

_LOGGER = logging.getLogger(__name__)


class VmScaleSetsManager(AzureManager):
    connector_name = 'VmScaleSetsConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        """
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

        """
        _LOGGER.debug("** VmScaleSet START **")
        start_time = time.time()

        subscription_info = params['subscription_info']

        vm_scale_set_conn: VmScaleSetsConnector = self.locator.get_connector(self.connector_name, **params)
        vm_scale_set_responses = []
        error_responses = []

        vm_scale_sets = vm_scale_set_conn.list_vm_scale_sets()

        for vm_scale_set in vm_scale_sets:
            vm_scale_set_id = ''

            try:
                vm_scale_set_dict = self.convert_nested_dictionary(vm_scale_set)
                vm_scale_set_id = vm_scale_set_dict['id']

                # update vm_scale_set_dict
                vm_scale_set_dict.update({
                    'resource_group': self.get_resource_group_from_id(vm_scale_set_id),  # parse resource_group from ID
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': vm_scale_set_id}
                })

                if vm_scale_set_dict.get('proximity_placement_group'):  # if it has a key -> get value -> check if it isn't None / if no 'Key' ->  return None
                    vm_scale_set_dict.update({
                        'proximity_placement_group_display':  self.get_proximity_placement_group_name(vm_scale_set_dict['proximity_placement_group']['id'])
                    })

                # Get Instance termination notification display
                if vm_scale_set_dict.get('virtual_machine_profile') is not None:
                    if vm_scale_set_dict['virtual_machine_profile'].get('scheduled_events_profile') is not None:
                        if vm_scale_set.virtual_machine_profile['scheduled_events_profile']['terminate_notification_profile']['enable']:
                            terminate_notification_display = 'On'
                        else:
                            terminate_notification_display = 'Off'

                        vm_scale_set_dict.update({
                            'terminate_notification_display': terminate_notification_display
                        })

                    # Convert disks' sku-dict to string display
                    if vm_scale_set_dict['virtual_machine_profile'].get('storage_profile') is not None:
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
                    if vm_scale_set_dict['virtual_machine_profile'].get('os_profile') is not None:
                        vm_scale_set_dict['virtual_machine_profile']['os_profile'].update({
                            'operating_system': self.get_operating_system(vm_scale_set_dict['virtual_machine_profile']['os_profile'])
                        })

                    # Get VM Profile's primary Vnet\
                    if vm_scale_set_dict['virtual_machine_profile'].get('network_profile') is not None:
                        vmss_vm_network_profile_dict = vm_scale_set_dict['virtual_machine_profile']['network_profile']

                        if primary_vnet := self.get_primary_vnet(vmss_vm_network_profile_dict['network_interface_configurations']):
                            vmss_vm_network_profile_dict.update({'primary_vnet': primary_vnet})

                # Add vm instances list attached to VMSS
                vm_instances_list = list()
                instance_count = 0
                resource_group = vm_scale_set_dict['resource_group']
                name = vm_scale_set_dict['name']

                for vm_instance in vm_scale_set_conn.list_vm_scale_set_vms(resource_group, name):
                    instance_count += 1
                    vm_scale_set_dict.update({
                        'instance_count': instance_count
                    })

                    vm_instance_dict = self.get_vm_instance_dict(vm_instance, vm_scale_set_conn,  resource_group, name)
                    vm_instances_list.append(vm_instance_dict)

                vm_scale_set_dict['vm_instances'] = vm_instances_list

                # Get auto scale settings by resource group and vm id
                vm_scale_set_dict.update({
                    'autoscale_settings': self.list_auto_scale_settings_obj(vm_scale_set_conn, resource_group, vm_scale_set_id)
                })

                # Set virtual_machine_scale_set_power_state information
                if vm_scale_set_dict.get('autoscale_settings') is not None:
                    vm_scale_set_dict.update({
                        'virtual_machine_scale_set_power_state': self.list_virtual_machine_scale_set_power_state(vm_scale_set_dict['autoscale_settings']),
                    })

                # update auto_scale_settings to autoscale_setting_resource_collection
                auto_scale_setting_resource_col_dict = dict()
                auto_scale_setting_resource_col_dict.update({
                    'value': self.list_auto_scale_settings(vm_scale_set_conn, resource_group, vm_scale_set_id)
                })

                vm_scale_set_dict.update({
                    'autoscale_setting_resource_collection': auto_scale_setting_resource_col_dict
                })

                vm_scale_set_data = VirtualMachineScaleSet(vm_scale_set_dict, strict=False)
                vm_scale_set_resource = VmScaleSetResource({
                    'data': vm_scale_set_data,
                    'region_code': vm_scale_set_data.location,
                    'reference': ReferenceModel(vm_scale_set_data.reference()),
                    'tags': vm_scale_set_dict.get('tags', {}),
                    'name': vm_scale_set_data.name,
                    'account': vm_scale_set_data.subscription_id,
                    'instance_type': vm_scale_set_data.sku.name
                })

                # Must set_region_code method for region collection
                self.set_region_code(vm_scale_set_data['location'])
                # _LOGGER.debug(f'[VM_SCALE_SET_INFO] {vm_scale_set_resource.to_primitive()}')
                vm_scale_set_responses.append(VmScaleSetResponse({'resource': vm_scale_set_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {vm_scale_set_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Compute', 'VMScaleSet', vm_scale_set_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** VmScaleSet Finished {time.time() - start_time} Seconds **')
        return vm_scale_set_responses, error_responses

    def get_autoscale_rules(self, rules_dict):
        rule_list = list()
        for rule in rules_dict:
            rule_dict = self.convert_nested_dictionary(rule)
            rule_list.append(rule_dict)
        return rule_list

    # Get instances of a virtual machine from a VM scale set
    def get_vm_instance_dict(self, vm_instance, vm_instance_conn, resource_group, vm_scale_set_name):
        vm_instance_dict = self.convert_nested_dictionary(vm_instance)

        # Get instance view of a virtual machine from a VM scale set instance
        if vm_instance_dict.get('instance_id') is not None:
            vm_instance_dict.update({
                'vm_instance_status_profile': self.get_vm_instance_view_dict(vm_instance_conn, resource_group, vm_scale_set_name, vm_instance.instance_id)
            })
        if vm_instance_dict.get('vm_instance_status_profile') is not None:
            if vm_instance_dict['vm_instance_status_profile'].get('vm_agent') is not None:
                vm_instance_dict.update({
                    'vm_instance_status_display': vm_instance_dict['vm_instance_status_profile']['vm_agent']['display_status']
                })

        # Get Primary Vnet display
        if getattr(vm_instance, 'network_profile_configuration') is not None:
            if primary_vnet := self.get_primary_vnet(vm_instance_dict['network_profile_configuration']['network_interface_configurations']):
                vm_instance_dict.update({'primary_vnet': primary_vnet})

        return vm_instance_dict

    # Get instance view of a virtual machine from a VM scale set instance
    def get_vm_instance_view_dict(self, vm_instance_conn, resource_group, vm_scale_set_name, instance_id):
        vm_instance_status_profile = vm_instance_conn.get_vm_scale_set_instance_view(resource_group, vm_scale_set_name, instance_id)
        vm_instance_status_profile_dict = self.convert_nested_dictionary(vm_instance_status_profile)

        if vm_instance_status_profile.vm_agent is not None:
            status_str = None

            for status in vm_instance_status_profile_dict.get('vm_agent').get('statuses'):
                status_str = status['display_status']

            if status_str:
                vm_instance_status_profile_dict['vm_agent'].update({'display_status': status_str})

        return vm_instance_status_profile_dict

    def list_auto_scale_settings(self, vm_scale_set_conn, resource_group_name, vm_scale_set_id):
        auto_scale_settings_list = list()
        auto_scale_settings_obj = vm_scale_set_conn.list_auto_scale_settings(resource_group=resource_group_name)  # List all of the Auto scaling Rules in this resource group

        ''''''
        for auto_scale_setting in auto_scale_settings_obj:
            auto_scale_setting_dict = self.convert_nested_dictionary(auto_scale_setting)
            auto_scale_setting_dict.update({
                 'profiles_display': self.get_autoscale_profiles_display(auto_scale_setting_dict['profiles'])
            })
            if auto_scale_setting_dict['target_resource_uri'].lower() == vm_scale_set_id.lower():  # Compare resources' id
                auto_scale_settings_list.append(auto_scale_setting_dict)

        return auto_scale_settings_list

    def get_autoscale_profiles_list(self, autoscale_setting):
        profiles_list = list()
        for profile in autoscale_setting.profiles:
            profile_dict = self.convert_nested_dictionary(profile)
            profiles_list.append(profile_dict)

        return profiles_list

    def list_virtual_machine_scale_set_power_state(self, autoscale_obj_list):
        power_state_dict = dict()
        power_state_list = list()

        for autoscale_setting in autoscale_obj_list:
            power_state_dict.update({
                'location': autoscale_setting.location,
                'profiles': self.get_autoscale_profiles_list(autoscale_setting),  # profiles_list
                'enabled': autoscale_setting.enabled,
                'name': autoscale_setting.name,
                'notifications': autoscale_setting.notifications,
                'target_resource_uri': autoscale_setting.target_resource_uri,
                'tags': autoscale_setting.tags
            })

            if power_state_dict.get('profiles') is not None:
                power_state_dict.update({
                   'profiles_display': self.get_autoscale_profiles_display(power_state_dict['profiles'])
                })
            power_state_list.append(power_state_dict)
        return power_state_list

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
        vnet_id = None

        # 1) Find Primary NIC
        for nic in network_interface_configurations:
            if nic['primary'] is True:
                # 2) Find primary ip configurations
                for ip_configuration in nic['ip_configurations']:
                    if ip_configuration['primary'] is True:
                        vnet_id = ip_configuration['subnet']['id'].split('/')[8]

        return vnet_id

    @staticmethod
    def list_auto_scale_settings_obj(vm_scale_set_conn, resource_group_name, vm_scale_set_id):
        auto_scale_settings_obj_list = list()
        # all List of the Auto scaling Rules in this resource group
        auto_scale_settings_obj = vm_scale_set_conn.list_auto_scale_settings(resource_group=resource_group_name)

        for auto_scale_setting in auto_scale_settings_obj:
            if auto_scale_setting.target_resource_uri.lower() == vm_scale_set_id.lower():
                auto_scale_settings_obj_list.append(auto_scale_setting)

        return auto_scale_settings_obj_list

    @staticmethod
    def get_autoscale_profiles_display(power_state_profiles):
        profiles_list = list()
        for profile in power_state_profiles:
            profiles_list.append('minimum : ' + str(profile['capacity']['minimum']) + ' / ' + 'maximum : ' + str(profile['capacity']['maximum'] + ' / ' + 'default : ' + profile['capacity']['default']))

        return profiles_list
