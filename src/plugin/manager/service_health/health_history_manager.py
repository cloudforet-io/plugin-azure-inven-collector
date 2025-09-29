import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.service_health.service_health_connector import (
    ServiceHealthConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class HealthHistoryManager(AzureBaseManager):
    cloud_service_group = "ServiceHealth"
    cloud_service_type = "HealthHistory"
    service_code = "/Microsoft.ResourceHealth/events"

    def create_cloud_service(self, options: dict, secret_data: dict, schema: str):
        cloud_services = []
        error_responses = []

        external_link_format = (
            "https://app.azure.com/h/{resource_id}/"
            + secret_data["subscription_id"][:3]
            + secret_data["subscription_id"][-3:]
        )

        health_history_conn = ServiceHealthConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)
        query_start_time = self._get_three_month_ago_date()

        # if not SubscriptionsConnector.region_display_map:
        #     locations = subscription_conn.list_location_info(
        #         secret_data["subscription_id"]
        #     )
        #     SubscriptionsConnector.region_display_map = (
        #         self._create_region_display_map_with_locations_info(locations)
        #     )
        health_histories = health_history_conn.list_health_history(query_start_time)
        for health_history in health_histories:
            try:
                health_history_info = self.convert_nested_dictionary(health_history)
                health_history_info.update(
                    {
                        "tenant_id": subscription_info.get("tenant_id"),
                        "subscription_id": subscription_info.get("subscription_id"),
                        "subscription_name": subscription_info.get("display_name"),
                    }
                )

                # add impacted service info at impacted region
                health_history_info["impact_display"] = []
                impacted_services_display = []
                impacted_regions_display = []
                impact_updates_display = []
                impacted_subscriptions_display = []

                for impact in health_history_info.get("impact", []):

                    impacted_service = impact["impacted_service"]
                    impacted_regions = impact.get("impacted_regions", [])

                    impacted_services_display.append(impacted_service)
                    for impacted_region in impacted_regions:
                        impacted_region["impacted_service_display"] = impacted_service
                        impacted_regions_display.append(
                            impacted_region.get("impacted_region")
                        )
                        impacted_subscriptions_display.extend(
                            impacted_region.get("impacted_subscriptions", [])
                        )

                        updates = impacted_region.get("updates") or []
                        impact_updates = self._create_impact_updates_display(
                            updates, impacted_service, impacted_region
                        )
                        if impact_updates:
                            impact_updates_display.extend(impact_updates)
                            del impacted_region["updates"]

                    if impacted_regions:
                        health_history_info["impact_display"].extend(impacted_regions)
                        del impact["impacted_regions"]

                if impacted_services_display:
                    health_history_info["impacted_services_display"] = list(
                        set(impacted_services_display)
                    )

                if impacted_subscriptions_display:
                    health_history_info["impacted_subscriptions_display"] = list(
                        set(impacted_subscriptions_display)
                    )

                if impacted_regions_display:
                    health_history_info["impacted_regions_display"] = list(
                        set(impacted_regions_display)
                    )

                if impact_updates_display:
                    health_history_info["impact_updates_display"] = (
                        impact_updates_display
                    )

                if len(impacted_regions_display) > 1:
                    region = "Multi Regions"
                else:
                    region = impacted_regions_display[0]

                cloud_services.append(
                    make_cloud_service(
                        name=health_history_info.get("title"),
                        account=secret_data["subscription_id"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        region_code=region,
                        data=health_history_info,
                        reference=self.make_reference(
                            health_history_info.get("id"), external_link_format
                        ),
                        data_format="dict",
                    )
                )
            except Exception as e:
                _LOGGER.error(f"[create_cloud_service] Error {self.service} {e}")
                error_responses.append(
                    make_error_response(
                        error=e,
                        provider=self.provider,
                        cloud_service_group=self.cloud_service_group,
                        cloud_service_type=self.cloud_service_type,
                    )
                )

        return cloud_services, error_responses

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Management"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-service-health.svg"},
        )

    @staticmethod
    def _create_impact_updates_display(
        updates: list, impacted_service: str, impacted_region: dict
    ) -> list:
        impact_updates_display = []
        for update in updates:
            update.update(
                {
                    "impacted_service_display": impacted_service,
                    "impacted_region_display": impacted_region.get("impacted_region"),
                }
            )
            impact_updates_display.append(update)
        return impact_updates_display

    @staticmethod
    def _get_three_month_ago_date() -> str:
        current_date = datetime.utcnow()
        three_months_ago_date = current_date - relativedelta(months=3)
        first_day_three_months_ago = three_months_ago_date.replace(day=1)
        return first_day_three_months_ago.strftime("%Y/%m/%d")

    def _create_region_display_map_with_locations_info(self, locations) -> dict:
        region_display_map = {}
        for location in locations:
            location_info = self.convert_nested_dictionary(location)
            display_name = location_info.get("display_name")
            region_name = location_info.get("name")
            region_display_map[display_name] = region_name
        return region_display_map
