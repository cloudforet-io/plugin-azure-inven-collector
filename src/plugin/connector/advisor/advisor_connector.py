import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class AdvisorConnector(AzureBaseConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get("secret_data"))

    def list_recommendations(self, recommendation_filter: str = None):
        return self.advisor_client.recommendations.list(
            api_version="2023-01-01", filter=recommendation_filter
        )

    def get_metadata(self, name: str):
        return self.advisor_client.recommendation_metadata.get(name=name)

    def list_metadata(self):
        return self.advisor_client.recommendation_metadata.list(expand="ibiza")

    def list_scores(self, subscription_id: str) -> dict:
        url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Advisor/advisorScore?api-version=2023-01-01"
        return self.request_azure_api(url, method="GET")

    def get_score(self, subscription_id: str, score_name: str):
        url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Advisor/advisorScore/{score_name}?api-version=2023-01-01"
        return self.request_azure_api(url, method="GET")
