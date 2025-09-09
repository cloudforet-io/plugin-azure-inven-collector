import logging
from typing import Union

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.advisor.advisor_connector import AdvisorConnector
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class RecommendationCostManager(AzureBaseManager):
    cloud_service_group = "Advisor"
    cloud_service_type = "Cost"
    service_code = "/Microsoft.ResourceHealth/events"

    def create_cloud_service(self, options: dict, secret_data: dict, schema: str):
        cloud_services = []
        error_responses = []

        advisor_conn = AdvisorConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)
        recommendation_filter = f"Category eq '{self.cloud_service_type}'"
        recommendations = advisor_conn.list_recommendations(
            recommendation_filter=recommendation_filter
        )

        for recommendation in recommendations:
            try:
                recommendation_info = self.convert_nested_dictionary(recommendation)
                recommendation_info.update(
                    {
                        "tenant_id": subscription_info.get("tenant_id"),
                        "subscription_id": subscription_info.get("subscription_id"),
                        "subscription_name": subscription_info.get("display_name"),
                    }
                )

                category = recommendation_info.get("category")
                self.cloud_service_type = category

                extended_properties = (
                    recommendation_info.get("extended_properties", {}) or {}
                )
                if (
                    extended_properties
                    and extended_properties.get("annualSavingsAmount") is not None
                ):
                    recommendation_info[
                        "potential_yearly_savings_based_on_retail_pricing_display"
                    ] = float(extended_properties["annualSavingsAmount"])

                if (
                    recommendation_info.get("impacted_field")
                    == "Microsoft.Subscriptions/subscriptions"
                ):
                    recommendation_info["impacted_value_display"] = (
                        recommendation_info.get("subscription_name")
                    )
                else:
                    recommendation_info["impacted_value_display"] = (
                        recommendation_info.get("impacted_value")
                    )

                short_description = recommendation_info.get("short_description")
                extended_properties = (
                    recommendation_info.get("extended_properties", {}) or {}
                )

                cloud_services.append(
                    make_cloud_service(
                        name=self._get_name_from_short_description(short_description),
                        account=secret_data["subscription_id"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        region_code=self._get_region_from_extended_properties(
                            extended_properties
                        ),
                        data=recommendation_info,
                        reference=self.make_reference(recommendation_info.get("id")),
                        data_format="dict",
                    )
                )
            except Exception as e:
                _LOGGER.error(
                    f"[create_cloud_service] Error {self.service} {e}", exc_info=True
                )
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
            is_primary=False,
            is_major=False,
            labels=["Management"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-advisor.svg"},
        )

    @staticmethod
    def _get_name_from_short_description(short_description: dict) -> str:
        return short_description["problem"]

    @staticmethod
    def _get_region_from_extended_properties(
        extended_properties: dict,
    ) -> Union[str, None]:
        region = None
        if "regionId" in extended_properties:
            region = extended_properties.get("regionId", None)
        elif "region" in extended_properties:
            region = extended_properties.get("region", None)

        return region
