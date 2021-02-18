from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.sqlserver import *
from spaceone.inventory.model.sqlserver.cloud_service import *
from spaceone.inventory.connector.sql import SqlConnector
from spaceone.inventory.connector.subscription import SubscriptionConnector
from spaceone.inventory.model.sqlserver.cloud_service_type import CLOUD_SERVICE_TYPES
from datetime import datetime
import time
import copy


class SqlServerManager(AzureManager):
    connector_name = 'SqlConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Sql Servers START **")
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
                - subscription_info
        Response:
            CloudServiceResponse
        """
        secret_data = params['secret_data']
        # subscription_info = params['subscription_info']
        subscription_info = {
            'subscription_id': '3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca',
            'subscription_name': 'Azure subscription 1',
            'tenant_id': '35f43e22-0c0b-4ff3-90aa-b2c04ef1054c'
        }

        sql_servers_conn: SqlConnector = self.locator.get_connector(self.connector_name, **params)
        sql_servers = []
        for sql_server in sql_servers_conn.list_servers():
            sql_servers_dict = self.convert_nested_dictionary(self, sql_server)

            # update sql_servers_data dict
            sql_servers_dict.update({
                'resource_group': self.get_resource_group_from_id(sql_servers_dict['id']),  # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            # Get Server Auditing Settings, Failover groups. azure ad administrators
            server_auditing_settings_dict = self.get_server_auditing_settings(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            failover_group_list = self.list_failover_groups(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            # transparent_data_encryption_dict = self.get_transparent_data_encryption_dict(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name']) -> DB에서 조회
            azure_ad_admin_list = self.list_azure_ad_administrators(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            server_automatic_tuning_dict = self.get_server_automatic_tuning(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            databases_list = self.list_databases(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            elastic_pools_list = self.list_elastic_pools(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            deleted_databases_list = self.list_deleted_databases(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])

            sql_servers_dict.update({
                'azure_ad_administrators': azure_ad_admin_list,
                'server_auditing_settings': server_auditing_settings_dict,
                'failover_groups': failover_group_list,
                'server_automatic_tuning': server_automatic_tuning_dict,
                'databases': databases_list,
                'elastic_pools': elastic_pools_list,
                'deleted_databases': deleted_databases_list
            })

            if sql_servers_dict.get('azure_ad_administrators') is not None:
                sql_servers_dict.update({
                    'azure_ad_admin_name': self.get_azure_ad_admin_name(sql_servers_dict['azure_ad_administrators'])
                })

            # switch tags form
            tags = sql_servers_dict.get('tags', {})
            _tags = self.convert_tag_format(tags)
            sql_servers_dict.update({
                'tags': _tags
            })

            sql_servers_data = SqlServer(sql_servers_dict, strict=False)

            print("sql_server_dict")
            print(sql_servers_dict)

            sql_servers_resource = SqlServerResource({
                'data': sql_servers_data,
                'region_code': sql_servers_data.location,
                'reference': ReferenceModel(sql_servers_data.reference()),
                'tags':  _tags
            })

            # Must set_region_code method for region collection
            self.set_region_code(sql_servers_data['location'])

            sql_servers.append(SqlServerResponse({'resource': sql_servers_resource}))

        print(f'** Sql Servers Finished {time.time() - start_time} Seconds **')
        return sql_servers

    @staticmethod
    def get_resource_group_from_id(sql_server_id):
        resource_group = sql_server_id.split('/')[4].lower()
        return resource_group

    @staticmethod
    def list_databases(self, sql_servers_conn, rg_name, server_name):
        databases_list = list()
        databases = sql_servers_conn.list_databases_by_server(resource_group=rg_name, server_name=server_name)

        for database in databases:
            database_dict = self.convert_nested_dictionary(self, database)
            if database_dict.get('sku') is not None:
                if database_dict.get('name') != 'master':  # No pricing tier for system database
                    database_dict.update({
                        'pricing_tier_display': self.get_pricing_tier_display(database_dict['sku'])
                    })
            databases_list.append(database_dict)

        return databases_list

    @staticmethod
    def list_elastic_pools(self, sql_servers_conn, rg_name, server_name):
        elastic_pools_list = list()
        elastic_pools = sql_servers_conn.list_elastic_pools_by_server(resource_group=rg_name, server_name=server_name)

        for elastic_pool in elastic_pools:
            elastic_pool_dict = self.convert_nested_dictionary(self, elastic_pool)

            # Get Databases list by elastic pool
            elastic_pool_dict['databases'] = self.get_databases_by_elastic_pools(self, sql_servers_conn, elastic_pool_dict['name'], rg_name, server_name)

            # Get pricing tier for display
            if elastic_pool_dict.get('per_database_settings') is not None:
                elastic_pool_dict.update({
                    'pricing_tier_display': self.get_pricing_tier_display(elastic_pool_dict['sku']),
                    'per_db_settings_display': self.get_per_db_settings(elastic_pool_dict['per_database_settings']),
                    'number_of_databases': len(elastic_pool_dict['databases']),
                    'unit_display': elastic_pool_dict['sku']['tier'],
                    'server_name_display': elastic_pool_dict['id'].split('/')[8],
                    'resource_group_display': elastic_pool_dict['id'].split('/')[4],
                    'max_size_gb': elastic_pool_dict['max_size_bytes'] / 1073741824
                })

            elastic_pools_list.append(elastic_pool_dict)

        return elastic_pools_list

    @staticmethod
    def get_databases_by_elastic_pools(self, sql_servers_conn, elastic_pool_name, rg_name, server_name):
        databases_obj = sql_servers_conn.list_databases_by_elastic_pool(elastic_pool_name, rg_name, server_name)
        databases_list = list()
        for database in databases_obj:
            database_dict = self.convert_nested_dictionary(self, database)
            databases_list.append(database_dict)

        return databases_list

    @staticmethod
    def list_deleted_databases(self, sql_servers_conn, rg_name, server_name):
        deleted_databases_obj = sql_servers_conn.list_restorable_dropped_databases_by_server(resource_group=rg_name, server_name=server_name)
        deleted_databases_list = list()
        for deleted_database in deleted_databases_obj:
            deleted_database_dict = self.convert_nested_dictionary(self, deleted_database)
            deleted_databases_list.append(deleted_database_dict)

        return deleted_databases_list

    @staticmethod
    def get_per_db_settings(per_database_settings_dict):
        per_db_settings = str(per_database_settings_dict['min_capacity']) + " - " + str(per_database_settings_dict['max_capacity']) + "vCores"
        return per_db_settings

    @staticmethod
    def get_pricing_tier_display(sku_dict):
        if sku_dict.get('capacity') is not None:
            pricing_tier = str(sku_dict['tier']) + " : " + str(sku_dict['family']) + " , " + str(sku_dict['capacity']) + " vCores"
        return pricing_tier

    @staticmethod
    def list_azure_ad_administrators(self, sql_servers_conn, rg_name, server_name):
        ad_admin_list = list()  # return list
        ad_admin_obj = sql_servers_conn.list_server_azure_ad_administrators(resource_group=rg_name, server_name=server_name)

        for ad_admin in ad_admin_obj:
            ad_admin_list.append(self.convert_dictionary(ad_admin))

        return ad_admin_list

    @staticmethod
    def get_server_automatic_tuning(self, sql_servers_conn, rg_name, server_name):
        server_automatic_tuning_obj = sql_servers_conn.get_server_automatic_tuning(rg_name, server_name)
        server_automatic_tuning_dict = self.convert_nested_dictionary(self, server_automatic_tuning_obj)
        print("server automatic tuning dict")
        print(server_automatic_tuning_dict)

        return server_automatic_tuning_dict

    @staticmethod
    def get_server_auditing_settings(self, sql_servers_conn, rg_name, server_name):
        server_auditing_settings_obj = sql_servers_conn.get_server_auditing_settings(rg_name, server_name)
        server_auditing_settings_dict = self.convert_nested_dictionary(self, server_auditing_settings_obj)

        return server_auditing_settings_dict

    @staticmethod
    def list_failover_groups(self, sql_servers_conn, rg_name, server_name):
        failover_groups_list = list()
        failover_groups_obj = sql_servers_conn.list_failover_groups(rg_name, server_name)
        for failover in failover_groups_obj:
            failover_dict = self.convert_nested_dictionary(self, failover)

            if failover_dict.get('id') is not None:  # Get Primary server's name
                failover_dict.update({
                    'primary_server': failover_dict['id'].split('/')[8]
                })

            if failover_dict.get('partner_servers') is not None:  # Get Secondary Server's name
                failover_dict.update({
                    'secondary_server': self.get_failover_secondary_server(failover_dict['partner_servers'])
                })

            if failover_dict.get('read_write_endpoint') is not None:
                failover_dict.update({
                    'failover_policy_display': failover_dict['read_write_endpoint'].get('failover_policy'),
                    'grace_period_display': failover_dict['read_write_endpoint'].get('failover_with_data_loss_grace_period_minutes')
                })

            failover_groups_list.append(failover_dict)

        return failover_groups_list

    @staticmethod
    def get_failover_secondary_server(partner_servers):
        for partner_server in partner_servers:
            if partner_server['replication_role'] == 'Secondary':
                secondary_server = partner_server['id'].split('/')[8]
            else:
                secondary_server = None

        return secondary_server

    @staticmethod
    def get_azure_ad_admin_name(azure_ad_administrators_list):
        az_admin_name = ''

        for az_admin in azure_ad_administrators_list:
            if az_admin.get('login') is not None:
                az_admin_name = az_admin.get('login')

        return az_admin_name
