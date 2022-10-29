import os
import logging

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.webpubsub import WebPubSubManagementClient
from spaceone.core.connector import BaseConnector

DEFAULT_SCHEMA = 'azure_client_secret'
_LOGGER = logging.getLogger(__name__)


class AzureConnector(BaseConnector):

    def __init__(self, **kwargs):
        """
        kwargs
            - schema
            - options
            - secret_data

        secret_data(dict)
            - type: ..
            - project_id: ...
            - token_uri: ...
            - ...
        """

        super().__init__(transaction=None, connector_conf=None)
        self.compute_client = None
        self.resource_client = None
        self.subscription_client = None
        self.network_client = None
        self.sql_client = None
        self.monitor_client = None
        self.storage_client = None
        self.blob_client = None
        self.key_vault_client = None
        self.mysql_client = None
        self.cosmosdb_client = None
        self.postgre_sql_client = None
        self.container_instance_client = None
        self.web_pubsub_service_client = None

    def set_connect(self, secret_data):
        subscription_id = secret_data['subscription_id']

        os.environ["AZURE_SUBSCRIPTION_ID"] = subscription_id
        os.environ["AZURE_TENANT_ID"] = secret_data['tenant_id']
        os.environ["AZURE_CLIENT_ID"] = secret_data['client_id']
        os.environ["AZURE_CLIENT_SECRET"] = secret_data['client_secret']

        credential = DefaultAzureCredential()

        self.compute_client = ComputeManagementClient(credential=credential, subscription_id=subscription_id)
        self.resource_client = ResourceManagementClient(credential=credential, subscription_id=subscription_id)
        self.network_client = NetworkManagementClient(credential=credential, subscription_id=subscription_id)
        self.subscription_client: SubscriptionClient = SubscriptionClient(credential=credential)
        self.sql_client = SqlManagementClient(credential=credential, subscription_id=subscription_id)
        self.monitor_client = MonitorManagementClient(credential=credential, subscription_id=subscription_id)
        self.storage_client = StorageManagementClient(credential=credential, subscription_id=subscription_id)
        self.key_vault_client = KeyVaultManagementClient(credential=credential, subscription_id=subscription_id)
        self.mysql_client = MySQLManagementClient(credential=credential, subscription_id=subscription_id)
        self.cosmosdb_client = CosmosDBManagementClient(credential=credential, subscription_id=subscription_id)
        self.postgre_sql_client = PostgreSQLManagementClient(credential=credential, subscription_id=subscription_id)
        self.container_instance_client = ContainerInstanceManagementClient(credential=credential, subscription_id=subscription_id)
        self.web_pubsub_service_client = WebPubSubManagementClient(credential=credential, subscription_id=subscription_id)

    def verify(self, **kwargs):
        self.set_connect(kwargs['secret_data'])
        return "ACTIVE"
