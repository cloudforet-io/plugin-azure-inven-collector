import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.postgre_sql_servers.postgresql_servers_connector import (
    PostgreSQLServersConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class PostgreSQLServersManager(AzureBaseManager):
    cloud_service_group = "PostgreSQLServers"
    cloud_service_type = "Server"
    service_code = "/Microsoft.DBforPostgreSQL/servers"

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

        postgre_sql_servers_conn = PostgreSQLServersConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        postgre_sql_servers = postgre_sql_servers_conn.list_servers()

        for postgre_sql_server in postgre_sql_servers:

            try:
                postgre_sql_server_dict = self.convert_nested_dictionary(
                    postgre_sql_server
                )
                postgre_sql_server_id = postgre_sql_server_dict["id"]

                # update application_gateway_dict
                postgre_sql_server_dict = self.update_tenant_id_from_secret_data(
                    postgre_sql_server_dict, secret_data
                )

                postgre_sql_server_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            postgre_sql_server_id
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": postgre_sql_server_id},
                    }
                )

                if postgre_sql_server_dict.get("name") is not None:
                    resource_group = postgre_sql_server_dict["resource_group"]
                    server_name = postgre_sql_server_dict["name"]
                    postgre_sql_server_dict.update(
                        {
                            "firewall_rules": self.list_firewall_rules_by_server(
                                postgre_sql_servers_conn, resource_group, server_name
                            ),
                            "virtual_network_rules": self.list_virtual_network_rules_by_server(
                                postgre_sql_servers_conn, resource_group, server_name
                            ),
                            "replicas": self.list_replicas_by_server(
                                postgre_sql_servers_conn, resource_group, server_name
                            ),
                            "server_administrators": self.list_server_administrators(
                                postgre_sql_servers_conn, resource_group, server_name
                            ),
                        }
                    )

                self.set_region_code(postgre_sql_server_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=postgre_sql_server_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=postgre_sql_server_dict,
                        account=secret_data["subscription_id"],
                        instance_type=postgre_sql_server_dict["sku"]["tier"],
                        instance_size=float(
                            postgre_sql_server_dict["storage_profile"]["max_size_gb"]
                        ),
                        region_code=postgre_sql_server_dict["location"],
                        reference=self.make_reference(
                            postgre_sql_server_dict.get("id")
                        ),
                        tags=postgre_sql_server_dict.get("tags", {}),
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

    def get_sql_resources(self, cosmos_db_conn, account_name, resource_group):
        sql_resources = []
        sql_resources_obj = cosmos_db_conn.list_sql_resources(
            account_name=account_name, resource_group_name=resource_group
        )

        for sql in sql_resources_obj:
            sql_dict = self.convert_nested_dictionary(sql)
            sql_resources.append(sql_dict)
        return sql_resources

    def list_firewall_rules_by_server(self, postgresql_conn, resource_group, name):
        firewall_rules = []
        firewall_rules_obj = postgresql_conn.list_firewall_rules_by_server(
            resource_group_name=resource_group, server_name=name
        )

        for firewall_rule in firewall_rules_obj:
            firewall_rule_dict = self.convert_nested_dictionary(firewall_rule)
            firewall_rules.append(firewall_rule_dict)

        return firewall_rules

    def list_virtual_network_rules_by_server(
        self, postgresql_conn, resource_group, name
    ):
        virtual_network_rules = []
        virtual_network_rules_obj = (
            postgresql_conn.list_virtual_network_rules_by_server(
                resource_group_name=resource_group, server_name=name
            )
        )

        for virtual_network in virtual_network_rules_obj:
            virtual_network_dict = self.convert_nested_dictionary(virtual_network)
            if virtual_network_dict.get("virtual_network_subnet_id") is not None:
                virtual_network_dict.update(
                    {
                        "subnet_name": self.get_subnet_name(
                            virtual_network_dict["virtual_network_subnet_id"]
                        ),
                        "virtual_network_name_display": self.get_virtual_network_name(
                            virtual_network_dict["virtual_network_subnet_id"]
                        ),
                    }
                )
            virtual_network_rules.append(virtual_network_dict)

        return virtual_network_rules

    def list_replicas_by_server(self, postgresql_conn, resource_group, name):
        replicas_list = []
        replicas_obj = postgresql_conn.list_replicas_by_server(
            resource_group_name=resource_group, server_name=name
        )
        for replica in replicas_obj:
            replica_dict = self.convert_nested_dictionary(replica)
            if replica_dict.get("master_server_id") is not None:
                replica_dict.update(
                    {
                        "master_server_name": self.get_replica_master_server_name(
                            replica_dict["master_server_id"]
                        )
                    }
                )

            replicas_list.append(replica_dict)
        return replicas_list

    def list_server_administrators(self, postgresql_conn, resource_group, name):
        server_administrators = []
        server_admin_obj = postgresql_conn.list_server_administrators(
            resource_group_name=resource_group, server_name=name
        )
        for server_admin in server_admin_obj:
            server_admin_dict = self.convert_nested_dictionary(server_admin)
            server_administrators.append(server_admin_dict)

        return server_administrators

    @staticmethod
    def get_subnet_name(subnet_id):
        subnet_name = ""
        if subnet_id:
            subnet_name = subnet_id.split("/")[10]
        return subnet_name

    @staticmethod
    def get_virtual_network_name(subnet_id):
        virtual_network_name = ""
        if subnet_id:
            virtual_network_name = subnet_id.split("/")[8]
        return virtual_network_name

    @staticmethod
    def get_replica_master_server_name(master_server_id):
        master_server_name = master_server_id.split("/")[8]
        return master_server_name
