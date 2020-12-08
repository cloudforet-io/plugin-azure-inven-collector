import logging

from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.error import *

__all__ = ['SubscriptionConnector']
_LOGGER = logging.getLogger(__name__)


class SubscriptionConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def get_subscription_info(self, subscription_id):
        return self.subscription_client.subscriptions.get(subscription_id)
