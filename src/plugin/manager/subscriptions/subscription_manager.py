import logging
import re

from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class SubscriptionsManager(AzureBaseManager):
    # cloud_service_group = "Subscriptions"
    # cloud_service_type = "Subscription"
    service_code = "/Microsoft.subscriptions"

    def create_cloud_service_type(self):
        pass

    def create_cloud_service(self, options: dict, secret_data: dict, schema: str):
        pass

    def list_location_info(self, secret_data: dict):
        subscription_connector = SubscriptionsConnector(secret_data=secret_data)
        location_infos = subscription_connector.list_location_info(
            secret_data["subscription_id"]
        )

        region_info = {}
        for location_info in location_infos:
            _loc_info = self.convert_nested_dictionary(location_info)
            _name = f'{re.sub(r"[/()]", "", _loc_info.get("regional_display_name"))} ({_loc_info.get("metadata").get("physical_location")})'
            _latitude = _loc_info.get("metadata", {}).get("latitude")
            _longitude = _loc_info.get("metadata", {}).get("longitude")
            _continent = _loc_info.get("metadata", {}).get("geography_group")

            if _name and _latitude and _longitude and _continent:
                region_info.update(
                    {
                        _loc_info["name"]: {
                            "region_code": _loc_info["name"],
                            "provider": self.provider,
                            "name": _name,
                            "tags": {
                                "latitude": _latitude,
                                "longitude": _longitude,
                                "continent": _continent.replace(" ", "_").lower(),
                            },
                        }
                    }
                )

        return region_info
