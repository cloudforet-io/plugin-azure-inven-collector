from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.disk import *
from spaceone.inventory.model.disk.cloud_service import *
from spaceone.inventory.connector.disk import DiskConnector
from spaceone.inventory.connector.subscription import SubscriptionConnector
from spaceone.inventory.model.disk.cloud_service_type import CLOUD_SERVICE_TYPES
from datetime import datetime
import time


class DiskManager(AzureManager):
    connector_name = 'DiskConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Disk START **")
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

        disk_conn: DiskConnector = self.locator.get_connector(self.connector_name, **params)
        disks = []
        for disk in disk_conn.list_disks():
            disk_dict = self.convert_dictionary(disk)
            sku_dict = self.convert_dictionary(disk.sku)
            creation_data_dict = self.convert_dictionary(disk.creation_data)
            encryption_dict = self.convert_dictionary(disk.encryption)

            # update sku_dict
            # switch DiskStorageAccountType to disk_sku_name for user-friendly words.
            # (ex.Premium SSD, Standard HDD..)
            sku_dict.update({
                'name': self.get_disk_sku_name(sku_dict['name'])
            })

            # update creation_data dict
            if disk.creation_data.image_reference is not None:
                image_reference_dict = self.convert_dictionary(disk.creation_data.image_reference)
                creation_data_dict.update({
                    'image_reference': image_reference_dict
                })

            # update disk_data dict
            disk_dict.update({
                'resource_group': self.get_resource_group_from_id(disk_dict['id']),  # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
                'size': disk_dict['disk_size_bytes'],
                'sku': sku_dict,
                'creation_data': creation_data_dict,
                'encryption': encryption_dict,
                'tier_display': self.get_tier_display(disk_dict['disk_iops_read_write'],
                                                      disk_dict['disk_m_bps_read_write']),
                'network_access_policy_display': self.get_network_access_policy(disk_dict['network_access_policy'])
            })

            # get attached vm's name
            managed_by = disk_dict['managed_by']
            if managed_by is not None:
                managed_by = self.get_attached_vm_name_from_managed_by(disk_dict['managed_by'])
            else:
                managed_by = ''

            disk_dict.update({
                    'managed_by': managed_by
                })

            # switch tags form
            tags = disk_dict.get('tags')
            if tags is not None:
                tags = self.get_tags(disk_dict)
            else:
                tags = []
            disk_dict.update({
                'tags': tags
            })

            disk_data = Disk(disk_dict, strict=False)
            print("----disk_data----")
            print(disk_data.to_primitive())

            disk_resource = DiskResource({
                'data': disk_data,
                'reference': ReferenceModel(disk_data.reference())
            })

            # Must set_region_code method for region collection
            self.set_region_code(disk_data['location'])

        print(f'** Disk Finished {time.time() - start_time} Seconds **')
        return disks

    @staticmethod
    def get_resource_group_from_id(disk_id):
        resource_group = disk_id.split('/')[4].lower()
        return resource_group

    @staticmethod
    def get_attached_vm_name_from_managed_by(managed_by):
        attached_vm_name = managed_by.split('/')[8]
        return attached_vm_name

    @staticmethod
    def get_disk_sku_name(sku_tier):
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
    def get_network_access_policy(network_access_policy):
        if network_access_policy == 'AllowAll':
            network_access_policy_display = 'Public endpoint (all network)'
        elif network_access_policy == 'AllowPrivate':
            network_access_policy_display = 'Private endpoint (through disk access)'
        elif network_access_policy == 'DenyAll':
            network_access_policy_display = 'Deny all'

        return network_access_policy_display

    @staticmethod
    def get_tier_display(disk_iops_read_write, disk_m_bps_read_write):
        tier_display = str(disk_iops_read_write) + ' IOPS' + ', ' + str(disk_m_bps_read_write) + ' Mbps'
        return tier_display

    @staticmethod
    def get_tags(disk_dict):
        tags = []
        for k, v in disk_dict.get('tags', {}).items():
            tags.append({
                'key': k,
                'value': v
            })
        return tags
