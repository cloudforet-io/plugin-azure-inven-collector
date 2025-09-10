import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class ApplicationGatewaysConnector(AzureBaseConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get("secret_data"))

    def list_all_application_gateways(self):
        return self.network_client.application_gateways.list_all()

    def get_public_ip_addresses(self, resource_group_name, public_ip_address_name):
        return self.network_client.public_ip_addresses.get(
            resource_group_name, public_ip_address_name
        )
