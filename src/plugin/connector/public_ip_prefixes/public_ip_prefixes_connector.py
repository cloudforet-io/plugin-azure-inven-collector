import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class PublicIPPrefixesConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get("secret_data"))

    def list_all_public_ip_prefixes(self):
        return self.network_client.public_ip_prefixes.list_all()
