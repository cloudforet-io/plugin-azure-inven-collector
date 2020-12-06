from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.disk import *
from spaceone.inventory.model.disk.cloud_service import *
from spaceone.inventory.connector.disk import DiskConnector
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
        Response:
            CloudServiceResponse
        """
        secret_data = params['secret_data']
        disk_conn: DiskConnector = self.locator.get_connector(self.connector_name, **params)

        disks = []
        for disk in disk_conn.list_disks():
            # TODO: to be Implemented
            disk_dict = self.convert_dictionary(disk)
            sku_dict = self.convert_dictionary(disk.sku)
            creation_data_dict = self.convert_dictionary(disk.creation_data)

            # update sku_dict
            sku_dict.update({  # switch DiskStorageAccountType to disk_sku_name for user-friendly word.
                # (ex.Premium SSD, Standard HDD..)
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
                'resource_group': self.get_resource_group_from_id(disk_dict['id']),  # parse resource group from ID
                'subscription_id': secret_data['subscription_id'],
                'subscription_name': '',
                'size': disk_dict['disk_size_bytes'],
                'sku': sku_dict,
                'creation_data': creation_data_dict,
            })
            managed_by = disk_dict.get('managed_by')  # get attached vm's name
            if managed_by is not None:
                disk_dict.update({
                    'managedBy': self.get_attached_vm_name_from_managed_by(disk_dict['managed_by'])
                })
            tags = disk_dict.get('tags')  # update tags
            if tags is not None:
                disk_dict.update({
                    'tags': self.get_tags(disk_dict)
                })

            # subscription dict
            subscription_info_dict = {'subscription_id': disk_dict['subscription_id'],
                                      'subscription_name': disk_dict['subscription_name']}
            # self.set_subscription_info(disk_conn, subscription_info_dict)

            print("----disk_dict----")
            print(disk_dict)

            disk_data = Disk(disk_dict, strict=False)
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
    def set_subscription_info(disk_conn, subscription_info_dict):  # 정제 된 애
        # 0. subscription['id' 'name' 'tenant_id'] 배열 만들고
        for subscription_info_dict in disk_conn.get_subscription_info():
            subscription_info_slist = {}
            # subscription_info_dict.update({
            # subscription_info_dict['name']= subscription['id']
            # })
        # 2. API 날려서 return 받고 중복제거 한 new 배열에 넣고
        # 3. id 키 기반으로 tenant 원래 subscription 에 매핑
        return subscription_info_dict

    @staticmethod
    def get_tags(disk_dict):
        tags = []
        for k, v in disk_dict.get('tags', {}).items():
            tags.append({
                'key': k,
                'value': v
            })
        return tags
