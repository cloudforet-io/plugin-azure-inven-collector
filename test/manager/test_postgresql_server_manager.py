import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core import utils
from spaceone.inventory.connector.postgresql_server import PostgreSQLServerConnector
from spaceone.inventory.manager.postgresql_servers.server_manager import PostgreSQLServerManager


class TestPostgreSQLServerManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')

        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})

        cls.postgresql_server_connector = PostgreSQLServerConnector(transaction=Transaction(), config={}, secret_data=cls.azure_credentials)
        cls.postgresql_server_manager = PostgreSQLServerManager(Transaction())

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_collect_cloud_service(self, *args):
        secret_data = self.azure_credentials
        subscription_info = {
            'subscription_id': '3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca',
            'subscription_name': 'Azure subscription 1',
            'tenant_id': '35f43e22-0c0b-4ff3-90aa-b2c04ef1054c'
        }

        params = {'options': {}, 'secret_data': secret_data, 'filter': {}, 'subscription_info': subscription_info}

        postgre_sql_servers = self.postgresql_server_manager.collect_cloud_service(params)

        for postgre_sql_server in postgre_sql_servers:
            print(postgre_sql_server.to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)