import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.monitor.monitor_connector import MonitorConnector
from plugin.connector.sql_databases.sql_databases_connector import SqlDatabasesConnector
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class SQLDatabasesManager(AzureBaseManager):
    cloud_service_group = "SQLDatabases"
    cloud_service_type = "Database"
    service_code = "/Microsoft.Sql/servers/databases"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Database"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-sql-databases.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        sql_databases_conn = SqlDatabasesConnector(secret_data=secret_data)
        sql_monitor_conn = MonitorConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        # get resource_group_name and server_name from sql_server for sql_databases list
        sql_servers = sql_databases_conn.list_servers()

        for sql_server in sql_servers:

            try:
                sql_server_dict = self.convert_nested_dictionary(sql_server)

                server_name = sql_server_dict["name"]
                resource_group_name = self.get_resource_group_from_id(
                    sql_server_dict["id"]
                )
                server_admin_name = sql_server_dict.get("administrator_login")

                # get list
                sql_databases = sql_databases_conn.list_databases_in_server(
                    resource_group_name, server_name
                )
                replication_links = self.list_replication_links(
                    sql_databases_conn.list_replication_link_by_server(
                        resource_group_name=resource_group_name, server_name=server_name
                    )
                )

                # database for loop
                for sql_database in sql_databases:
                    sql_database_dict = self.convert_nested_dictionary(sql_database)
                    database_name = sql_database_dict["name"]
                    sql_database_id = sql_database_dict["id"]
                    current_sku_tier = sql_database_dict.get("current_sku").get("tier")

                    if sql_database_dict.get("sku"):
                        if (
                            sql_database_dict.get("name") != "master"
                        ):  # No pricing tier for system database
                            sql_database_dict.update(
                                {
                                    "pricing_tier_display": self.get_pricing_tier_display(
                                        sql_database_dict["sku"]
                                    ),
                                    "service_tier_display": sql_database_dict[
                                        "sku"
                                    ].get("tier"),
                                }
                            )

                    if db_id := sql_database_dict.get("id"):
                        sql_database_dict.update(
                            {
                                "server_name": db_id.split("/")[8],
                                "subscription_id": db_id.split("/")[2],
                                "resource_group": db_id.split("/")[4],
                                "azure_monitor": {"resource_id": db_id},
                            }
                        )

                    if compute_tier := sql_database_dict.get("kind"):
                        sql_database_dict.update(
                            {"compute_tier": self.get_db_compute_tier(compute_tier)}
                        )

                    if sql_database_dict.get("max_size_bytes"):
                        sql_database_dict.update(
                            {
                                "max_size_gb": sql_database_dict["max_size_bytes"]
                                / 1073741824  # 2^30
                            }
                        )

                    # Get Sync Groups by databases
                    if current_sku_tier not in ["DataWarehouse", "Hyperscale"]:
                        sql_database_sync_groups = (
                            sql_databases_conn.list_sync_groups_by_databases(
                                resource_group=resource_group_name,
                                server_name=server_name,
                                database_name=database_name,
                            )
                        )

                        sql_database_dict.update(
                            {
                                "sync_group": self.get_sync_group_by_databases(
                                    sql_database_sync_groups
                                )
                            }
                        )

                    if sql_database_dict.get("sync_group"):
                        sql_database_dict.update(
                            {
                                "sync_group_display": self.get_sync_group_display(
                                    sql_database_dict["sync_group"]
                                )
                            }
                        )

                    # Get Sync Agents by servers
                    sql_database_dict.update(
                        {
                            "sync_agent": self.get_sync_agent_by_servers(
                                sql_databases_conn, resource_group_name, server_name
                            )
                        }
                    )

                    if sql_database_dict["sync_agent"]:
                        sql_database_dict.update(
                            {
                                "sync_agent_display": self.get_sync_agent_display(
                                    sql_database_dict["sync_agent"]
                                )
                            }
                        )

                    # Get Diagnostic Settings
                    sql_database_dict.update(
                        {
                            "diagnostic_settings_resource": self.list_diagnostics_settings(
                                sql_monitor_conn, sql_database_dict["id"]
                            )
                        }
                    )
                    # Get Database Replication Type
                    sql_database_dict.update(
                        {
                            "replication_link": self.list_replication_link_in_database(
                                replication_links, database_name=database_name
                            )
                        }
                    )
                    # Get azure_ad_admin name
                    if server_admin_name is not None:
                        sql_database_dict.update(
                            {"administrator_login": server_admin_name}
                        )

                    # Get Database Auditing settings
                    sql_database_dict.update(
                        {
                            "database_auditing_settings": self.get_database_auditing_settings(
                                sql_databases_conn,
                                resource_group_name,
                                server_name,
                                database_name=database_name,
                            )
                        }
                    )

                    sql_database_dict.update(
                        {
                            "resource_group": resource_group_name,
                            "subscription_id": subscription_info["subscription_id"],
                            "subscription_name": subscription_info["display_name"],
                            "azure_monitor": {"resource_id": sql_database_id},
                        }
                    )

                    self.set_region_code(sql_database_dict["location"])

                    cloud_services.append(
                        make_cloud_service(
                            name=database_name,
                            cloud_service_type=self.cloud_service_type,
                            cloud_service_group=self.cloud_service_group,
                            provider=self.provider,
                            data=sql_database_dict,
                            account=secret_data["subscription_id"],
                            instance_type=sql_database_dict["sku"]["tier"],
                            instance_size=float(sql_database_dict["max_size_gb"]),
                            region_code=sql_database_dict["location"],
                            reference=self.make_reference(sql_database_dict.get("id")),
                            # launched_at=sql_database_dict["creation_date"],
                            tags=sql_database_dict.get("tags", {}),
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

    def list_replication_links(self, replication_links_from_params) -> list:
        replication_links = []
        for replication_link in replication_links_from_params:
            replication_link_dict = self.convert_nested_dictionary(replication_link)
            replication_link_dict["replica_state"] = (
                "Online" if replication_link_dict["role"] == "Primary" else "Readable"
            )
            replication_links.append(replication_link_dict)

        return replication_links

    def get_sync_group_by_databases(self, replication_links_from_params: list) -> list:
        sync_groups = []
        for sync_group in replication_links_from_params:
            sync_group_dict = self.convert_nested_dictionary(sync_group)
            sync_group_dict["automatic_sync"] = (
                True if sync_group_dict["interval"] > 0 else True
            )
            sync_groups.append(sync_group_dict)

        return sync_groups

    def get_sync_agent_by_servers(self, sql_servers_conn, rg_name, server_name):
        sync_agent_list = list()
        sync_agent_obj = sql_servers_conn.list_sync_agents_by_server(
            rg_name, server_name
        )

        for sync_agent in sync_agent_obj:
            sync_agent_dict = self.convert_nested_dictionary(sync_agent)
            sync_agent_list.append(sync_agent_dict)

        return sync_agent_list

    def list_diagnostics_settings(self, sql_monitor_conn, resource_uri):
        diagnostic_settings_list = list()
        diagnostic_settings_objs = sql_monitor_conn.list_diagnostic_settings(
            resource_uri=resource_uri
        )

        for diagnostic_setting in diagnostic_settings_objs:
            diagnostic_setting_dict = self.convert_nested_dictionary(diagnostic_setting)
            diagnostic_settings_list.append(diagnostic_setting_dict)

        return diagnostic_settings_list

    def get_database_auditing_settings(
        self, sql_databases_conn, resource_group_name, server_name, database_name
    ):
        database_auditing_settings = sql_databases_conn.get_database_auditing_settings(
            resource_group_name=resource_group_name,
            server_name=server_name,
            database_name=database_name,
        )
        return self.convert_nested_dictionary(database_auditing_settings)

    @staticmethod
    def get_pricing_tier_display(sku_dict):
        if sku_dict["name"] in ["Basic", "Standard", "Premium"]:
            pricing_tier = f'{sku_dict["tier"]}: {sku_dict["capacity"]} DTU'
        else:
            pricing_tier = f'{str(sku_dict["tier"])} : {str(sku_dict["family"])} , {str(sku_dict["capacity"])} vCores'
        return pricing_tier

    @staticmethod
    def get_db_compute_tier(kind):
        if "serverless" in kind:
            compute_tier = "Serverless"
        else:
            compute_tier = "Provisioned"

        return compute_tier

    @staticmethod
    def get_sync_group_display(sync_group_list):
        sync_group_display_list = []
        for sync_group in sync_group_list:
            sync_display = f"{sync_group['name']} / {sync_group['conflict_resolution_policy']} / {sync_group['sync_state']}"
            sync_group_display_list.append(sync_display)

        return sync_group_display_list

    @staticmethod
    def get_sync_agent_display(sync_agent_list):
        sync_agent_display_list = []
        for sync_agent in sync_agent_list:
            sync_display = f"{sync_agent['name']} / {sync_agent['state']}"
            sync_agent_display_list.append(sync_display)

        return sync_agent_display_list

    @staticmethod
    def list_replication_link_in_database(
        replication_links_from_params, database_name
    ) -> list:
        replication_links = []
        for replication_link in replication_links_from_params:
            if replication_link["partner_database"] == database_name:
                replication_links.append(replication_link)

        return replication_links
