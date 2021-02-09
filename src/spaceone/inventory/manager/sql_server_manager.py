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

            # Get Server Automatic Tuning
            server_automatic_tuning_dict = self.get_server_automatic_tuning(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            if server_automatic_tuning_dict == {}:  # if automatic tuning is not configured
                sql_servers_dict.update({
                    'server_automatic_tuning_display': False
                })
            else:
                sql_servers_dict.update({
                    'server_automatic_tuning': server_automatic_tuning_dict,
                    'server_automatic_tuning_display': True
                })

            # Get Server Auditing Settings, Failover groups. azure ad administrators
            server_auditing_settings_dict = self.get_server_auditing_settings(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            failover_dict = self.list_failover_groups(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            # transparent_data_encryption_dict = self.get_transparent_data_encryption_dict(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name']) -> DB에서 조회
            azure_ad_admin_dict = self.list_azure_ad_administrators(self, sql_servers_conn, sql_servers_dict['resource_group'], sql_servers_dict['name'])
            sql_servers_dict.update({
                'server_auditing_settings': server_auditing_settings_dict,
                'failover_groups': failover_dict,
                'azure_ad_administrators': azure_ad_admin_dict

            })

            # switch tags form
            tags = sql_servers_dict.get('tags', {})
            _tags = self.convert_tag_format(tags)
            sql_servers_dict.update({
                'tags': _tags
            })

            sql_servers_data = SqlServer(sql_servers_dict, strict=False)

            # print("sql_server_dict")
            # print(sql_servers_dict)

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
    def list_azure_ad_administrators(self, sql_servers_conn, rg_name, server_name):  # TODO: here
        ad_admin_dict = dict()
        ad_admin_obj = sql_servers_conn.list_server_azure_ad_administrators(resource_group=rg_name, server_name=server_name)
        print("ad_admin_obj")
        print(ad_admin_obj)

        '''
        ad_admin_dict['data'] = self.convert_dictionary(ad_admin_obj)
        ad_admin_dict.update({
            'data': self.convert_nested_dictionary(self,  ad_admin_dict['data'])
        })
        '''
        return ad_admin_dict

    @staticmethod
    def get_server_automatic_tuning(self, sql_servers_conn, rg_name, server_name):
        server_automatic_tuning_obj = sql_servers_conn.get_server_automatic_tuning(rg_name, server_name)
        server_automatic_tuning_dict = self.convert_nested_dictionary(self, server_automatic_tuning_obj)

        return server_automatic_tuning_dict

    @staticmethod
    def get_server_auditing_settings(self, sql_servers_conn, rg_name, server_name):
        server_auditing_settings_obj = sql_servers_conn.get_server_auditing_settings(rg_name, server_name)
        server_auditing_settings_dict = self.convert_nested_dictionary(self, server_auditing_settings_obj)

        return server_auditing_settings_dict

    @staticmethod
    def list_failover_groups(self, sql_servers_conn, rg_name, server_name):
        failover_groups_dict = dict()
        failover_groups_obj = sql_servers_conn.list_failover_groups(rg_name, server_name)
        failover_groups_dict['data'] = next(failover_groups_obj, {})

        if len(failover_groups_dict['data']) != 0:
            failover_groups_dict = self.convert_nested_dictionary(self, failover_groups_dict['data'])

        return failover_groups_dict

