import abc
import datetime
import logging
import os
import re
import time
from typing import Union

from spaceone.core import utils
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *

_LOGGER = logging.getLogger("spaceone")
_CURRENT_DIR = os.path.dirname(__file__)
_METRIC_DIR = os.path.join(_CURRENT_DIR, "../metrics/")
_METADATA_DIR = os.path.join(_CURRENT_DIR, "../metadata/")

__all__ = ["AzureBaseManager"]


class AzureBaseManager(BaseManager):
    service = None
    cloud_service_group = None
    cloud_service_type = None
    region_info = {}
    collected_region_codes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = "azure"

    @abc.abstractmethod
    def create_cloud_service_type(self):
        raise NotImplementedError(
            "method `create_cloud_service_type` should be implemented"
        )

    @abc.abstractmethod
    def create_cloud_service(self, options, secret_data, schema):
        raise NotImplementedError("method `create_cloud_service` should be implemented")

    @classmethod
    def list_managers_by_cloud_service_groups(
        cls, cloud_service_groups: list, create_job: bool = False
    ):
        yielded_groups = set()

        check_all = not cloud_service_groups or "All" in cloud_service_groups

        for manager in cls.__subclasses__():
            group = manager.cloud_service_group

            if group and (check_all or group in cloud_service_groups):
                if create_job:
                    if group not in yielded_groups:
                        yielded_groups.add(group)
                        yield manager
                else:
                    yield manager

    @classmethod
    def get_managers_by_cloud_service_group(cls, cloud_service_group: str):
        sub_cls = cls.__subclasses__()
        for manager in sub_cls:
            if manager.__name__ == cloud_service_group:
                return manager

    @classmethod
    def collect_metrics(cls, cloud_service_group: str):
        if not os.path.exists(os.path.join(_METRIC_DIR, cloud_service_group)):
            os.mkdir(os.path.join(_METRIC_DIR, cloud_service_group))
        for dirname in os.listdir(os.path.join(_METRIC_DIR, cloud_service_group)):
            for filename in os.listdir(
                os.path.join(_METRIC_DIR, cloud_service_group, dirname)
            ):
                if filename.endswith(".yaml"):
                    file_path = os.path.join(
                        _METRIC_DIR, cloud_service_group, dirname, filename
                    )
                    info = utils.load_yaml_from_file(file_path)
                    if filename == "namespace.yaml":
                        yield make_response(
                            namespace=info,
                            resource_type="inventory.Namespace",
                            match_keys=[],
                        )
                    else:
                        yield make_response(
                            metric=info, resource_type="inventory.Metric", match_keys=[]
                        )

    def collect_resources(self, options: dict, secret_data: dict, schema: str):
        subscription_id = secret_data.get("subscription_id")
        start_time = time.time()
        _LOGGER.debug(
            f"[START] Collecting {self.__repr__()} (subscription_id: {subscription_id})"
        )
        success_count, error_count = [0, 0]
        try:
            yield from self.collect_cloud_service_type()

            cloud_services, total_count = self.collect_cloud_service(
                options, secret_data, schema
            )
            for cloud_service in cloud_services:
                yield cloud_service
            success_count, error_count = total_count

            subscriptions_manager = (
                AzureBaseManager.get_managers_by_cloud_service_group(
                    "SubscriptionsManager"
                )
            )
            location_info = subscriptions_manager().list_location_info(secret_data)

            yield from self.collect_region(location_info)

        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

        _LOGGER.debug(
            f"[DONE] {self.__repr__()} Collected Time: {time.time() - start_time:.2f}s, Total Count: {success_count + error_count} (Success: {success_count}, Failure: {error_count})"
        )

    def collect_cloud_service_type(self):
        _LOGGER.debug(f"[START] Collecting cloud service type {self.__repr__()}")

        cloud_service_type = self.create_cloud_service_type()
        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "group", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_services(self, options: dict, secret_data: dict, schema: str):
        subscription_id = secret_data.get("subscription_id")
        start_time = time.time()
        _LOGGER.debug(
            f"[START] Collecting cloud services {self.__repr__()} (subscription_id: {subscription_id})"
        )
        success_count, error_count = [0, 0]
        try:
            cloud_services, total_count = self.collect_cloud_service(
                options, secret_data, schema
            )
            for cloud_service in cloud_services:
                yield cloud_service
            success_count, error_count = total_count

        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

        _LOGGER.debug(
            f"[DONE] {self.__repr__()} Collected Time: {time.time() - start_time:.2f}s, Total Count: {success_count + error_count} (Success: {success_count}, Failure: {error_count})"
        )

    def collect_cloud_service(self, options: dict, secret_data: dict, schema: str):
        total_resources = []
        cloud_services, error_resources = self.create_cloud_service(
            options, secret_data, schema
        )

        for cloud_service in cloud_services:
            total_resources.append(
                make_response(
                    cloud_service=cloud_service,
                    match_keys=[
                        [
                            "reference.resource_id",
                            "provider",
                            "cloud_service_type",
                            "cloud_service_group",
                            "account",
                        ]
                    ],
                )
            )
        total_resources.extend(error_resources)
        total_count = [len(cloud_services), len(error_resources)]
        return total_resources, total_count

    def collect_region(self, location_info: dict):
        _LOGGER.debug(f"[START] Collecting region {self.__repr__()}")
        for region_info in location_info.values():
            yield make_response(
                region=region_info,
                match_keys=[["region_code", "provider"]],
                resource_type="inventory.Region",
            )

    def get_metadata_path(self):
        _cloud_service_group = self._camel_to_snake(self.cloud_service_group)
        _cloud_service_type = self._camel_to_snake(self.cloud_service_type)

        return os.path.join(
            _METADATA_DIR, _cloud_service_group, f"{_cloud_service_type}.yaml"
        )

    def convert_nested_dictionary(
        self, cloud_svc_object: object
    ) -> Union[object, dict]:
        cloud_svc_dict = {}
        if hasattr(
            cloud_svc_object, "__dict__"
        ):  # if cloud_svc_object is not a dictionary type but has dict method
            cloud_svc_dict = cloud_svc_object.__dict__
        elif isinstance(cloud_svc_object, dict):
            cloud_svc_dict = cloud_svc_object
        elif not isinstance(
            cloud_svc_object, list
        ):  # if cloud_svc_object is one of type like int, float, char, ...
            return cloud_svc_object

        # if cloud_svc_object is dictionary type
        for key, value in cloud_svc_dict.items():
            if hasattr(value, "__dict__") or isinstance(value, dict):
                cloud_svc_dict[key] = self.convert_nested_dictionary(value)
            if "azure" in str(type(value)):
                cloud_svc_dict[key] = self.convert_nested_dictionary(value)
            elif isinstance(value, list):
                value_list = []
                for v in value:
                    value_list.append(self.convert_nested_dictionary(v))
                cloud_svc_dict[key] = value_list
            elif isinstance(value, datetime.datetime):
                cloud_svc_dict[key] = utils.datetime_to_iso8601(value)
            elif isinstance(value, datetime.timedelta):
                cloud_svc_dict[key] = str(value)

        return cloud_svc_dict

    def set_region_code(self, region):
        if region not in self.region_info:
            region = "global"

        if region not in self.collected_region_codes:
            self.collected_region_codes.append(region)

    @staticmethod
    def make_reference(resource_id: str, external_link_format: str = None) -> dict:
        if external_link_format:
            external_link = external_link_format.format(resource_id=resource_id)
        else:
            external_link = f"https://portal.azure.com/#@.onmicrosoft.com/resource{resource_id}/overview"
        return {"resource_id": resource_id, "external_link": external_link}

    @staticmethod
    def _camel_to_snake(name):
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split("/")[4]
        return resource_group

    @staticmethod
    def update_tenant_id_from_secret_data(
        cloud_service_data: dict, secret_data: dict
    ) -> dict:
        if tenant_id := secret_data.get("tenant_id"):
            cloud_service_data.update({"tenant_id": tenant_id})
        return cloud_service_data

    @staticmethod
    def convert_dictionary(obj):
        return vars(obj)

    @staticmethod
    def convert_tag_format(tags):
        convert_tags = []

        if tags:
            for k, v in tags.items():
                convert_tags.append({"key": k, "value": v})

        return convert_tags
