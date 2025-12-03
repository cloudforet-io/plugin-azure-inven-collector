import logging
from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")

MANAGEMENT_BASE_URL = "https://management.azure.com"
WEB_API_VERSION = "2025-03-01"


class FunctionsConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        secret_data = kwargs.get("secret_data", {})
        self.set_connect(secret_data)
        self.subscription_id = secret_data.get("subscription_id")

    def list_function_apps(self):
        function_apps = []

        for res in self.resource_client.resources.list():
            if res.type == "Microsoft.Web/sites":
                kind = (getattr(res, "kind", "") or "").lower()
                if "functionapp" in kind:
                    function_apps.append(res)

        _LOGGER.debug(f"[FunctionsConnector] Found {len(function_apps)} function apps")
        return function_apps

    def get_function_app_detail(self, resource_id: str) -> dict:
        if not resource_id:
            return {}

        url = f"{MANAGEMENT_BASE_URL}{resource_id}?api-version={WEB_API_VERSION}"
        return self.request_azure_api(url, method="GET") or {}

    def get_app_service_plan_detail(self, server_farm_id: str) -> dict:
        if not server_farm_id:
            return {}

        url = f"{MANAGEMENT_BASE_URL}{server_farm_id}?api-version={WEB_API_VERSION}"
        return self.request_azure_api(url, method="GET") or {}