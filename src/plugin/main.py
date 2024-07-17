import logging
import time
from typing import Generator

from spaceone.core.error import ERROR_REQUIRED_PARAMETER
from spaceone.inventory.plugin.collector.lib.server import CollectorPluginServer

from plugin.manager.base import AzureBaseManager
from plugin.manager.subscriptions.subscriptions_manager import SubscriptionsManager

app = CollectorPluginServer()

_LOGGER = logging.getLogger("spaceone")

DEFAULT_RESOURCE_TYPES = ["inventory.CloudService", "inventory.CloudServiceType", "inventory.Metric",
                          "inventory.Region"]


@app.route('Collector.init')
def collector_init(params: dict) -> dict:
    metadata = {
        "options_schema": {
            "type": "object",
            "properties": {
                "cloud_service_groups": {
                    "title": "Specific services",
                    "type": "string",
                    "items": {"type": "string"},
                    "default": "All",
                    "enum": ["All", "Disks"],
                    "description": "Choose one of the service to collect data. If you choose 'All', it will collect all services."
                }
            }
        }
    }
    return {"metadata": metadata}


@app.route('Collector.verify')
def collector_verify(params: dict) -> None:
    pass


@app.route('Collector.collect')
def collector_collect(params: dict) -> Generator[dict, None, None]:
    options: dict = params.get("options", {}) or {}
    secret_data: dict = params["secret_data"]
    schema: str = params.get("schema")
    task_options: dict = params.get("task_options", {}) or {}
    domain_id: str = params["domain_id"]
    subscription_id = secret_data.get("subscription_id")

    _check_secret_data(secret_data)

    start_time = time.time()
    _LOGGER.debug(f"[collector_collect] Start Collecting Azure Resources {subscription_id}")

    cloud_service_groups = _get_cloud_service_groups_from_options_and_task_options(options, task_options)
    resource_type = task_options.get("resource_type")

    if resource_type == "inventory.Region":
        subscriptions_mgr = SubscriptionsManager()
        location_info = subscriptions_mgr.list_location_info(secret_data)
        print("hererere")
        print(location_info)
        yield from AzureBaseManager().collect_region(location_info)
    else:
        for manager in AzureBaseManager.list_managers_by_cloud_service_groups(cloud_service_groups):
            if resource_type == "inventory.CloudService":
                yield from manager().collect_cloud_services(options, secret_data, schema)
            elif resource_type == "inventory.CloudServiceType":
                yield from manager().collect_cloud_service_type()
            elif resource_type == "inventory.Metric":
                yield from AzureBaseManager.collect_metrics(manager.cloud_service_group)
            else:
                yield from manager().collect_resources(options, secret_data, schema)
    _LOGGER.debug(
        f"[collector_collect] Finished Collecting Azure Resources {subscription_id} duration: {time.time() - start_time} seconds")


@app.route('Job.get_tasks')
def job_get_tasks(params: dict) -> dict:
    domain_id = params["domain_id"]
    options = params.get("options", {})
    cloud_service_groups = options.get("cloud_service_groups", [])
    resource_types = options.get("resource_types", DEFAULT_RESOURCE_TYPES)

    tasks = []

    if not resource_types:
        resource_types = DEFAULT_RESOURCE_TYPES

    for manager in AzureBaseManager.list_managers_by_cloud_service_groups(cloud_service_groups):
        for resource_type in resource_types:
            tasks.append({
                "task_options": {
                    "resource_type": resource_type,
                    "cloud_service_groups": [manager.cloud_service_group]
                }
            })

    return {"tasks": tasks}


def _get_cloud_service_groups_from_options_and_task_options(options: dict, task_options: dict) -> list:
    cloud_service_groups = options.get("cloud_service_groups", [])
    if task_options:
        cloud_service_groups = task_options.get("cloud_service_groups", cloud_service_groups)
    return cloud_service_groups


def _check_secret_data(secret_data: dict):
    if "tenant_id" not in secret_data:
        raise ERROR_REQUIRED_PARAMETER(key='secret_data.tenant_id')

    if "subscription_id" not in secret_data:
        raise ERROR_REQUIRED_PARAMETER(key='secret_data.subscription_id')

    if "client_id" not in secret_data:
        raise ERROR_REQUIRED_PARAMETER(key='secret_data.client_id')

    if "client_secret" not in secret_data:
        raise ERROR_REQUIRED_PARAMETER(key='secret_data.client_secret')
