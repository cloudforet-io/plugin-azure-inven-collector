import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.postgre_sql_flexible_servers.postgresql_flexible_servers_connector import (
    PostgreSQLFlexibleServersConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class PostgreSQLFlexibleServersManager(AzureBaseManager):
    cloud_service_group = "PostgreSQLFlexibleServers"
    cloud_service_type = "Server"
    service_code = "/Microsoft.DBforPostgreSQL/flexibleServers"

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
            tags={"spaceone:icon": f"{ICON_URL}/azure-sql-postgresql-server.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        postgre_sql_flexible_servers_conn = PostgreSQLFlexibleServersConnector(
            secret_data=secret_data
        )
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        postgre_sql_flexible_servers = (
            postgre_sql_flexible_servers_conn.list_flexible_servers()
        )

        for postgre_sql_flexible_server in postgre_sql_flexible_servers:

            try:
                postgre_sql_flexible_server_dict = self.convert_nested_dictionary(
                    postgre_sql_flexible_server
                )
                postgre_sql_flexible_server_id = postgre_sql_flexible_server_dict["id"]

                postgre_sql_flexible_server_dict = (
                    self.update_tenant_id_from_secret_data(
                        postgre_sql_flexible_server_dict, secret_data
                    )
                )

                postgre_sql_flexible_server_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            postgre_sql_flexible_server_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {
                            "resource_id": postgre_sql_flexible_server_id
                        },
                        "version_display": self.get_version_display(
                            postgre_sql_flexible_server_dict.get("version"),
                            postgre_sql_flexible_server_dict.get("minor_version"),
                        ),
                    }
                )

                if postgre_sql_flexible_server_dict.get("name") is not None:
                    resource_group = postgre_sql_flexible_server_dict["resource_group"]
                    server_name = postgre_sql_flexible_server_dict["name"]
                    postgre_sql_flexible_server_dict.update(
                        {
                            "firewall_rules": self.list_firewall_rules_by_server(
                                postgre_sql_flexible_servers_conn,
                                resource_group,
                                server_name,
                            ),
                        }
                    )

                self.set_region_code(postgre_sql_flexible_server_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=postgre_sql_flexible_server_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=postgre_sql_flexible_server_dict,
                        account=secret_data["subscription_id"],
                        instance_type="Azure DB for PostgreSQL Flexible Server",
                        instance_size=float(
                            postgre_sql_flexible_server_dict["storage"][
                                "storage_size_gb"
                            ]
                        ),
                        region_code=postgre_sql_flexible_server_dict["location"],
                        reference=self.make_reference(
                            postgre_sql_flexible_server_dict.get("id")
                        ),
                        tags=postgre_sql_flexible_server_dict.get("tags", {}),
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

    def list_firewall_rules_by_server(self, postgresql_conn, resource_group, name):
        firewall_rules = []
        firewall_rules_obj = postgresql_conn.list_firewall_rules_by_server(
            resource_group_name=resource_group, server_name=name
        )

        for firewall_rule in firewall_rules_obj:
            firewall_rule_dict = self.convert_nested_dictionary(firewall_rule)
            firewall_rules.append(firewall_rule_dict)

        return firewall_rules

    @staticmethod
    def get_version_display(version, minor_version):
        version_display = f"{version}.{minor_version}"
        return version_display
