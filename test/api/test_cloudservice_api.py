import os
import unittest
import json

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.transaction import Transaction
from spaceone.tester import TestCase, print_json


class TestCollector(TestCase):

    @classmethod
    def setUpClass(cls):
        azure_cred = os.environ.get('AZURE_CRED')
        test_config = utils.load_yaml_from_file(azure_cred)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})
        super().setUpClass()

    def test_init(self):
        v_info = self.inventory.Collector.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {
        }
        v_info = self.inventory.Collector.verify({'options': options, 'secret_data': self.azure_credentials})
        print_json(v_info)

    def test_collect(self):

        options = {'cloud_service_types': ['NetworkSecurityGroups']}
        # options = {}
        filter = {}
        resource_stream = self.inventory.Collector.collect({'options': options, 'secret_data': self.azure_credentials,
                                                            'filter': filter})

        for res in resource_stream:
            print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)