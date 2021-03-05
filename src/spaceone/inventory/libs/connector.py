import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.monitor import MonitorManagementClient

from spaceone.core.error import *
from spaceone.core.connector import BaseConnector

DEFAULT_SCHEMA = 'azure_client_secret'


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

        super().__init__(transaction=None, config=None)
        self.compute_client = None
        self.resource_client = None
        self.subscription_client = None
        self.network_client = None
        self.sql_client = None
        self.monitor_client = None

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

    def verify(self, **kwargs):
        self.set_connect(**kwargs)
        return "ACTIVE"
