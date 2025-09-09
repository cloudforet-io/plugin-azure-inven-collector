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


class ScoreManager(AzureBaseManager):
    cloud_service_group = "Advisor"
    cloud_service_type = "Score"
    service_code = "Microsoft.Advisor/advisorScore"

    def create_cloud_service(self, options: dict, secret_data: dict, schema: str):
        cloud_services = []
        error_responses = []

        advisor_conn = AdvisorConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)
        scores: list = (
            advisor_conn.list_scores(secret_data["subscription_id"]).get("value", [])
            or []
        )

        for score_value in scores:
            try:
                score_id = score_value.get("id")
                score_name = score_value.get("name")
                score_info = self.convert_nested_dictionary(
                    score_value.get("properties", {})
                )
                score_category_display = self._get_score_category_from_id(score_id)

                score_info.update(
                    {
                        "tenant_id": subscription_info.get("tenant_id"),
                        "subscription_id": subscription_info.get("subscription_id"),
                        "subscription_name": subscription_info.get("display_name"),
                    }
                )

                score_info["score_category_display"] = score_category_display

                time_series_infos = score_info.get("timeSeries", []) or []

                for time_series_info in time_series_infos:
                    aggregation_level = time_series_info.get("aggregationLevel")
                    if aggregation_level == "Daily":
                        daily_score_history_display = time_series_info.get(
                            "scoreHistory"
                        )
                        score_info["daily_score_history_display"] = (
                            daily_score_history_display
                        )
                    elif aggregation_level == "Weekly":
                        weekly_score_history_display = time_series_info.get(
                            "scoreHistory"
                        )
                        score_info["weekly_score_history_display"] = (
                            weekly_score_history_display
                        )
                    elif aggregation_level == "Monthly":
                        monthly_score_history_display = time_series_info.get(
                            "scoreHistory"
                        )
                        score_info["monthly_score_history_display"] = (
                            monthly_score_history_display
                        )

                cloud_services.append(
                    make_cloud_service(
                        name=score_name,
                        account=score_info["subscription_id"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        region_code=None,
                        data=score_info,
                        reference=self.make_reference(score_id),
                        data_format="dict",
                    )
                )
            except Exception as e:
                _LOGGER.error(
                    f"[create_cloud_service] Error {self.cloud_service_type} {e}",
                    exc_info=True,
                )
                _LOGGER.error(
                    f"[create_cloud_service] Error {self.cloud_service_type} {score_value}",
                    exc_info=True,
                )
                _LOGGER.error(
                    f"[create_cloud_service] Error {self.cloud_service_type} {scores}",
                    exc_info=True,
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
            is_primary=True,
            is_major=True,
            labels=["Management"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-advisor.svg"},
        )

    @staticmethod
    def _get_score_category_from_id(score_id: id) -> Union[str, None]:
        score_category = score_id.split("/")[-1]
        if score_category in [
            "Cost",
            "Security",
            "Performance",
            "OperationalExcellence",
            "HighAvailability",
            "Advisor",
        ]:
            if score_category == "HighAvailability":
                score_category = "Reliability"
        return score_category
