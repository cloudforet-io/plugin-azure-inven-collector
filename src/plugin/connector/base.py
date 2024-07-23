import os
import logging

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.monitor import MonitorManagementClient

from spaceone.core.connector import BaseConnector

DEFAULT_SCHEMA = 'azure_client_secret'
_LOGGER = logging.getLogger(__name__)


class AzureBaseConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscription_client = None
        self.compute_client = None
        self.network_client = None
        self.sql_client = None
        self.monitor_client = None

    def set_connect(self, secret_data: dict):
        subscription_id = secret_data['subscription_id']

        os.environ["AZURE_SUBSCRIPTION_ID"] = subscription_id
        os.environ["AZURE_TENANT_ID"] = secret_data['tenant_id']
        os.environ["AZURE_CLIENT_ID"] = secret_data['client_id']
        os.environ["AZURE_CLIENT_SECRET"] = secret_data['client_secret']

        credential = DefaultAzureCredential()

        self.subscription_client = SubscriptionClient(credential=credential)
        self.compute_client = ComputeManagementClient(credential=credential, subscription_id=subscription_id)
        self.network_client = NetworkManagementClient(credential=credential, subscription_id=subscription_id)
        self.sql_client = SqlManagementClient(credential=credential, subscription_id=subscription_id)
        self.monitor_client = MonitorManagementClient(credential=credential, subscription_id=subscription_id)

    def get_connector(self, cloud_service_group: str, cloud_service_type: str):
        pass
