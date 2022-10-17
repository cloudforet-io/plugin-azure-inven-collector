import time
import logging
from spaceone.core.utils import *
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.disks.cloud_service import *
from spaceone.inventory.connector.disks import DisksConnector
from spaceone.inventory.model.disks.cloud_service_type import CLOUD_SERVICE_TYPES

_LOGGER = logging.getLogger(__name__)


class DisksManager(AzureManager):
    connector_name = 'DisksConnector'
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
                CloudServiceResponse (list) : dictionary of azure disk data resource information
                ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug(f'** Disk START **')
        start_time = time.time()
        subscription_info = params['subscription_info']

        disk_conn: DisksConnector = self.locator.get_connector(self.connector_name, **params)
        disk_responses = []
        error_responses = []

        disks = disk_conn.list_disks()
        for disk in disks:
            disk_id = ''

            try:
                disk_dict = self.convert_nested_dictionary(disk)
                disk_id = disk_dict['id']

                # Switch DiskStorageAccountType to disk_sku_name for user-friendly words. (ex.Premium SSD, Standard HDD..)
                if disk_dict.get('sku') is not None:
                    sku_dict = disk_dict['sku']
                    sku_dict.update({
                        'name': self.get_disk_sku_name(sku_dict['name'])
                    })
                    disk_dict.update({
                        'sku': sku_dict
                    })

                # update disk_data dict
                disk_dict.update({
                    'resource_group': self.get_resource_group_from_id(disk_dict['id']),  # parse resource_group from ID
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'size': disk_dict['disk_size_bytes'],
                    'tier_display': self.get_tier_display(disk_dict['disk_iops_read_write'],
                                                          disk_dict['disk_m_bps_read_write']),
                    'azure_monitor': {'resource_id': disk_id},
                    'time_created': datetime_to_iso8601(disk_dict['time_created'])
                })

                # Update Network access policy to user-friendly words
                if disk_dict.get('network_access_policy') is not None:
                    disk_dict.update({
                        'network_access_policy_display': self.get_network_access_policy(
                            disk_dict['network_access_policy'])
                    })

                # get attached vm's name
                if disk_dict.get('managed_by') is not None:
                    managed_by = disk_dict['managed_by']
                    disk_dict.update({
                        'managed_by': self.get_attached_vm_name_from_managed_by(managed_by)
                    })

                disk_data = Disk(disk_dict, strict=False)

                disk_resource = DiskResource({
                    'data': disk_data,
                    'region_code': disk_data.location,
                    'reference': ReferenceModel(disk_data.reference()),
                    'tags': disk_dict.get('tags', {}),
                    'name': disk_data.name,
                    'account': disk_data.subscription_id,
                    'instance_type': disk_data.sku.name,
                    'instance_size': float(disk_data.disk_size_gb)
                })

                # Must set_region_code method for region collection
                self.set_region_code(disk_data['location'])
                # _LOGGER.debug(f'[DISK INFO: {disk_resource.to_primitive()}]')
                disk_responses.append(DiskResponse({'resource': disk_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {disk_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, resource_id=disk_id,
                                                                                cloud_service_group='Compute',
                                                                                cloud_service_type='Disk')
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** Disk Finished {time.time() - start_time} Seconds **')
        return disk_responses, error_responses

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
        network_access_policy_display = ''
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
