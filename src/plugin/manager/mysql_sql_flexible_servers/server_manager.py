import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.mysql_sql_flexible_servers.mysql_flexible_servers_connector import (
    MySQLFlexibleServersConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class MySQLFlexibleServersManager(AzureBaseManager):
    cloud_service_group = "MySQLFlexibleServers"
    cloud_service_type = "Server"
    service_code = "/Microsoft.DBforMySQL/flexibleServers"

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
            tags={"spaceone:icon": f"{ICON_URL}/azure-mysql-servers.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        mysql_flexible_servers_conn = MySQLFlexibleServersConnector(
            secret_data=secret_data
        )
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        mysql_flexible_servers_obj_list = (
            mysql_flexible_servers_conn.list_flexible_servers()
        )

        for mysql_flexible_server in mysql_flexible_servers_obj_list:

            try:
                mysql_flexible_server_dict = self.convert_nested_dictionary(
                    mysql_flexible_server
                )
                mysql_flexible_server_id = mysql_flexible_server_dict["id"]

                mysql_flexible_server_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            mysql_flexible_server_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": mysql_flexible_server_id},
                    }
                )

                if mysql_flexible_server_dict.get("name") is not None:
                    resource_group = mysql_flexible_server_dict.get(
                        "resource_group", ""
                    )
                    server_name = mysql_flexible_server_dict.get("name")
                    mysql_flexible_server_dict.update(
                        {
                            "firewall_rules": self.get_firewall_rules_by_server(
                                mysql_flexible_servers_conn, resource_group, server_name
                            ),
                        }
                    )

                if mysql_flexible_server_dict.get("firewall_rules") is not None:
                    mysql_flexible_server_dict.update(
                        {
                            "allow_azure_services_access": self.get_azure_service_access(
                                mysql_flexible_server_dict["firewall_rules"]
                            )
                        }
                    )

                self.set_region_code(mysql_flexible_server_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=mysql_flexible_server_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=mysql_flexible_server_dict,
                        account=secret_data["subscription_id"],
                        instance_type="Azure DB for MySQL Flexible Server",
                        region_code=mysql_flexible_server_dict["location"],
                        reference=self.make_reference(
                            mysql_flexible_server_dict.get("id")
                        ),
                        tags=mysql_flexible_server_dict.get("tags", {}),
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

    def get_firewall_rules_by_server(
        self, mysql_flexible_servers_conn, resource_group, server_name
    ):
        firewall_rules = []
        firewall_rule_obj = mysql_flexible_servers_conn.list_firewall_rules_by_server(
            resource_group_name=resource_group, server_name=server_name
        )

        for firewall_rule in firewall_rule_obj:
            firewall_dict = self.convert_nested_dictionary(firewall_rule)
            firewall_rules.append(firewall_dict)

        return firewall_rules

    @staticmethod
    def get_azure_service_access(firewall_rules):
        firewall_rule_name_list = []

        for firewall_rule in firewall_rules:
            if firewall_rule.get("name") is not None:
                firewall_rule_name_list.append(firewall_rule["name"])

        if "AllowAllWindowsAzureIps" in firewall_rule_name_list:
            return True

        return False
