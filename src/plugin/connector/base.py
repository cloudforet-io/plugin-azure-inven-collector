import logging
import os

import azure.core.exceptions
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.advisor import AdvisorManagementClient
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.rdbms.mysql_flexibleservers import (
    MySQLManagementClient as MySQLFlexibleManagementClient,
)
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers import (
    PostgreSQLManagementClient as PostgreSQLFlexibleManagementClient,
)
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from azure.mgmt.resourcehealth import ResourceHealthMgmtClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.webpubsub import WebPubSubManagementClient
from spaceone.core.connector import BaseConnector

DEFAULT_SCHEMA = "azure_client_secret"
_LOGGER = logging.getLogger("spaceone")


class AzureBaseConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credential = None
        self.subscription_client = None
        self.compute_client = None
        self.network_client = None
        self.sql_client = None
        self.monitor_client = None
        self.container_instance_client = None
        self.container_registry_client = None
        self.container_service_client = None
        self.resource_client = None
        self.resource_health_client = None
        self.storage_client = None
        self.cosmosdb_client = None
        self.postgre_sql_client = None
        self.postgre_sql_flexible_client = None
        self.web_pubsub_service_client = None
        self.key_vault_client = None
        self.mysql_client = None
        self.mysql_flexible_client = None
        self.advisor_client = None
        self.cognitive_services_client = None
        self.next_link = None

    def set_connect(self, secret_data: dict):
        subscription_id = secret_data["subscription_id"]

        os.environ["AZURE_SUBSCRIPTION_ID"] = subscription_id
        os.environ["AZURE_TENANT_ID"] = secret_data["tenant_id"]
        os.environ["AZURE_CLIENT_ID"] = secret_data["client_id"]
        os.environ["AZURE_CLIENT_SECRET"] = secret_data["client_secret"]

        self.credential = DefaultAzureCredential()

        self.subscription_client = SubscriptionClient(credential=self.credential)
        self.compute_client = ComputeManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.network_client = NetworkManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.sql_client = SqlManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.monitor_client = MonitorManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.container_instance_client = ContainerInstanceManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.container_registry_client = ContainerRegistryManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.container_service_client = ContainerServiceClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.resource_client = ResourceManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.resource_health_client = ResourceHealthMgmtClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.storage_client = StorageManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.cosmosdb_client = CosmosDBManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.postgre_sql_client = PostgreSQLManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.postgre_sql_flexible_client = PostgreSQLFlexibleManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.web_pubsub_service_client = WebPubSubManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.key_vault_client = KeyVaultManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.mysql_client = MySQLManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.mysql_flexible_client = MySQLFlexibleManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.advisor_client = AdvisorManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )
        self.cognitive_services_client = CognitiveServicesManagementClient(
            credential=self.credential, subscription_id=subscription_id
        )

    def get_connector(self, cloud_service_group: str, cloud_service_type: str):
        pass

    def request_azure_api(
        self, url: str, method: str = "GET", parameter: dict = None
    ) -> dict:
        headers = self._make_request_headers()
        try:

            response = requests.request(
                method=method, url=url, headers=headers, json=parameter
            )
            response_json = response.json()

            if isinstance(response_json, dict):
                properties = response_json.get("properties", {})
            else:
                properties = {}

            if properties:
                self.next_link = properties.get("nextLink", None)

            if response_error := response_json.get("error"):
                if response_error.get("code") != "NotFound":
                    raise azure.core.exceptions.HttpResponseError(response_json)
                else:
                    return {}

            return response_json
        except azure.core.exceptions.HttpResponseError as e:
            _LOGGER.error(f"[ERROR] request_azure_api with azure error model :{e}")
            raise
        except Exception as e:
            _LOGGER.error(f"[ERROR] request_azure_api :{e}")
            raise e

    def _make_request_headers(self, client_type=None):
        access_token = self._get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        if client_type:
            headers["ClientType"] = client_type

        return headers

    def _get_access_token(self):
        try:
            # credential = DefaultAzureCredential(logging_enable=True)
            scopes = ["https://management.azure.com/.default"]
            token_info = self.credential.get_token(*scopes)
            return token_info.token
        except Exception as e:
            _LOGGER.error(f"[ERROR] _get_access_token :{e}")
            raise e
