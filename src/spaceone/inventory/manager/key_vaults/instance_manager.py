import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.key_vaults import KeyVaultsConnector
from spaceone.inventory.model.key_vaults.cloud_service import *
from spaceone.inventory.model.key_vaults.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.key_vaults.data import *

_LOGGER = logging.getLogger(__name__)


class KeyVaultsManager(AzureManager):
    connector_name = 'KeyVaultsConnector'
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
                CloudServiceResponse (list) : dictionary of azure key vault data resource information
                ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug(f'** Key Vault START **')
        start_time = time.time()

        subscription_info = params['subscription_info']

        key_vault_conn: KeyVaultsConnector = self.locator.get_connector(self.connector_name, **params)
        key_vault_responses = []
        error_responses = []

        key_vaults_obj_list = key_vault_conn.list_all_key_vaults()

        for key_vault in key_vaults_obj_list:
            key_vault_id = ''

            try:
                key_vault_dict = self.convert_nested_dictionary(key_vault)
                key_vault_id = key_vault_dict['id']

                key_vault_dict.update({
                    'resource_group': self.get_resource_group_from_id(key_vault_id),  # parse resource_group from ID
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': key_vault_id}
                })

                resource_group_name = key_vault_dict.get('resource_group', '')
                subscription_id = key_vault_dict.get('subscription_id', '')

                # Get list of keys, secrets
                if key_vault_dict.get('properties', {}).get('vault_uri') is not None:
                    vault_name = key_vault_dict['name']
                    vault_uri = key_vault_dict['properties']['vault_uri']

                    keys = self.list_keys(key_vault_conn, resource_group_name, vault_name)
                    secrets = self.list_secrets(key_vault_conn, subscription_id, vault_uri)
                    certificates = self.list_certificates(key_vault_conn, subscription_id, vault_uri)
                    key_vault_dict.update({
                        'keys': keys,
                        'secrets': secrets,
                        'certificates': certificates
                    })

                # Get name of private connection from ID
                if key_vault_dict.get('properties', {}).get('private_endpoint_connections') is not None:
                    key_vault_dict['properties'].update({
                        'private_endpoint_connections': self.get_private_endpoint_name(
                            key_vault_dict['properties']['private_endpoint_connections'])
                    })

                # Change purge protection to user-friendly word
                if key_vault_dict.get('properties', {}).get('enable_purge_protection') is not None:
                    key_vault_dict['properties'].update({
                        'enable_purge_protection_str': 'Disabled' if key_vault_dict['properties'][
                                                                         'enable_purge_protection'] is False else 'Enabled'
                    })

                # switch tags form

                key_vault_data = KeyVault(key_vault_dict, strict=False)
                key_vault_resource = KeyVaultResource({
                    'data': key_vault_data,
                    'region_code': key_vault_data.location,
                    'reference': ReferenceModel(key_vault_data.reference()),
                    'name': key_vault_data.name,
                    'instance_type': key_vault_data.properties.sku.name,
                    'account': key_vault_data.subscription_id,
                    'tags': key_vault_dict.get('tags', {})
                })

                # Must set_region_code method for region collection
                self.set_region_code(key_vault_data['location'])
                # _LOGGER.debug(f'[KEY VAULT INFO]{key_vault_resource.to_primitive()}')
                key_vault_responses.append(KeyVaultResponse({'resource': key_vault_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {key_vault_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'KeyVault', 'KeyVault', key_vault_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** Key Vault Finished {time.time() - start_time} Seconds **')
        return key_vault_responses, error_responses

    def list_keys(self, key_vault_conn, resource_group_name, vault_name):
        keys = []
        keys_obj_list = key_vault_conn.list_keys(resource_group_name=resource_group_name, vault_name=vault_name)

        if keys_obj_list:
            for key in keys_obj_list:
                key_dict = self.convert_nested_dictionary(key)
                keys.append(key_dict)
        return keys

    def list_secrets(self, key_vault_conn, subscription_id, vault_uri):
        key_vault_secret_client = key_vault_conn.init_key_vault_secret_client(subscription_id=subscription_id,
                                                                              vault_uri=vault_uri)

        secrets = []
        secrets_obj_list = key_vault_secret_client.list_properties_of_secrets()

        if secrets_obj_list:
            for secret in secrets_obj_list:
                secret_dict = self.convert_nested_dictionary(secret)
                secrets.append(secret_dict)
        return secrets

    def list_certificates(self, key_vault_conn, subscription_id, vault_uri):
        key_vault_certificate_client = key_vault_conn.init_key_vault_certificate_client(subscription_id=subscription_id,
                                                                                        vault_uri=vault_uri)

        certificates = []
        certificate_obj_list = key_vault_certificate_client.list_properties_of_certificates()

        if certificate_obj_list:
            for certificate in certificate_obj_list:
                secret_dict = self.convert_nested_dictionary(certificate)
                certificates.append(secret_dict)

        return certificates

    @staticmethod
    def get_private_endpoint_name(private_endpoint_connections):
        for private_endpoint in private_endpoint_connections:
            private_endpoint.update({
                'name': private_endpoint['id'].split('/')[10]
            })
        return private_endpoint_connections
