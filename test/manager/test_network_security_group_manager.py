import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core import utils
from spaceone.inventory.connector.network_security_group import NetworkSecurityGroupConnector
from spaceone.inventory.manager.network_security_groups.instance_manager import NetworkSecurityGroupManager


class TestNetworkSecurityGroupManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')

        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})

        cls.network_security_group_connector = NetworkSecurityGroupConnector(transaction=Transaction(), config={}, secret_data=cls.azure_credentials)
        cls.network_security_group_manager = NetworkSecurityGroupManager(Transaction())

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_collect_cloud_service(self, *args):
        secret_data = self.azure_credentials

        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        network_security_groups = self.network_security_group_manager.collect_cloud_service(params)

        for network_security_group in network_security_groups:
            print(network_security_group.to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)