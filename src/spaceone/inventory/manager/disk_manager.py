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
            # 여기 요부분.. 함수로 뺄까
            if disk.creation_data.image_reference is not None:
                image_reference_dict = self.convert_dictionary(disk.creation_data.image_reference)
                creation_data_dict.update({
                    'image_reference': image_reference_dict
                })

            managed_by = disk_dict.get('managed_by')
            disk_dict.update({
                'resource_group': self.get_resource_group_from_id(disk_dict['id']),
                'size': disk_dict['disk_size_bytes'],
                'sku': sku_dict,
                'creation_data': creation_data_dict
            })

            if managed_by is not None:
                disk_dict.update({
                    'managedBy': self.get_attached_vm_name_from_managed_by(disk_dict['managed_by'])
                })

            print("----disk_dict----")
            print(disk_dict)

            disk_data = Disk(disk_dict, strict=False)
            print(disk_data.to_primitive())

            disk_resource = DiskResource({
                'data': disk_data,
                'reference': ReferenceModel(disk_data.reference())
            })

            '''
            sku_resource = DiskResource({
                'data': sku_data
            })
            '''
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
