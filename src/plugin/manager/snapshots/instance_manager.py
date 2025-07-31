import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.snapshots.snapshots_connector import SnapshotsConnector
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class SnapshotsManager(AzureBaseManager):
    cloud_service_group = "Snapshots"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.Compute/snapshots"

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
            tags={"spaceone:icon": f"{ICON_URL}/azure-disk-snapshot.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        snapshots_conn = SnapshotsConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        snapshots = snapshots_conn.list_snapshots()

        for snapshot in snapshots:

            try:
                snapshot_dict = self.convert_nested_dictionary(snapshot)
                snapshot_id = snapshot_dict["id"]

                # update sku_dict
                # switch SnapshotStorageAccountType to snapshot_sku_name for user-friendly words.
                # (ex.Premium_LRS -> Premium SSD, Standard HDD..)
                sku_dict = snapshot_dict.get("sku", {})
                sku_dict.update(
                    {"name": self.get_disk_sku_name(sku_dict.get("name", ""))}
                )

                # update encryption_dict type to user-friendly words
                # (ex.EncryptionAtRestWithPlatformKey -> Platform-managed key...)
                if snapshot_dict.get("encryption", {}).get("type") is not None:
                    type = snapshot_dict["encryption"]["type"]
                    encryption_type = ""
                    if type == "EncryptionAtRestWithPlatformKey":
                        encryption_type = "Platform-managed key"
                    elif type == "EncryptionAtRestWithPlatformAndCustomerKeys":
                        encryption_type = "Platform and customer managed key"
                    elif type == "EncryptionAtRestWithCustomerKey":
                        encryption_type = "Customer-managed key"

                    snapshot_dict["encryption"].update(
                        {"type_display": encryption_type}
                    )

                # update snapshot_dict
                snapshot_dict = self.update_tenant_id_from_secret_data(
                    snapshot_dict, secret_data
                )
                snapshot_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            snapshot_id
                        ),  # parse resource_group from ID
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "size": snapshot_dict["disk_size_bytes"],
                        "sku": sku_dict,
                        "incremental_display": self.get_incremental_display(
                            snapshot_dict["incremental"]
                        ),
                        "azure_monitor": {"resource_id": snapshot_id},
                        "time_created": snapshot_dict["time_created"],
                    }
                )

                if snapshot_dict.get("network_access_policy") is not None:
                    snapshot_dict.update(
                        {
                            "network_access_policy_display": self.get_network_access_policy(
                                snapshot_dict["network_access_policy"]
                            )
                        }
                    )

                # get source_disk_name from source_resource_id
                if snapshot_dict.get("creation_data") is not None:
                    source_resource_id = snapshot_dict["creation_data"].get(
                        "source_resource_id", ""
                    )
                    snapshot_dict.update(
                        {
                            "source_disk_name": self.get_source_disk_name(
                                source_resource_id
                            )
                        }
                    )

                # get attached vm's name
                if snapshot_dict.get("managed_by") is not None:
                    snapshot_dict.update(
                        {
                            "managed_by": self.get_attached_vm_name_from_managed_by(
                                snapshot_dict["managed_by"]
                            )
                        }
                    )

                self.set_region_code(snapshot_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=snapshot_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=snapshot_dict,
                        account=snapshot_dict["subscription_id"],
                        instance_type=snapshot_dict["sku"]["name"],
                        instance_size=float(snapshot_dict["disk_size_bytes"]),
                        region_code=snapshot_dict["location"],
                        reference=self.make_reference(snapshot_dict.get("id")),
                        tags=snapshot_dict.get("tags", {}),
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
    def get_attached_vm_name_from_managed_by(managed_by):
        attached_vm_name = ""
        if managed_by:
            attached_vm_name = managed_by.split("/")[8]  # parse attached_ from ID
        return attached_vm_name

    @staticmethod
    def get_disk_sku_name(sku_tier):
        sku_name = ""
        if sku_tier == "Premium_LRS":
            sku_name = "Premium SSD"
        elif sku_tier == "Standard_ZRS":
            sku_name = "Standard zone"
        elif sku_tier == "Standard_LRS":
            sku_name = "Standard HDD"

        return sku_name

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
    def get_incremental_display(incremental):
        if incremental is False:
            incremental_display = "Full"
        else:
            incremental_display = "Incremental"

        return incremental_display

    @staticmethod
    def get_source_disk_name(source_resource_id):
        source_disk_name = ""
        if source_resource_id:
            source_disk_name = source_resource_id.split("/")[
                8
            ]  # parse source_disk_name from source_resource_id
        return source_disk_name
