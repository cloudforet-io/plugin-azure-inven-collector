from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.key_vault import KeyVaultConnector
from spaceone.inventory.model.keyvault.cloud_service import *
from spaceone.inventory.model.keyvault.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.keyvault.data import *
from spaceone.inventory.error.custom import *
import time
import logging

_LOGGER = logging.getLogger(__name__)


class KeyVaultManager(AzureManager):
    connector_name = 'KeyVaultConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Key Vault START **")
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
        subscription_info = params['subscription_info']

        key_vault_conn: KeyVaultConnector = self.locator.get_connector(self.connector_name, **params)
        key_vaults = []
        key_vaults_obj_list = key_vault_conn.list_all_key_vaults()

        for key_vault in key_vaults_obj_list:
            key_vault_dict = self.convert_nested_dictionary(self, key_vault)

            key_vault_dict.update({
                'resource_group': self.get_resource_group_from_id(key_vault_dict['id']), # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            resource_group_name = key_vault_dict.get('resource_group', '')
            subscription_id = key_vault_dict.get('subscription_id', '')

            # Get list of keys, secrets
            if key_vault_dict.get('properties', {}).get('vault_uri') is not None:
                vault_name = key_vault_dict['name']
                vault_uri = key_vault_dict['properties']['vault_uri']
                try:
                    key_vault_dict.update({
                        'keys': self.list_keys(self, key_vault_conn, resource_group_name, vault_name),
                        'secrets': self.list_secrets(self, key_vault_conn, subscription_id, vault_uri),
                        'certificates': self.list_certificates(self, key_vault_conn, subscription_id, vault_uri)
                    })
                except PermissionError:
                    _LOGGER.error(ERROR_KEY_VAULTS_PERMISSION(field='Key Vaults'))

            # Get name of private connection from ID
            if key_vault_dict.get('properties', {}).get('private_endpoint_connections') is not None:
                key_vault_dict['properties'].update({
                    'private_endpoint_connections': self.get_private_endpoint_name(key_vault_dict['properties']['private_endpoint_connections'])
                })

            print(f'[KEY VAULT INFO] {key_vault_dict}')

            key_vault_data = KeyVault(key_vault_dict, strict=False)
            key_vault_resource = KeyVaultResource({
                'data': key_vault_data,
                'region_code': key_vault_data.location,
                'reference': ReferenceModel(key_vault_data.reference()),
                'name': key_vault_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(key_vault_data['location'])
            key_vaults.append(KeyVaultResponse({'resource': key_vault_resource}))

        print(f'** Key Vault Finished {time.time() - start_time} Seconds **')
        return key_vaults

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split('/')[4]
        return resource_group

    @staticmethod
    def list_keys(self, key_vault_conn, resource_group_name, vault_name):
        try:
            keys = []
            keys_obj_list = key_vault_conn.list_keys(resource_group_name=resource_group_name, vault_name=vault_name)

            if keys_obj_list:
                for key in keys_obj_list:
                    key_dict = self.convert_nested_dictionary(self, key)
                    keys.append(key_dict)
            return keys

        except ValueError:
            _LOGGER.error(ERROR_KEY_VAULTS(field='Key Vaults'))

    @staticmethod
    def list_secrets(self, key_vault_conn, subscription_id, vault_uri):
        try:
            key_vault_secret_client = key_vault_conn.init_key_vault_secret_client(subscription_id=subscription_id, vault_uri=vault_uri)

            secrets = []
            secrets_obj_list = key_vault_secret_client.list_properties_of_secrets()

            if secrets_obj_list:
                for secret in secrets_obj_list:
                    secret_dict = self.convert_nested_dictionary(self, secret)
                    secrets.append(secret_dict)
            return secrets

        except ValueError:
            _LOGGER.error(ERROR_KEY_VAULTS(field='Key Vaults'))

    @staticmethod
    def list_certificates(self, key_vault_conn, subscription_id, vault_uri):
        try:
            key_vault_certificate_client = key_vault_conn.init_key_vault_certificate_client(subscription_id=subscription_id, vault_uri=vault_uri)

            certificates = []
            certificate_obj_list = key_vault_certificate_client.list_properties_of_certificates()

            if certificate_obj_list:
                for certificate in certificate_obj_list:
                    secret_dict = self.convert_nested_dictionary(self, certificate)
                    certificates.append(secret_dict)

            return certificates
        except ValueError:
            _LOGGER.error(ERROR_KEY_VAULTS(field='Key Vaults'))

    @staticmethod
    def get_private_endpoint_name(private_endpoint_connections):
        try:
            for private_endpoint in private_endpoint_connections:
                private_endpoint.update({
                    'name': private_endpoint['id'].split('/')[10]
                })
            return private_endpoint_connections

        except ValueError:
            _LOGGER.error(ERROR_KEY_VAULTS(field='Private Endpoints'))

