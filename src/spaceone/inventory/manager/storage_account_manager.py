from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.storage_account import StorageAccountConnector
from spaceone.inventory.model.storageaccount.cloud_service import *
from spaceone.inventory.model.storageaccount.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.storageaccount.data import *
import time
import ipaddress
import logging

_LOGGER = logging.getLogger(__name__)


class StorageAccountManager(AzureManager):
    connector_name = 'StorageAccountConnector'
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
                CloudServiceResponse (dict) : dictionary of azure storage account data resource information
        """
        _LOGGER.debug("** Storage Account START **")
        start_time = time.time()

        subscription_info = params['subscription_info']
        storage_account_conn: StorageAccountConnector = self.locator.get_connector(self.connector_name, **params)
        storage_accounts = []
        storage_account_list = storage_account_conn.list_storage_accounts()

        for storage_account in storage_account_list:
            storage_account_dict = self.convert_nested_dictionary(self, storage_account)

            if storage_account_dict.get('network_rule_set') is not None:
                storage_account_dict.update({
                    'network_rule_set': self.get_network_rule_set(self, storage_account_dict['network_rule_set'])
                })
            resource_group = self.get_resource_group_from_id(storage_account_dict['id'])

            if storage_account_dict.get('name') is not None:
                storage_account_dict.update({
                    'container_item': self.list_containers(self, storage_account_conn, resource_group, storage_account_dict['name'])
                })

            if storage_account_dict.get('routing_preference') is not None:
                storage_account_dict.update({
                    'routing_preference_display': 'Internet routing'
                })
            else:
                storage_account_dict.update({
                    'routing_preference_display': 'Microsoft network routing'
                })

            storage_account_dict.update({
                'resource_group': self.get_resource_group_from_id(storage_account_dict['id']),
                # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            _LOGGER.debug(f'[STORAGE ACCOUNT INFO] {storage_account_dict}')

            storage_account_data = StorageAccount(storage_account_dict, strict=False)
            storage_account_resource = StorageAccountResource({
                'data': storage_account_data,
                'region_code': storage_account_data.location,
                'reference': ReferenceModel(storage_account_data.reference()),
                'name': storage_account_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(storage_account_data['location'])
            storage_accounts.append(StorageAccountResponse({'resource': storage_account_resource}))

        _LOGGER.debug(f'** Storage Account Finished {time.time() - start_time} Seconds **')
        return storage_accounts

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split('/')[4]
        return resource_group

    @staticmethod
    def get_public_ip_address(self, application_gateway_conn, resource_group_name, pip_name):
        public_ip_address_obj = application_gateway_conn.get_public_ip_addresses(resource_group_name, pip_name)
        public_ip_address_dict = self.convert_nested_dictionary(self, public_ip_address_obj)

        _LOGGER.debug(f'[Public IP Address]{public_ip_address_dict}')

        return public_ip_address_dict

    @staticmethod
    def get_associated_listener(frontend_ip_configuration_dict, http_listeners_list):
        associated_listener = ''
        for http_listener in http_listeners_list:
            if http_listener.get('frontend_ip_configuration') is not None:
                if frontend_ip_configuration_dict['id'] in http_listener.get('frontend_ip_configuration', {}).get('id', ''):
                    associated_listener = http_listener.get('name', '-')
                else:
                    associated_listener = '-'

        return associated_listener

    @staticmethod
    def get_port(port_id, frontend_ports_list):
        port = 0
        for fe_port in frontend_ports_list:
            if port_id in fe_port['id']:
                port = fe_port.get('port', 0)
                return port
            else:
                return port

    @staticmethod
    def update_backend_pool_dict(backend_pool_list, backend_pool_id, request_rules):
        for backend_pool in backend_pool_list:
            if backend_pool['id'] == backend_pool_id:
                backend_pool.update({
                    'associated_rules': request_rules
                })

    @staticmethod
    def update_rewrite_ruleset_dict(rewrite_rule_sets_list, rewrite_rule_id, applied_rules_list):
        for rewrite_rule in rewrite_rule_sets_list:
            if rewrite_rule['id'] == rewrite_rule_id:
                rewrite_rule.update({
                    'rules_applied': applied_rules_list
                })


    @staticmethod
    def update_http_listeners_list(http_listeners_list, http_listener_id, http_applied_rules):
        for http_listener in http_listeners_list:
            if http_listener['id'] == http_listener_id:
                http_listener.update({
                    'associated_rules': http_applied_rules
                })

    @staticmethod
    def get_network_rule_set(self, network_rule_dict):
        if network_rule_dict.get('virtual_network_rules') is not None:
            network_rule_dict.update({
                'virtual_networks': self.get_virtual_network_names(network_rule_dict['virtual_network_rules']),
                'is_public_access_allowed': False
            })
        if not network_rule_dict.get('virtual_network_rules'): # if virtual_network_rules are empty, this SA is public allowable
            network_rule_dict.update({
                'is_public_access_allowed': True
            })

        if network_rule_dict.get('ip_rules') is not None:
            firewall_address_list = []
            for rule in network_rule_dict['ip_rules']:
                firewall_address_list.append(rule['ip_address_or_range'])

            network_rule_dict.update({
                'firewall_address_range': firewall_address_list
            })

        if network_rule_dict.get('resource_access_rules') is not None:
            resource_access_rules_list = []
            for rule in network_rule_dict['resource_access_rules']:
                try:
                    resource_type = rule.get('resource_id').split('/')[6]
                    resource_access_rules_list.append(resource_type)

                except Exception as e:
                    _LOGGER.error(f'[ERROR: Azure Storage Account Network Rules]: {e}')

            network_rule_dict.update({
                'resource_access_rules_display': resource_access_rules_list
            })

        return network_rule_dict
    

    @staticmethod
    def list_containers(self, storage_conn, rg_name, account_name):
        blob_list = []
        blob_obj = storage_conn.list_blobs(rg_name=rg_name, account_name=account_name)
        for blob in blob_obj:
            blob_dict = self.convert_nested_dictionary(self, blob)
            blob_list.append(blob_dict)

        return blob_list

    @staticmethod
    def get_virtual_network_names(virtual_network_rules):
        names = []
        try:
            for virtual_network_rule in virtual_network_rules:
                name = virtual_network_rule['virtual_network_resource_id'].split('/')[8]
                names.append(name)

        except Exception as e:
            _LOGGER.error(f'[ERROR: Azure Storage Account Network Rule Get Name]: {e}')

        return names
