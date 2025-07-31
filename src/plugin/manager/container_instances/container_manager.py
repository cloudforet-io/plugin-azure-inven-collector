import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.container_instances.container_instances_connector import (
    ContainerInstancesConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class ContainerInstancesManage(AzureBaseManager):
    cloud_service_group = "ContainerInstances"
    cloud_service_type = "Container"
    service_code = "/Microsoft.Compute/disks"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Container"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-container-instances.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        container_instances_conn = ContainerInstancesConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        container_instances = container_instances_conn.list_container_groups()

        for container_instance in container_instances:

            try:
                container_instance_dict = self.convert_nested_dictionary(
                    container_instance
                )
                container_instance_id = container_instance_dict["id"]

                resource_group_name = self.get_resource_group_from_id(
                    container_instance_id
                )
                container_group_name = container_instance_dict["name"]

                container_instance = container_instances_conn.get_container_groups(
                    resource_group_name=resource_group_name,
                    container_group_name=container_group_name,
                )
                container_instance_dict = self.convert_nested_dictionary(
                    container_instance
                )

                # Update data info in Container Instance's Raw Data
                _cpu_count_display = 0
                _gpu_count_display = 0
                _memory_size_display = 0.0

                for container in container_instance_dict["containers"]:
                    _cpu_count_display += int(container["resources"]["requests"]["cpu"])
                    _memory_size_display += float(
                        container["resources"]["requests"]["memory_in_gb"]
                    )
                    _gpu_count_display += int(self._get_gpu_count_display(container))

                # Set detail volume info for container
                if container_instance_dict["volumes"] is not None:
                    for volume in container_instance_dict["volumes"]:
                        self._set_volumes_detail_info(
                            volume, container_instance_dict["containers"]
                        )

                    # Set Container Instance volume type and volume count
                    self._set_container_instance_volume_type(
                        container_instance_dict["volumes"]
                    )
                    container_instance_dict["volume_count_display"] = len(
                        container_instance_dict["volumes"]
                    )
                else:
                    for container in container_instance_dict["containers"]:
                        container["volume_mount_count_display"] = 0

                    container_instance_dict["volume_count_display"] = 0

                container_instance_dict = self.update_tenant_id_from_secret_data(
                    container_instance_dict, secret_data
                )

                container_instance_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            container_instance_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": container_instance_id},
                        "container_count_display": len(
                            container_instance_dict["containers"]
                        ),
                        "cpu_count_display": _cpu_count_display,
                        "memory_size_display": _memory_size_display,
                        "gpu_count_display": _gpu_count_display,
                    }
                )

                self.set_region_code(container_instance_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=container_instance_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=container_instance_dict,
                        account=container_instance_dict["subscription_id"],
                        region_code=container_instance_dict["location"],
                        reference=self.make_reference(
                            container_instance_dict.get("id")
                        ),
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

    @staticmethod
    def _set_container_instance_volume_type(volumes):
        for volume in volumes:
            if volume.get("git_repo") is not None:
                volume["volume_type"] = "Git repo"
            elif volume.get("azure_file") is not None:
                volume["volume_type"] = "Azure file"
            elif volume.get("empty_dir") is not None:
                volume["volume_type"] = "Empty directory"
            elif volume.get("secret") is not None:
                volume["volume_type"] = "Secret"

    @staticmethod
    def _set_volumes_detail_info(volume, containers):
        for container in containers:
            if volume_mounts := container["volume_mounts"]:
                container["volume_mount_count_display"] = len(volume_mounts)
                for volume_mount in volume_mounts:
                    if volume_mount["name"] == volume["name"]:
                        volume.update(
                            {
                                "mount_path": volume_mount["mount_path"],
                                "container_name": container["name"],
                            }
                        )
                        return

    @staticmethod
    def _get_gpu_count_display(container):
        _gpu_count = 0
        if (
            _gpu_info := container.get("resources", {})
            .get("requests", {})
            .get("gpu", {})
        ):
            _gpu_count = _gpu_info.get("count", 0)
        return _gpu_count
