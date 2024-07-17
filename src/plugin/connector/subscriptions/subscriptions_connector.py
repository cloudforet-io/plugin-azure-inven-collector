import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class SubscriptionsConnector(AzureBaseConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def get_subscription(self, subscription_id: str):
        return self.subscription_client.subscriptions.get(subscription_id)

    def list_location_info(self, subscription_id: str):
        return self.subscription_client.subscriptions.list_locations(subscription_id)
