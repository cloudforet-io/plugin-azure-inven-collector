import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core import utils
from spaceone.inventory.connector.application_gateway import ApplicationGatewayConnector
from spaceone.inventory.manager.application_gateways.instance_manager import ApplicationGatewayManager


class TestApplicationGatewayManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')

        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})

        cls.application_gateway_connector = ApplicationGatewayConnector(transaction=Transaction(), config={}, secret_data=cls.azure_credentials)
        cls.application_gateway_manager = ApplicationGatewayManager(Transaction())

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_collect_cloud_service(self, *args):
        secret_data = self.azure_credentials

        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        application_gateways = self.application_gateway_manager.collect_cloud_service(params)

        for applicaiton_gateway in application_gateways:
            print(applicaiton_gateway.to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)