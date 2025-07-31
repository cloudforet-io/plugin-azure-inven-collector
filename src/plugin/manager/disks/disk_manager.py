import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.disks.disks_connector import DisksConnector
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class DisksManager(AzureBaseManager):
    cloud_service_group = "Disks"
    cloud_service_type = "Disk"
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
            labels=["Compute", "Storage"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-disk.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        disks_conn = DisksConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        disks = disks_conn.list_disks()

        for disk in disks:

            try:
                disk_dict = self.convert_nested_dictionary(disk)
                disk_id = disk_dict["id"]

                # Switch DiskStorageAccountType to disk_sku_name for user-friendly words. (ex.Premium SSD, Standard HDD..)
                if disk_dict.get("sku") is not None:
                    sku_dict = disk_dict["sku"]
                    sku_dict.update({"name": self.get_disk_sku_name(sku_dict["name"])})
                    disk_dict.update({"sku": sku_dict})

                # update disk_data dict
                disk_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            disk_dict["id"]
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "size": disk_dict["disk_size_bytes"],
                        "tier_display": self.get_tier_display(
                            disk_dict["disk_iops_read_write"],
                            disk_dict["disk_m_bps_read_write"],
                        ),
                        "azure_monitor": {"resource_id": disk_id},
                    }
                )

                # Update Network access policy to user-friendly words
                if disk_dict.get("network_access_policy") is not None:
                    disk_dict.update(
                        {
                            "network_access_policy_display": self.get_network_access_policy(
                                disk_dict["network_access_policy"]
                            )
                        }
                    )

                # get attached vm's name
                if disk_dict.get("managed_by") is not None:
                    managed_by = disk_dict["managed_by"]
                    disk_dict.update(
                        {
                            "managed_by": self.get_attached_vm_name_from_managed_by(
                                managed_by
                            )
                        }
                    )

                max_shares = disk_dict.get("max_shares")
                if max_shares is not None and max_shares > 0:
                    disk_dict.update({"enable_shared_disk_display": True})
                else:
                    disk_dict.update({"enable_shared_disk_display": False})

                if disk_dict.get("bursting_enabled") is None:
                    disk_dict["bursting_enabled"] = False

                disk_data = self.update_tenant_id_from_secret_data(
                    disk_dict, secret_data
                )

                self.set_region_code(disk_data["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=disk_data["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=disk_data,
                        account=secret_data["subscription_id"],
                        instance_type=disk_data["sku"]["name"],
                        instance_size=disk_data["disk_size_bytes"],
                        region_code=disk_data["location"],
                        reference=self.make_reference(disk_data.get("id")),
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
    def get_disk_sku_name(sku_tier):
        if sku_tier == "Premium_LRS":
            sku_name = "Premium SSD"
        elif sku_tier == "StandardSSD_LRS":
            sku_name = "Standard SSD"
        elif sku_tier == "Standard_LRS":
            sku_name = "Standard HDD"
        else:
            sku_name = "Ultra SSD"
        return sku_name

    @staticmethod
    def get_tier_display(disk_iops_read_write, disk_m_bps_read_write):
        tier_display = (
            str(disk_iops_read_write)
            + " IOPS"
            + ", "
            + str(disk_m_bps_read_write)
            + " Mbps"
        )
        return tier_display

    @staticmethod
    def get_network_access_policy(network_access_policy):
        network_access_policy_display = ""
        if network_access_policy == "AllowAll":
            network_access_policy_display = "Public endpoint (all network)"
        elif network_access_policy == "AllowPrivate":
            network_access_policy_display = "Private endpoint (through disk access)"
        elif network_access_policy == "DenyAll":
            network_access_policy_display = "Deny all"

        return network_access_policy_display

    @staticmethod
    def get_attached_vm_name_from_managed_by(managed_by):
        attached_vm_name = managed_by.split("/")[8]
        return attached_vm_name
