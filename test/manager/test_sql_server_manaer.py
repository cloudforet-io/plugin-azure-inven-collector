import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core import utils
from spaceone.inventory.connector.sql import SqlConnector
from spaceone.inventory.manager.sql_databases.database_manager import SqlServerManager


class TestSqlServerManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')

        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})

        cls.sql_server_connector = SqlConnector(transaction=Transaction(), config={}, secret_data=cls.azure_credentials)

        cls.sql_server_manager = SqlServerManager(Transaction())

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_collect_cloud_service(self, *args):
        secret_data = self.azure_credentials

        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        sql_servers = self.sql_server_manager.collect_cloud_service(params)

        for sql_server in sql_servers:
            print(sql_server.to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)