import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.snapshots.cloud_service import *
from spaceone.inventory.connector.snapshots import SnapshotsConnector
from spaceone.inventory.model.snapshots.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.core.utils import *

_LOGGER = logging.getLogger(__name__)


class SnapshotsManager(AzureManager):
    connector_name = 'SnapshotsConnector'
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
                CloudServiceResponse (list) : dictionary of azure snapshot data resource information
                ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug("** Snapshot START **")
        start_time = time.time()

        subscription_info = params['subscription_info']

        snapshot_conn: SnapshotsConnector = self.locator.get_connector(self.connector_name, **params)
        snapshot_responses = []
        error_responses = []

        snapshots = snapshot_conn.list_snapshots()

        for snapshot in snapshots:
            snapshot_id = ''
            try:
                snapshot_dict = self.convert_nested_dictionary(snapshot)
                snapshot_id = snapshot_dict['id']

                # update sku_dict
                # switch SnapshotStorageAccountType to snapshot_sku_name for user-friendly words.
                # (ex.Premium_LRS -> Premium SSD, Standard HDD..)
                sku_dict = snapshot_dict.get('sku', {})
                sku_dict.update({
                    'name': self.get_disk_sku_name(sku_dict.get('name', ''))
                })

                # update encryption_dict type to user-friendly words
                # (ex.EncryptionAtRestWithPlatformKey -> Platform-managed key...)
                if snapshot_dict.get('encryption', {}).get('type') is not None:
                    type = snapshot_dict['encryption']['type']
                    encryption_type = ''
                    if type == 'EncryptionAtRestWithPlatformKey':
                        encryption_type = 'Platform-managed key'
                    elif type == 'EncryptionAtRestWithPlatformAndCustomerKeys':
                        encryption_type = 'Platform and customer managed key'
                    elif type == 'EncryptionAtRestWithCustomerKey':
                        encryption_type = 'Customer-managed key'

                    snapshot_dict['encryption'].update({
                        'type_display': encryption_type
                    })

                # update snapshot_dict
                snapshot_dict.update({
                    'resource_group': self.get_resource_group_from_id(snapshot_id),  # parse resource_group from ID
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'size': snapshot_dict['disk_size_bytes'],
                    'sku': sku_dict,
                    'incremental_display': self.get_incremental_display(snapshot_dict['incremental']),
                    'azure_monitor': {'resource_id': snapshot_id},
                    'time_created': datetime_to_iso8601(snapshot_dict['time_created'])
                })

                if snapshot_dict.get('network_access_policy') is not None:
                    snapshot_dict.update({
                        'network_access_policy_display': self.get_network_access_policy(snapshot_dict['network_access_policy'])
                    })

                # get attached vm's name
                if snapshot_dict.get('managed_by') is not None:
                    snapshot_dict.update({
                        'managed_by': self.get_attached_vm_name_from_managed_by(snapshot_dict['managed_by'])
                    })

                # get source_disk_name from source_resource_id
                if snapshot_dict.get('creation_data') is not None:
                    source_resource_id = snapshot_dict['creation_data'].get('source_resource_id', '')
                    snapshot_dict.update({
                        'source_disk_name': self.get_source_disk_name(source_resource_id)
                    })

                snapshot_data = Snapshot(snapshot_dict, strict=False)
                snapshot_resource = SnapshotResource({
                    'data': snapshot_data,
                    'region_code': snapshot_data.location,
                    'reference': ReferenceModel(snapshot_data.reference()),
                    'tags': snapshot_dict.get('tags', {}),
                    'name': snapshot_data.name,
                    'account': snapshot_data.subscription_id,
                    'instance_size': float(snapshot_data.disk_size_gb),
                    'instance_type': snapshot_data.sku.name
                })

                # Must set_region_code method for region collection
                self.set_region_code(snapshot_data['location'])
                # _LOGGER.debug(f'[SNAPSHOT INFO] {snapshot_resource.to_primitive()}')
                snapshot_responses.append(SnapshotResponse({'resource': snapshot_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {snapshot_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Compute', 'Snapshot', snapshot_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** Snapshot Finished {time.time() - start_time} Seconds **')
        return snapshot_responses, error_responses

    @staticmethod
    def get_attached_vm_name_from_managed_by(managed_by):
        attached_vm_name = ''
        if managed_by:
            attached_vm_name = managed_by.split('/')[8]  # parse attached_ from ID
        return attached_vm_name

    @staticmethod
    def get_disk_sku_name(sku_tier):
        sku_name = ''
        if sku_tier == 'Premium_LRS':
            sku_name = 'Premium SSD'
        elif sku_tier == 'Standard_ZRS':
            sku_name = 'Standard zone'
        elif sku_tier == 'Standard_LRS':
            sku_name = 'Standard HDD'

        return sku_name

    @staticmethod
    def get_network_access_policy(network_access_policy):
        network_access_policy_display = ''
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
        source_disk_name = ''
        if source_resource_id:
            source_disk_name = source_resource_id.split('/')[8]  # parse source_disk_name from source_resource_id
        return source_disk_name
