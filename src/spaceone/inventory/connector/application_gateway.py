import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['ApplicationGatewayConnector']
_LOGGER = logging.getLogger(__name__)


class ApplicationGatewayConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_application_gateways(self):

        obj = self.network_client.virtual_networks.list_all()
        for i in obj:
            print("#####")
            print(i)
        print(obj)

        return self.network_client.application_gateways.list_all()

    def get_public_ip_addresses(self, public_ip_address_name, resource_group_name):
        return self.network_client.public_ip_addresses.get(public_ip_address_name, resource_group_name)