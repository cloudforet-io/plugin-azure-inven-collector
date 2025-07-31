import datetime
import logging
from typing import Union

import azure.core.exceptions
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.key_vaults.key_vaults_connector import KeyVaultsConnector
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class KeyVaultsManager(AzureBaseManager):
    cloud_service_group = "KeyVaults"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.KeyVault/vaults"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Security"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-key-vault.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        key_vaults_conn = KeyVaultsConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        key_vaults_obj_list = key_vaults_conn.list_all_key_vaults()

        for key_vault in key_vaults_obj_list:

            try:
                key_vault_dict = self.convert_nested_dictionary(key_vault)
                key_vault_id = key_vault_dict["id"]

                key_vault_dict = self.update_tenant_id_from_secret_data(
                    key_vault_dict, secret_data
                )

                key_vault_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            key_vault_id
                        ),  # parse resource_group from ID
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
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
                        key_vaults_conn, resource_group_name, vault_name
                    )

                    for key in keys:
                        key["attributes"].update(
                            {
                                "created": self.timestamp_to_iso8601(
                                    key["attributes"]["created"]
                                ),
                                "updated": self.timestamp_to_iso8601(
                                    key["attributes"]["updated"]
                                ),
                            }
                        )

                    secrets, secrets_permissions_display = self.list_secrets(
                        key_vaults_conn, subscription_id, vault_uri
                    )

                    (
                        certificates,
                        certificates_permissions_display,
                    ) = self.list_certificates(
                        key_vaults_conn, subscription_id, vault_uri
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
                    key_vault_dict["properties"].update(
                        {"enable_purge_protection_str": "Disabled"}
                    )
                    if (
                        key_vault_dict.get("properties", {}).get(
                            "enable_purge_protection"
                        )
                        is not None
                    ):
                        if key_vault_dict["properties"]["enable_purge_protection"]:
                            key_vault_dict["properties"].update(
                                {"enable_purge_protection_str": "Enabled"}
                            )
                    if sku := key_vault_dict.get("properties", {}).get("sku"):
                        key_vault_dict["sku"] = sku

                    self.set_region_code(key_vault_dict["location"])

                    cloud_services.append(
                        make_cloud_service(
                            name=key_vault_dict["name"],
                            cloud_service_type=self.cloud_service_type,
                            cloud_service_group=self.cloud_service_group,
                            provider=self.provider,
                            data=key_vault_dict,
                            account=secret_data["subscription_id"],
                            instance_type=key_vault_dict["properties"]["sku"]["name"],
                            region_code=key_vault_dict["location"],
                            reference=self.make_reference(key_vault_dict.get("id")),
                            tags=key_vault_dict.get("tags", {}),
                            data_format="dict",
                        )
                    )

            except Exception as e:
                _LOGGER.error(
                    f"[create_cloud_service] Error {self.service} {e}", exc_info=True
                )
                error_responses.append(
                    make_error_response(
                        error=e,
                        provider=self.provider,
                        cloud_service_group=self.cloud_service_group,
                        cloud_service_type=self.cloud_service_type,
                    )
                )

        return cloud_services, error_responses

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

    @staticmethod
    def timestamp_to_iso8601(timestamp: int) -> Union[str, None]:
        if isinstance(timestamp, int):
            dt = datetime.datetime.utcfromtimestamp(timestamp)
            return f"{dt.isoformat(timespec='milliseconds')}Z"

        return None
