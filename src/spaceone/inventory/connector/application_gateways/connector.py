import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *
__all__ = ['ApplicationGatewaysConnector']
_LOGGER = logging.getLogger(__name__)


class ApplicationGatewaysConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_application_gateways(self):
        return self.network_client.application_gateways.list_all()

    def get_public_ip_addresses(self, public_ip_address_name, resource_group_name):
        return self.network_client.public_ip_addresses.get(public_ip_address_name, resource_group_name)
