import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error.custom import *
__all__ = ['ApplicationGatewayConnector']
_LOGGER = logging.getLogger(__name__)


class ApplicationGatewayConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_application_gateways(self):
        try:
            return self.network_client.application_gateways.list_all()

        except Exception as e:
            _LOGGER.error(ERROR_CONNECTOR(field='Application Gateway'))

    def get_public_ip_addresses(self, public_ip_address_name, resource_group_name):
        try:
            return self.network_client.public_ip_addresses.get(public_ip_address_name, resource_group_name)

        except Exception as e:
            raise ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(field='Application Gateway')

