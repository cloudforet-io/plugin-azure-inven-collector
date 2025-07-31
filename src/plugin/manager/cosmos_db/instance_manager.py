import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.cosmos_db.cosmos_db_connector import CosmosDBConnector
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class CosmosDBManager(AzureBaseManager):
    cloud_service_group = "CosmosDB"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.DocumentDB/databaseAccounts"

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
            tags={"spaceone:icon": f"{ICON_URL}/azure-cosmos-db.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        cosmos_db_conn = CosmosDBConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        cosmos_db_accounts_list = cosmos_db_conn.list_all_cosmos_db_accounts()

        for cosmos_db_account in cosmos_db_accounts_list:

            try:
                cosmos_db_account_dict = self.convert_nested_dictionary(
                    cosmos_db_account
                )
                cosmos_db_account_id = cosmos_db_account_dict.get("id")
                cosmos_db_account_dict["location"] = (
                    cosmos_db_account_dict["location"].replace(" ", "").lower()
                )

                # update cosmosdb_dict
                cosmos_db_account_dict = self.update_tenant_id_from_secret_data(
                    cosmos_db_account_dict, secret_data
                )
                cosmos_db_account_dict.update(
                    {
                        "resource_group": self.get_resource_group_from_id(
                            cosmos_db_account_dict["id"]
                        ),
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": cosmos_db_account_id},
                    }
                )

                if cosmos_db_account_dict.get("capabilities") is not None:
                    cosmos_db_account_dict.update(
                        {
                            "capability_display": self.get_capability_type(
                                cosmos_db_account_dict["capabilities"]
                            )
                        }
                    )

                if cosmos_db_account_dict.get("virtual_network_rules") is not None:
                    cosmos_db_account_dict.update(
                        {
                            "virtual_network_display": self.get_virtual_networks(
                                cosmos_db_account_dict["virtual_network_rules"]
                            )
                        }
                    )

                if (
                    cosmos_db_account_dict.get("private_endpoint_connections")
                    is not None
                ):
                    for private_connection in cosmos_db_account_dict[
                        "private_endpoint_connections"
                    ]:
                        private_connection.update(
                            {
                                "private_endpoint": self.get_private_endpoint_name(
                                    private_connection["private_endpoint"]
                                ),
                                "name": self.get_private_connection_name(
                                    private_connection["id"]
                                ),
                            }
                        )

                if cosmos_db_account_dict.get("cors") is not None:
                    cosmos_db_account_dict.update(
                        {
                            "cors_display": self.get_cors_display(
                                cosmos_db_account_dict["cors"]
                            )
                        }
                    )

                if cosmos_db_account_dict.get("name") is not None:
                    sql_databases = self.get_sql_resources(
                        cosmos_db_conn,
                        cosmos_db_account_dict["name"],
                        cosmos_db_account_dict["resource_group"],
                    )

                    cosmos_db_account_dict.update(
                        {
                            # "keys": self.get_keys(
                            #     cosmos_db_conn,
                            #     cosmos_db_account_dict["name"],
                            #     cosmos_db_account_dict["resource_group"],
                            # ),
                            "sql_databases": sql_databases,
                            "sql_databases_count_display": len(sql_databases),
                        }
                    )

                self.set_region_code(cosmos_db_account_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=cosmos_db_account_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=cosmos_db_account_dict,
                        account=secret_data["subscription_id"],
                        instance_type=cosmos_db_account_dict[
                            "database_account_offer_type"
                        ],
                        region_code=cosmos_db_account_dict["location"],
                        reference=self.make_reference(cosmos_db_account_dict.get("id")),
                        # launched_at=cosmos_db_account_dict.system_data.created_at,
                        tags=cosmos_db_account_dict.get("tags", {}),
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

    def get_keys(self, cosmos_db_conn, account_name, resource_group):
        keys_obj = cosmos_db_conn.list_keys(
            account_name=account_name, resource_group_name=resource_group
        )
        key_dict = self.convert_nested_dictionary(keys_obj)
        return key_dict

    def get_sql_resources(self, cosmos_db_conn, account_name, resource_group):
        sql_resources = []
        sql_resources_obj = cosmos_db_conn.list_sql_resources(
            account_name=account_name, resource_group_name=resource_group
        )

        for sql in sql_resources_obj:
            sql_dict = self.convert_nested_dictionary(sql)
            sql_resources.append(sql_dict)
        return sql_resources

    @staticmethod
    def get_capability_type(capabilities):
        if capabilities:
            capability_str_list = []
            for capability in capabilities:
                capability_str_list.append(capability.get("name"))

            if "EnableServerless" in capability_str_list:
                return "Serverless"
            else:
                return "Provisioned Throughput"

    @staticmethod
    def get_virtual_networks(virtual_network_rules):
        virtual_network_rules_display = []

        for virtual_network in virtual_network_rules:
            virtual_network_name = virtual_network["id"].split("/")[8]
            virtual_network_rules_display.append(virtual_network_name)

            return virtual_network_rules_display

    @staticmethod
    def get_private_endpoint_name(private_endpoint):
        if private_endpoint.get("id") is not None:
            private_endpoint.update({"name": private_endpoint["id"].split("/")[8]})
            return private_endpoint

    @staticmethod
    def get_private_connection_name(private_connection_id):
        private_connection_name = private_connection_id.split("/")[10]
        return private_connection_name

    @staticmethod
    def get_cors_display(cors_list):
        cors_display = []

        for cors in cors_list:
            cors_display.append(cors.get("allowed_origins", ""))
        return cors_display
