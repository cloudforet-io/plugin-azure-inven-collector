import unittest
import time
import os
from datetime import datetime, timedelta
from unittest.mock import patch
from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core import utils
from spaceone.inventory.error import *
from spaceone.inventory.connector.mysql_server import MySQLServerConnector
from spaceone.inventory.manager.mysql_server_manager import MySQLServerManager


class TestMySQLServerManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')

        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})
        cls.subscription_info = test_config.get('SUBSCRIPTION_INFO', {})

        cls.mysql_servers_connector = MySQLServerConnector(transaction=Transaction(), config={}, secret_data=cls.azure_credentials)
        cls.mysql_servers_manager = MySQLServerManager(Transaction())

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_collect_cloud_service(self, *args):
        secret_data = self.azure_credentials
        subscription_info = self.subscription_info
        params = {'options': {}, 'secret_data': secret_data, 'filter': {}, 'subscription_info': subscription_info}

        mysql_servers = self.mysql_servers_manager.collect_cloud_service(params)

        for mysql_server in mysql_servers:
            print(mysql_server.to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)