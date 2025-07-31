import datetime
import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.monitor.monitor_connector import MonitorConnector
from plugin.connector.storage_accounts.storage_accounts_connector import (
    StorageAccountsConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class StorageAccountsManager(AzureBaseManager):
    cloud_service_group = "StorageAccounts"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.Storage/storageAccounts"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Storage"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-service-accounts.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        storage_accounts_conn = StorageAccountsConnector(secret_data=secret_data)
        monitor_conn = MonitorConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        storage_accounts = storage_accounts_conn.list_storage_accounts()

        for storage_account in storage_accounts:

            try:
                storage_account_dict = self.convert_nested_dictionary(storage_account)
                kind = storage_account_dict.get("kind")
                storage_account_id = storage_account_dict["id"]
                resource_group = self.get_resource_group_from_id(storage_account_id)

                if storage_account_dict.get("network_rule_set") is not None:
                    storage_account_dict.update(
                        {
                            "network_rule_set": self.get_network_rule_set(
                                storage_account_dict["network_rule_set"]
                            )
                        }
                    )

                # https://learn.microsoft.com/en-us/rest/api/storagerp/storage-accounts/list?view=rest-storagerp-2023-01-01&tabs=HTTP#kind
                if storage_account_dict.get("name") is not None and kind not in [
                    "FileStorage"
                ]:
                    container_count = self.get_blob_containers_count(
                        storage_accounts_conn,
                        resource_group,
                        storage_account_dict["name"],
                    )
                    storage_account_dict.update(
                        {"container_count_display": container_count}
                    )
                if storage_account_dict.get("routing_preference") is not None:
                    storage_account_dict.update(
                        {"routing_preference_display": "Internet routing"}
                    )
                else:
                    storage_account_dict.update(
                        {"routing_preference_display": "Microsoft network routing"}
                    )
                storage_account_dict = self.update_tenant_id_from_secret_data(
                    storage_account_dict, secret_data
                )
                storage_account_dict.update(
                    {
                        "resource_group": resource_group,
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": storage_account_id},
                        "blob_count_display": self._get_blob_count_from_monitoring(
                            monitor_conn, storage_account_id
                        ),
                        "blob_size_display": self._get_blob_size_from_monitoring(
                            monitor_conn, storage_account_id
                        ),
                    }
                )

                self.set_region_code(storage_account_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=storage_account_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=storage_account_dict,
                        account=storage_account_dict["subscription_id"],
                        instance_type=storage_account_dict["sku"]["tier"],
                        region_code=storage_account_dict["location"],
                        reference=self.make_reference(storage_account_dict.get("id")),
                        tags=storage_account_dict.get("tags", {}),
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

    def get_public_ip_address(
        self, application_gateway_conn, resource_group_name, pip_name
    ):
        public_ip_address_obj = application_gateway_conn.get_public_ip_addresses(
            resource_group_name, pip_name
        )
        public_ip_address_dict = self.convert_nested_dictionary(public_ip_address_obj)

        return public_ip_address_dict

    def get_network_rule_set(self, network_rule_dict):
        if network_rule_dict.get("virtual_network_rules") is not None:
            network_rule_dict.update(
                {
                    "virtual_networks": self.get_virtual_network_names(
                        network_rule_dict["virtual_network_rules"]
                    ),
                    "is_public_access_allowed": False,
                }
            )
        if not network_rule_dict.get(
            "virtual_network_rules"
        ):  # if virtual_network_rules are empty, this SA is public allowable
            network_rule_dict.update({"is_public_access_allowed": True})

        if network_rule_dict.get("ip_rules") is not None:
            firewall_address_list = []
            for rule in network_rule_dict["ip_rules"]:
                firewall_address_list.append(rule["ip_address_or_range"])

            network_rule_dict.update({"firewall_address_range": firewall_address_list})

        if network_rule_dict.get("resource_access_rules") is not None:
            resource_access_rules_list = []
            for rule in network_rule_dict["resource_access_rules"]:
                try:
                    resource_type = rule.get("resource_id").split("/")[6]
                    resource_access_rules_list.append(resource_type)

                except Exception as e:
                    _LOGGER.error(f"[ERROR: Azure Storage Account Network Rules]: {e}")

            network_rule_dict.update(
                {"resource_access_rules_display": resource_access_rules_list}
            )

        return network_rule_dict

    def list_blob_containers(self, storage_conn, rg_name, account_name):
        blob_containers_list = []
        blob_containers_obj = storage_conn.list_blob_containers(
            rg_name=rg_name, account_name=account_name
        )
        for blob_container in blob_containers_obj:
            blob_dict = self.convert_nested_dictionary(blob_container)
            blob_containers_list.append(blob_dict)

        return blob_containers_list

    def _get_blob_count_from_monitoring(self, monitor_conn, storage_account_id):
        timespan = self._get_timespan_from_now(1)
        aggregation = "total"
        interval = "PT1H"
        container_blob_count_metric = self._get_metric_data(
            monitor_conn,
            f"{storage_account_id}/blobServices/default",
            metricnames="BlobCount",
            aggregation=aggregation,
            timespan=timespan,
            interval=interval,
        )

        container_blob_count_metric_dict = self.convert_nested_dictionary(
            container_blob_count_metric
        )
        return self._get_timeseries_data_from_metric(
            container_blob_count_metric_dict, aggregation
        )

    def _get_blob_size_from_monitoring(self, monitor_conn, storage_account_id):
        timespan = self._get_timespan_from_now(1)
        aggregation = "total"
        interval = "PT1H"
        container_blob_capacity_metric = self._get_metric_data(
            monitor_conn,
            f"{storage_account_id}/blobServices/default",
            metricnames="BlobCapacity",
            aggregation=aggregation,
            timespan=timespan,
            interval=interval,
        )
        container_blob_capacity_metric_dict = self.convert_nested_dictionary(
            container_blob_capacity_metric
        )
        return self._get_timeseries_data_from_metric(
            container_blob_capacity_metric_dict, aggregation
        )

    @staticmethod
    def _get_timeseries_data_from_metric(metric_dict, aggregation):
        try:
            timeseries_data = metric_dict["value"][0]["timeseries"][0]["data"][0].get(
                aggregation
            )
            return timeseries_data if timeseries_data is not None else 0
        except Exception as e:
            _LOGGER.warning(f"[_get_timeseries_data_from_metric]: {e}")
            return 0

    @staticmethod
    def get_associated_listener(frontend_ip_configuration_dict, http_listeners_list):
        associated_listener = ""
        for http_listener in http_listeners_list:
            if http_listener.get("frontend_ip_configuration") is not None:
                if frontend_ip_configuration_dict["id"] in http_listener.get(
                    "frontend_ip_configuration", {}
                ).get("id", ""):
                    associated_listener = http_listener.get("name", "-")
                else:
                    associated_listener = "-"

        return associated_listener

    @staticmethod
    def get_port(port_id, frontend_ports_list):
        port = 0
        for fe_port in frontend_ports_list:
            if port_id in fe_port["id"]:
                port = fe_port.get("port", 0)
                return port
            else:
                return port

    @staticmethod
    def update_backend_pool_dict(backend_pool_list, backend_pool_id, request_rules):
        for backend_pool in backend_pool_list:
            if backend_pool["id"] == backend_pool_id:
                backend_pool.update({"associated_rules": request_rules})

    @staticmethod
    def update_rewrite_ruleset_dict(
        rewrite_rule_sets_list, rewrite_rule_id, applied_rules_list
    ):
        for rewrite_rule in rewrite_rule_sets_list:
            if rewrite_rule["id"] == rewrite_rule_id:
                rewrite_rule.update({"rules_applied": applied_rules_list})

    @staticmethod
    def update_http_listeners_list(
        http_listeners_list, http_listener_id, http_applied_rules
    ):
        for http_listener in http_listeners_list:
            if http_listener["id"] == http_listener_id:
                http_listener.update({"associated_rules": http_applied_rules})

    @staticmethod
    def get_virtual_network_names(virtual_network_rules):
        names = []
        try:
            for virtual_network_rule in virtual_network_rules:
                name = virtual_network_rule["virtual_network_resource_id"].split("/")[8]
                names.append(name)

        except Exception as e:
            _LOGGER.error(f"[ERROR: Azure Storage Account Network Rule Get Name]: {e}")

        return names

    @staticmethod
    def _get_metric_data(
        monitor_conn,
        resource_uri,
        metricnames,
        aggregation=None,
        timespan=None,
        interval=None,
    ):
        return monitor_conn.list_metrics(
            resource_uri,
            metricnames=metricnames,
            aggregation=aggregation,
            timespan=timespan,
            interval=interval,
        )

    @staticmethod
    def _get_timespan_from_now(hours):
        time_now = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        time_now_hours_ago = time_now - datetime.timedelta(hours=hours)
        return "{}/{}".format(time_now_hours_ago, time_now)

    @staticmethod
    def get_blob_containers_count(storage_conn, rg_name, account_name):
        blob_containers_obj = storage_conn.list_blob_containers(
            rg_name=rg_name, account_name=account_name
        )
        return len(list(blob_containers_obj))
