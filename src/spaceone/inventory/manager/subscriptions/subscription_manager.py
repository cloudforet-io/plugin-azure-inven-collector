from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.connector.subscriptions import SubscriptionsConnector
import re


class SubscriptionsManager(AzureManager):
    connector_name = 'SubscriptionsConnector'

    def get_subscription_info(self, params):
        secret_data = params['secret_data']
        subscription_connector: SubscriptionsConnector = self.locator.get_connector(self.connector_name, secret_data=secret_data)
        subscription_info = subscription_connector.get_subscription_info(secret_data['subscription_id'])

        return {
            'subscription_id': subscription_info.subscription_id,
            'subscription_name': subscription_info.display_name,
            'tenant_id': subscription_info.tenant_id
        }

    def list_location_info(self, params):
        secret_data = params['secret_data']
        subscription_connector: SubscriptionsConnector = self.locator.get_connector(self.connector_name, secret_data=secret_data)
        location_info = subscription_connector.list_location_info(secret_data['subscription_id'])

        region_info = {}
        for location_info in location_info:
            _loc_info = self.convert_nested_dictionary(location_info)
            _name = f'{re.sub(r"[/()]", "", _loc_info.get("regional_display_name"))} ({_loc_info.get("metadata").get("physical_location")})'
            _latitude = _loc_info.get('metadata', {}).get('latitude')
            _longitude = _loc_info.get('metadata', {}).get('longitude')
            _continent = _loc_info.get('metadata', {}).get('geography_group')

            if _name and _latitude and _longitude and _continent:
                region_info.update({
                    _loc_info['name']: {
                        'name': _name,
                        'tags': {
                            'latitude': _latitude,
                            'longitude': _longitude,
                            'continent': _continent.replace(' ', '_').lower()
                        }
                    }
                })

        return region_info
