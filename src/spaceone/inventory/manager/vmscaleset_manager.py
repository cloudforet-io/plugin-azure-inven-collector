from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.vmscaleset import VmScaleSetConnector
from spaceone.inventory.connector.subscription import SubscriptionConnector
from spaceone.inventory.model.vmscaleset.cloud_service_type import CLOUD_SERVICE_TYPES
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
        # subscription_info = params['subscription_info']

        vm_scale_set_conn: VmScaleSetConnector = self.locator.get_connector(self.connector_name, **params)
        vm_scale_sets = []
        for vm_scale_set in vm_scale_set_conn.list_vm_scale_sets():
            snapshot_dict = self.convert_dictionary(vm_scale_set)
            sku_dict = self.convert_dictionary(vm_scale_set.sku)
            creation_data_dict = self.convert_dictionary(vm_scale_set.creation_data)
            encryption_dict = self.convert_dictionary(vm_scale_set.encryption)

            # update sku_dict
            # switch SnapshotStorageAccountType to snapshot_sku_name for user-friendly words.
            # (ex.Premium_LRS -> Premium SSD, Standard HDD..)
            sku_dict.update({
                'name': self.get_disk_sku_name(sku_dict['name'])
            })

            # update creation_data dict
            # update creation_data_dict >> image_reference_dict
            if vm_scale_set.creation_data.image_reference in snapshot_dict:
                image_reference_dict = self.convert_dictionary(vm_scale_set.creation_data.image_reference)
                creation_data_dict.update({
                    'image_reference': image_reference_dict
                })

            # update creation_data_dict >> gallery_image_reference_dict
            if vm_scale_set.creation_data.gallery_image_reference in snapshot_dict:
                gallery_image_dict = self.convert_dictionary(vm_scale_set.creation_data.gallery_image_reference)
                creation_data_dict.update({
                    'gallery_image_reference': gallery_image_dict
                })

            # update encryption_dict type to user-friendly words
            # (ex.EncryptionAtRestWithPlatformKey -> Platform-managed key...)
            if vm_scale_set.encryption.type is not None:
                if vm_scale_set.encryption.type == 'EncryptionAtRestWithPlatformKey':
                    encryption_type = 'Platform-managed key'
                elif vm_scale_set.encryption.type == 'EncryptionAtRestWithPlatformAndCustomerKeys':
                    encryption_type = 'Platform and customer managed key'
                elif vm_scale_set.encryption.type == 'EncryptionAtRestWithCustomerKey':
                    encryption_type = 'Customer-managed key'

                encryption_dict.update({
                    'type_display': encryption_type
                })

            # update snapshot_dict
            snapshot_dict.update({
                'resource_group': self.get_resource_group_from_id(snapshot_dict['id']),  # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
                'size': snapshot_dict['disk_size_bytes'],
                'sku': sku_dict,
                'creation_data': creation_data_dict,
                'encryption': encryption_dict,
                'incremental_display': self.get_incremental_display(snapshot_dict['incremental'])
            })

            if 'network_access_policy' in snapshot_dict:
                snapshot_dict.update({
                    'network_access_policy_display': self.get_network_access_policy(
                        snapshot_dict['network_access_policy'])
                })

            # get attached vm's name
            managed_by = snapshot_dict['managed_by']
            if managed_by:
                snapshot_dict.update({
                    'managed_by': self.get_attached_vm_name_from_managed_by(snapshot_dict['managed_by'])
                })

            # get source_disk_name from source_resource_id
            source_disk_name = creation_data_dict['source_resource_id']
            if source_disk_name:
                snapshot_dict.update({
                    'source_disk_name': self.get_source_disk_name(creation_data_dict['source_resource_id'])
                })

            # switch tags form
            tags = snapshot_dict.get('tags', {})
            snapshot_dict.update({
                'tags': self.convert_tag_format(tags)
            })

            snapshot_data = Snapshot(snapshot_dict, strict=False)
            snapshot_resource = SnapshotResource({
                'data': snapshot_data,
                'region_code': snapshot_data.location,
                'reference': ReferenceModel(snapshot_data.reference())
            })

            # Must set_region_code method for region collection
            self.set_region_code(snapshot_data['location'])
            vm_scale_sets.append(SnapshotResponse({'resource': snapshot_resource}))

        print(f'** Snapshot Finished {time.time() - start_time} Seconds **')
        return vm_scale_sets

    @staticmethod
    def get_resource_group_from_id(disk_id):
        resource_group = disk_id.split('/')[4].lower()
        return resource_group

    @staticmethod
    def get_attached_vm_name_from_managed_by(managed_by):
        if managed_by:
            attached_vm_name = managed_by.split('/')[8]  # parse attached_ from ID
        return attached_vm_name

    @staticmethod
    def get_disk_sku_name(sku_tier):
        if sku_tier == 'Premium_LRS':
            sku_name = 'Premium SSD'
        elif sku_tier == 'Standard_ZRS':
            sku_name = 'Standard zone'
        elif sku_tier == 'Standard_LRS':
            sku_name = 'Standard HDD'

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
