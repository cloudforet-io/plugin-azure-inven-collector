import concurrent.futures
import logging
import time
import os

from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.manager.subscriptions.subscription_manager import (
    SubscriptionsManager,
)
from spaceone.core import utils
from spaceone.core.service import *
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)

_CURRENT_DIR = os.path.dirname(__file__)
_BEFORE_CURRENT_DIR, _ = _CURRENT_DIR.rsplit("/", 1)
_METRIC_DIR = os.path.join(_BEFORE_CURRENT_DIR, "metrics/")


@authentication_handler
class CollectorService(BaseService):
    resource = "Collector"

    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(["options"])
    def init(self, params):
        """init plugin by options"""
        capability = {
            "filter_format": FILTER_FORMAT,
            "supported_resource_type": SUPPORTED_RESOURCE_TYPE,
            "supported_features": SUPPORTED_FEATURES,
            "supported_schedules": SUPPORTED_SCHEDULES,
        }
        return {"metadata": capability}

    @transaction
    @check_required(["options", "secret_data"])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params["options"]
        secret_data = params.get("secret_data", {})
        if secret_data != {}:
            azure_manager = AzureManager()
            active = azure_manager.verify({}, secret_data=secret_data)

        return {}

    @transaction
    @check_required(["options", "secret_data", "filter"])
    def collect(self, params: dict):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - task_options
        """

        start_time = time.time()
        options = params.get("options", {})
        task_options = params.get("task_options", {})
        params.update({"subscription_info": self.get_subscription_info(params)})

        _LOGGER.debug("[ EXECUTOR START: Azure Cloud Service ]")
        target_execute_managers = self._get_target_execute_manger(options, task_options)

        # Thread per cloud services
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []

            for execute_manager in target_execute_managers:
                _LOGGER.info(f"@@@ {execute_manager} @@@")
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(
                    executor.submit(_manager.collect_resources, params)
                )

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    yield result.to_primitive()

        """
        for manager in self.execute_managers:
            _LOGGER.debug(f'@@@ {manager} @@@')
            _manager = self.locator.get_manager(manager)

            for resource in _manager.collect_resources(params):
                yield resource.to_primitive()
        """

        if cloud_service_types := params.get("options", {}).get("cloud_service_types"):
            for service in cloud_service_types:
                for response in self.collect_metrics(service):
                    yield response
        else:
            for service in CLOUD_SERVICE_GROUP_MAP.keys():
                for response in self.collect_metrics(service):
                    yield response
        _LOGGER.debug(f"TOTAL TIME : {time.time() - start_time} Seconds")

    def get_subscription_info(self, params):
        subscription_manager: SubscriptionsManager = self.locator.get_manager(
            "SubscriptionsManager"
        )
        return subscription_manager.get_subscription_info(params)

    def list_location_info(self, params):
        subscription_manager: SubscriptionsManager = self.locator.get_manager(
            "SubscriptionsManager"
        )
        return subscription_manager.list_location_info(params)

    def _get_target_execute_manger(self, options: dict, task_options: dict) -> list:
        if "cloud_service_types" in options:
            execute_managers = self._match_execute_manager(
                options["cloud_service_types"]
            )
        elif "cloud_service_types" in task_options:
            execute_managers = self._match_execute_manager(
                task_options["cloud_service_types"]
            )
        else:
            execute_managers = list(CLOUD_SERVICE_GROUP_MAP.values())

        return execute_managers

    @staticmethod
    def _match_execute_manager(cloud_service_groups):
        return [
            CLOUD_SERVICE_GROUP_MAP[_cloud_service_group]
            for _cloud_service_group in cloud_service_groups
            if _cloud_service_group in CLOUD_SERVICE_GROUP_MAP
        ]

    def collect_metrics(self, service: str) -> list:
        if not os.path.exists(os.path.join(_METRIC_DIR, service)):
            os.mkdir(os.path.join(_METRIC_DIR, service))
        for dirname in os.listdir(os.path.join(_METRIC_DIR, service)):
            for filename in os.listdir(os.path.join(_METRIC_DIR, service, dirname)):
                if filename.endswith(".yaml"):
                    file_path = os.path.join(_METRIC_DIR, service, dirname, filename)
                    info = utils.load_yaml_from_file(file_path)
                    if filename == "namespace.yaml":
                        yield self.make_namespace_or_metric_response(
                            namespace=info,
                            resource_type="inventory.Namespace",
                        )
                    else:
                        yield self.make_namespace_or_metric_response(
                            metric=info,
                            resource_type="inventory.Metric",
                        )

    @staticmethod
    def make_namespace_or_metric_response(
        metric=None,
        namespace=None,
        resource_type: str = "inventory.Metric",
    ) -> dict:
        response = {
            "state": "SUCCESS",
            "resource_type": resource_type,
            "match_rules": {},
        }

        if resource_type == "inventory.Metric" and metric is not None:
            response["resource"] = metric
        elif resource_type == "inventory.Namespace" and namespace is not None:
            response["resource"] = namespace

        return response
