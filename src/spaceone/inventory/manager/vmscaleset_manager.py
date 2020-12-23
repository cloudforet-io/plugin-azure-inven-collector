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
            vm_scale_set_dict = self.convert_dictionary(vm_scale_set)

            if vm_scale_set.plan:
                plan_dict = self.convert_dictionary(vm_scale_set.plan)
                vm_scale_set_dict.update({
                    'plan': plan_dict
                })
            if vm_scale_set.additional_capabilities:
                additional_capabilities_dict = self.convert_dictionary(vm_scale_set.additional_capabilities)
                vm_scale_set_dict.update({
                    'additional_capabilities': additional_capabilities_dict
                })
            if vm_scale_set.identity:
                identity_dict = self.convert_dictionary(vm_scale_set.identity)
                vm_scale_set_dict.update({
                    'identity': identity_dict
                })
            if vm_scale_set.automatic_repairs_policy:
                automatic_repairs_policy_dict = self.convert_dictionary(vm_scale_set.automatic_repairs_policy)
                vm_scale_set_dict.update({
                    'automatic_repairs_policy': automatic_repairs_policy_dict
                })

            if vm_scale_set.host_group:
                host_group_dict = self.convert_dictionary(vm_scale_set.host_group)
                vm_scale_set_dict.update({
                    'host_group': host_group_dict
                })

            if vm_scale_set.proximity_placement_group:
                proximity_placement_group_dict = self.convert_dictionary(vm_scale_set.proximity_placement_group)
                vm_scale_set_dict.update({
                    'proximity_placement_group': proximity_placement_group_dict,
                    'proximity_placement_group_name': self.get_proximity_placement_group_name(proximity_placement_group_dict['id'])
                })

            if vm_scale_set.scale_in_policy:
                scale_in_policy_dict = self.convert_dictionary(vm_scale_set.scale_in_policy)
                vm_scale_set_dict.update({
                    'scale_in_policy': scale_in_policy_dict
                })

            if vm_scale_set.upgrade_policy:
                upgrade_policy_dict = self.get_upgrade_policy_dict(self, vm_scale_set.upgrade_policy)
                vm_scale_set_dict.update({
                    'upgrade_policy': upgrade_policy_dict
                })

            if vm_scale_set.sku:
                sku_dict = self.convert_dictionary(vm_scale_set.sku)
                vm_scale_set_dict.update({
                    'sku': sku_dict
                })

            virtual_machine_profile_dict = self.get_virtual_machine_profile_dict(self,
                                                                                 vm_scale_set.virtual_machine_profile)

            # update vm_scale_set_dict
            vm_scale_set_dict.update({
                # parse resource_group from ID
                'resource_group': self.get_resource_group_from_id(vm_scale_set_dict['id']),
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
                'virtual_machine_profile': virtual_machine_profile_dict,
                'overprovision_display': self.get_overprovision_display(vm_scale_set_dict['overprovision']),
            })

            # Add Repairs policy to the dictionary to display with user-friendly words.
            if vm_scale_set_dict['automatic_repairs_policy'] is not None:
                vm_scale_set_dict.update({
                    'automatic_repairs_policy_display': self.get_automatic_repairs_policy_display(vm_scale_set_dict['automatic_repairs_policy']['enabled'])
                })

            # vm instances 리스트 api날려서 dict에다가 instances list로 첨부하기
            '''
            vm_instances_list = list()
            instance_count = 0
            for vm_instance in vm_scale_set_conn.list_vm_scale_set_vms(vm_scale_set_dict['resource_group'], vm_scale_set_dict['name']):
                instance_count += 1
                vm_scale_set_dict.update({
                    'instance_count': instance_count
                })
                vm_instances_dict = self.vm_instances_dict_update(self, self.convert_dictionary(vm_instance))
                vm_instances_list.append(vm_instances_dict)

            vm_scale_set_dict['vm_instances'] = vm_instances_list
            '''
            print("vm_scale_set_dict")
            print(vm_scale_set_dict)

            # switch tags form
            tags = vm_scale_set_dict.get('tags', {})
            vm_scale_set_dict.update({
                'tags': self.convert_tag_format(tags)
            })

            vm_scale_set_data = VmScaleSet(vm_scale_set_dict, strict=False)
            vm_scale_set_resource = VmScaleSetResource({
                'data': vm_scale_set_data,
                'region_code': vm_scale_set_data.location,
                'reference': ReferenceModel(vm_scale_set_data.reference())
            })

            # Must set_region_code method for region collection
            self.set_region_code(vm_scale_set_data['location'])
            vm_scale_sets.append(VmScaleSetResource({'resource': vm_scale_set_resource}))

        print(f'** VmScaleSet Finished {time.time() - start_time} Seconds **')
        return vm_scale_sets

    @staticmethod
    def get_resource_group_from_id(disk_id):
        resource_group = disk_id.split('/')[4].lower()
        return resource_group

    @staticmethod
    def get_virtual_machine_profile_dict(self, virtual_machine_profile_object):
        vm_dict = dict()

        # 1) get billing_profile_dict
        if virtual_machine_profile_object.billing_profile is not None:
            vm_dict.update({
                'billing_profile': self.convert_dictionary(virtual_machine_profile_object.billing_profile)
            })

        # 2) get_diagnostics_profile_dict
        if virtual_machine_profile_object.diagnostics_profile is not None:
            vm_dict.update({
                'diagnostics_profile': self.get_diagnostics_profile(self,
                                                                    virtual_machine_profile_object.diagnostics_profile)
            })

        # 3) get extension_profile_dict
        if virtual_machine_profile_object.extension_profile is not None:
            vm_dict.update({
                'extension_profile': self.get_extension_dict(self, virtual_machine_profile_object.extension_profile)
            })
        if virtual_machine_profile_object.os_profile is not None:
            vm_dict.update({
                'os_profile': self.get_os_profile_dict(self, virtual_machine_profile_object.os_profile)
            })
        if virtual_machine_profile_object.network_profile is not None:
            vm_dict.update({
                'network_profile': self.get_network_profile_dict(self, virtual_machine_profile_object.network_profile)
            })

        if virtual_machine_profile_object.scheduled_events_profile is not None:
            vm_dict.update({
                'scheduled_events_profile': self.get_scheduled_events_profile(self, virtual_machine_profile_object.scheduled_events_profile)
            })

        if virtual_machine_profile_object.security_profile is not None:
            vm_dict.update({
                'security_profile': self.get_security_profile(self, virtual_machine_profile_object.security_profile)
            })

        if virtual_machine_profile_object.storage_profile is not None:
            vm_dict.update({
                'storage_profile': self.get_storage_profile(self, virtual_machine_profile_object.storage_profile)
            })

        return vm_dict

    @staticmethod
    def get_upgrade_policy_dict(self, upgrade_policy_object):

        def get_automatic_os_upgrade_policy(upgrade_policy_object):
            def get_automatic_os_upgrade_policy_display(enable_automatic_os_upgrade):
                if enable_automatic_os_upgrade is True:
                    enable_automatic_os_upgrade_display = 'Enabled'
                else:
                    enable_automatic_os_upgrade_display = 'Disabled'
                return enable_automatic_os_upgrade_display

            automatic_os_upgrade_policy_dict = self.convert_dictionary(upgrade_policy_object.automatic_os_upgrade_policy)
            automatic_os_upgrade_policy_dict['automatic_os_upgrade_display'] = get_automatic_os_upgrade_policy_display(automatic_os_upgrade_policy_dict['enable_automatic_os_upgrade'])
            return automatic_os_upgrade_policy_dict

        def rolling_upgrade_policy(upgrade_policy_object):
            return self.convert_dictionary(upgrade_policy_object.rolling_upgrade_policy)

        upgrade_policy_dict = self.convert_dictionary(upgrade_policy_object)

        if upgrade_policy_object.automatic_os_upgrade_policy is not None:
            upgrade_policy_dict.update({
                'automatic_os_upgrade_policy': get_automatic_os_upgrade_policy(upgrade_policy_object)
            })

        if upgrade_policy_object.rolling_upgrade_policy is not None:
            upgrade_policy_dict.update({
                'rolling_upgrade_policy': rolling_upgrade_policy(upgrade_policy_object)
            })

        return upgrade_policy_dict

    @staticmethod
    def get_diagnostics_profile(self, diagnostics_object):
        def get_boot_diagnostics(boot_diagnostics_object):
            return self.convert_dictionary(boot_diagnostics_object)

        diagnostics_dict = self.convert_dictionary(diagnostics_object)

        if diagnostics_object.boot_diagnostics is not None:
            diagnostics_dict.update({
                'boot_diagnostics': get_boot_diagnostics(diagnostics_object.boot_diagnostics)
            })

        return diagnostics_dict

    @staticmethod
    def get_extension_dict(self, extension_object):
        extension_dict = self.convert_dictionary(extension_object)
        extension_list = list()

        # extensions list
        for extension in extension_dict['extensions']:
            extensions = self.convert_dictionary(extension)
            extensions['settings'] = str(extensions['settings'])  # convert JSON object to StringType
            extension_list.append(extensions)

        extension_dict.update({
            'extensions': extension_list
        })
        return extension_dict

    @staticmethod
    def get_os_profile_dict(self, os_profile_object):
        def get_operating_system(os_profile_dictionary):
            if os_profile_dictionary['linux_configuration'] is None:
                operating_system = 'Windows'
            else:
                operating_system = 'Linux'
            return operating_system

        def get_linux_configuration(linux_configuration_object):
            def get_vm_agent_display(provision_vm_agent):
                if provision_vm_agent is True:
                    provision_vm_agent_display = 'Enabled'
                else:
                    provision_vm_agent_display = 'Disabled'
                return provision_vm_agent_display

            if linux_configuration_object is not None:
                linux_configuration_dict = self.convert_dictionary(linux_configuration_object)
                linux_configuration_dict.update({
                    'provision_vm_agent_display': get_vm_agent_display(linux_configuration_dict['provision_vm_agent'])
                })
                return linux_configuration_dict

        def get_windows_configuration(windows_configuration_object):
            if windows_configuration_object is not None:
                return self.convert_dictionary(windows_configuration_object)

        def get_secrets(secret_object):
            def get_source_vault(source_vault_object):
                return self.convert_dictionary(source_vault_object)

            def get_vault_certificate(vault_certificate_object):
                # vault_list
                vault_certificates_list = list()
                for vault_certificate in vault_certificate_object:
                    vault_certificate_dict = self.convert_dictionary(vault_certificate)
                    vault_certificates_list.append(vault_certificate_dict)
                return vault_certificates_list

            # secrets list
            secret_list = list()
            for secret in os_profile_dict['secrets']:
                secret_dict = self.convert_dictionary(secret_object)
                secret_dict.update({
                    'source_vault': get_source_vault(secret.source_vault),
                    'vault_certificates': get_vault_certificate(secret.vault_certificates)
                })
                secret_list.append(secret)

            return secret_list

        os_profile_dict = self.convert_dictionary(os_profile_object)
        os_profile_dict.update({
            'linux_configuration': get_linux_configuration(os_profile_object.linux_configuration),
            'secrets': get_secrets(os_profile_object.secrets),
            'windows_configuration': get_windows_configuration(os_profile_object.windows_configuration)
        })
        # get operating system type
        os_profile_dict['operating_system'] = get_operating_system(os_profile_dict)
        return os_profile_dict

    @staticmethod
    def get_network_profile_dict(self, network_object):
        def get_network_interface_configuration(network_profile_dict):
            def get_subnet_dict(subnet_object):
                subnet_dict = self.convert_dictionary(subnet_object)
                return subnet_dict

            def get_public_ip_address_configuration_dict(public_ip_address_configuration_object):

                def get_public_ip_address_configuration_detail(public_ip_address_configuration):
                    def get_public_ip_address_dns_settings(dns_settings_object):
                        return self.convert_dictionary(dns_settings_object)

                    def get_ip_tags(ip_tags_object):
                        ip_tags_list = list()
                        for ip_tag in ip_tags_object:
                            ip_tag_dict = self.convert_dictionary(ip_tag)
                            ip_tags_list.append(ip_tag_dict)
                        return ip_tags_list

                    def get_public_ip_prefix(public_ip_prefix_object):
                        return self.convert_dictionary(public_ip_prefix_object)

                    public_ip_address_configuration_detail_dict = self.convert_dictionary(public_ip_address_configuration)

                    if public_ip_address_configuration_detail_dict['dns_settings'] is not None:
                        public_ip_address_configuration_detail_dict.update({
                            'dns_settings': get_public_ip_address_dns_settings(public_ip_address_configuration_detail_dict['dns_settings']),

                        })

                    if public_ip_address_configuration_detail_dict['ip_tags'] is not None:
                        public_ip_address_configuration_detail_dict.update({
                            'ip_tags': get_ip_tags(public_ip_address_configuration_detail_dict['ip_tags'])
                        })

                    if public_ip_address_configuration_detail_dict['public_ip_prefix'] is not None:
                        public_ip_address_configuration_detail_dict.update({
                            'public_ip_prefix' : get_public_ip_prefix(public_ip_address_configuration_detail_dict['public_ip_prefix'])
                        })
                    return public_ip_address_configuration_detail_dict

                public_ip_address_configuration_dict = self.convert_dictionary(public_ip_address_configuration_object)
                if public_ip_address_configuration_dict['public_ip_address_configuration'] is not None:
                    public_ip_address_configuration_dict.update({
                        'public_ip_address_configuration': get_public_ip_address_configuration_detail(public_ip_address_configuration_dict['public_ip_address_configuration'])
                    })

                return public_ip_address_configuration_dict

            # update ip_configuration_list
            ip_configuration_list = list()
            for ip_configuration in network_profile_dict.ip_configurations:
                ip_configuration_dict = self.convert_dictionary(ip_configuration)
                # ip configuration = subnet + network_security_group
                if ip_configuration_dict['subnet'] is not None:
                    ip_configuration_dict.update({
                        'subnet': get_subnet_dict(ip_configuration.subnet),
                    })

                if ip_configuration_dict['public_ip_address_configuration'] is not None:
                    ip_configuration_dict.update({
                        'public_ip_address_configuration': get_public_ip_address_configuration_dict(
                            ip_configuration.public_ip_address_configuration)
                    })

                ip_configuration_list.append(ip_configuration_dict)

            return ip_configuration_list

        def get_dns_settings(dns_settings_object):
            def get_vmss_network_configuration_dns_settings(dns_servers_object):  # return dns servers list
                dns_servers_list = list()
                for dns_server in dns_servers_object:
                    dns_server = self.convert_dictionary(dns_server)  # 까보면 string이지만 model로 싸여 있는 애를
                    dns_servers_list.append(dns_server)
                return dns_servers_list

            dns_settings_dict = self.convert_dictionary(dns_settings_object)
            dns_settings_dict.update({
                'dns_servers': get_vmss_network_configuration_dns_settings(dns_settings_object.dns_servers)
            })
            return dns_settings_dict

        def get_security_group(security_group_object):
            return self.convert_dictionary(security_group_object)

        network_profile_dict = self.convert_dictionary(network_object)

        def get_network_interface_configurations_list(network_interface_configurations_object):
            def get_enable_accelerated_networking_display(enable_accelerated_networking):
                if enable_accelerated_networking is True:
                    enable_accelerated_networking_display = 'Enabled'
                elif enable_accelerated_networking is False:
                    enable_accelerated_networking_display = 'Disabled'

                return enable_accelerated_networking_display

            # get network interface configuration list
            network_interface_configuration_list = list()
            for network_interface_configuration in network_interface_configurations_object:
                network_interface_configuration_dict = self.convert_dictionary(network_interface_configuration)
                network_interface_configuration_dict.update({
                    'dns_settings': get_dns_settings(network_interface_configuration.dns_settings),
                    'ip_configurations': get_network_interface_configuration(network_interface_configuration),
                    'network_security_group': get_security_group(network_interface_configuration.network_security_group)
                })
                network_interface_configuration_dict['enable_accelerated_networking_display'] = get_enable_accelerated_networking_display(network_interface_configuration_dict['enable_accelerated_networking'])
                network_interface_configuration_dict['vnet'] = network_interface_configuration_dict['name'].split('-')[0]
                network_interface_configuration_list.append(network_interface_configuration_dict)
            return network_interface_configuration_list

        def get_health_probe(network_profile_object):
            def get_api_entity_reference_model(api_entity_reference_object):
                api_entity_reference_dict = self.convert_dictionary(api_entity_reference_object)
                return api_entity_reference_dict

            health_probe_dict = self.convert_dictionary(network_profile_object.health_probe)
            health_probe_dict.update({
                'api_entity_reference_model': get_api_entity_reference_model(health_probe_dict['health_probe'])
            })

            return health_probe_dict

        # update network_profile
        if network_object.health_probe is not None:
            network_profile_dict.update({
                'health_probe': get_health_probe(network_object.health_probe),
            })
        if network_object.network_interface_configurations is not None:
            network_profile_dict.update({
                'network_interface_configurations': get_network_interface_configurations_list(
                    network_profile_dict['network_interface_configurations'])
            })

        return network_profile_dict

    @staticmethod
    def get_scheduled_events_profile(self, scheduled_events_profile_object):
        scheduled_events_profile_dict = self.convert_dictionary(scheduled_events_profile_object)
        if scheduled_events_profile_dict['terminate_notification_profile'] is not None:
            scheduled_events_profile_dict.update({
                'terminate_notification_profile': self.convert_dictionary(scheduled_events_profile_dict['terminate_notification_profile'])
            })
        return scheduled_events_profile_dict

    @staticmethod
    def get_security_profile(self, security_profile_object):
        return self.convert_dictionary(security_profile_object)

    @staticmethod
    def get_storage_profile(self, storage_profile_object):
        def get_data_disks(data_disks_object):
            def get_managed_disk(managed_disk_object):
                managed_disk_dict = self.convert_dictionary(managed_disk_object)
                if managed_disk_dict['disk_encryption_set'] is not None:
                    managed_disk_dict.update({
                        'disk_encryption_set': self.convert_dictionary(managed_disk_object.disk_encryption_set)
                    })
                    # parse disk_encryption_set's name from it's id
                    managed_disk_dict['disk_encryption_set_display'] = managed_disk_dict['disk_encryption_set']['id'].split('/')[8]
                return managed_disk_dict

            data_disks_list = list()
            for data_disk in data_disks_object:
                data_disk_dict = self.convert_dictionary(data_disk)
                if(data_disk_dict['managed_disk']) is not None:
                    data_disk_dict.update({
                        'managed_disk': get_managed_disk(data_disk_dict['managed_disk'])
                    })

                data_disks_list.append(data_disk_dict)
            return data_disks_list

        def get_image_reference(image_reference_object):
            return self.convert_dictionary(image_reference_object)

        def get_os_disk(os_disk_object):
            def get_diff_disk_settings(diff_disk_object):
                diff_disk_dict = self.convert_dictionary(diff_disk_object)
                if diff_disk_dict['option'] is not None:
                    diff_disk_dict.update({
                        'option': self.convert_dictionary(diff_disk_dict['option'])
                    })
                return diff_disk_dict

            def get_image(image_object):
                return self.convert_dictionary(image_object)

            def get_managed_disk(managed_disk_object):
                managed_disk_dict = self.convert_dictionary(managed_disk_object)
                if(managed_disk_dict['disk_encryption_set']) is not None:
                    managed_disk_dict.update({
                        'disk_encryption_set': self.convert_dictionary(managed_disk_dict['disk_encryption_set'])
                    })
                return managed_disk_dict

            def get_vhd_containers(vhd_containers_object):
                vhd_containers_list = list()
                for vhd_container in vhd_containers_object:
                    vhd_containers_list.append(vhd_container)
                return vhd_containers_list

            os_disk_dict = self.convert_dictionary(os_disk_object)
            if os_disk_dict['diff_disk_settings'] is not None:
                os_disk_dict.update({
                    'diff_disk_settings': get_diff_disk_settings(os_disk_dict['diff_disk_settings'])
                })
            if os_disk_dict['image'] is not None:
                os_disk_dict.update({
                    'image': get_image(os_disk_dict['image'])
                })
            if os_disk_dict['managed_disk'] is not None:
                os_disk_dict.update({
                    'managed_disk': get_managed_disk(os_disk_dict['managed_disk'])
                })
            if os_disk_dict['vhd_containers'] is not None:
                os_disk_dict.update({
                    'vhd_containers': get_vhd_containers(os_disk_dict['vhd_containers'])
                })

            return os_disk_dict

        storage_profile_dict = self.convert_dictionary(storage_profile_object)
        if storage_profile_dict['data_disks'] is not None:
            storage_profile_dict.update({
                'data_disks': get_data_disks(storage_profile_dict['data_disks'])
            })
        if storage_profile_dict['image_reference'] is not None:
            storage_profile_dict.update({
                'image_reference': get_image_reference(storage_profile_dict['image_reference'])
            })
            # get os_disk spec in listType (for display)
            image_reference_list = list()
            for image in storage_profile_dict['image_reference'].items():
                image_reference_list.append(list(image))
            storage_profile_dict['os_disk_spec_list'] = image_reference_list

        if storage_profile_dict['os_disk'] is not None:
            storage_profile_dict.update({
                'os_disk': get_os_disk(storage_profile_dict['os_disk'])
            })

        return storage_profile_dict

    @staticmethod
    def convert_diagnostics_recursive(self, diagnostics_object):
        self.diagnostics_dict.update({
            'boot_diagnostics': self.convert_dictionary(diagnostics_object.boot_diagnostics)
        })
        return self.diagnostics_dict

    @staticmethod
    def get_overprovision_display(overprovision):
        if overprovision is True:
            overprovision_display = 'Enabled'
        else:
            overprovision_display = 'Disabled'
        return overprovision_display

    @staticmethod
    def get_proximity_placement_group_name(placement_group_id):
        placement_group_name = placement_group_id.split('/')[8]  # parse placement_group_name from placement_group_id
        return placement_group_name

    @staticmethod
    def get_network_access_policy(network_access_policy):
        if network_access_policy == 'AllowAll':
            network_access_policy_display = 'Public endpoint (all network)'
        elif network_access_policy == 'AllowPrivate':
            network_access_policy_display = 'Private endpoint (through disk access)'
        elif network_access_policy == 'DenyAll':
            network_access_policy_display = 'Deny all'

        return network_access_policy_display

    @staticmethod
    def get_incremental_display(incremental):
        if incremental is False:
            incremental_display = 'Full'
        else:
            incremental_display = 'Incremental'

        return incremental_display

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

    @staticmethod
    def get_instance_count(vm_scale_set_dict):
        return vm_scale_set_dict['instance_count']

    # instance dictionary
    @staticmethod
    def vm_instances_dict_update(self, vm_instances_dict):
        def get_computer_name_from_os_profile(os_profile):
            os_profile_dict = self.convert_dictionary(os_profile)
            return os_profile_dict['computer_name']

        def get_latest_model_display(latest_model_applied):
            if latest_model_applied is True:
                latest_model_display = 'Yes'
            elif latest_model_applied is False:
                latest_model_display = 'No'
            return latest_model_display

        def get_linux_configuration(linux_configuration_object):
            if linux_configuration_object is not None:
                return self.convert_dictionary(linux_configuration_object)

        def get_windows_configuration(windows_configuration_object):
            if windows_configuration_object is not None:
                return self.convert_dictionary(windows_configuration_object)

        if vm_instances_dict['os_profile'] is not None:
            os_profile_dict = self.convert_dictionary(vm_instances_dict['os_profile'])

            # if OS type is Linux
            if os_profile_dict['linux_configuration'] is not None:
                os_profile_dict.update({
                    'linux_configuration': get_linux_configuration(os_profile_dict['linux_configuration'])
                })
            # if OS type is Windows
            if os_profile_dict['windows_configuration'] is not None:
                os_profile_dict.update({
                    'windows_configuration': get_windows_configuration(os_profile_dict['windows_configuration'])
                })

            vm_instances_dict.update({
                'computer_name': get_computer_name_from_os_profile(vm_instances_dict['os_profile'])
            })
        if vm_instances_dict['latest_model_applied'] is not None:
            vm_instances_dict.update({
                'latest_model_applied_display': get_latest_model_display(vm_instances_dict['latest_model_applied'])
            })
        return vm_instances_dict

