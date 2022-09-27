import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core import utils
from spaceone.inventory.connector.virtual_network import VirtualNetworkConnector
from spaceone.inventory.manager.virtual_networks.instance_manager import VirtualNetworkManager


class TestVirtualNetworkManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')

        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})

        cls.vnet_connector = VirtualNetworkConnector(transaction=Transaction(), config={}, secret_data=cls.azure_credentials)
        cls.vnet_manager = VirtualNetworkManager(Transaction())

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_collect_cloud_service(self, *args):
        secret_data = self.azure_credentials

        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        virtual_networks = self.vnet_manager.collect_cloud_service(params)

        for virtual_network in virtual_networks:
            print(virtual_network.to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)