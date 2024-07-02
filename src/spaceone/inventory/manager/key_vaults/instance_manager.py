import time
import logging

import azure.core.exceptions

from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.key_vaults import KeyVaultsConnector
from spaceone.inventory.model.key_vaults.cloud_service import *
from spaceone.inventory.model.key_vaults.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.key_vaults.data import *

_LOGGER = logging.getLogger(__name__)


class KeyVaultsManager(AzureManager):
    connector_name = "KeyVaultsConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params: dict):
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
        _LOGGER.debug(f"** Key Vault START **")
        start_time = time.time()

        subscription_info = params["subscription_info"]

        key_vault_conn: KeyVaultsConnector = self.locator.get_connector(
            self.connector_name, **params
        )

        key_vault_responses = []
        error_responses = []

        key_vaults_obj_list = key_vault_conn.list_all_key_vaults()

        for key_vault in key_vaults_obj_list:
            key_vault_id = ""

            try:
                key_vault_dict = self.convert_nested_dictionary(key_vault)
                key_vault_id = key_vault_dict["id"]

                key_vault_dict = self.update_tenant_id_from_secret_data(
                    key_vault_dict, params.get("secret_data", {})
                )

                key_vault_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            key_vault_id
                        ),  # parse resource_group from ID
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["subscription_name"],
                        "azure_monitor": {"resource_id": key_vault_id},
                    }
                )

                resource_group_name = key_vault_dict.get("resource_group", "")
                subscription_id = key_vault_dict.get("subscription_id", "")

                # Get list of keys, secrets
                if key_vault_dict.get("properties", {}).get("vault_uri") is not None:
                    vault_name = key_vault_dict["name"]
                    vault_uri = key_vault_dict["properties"]["vault_uri"]

                    keys = self.list_keys(
                        key_vault_conn, resource_group_name, vault_name
                    )
                    secrets, secrets_permissions_display = self.list_secrets(
                        key_vault_conn, subscription_id, vault_uri
                    )
                    (
                        certificates,
                        certificates_permissions_display,
                    ) = self.list_certificates(
                        key_vault_conn, subscription_id, vault_uri
                    )

                    key_vault_dict.update(
                        {
                            "keys": keys,
                            "secrets": secrets,
                            "certificates": certificates,
                            "key_count": len(keys),
                            "secret_count": len(secrets),
                            "certificate_count": len(certificates),
                            "total_credentials_count": len(keys)
                            + len(secrets)
                            + len(certificates),
                            "keys_permissions_description_display": "Microsoft.KeyVault/vaults/read",
                            "secrets_permissions_description_display": secrets_permissions_display,
                            "certificates_permissions_description_display": certificates_permissions_display,
                        }
                    )

                # Get name of private connection from ID
                if (
                    key_vault_dict.get("properties", {}).get(
                        "private_endpoint_connections"
                    )
                    is not None
                ):
                    key_vault_dict["properties"].update(
                        {
                            "private_endpoint_connections": self.get_private_endpoint_name(
                                key_vault_dict["properties"][
                                    "private_endpoint_connections"
                                ]
                            )
                        }
                    )

                # Change purge protection to user-friendly word
                if (
                    key_vault_dict.get("properties", {}).get("enable_purge_protection")
                    is not None
                ):
                    key_vault_dict["properties"].update(
                        {
                            "enable_purge_protection_str": "Disabled"
                            if key_vault_dict["properties"]["enable_purge_protection"]
                            is False
                            else "Enabled"
                        }
                    )
                if sku := key_vault_dict.get("properties", {}).get("sku"):
                    key_vault_dict["sku"] = sku

                # switch tags form

                key_vault_data = KeyVault(key_vault_dict, strict=False)

                key_vault_resource = KeyVaultResource(
                    {
                        "data": key_vault_data,
                        "region_code": key_vault_data.location,
                        "reference": ReferenceModel(key_vault_data.reference()),
                        "name": key_vault_data.name,
                        "instance_type": key_vault_data.properties.sku.name,
                        "account": key_vault_data.subscription_id,
                        "tags": key_vault_dict.get("tags", {}),
                    }
                )

                # Must set_region_code method for region collection
                self.set_region_code(key_vault_data["location"])
                # _LOGGER.debug(f'[KEY VAULT INFO]{key_vault_resource.to_primitive()}')
                key_vault_responses.append(
                    KeyVaultResponse({"resource": key_vault_resource})
                )

            except Exception as e:
                _LOGGER.error(f"[list_instances] {key_vault_id} {e}", exc_info=True)
                error_resource_response = self.generate_resource_error_response(
                    e, "KeyVault", "KeyVault", key_vault_id
                )
                error_responses.append(error_resource_response)

        _LOGGER.debug(f"** Key Vault Finished {time.time() - start_time} Seconds **")
        return key_vault_responses, error_responses

    def list_keys(self, key_vault_conn, resource_group_name, vault_name):
        keys = []
        keys_obj_list = key_vault_conn.list_keys(
            resource_group_name=resource_group_name, vault_name=vault_name
        )

        if keys_obj_list:
            for key in keys_obj_list:
                key_dict = self.convert_nested_dictionary(key)
                keys.append(key_dict)
        return keys

    def list_secrets(self, key_vault_conn, subscription_id, vault_uri):
        secrets = []
        permissions_display = "Microsoft.KeyVault/vaults/secrets/read, Microsoft.KeyVault/vaults/secrets/readMetadata/action"

        try:
            key_vault_secret_client = key_vault_conn.init_key_vault_secret_client(
                subscription_id=subscription_id, vault_uri=vault_uri
            )

            secrets_obj_list = key_vault_secret_client.list_properties_of_secrets()

            if secrets_obj_list:
                for secret in secrets_obj_list:
                    secret_dict = self.convert_nested_dictionary(secret)
                    secrets.append(secret_dict)
        except azure.core.exceptions.HttpResponseError as e:
            _LOGGER.error(f"[list_secrets] {e}", exc_info=True)
            permissions_display = "If you want to see the secretes list, please grant 'List' permission(Microsoft.KeyVault/vaults/secrets/read, Microsoft.KeyVault/vaults/secrets/readMetadata/action) to the service principal. or assign built-in role KeyVault Reader to the service principal.(https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide?tabs=azure-cli#azure-built-in-roles-for-key-vault-data-plane-operations)"
        return secrets, permissions_display

    def list_certificates(self, key_vault_conn, subscription_id, vault_uri):
        certificates = []
        permissions_display = "Microsoft.KeyVault/vaults/secrets/readMetadata/action, Microsoft.KeyVault/vaults/certificates/read"
        try:
            key_vault_certificate_client = (
                key_vault_conn.init_key_vault_certificate_client(
                    subscription_id=subscription_id, vault_uri=vault_uri
                )
            )

            certificate_obj_list = (
                key_vault_certificate_client.list_properties_of_certificates()
            )

            if certificate_obj_list:
                for certificate in certificate_obj_list:
                    secret_dict = self.convert_nested_dictionary(certificate)
                    certificates.append(secret_dict)
        except azure.core.exceptions.HttpResponseError as e:
            _LOGGER.error(f"[list_secrets] {e}", exc_info=True)
            permissions_display = "If you want to see the secretes list, please grant 'List' permission(Microsoft.KeyVault/vaults/secrets/read, Microsoft.KeyVault/vaults/secrets/readMetadata/action) to the service principal. or assign built-in role 'KeyVault Reader' to the service principal.(https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide?tabs=azure-cli#azure-built-in-roles-for-key-vault-data-plane-operations)"

        return certificates, permissions_display

    @staticmethod
    def get_private_endpoint_name(private_endpoint_connections):
        for private_endpoint in private_endpoint_connections:
            private_endpoint.update({"name": private_endpoint["id"].split("/")[10]})
        return private_endpoint_connections
