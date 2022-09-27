from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.connector.subscriptions import SubscriptionsConnector


class SubscriptionsManager(AzureManager):
    connector_name = 'SubscriptionsConnector'

    def get_subscription_info(self, params):
        secret_data = params['secret_data']
        subscription_connector: SubscriptionsConnector = self.locator.get_connector(self.connector_name,
                                                                                   secret_data=secret_data)
        subscription_info = subscription_connector.get_subscription_info(secret_data['subscription_id'])

        return {
            'subscription_id': subscription_info.subscription_id,
            'subscription_name': subscription_info.display_name,
            'tenant_id': subscription_info.tenant_id
        }
