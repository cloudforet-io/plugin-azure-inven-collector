import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.sql_servers.cloud_service import *
from spaceone.inventory.model.sql_databases.cloud_service import *
from spaceone.inventory.connector.sql_servers import SQLServersConnector
from spaceone.inventory.connector.monitor import MonitorConnector
from spaceone.inventory.model.sql_servers.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.sql_databases.data import *
from spaceone.inventory.model.sql_servers.data import *
from spaceone.inventory.manager.sql_databases.database_manager import SQLDatabasesManager
from spaceone.core.utils import *

_LOGGER = logging.getLogger(__name__)


class SQLServersManager(AzureManager):
    connector_name = 'SQLServersConnector'
    monitor_connector_name = 'MonitorConnector'

    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        """
           Args:
               params (dict):
                   - 'options' : 'dict'
                   - 'schema' : 'str'
                   - 'secret_data' : 'dict'
                   - 'filter' : 'dict'
                   - 'zones' : 'list'
                   - 'subscription_info' :  'dict'
           Response:
               CloudServiceResponse (list) : dictionary of azure sql servers data resource information
               ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug(f'** SQL Servers START **')
        start_time = time.time()

        subscription_info = params['subscription_info']

        sql_servers_conn: SQLServersConnector = self.locator.get_connector(self.connector_name, **params)
        sql_servers_monitor_conn: MonitorConnector = self.locator.get_connector(self.monitor_connector_name, **params)

        sql_server_responses = []
        error_responses = []

        sql_servers = sql_servers_conn.list_servers()

        for sql_server in sql_servers:
            sql_server_id = ''

            try:
                sql_server_dict = self.convert_nested_dictionary(sql_server)
                sql_server_id = sql_server_dict['id']

                # update sql_servers_data dict
                sql_server_dict.update({
                    'resource_group': self.get_resource_group_from_id(sql_server_id),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': sql_server_id}
                })

                resource_group_name = sql_server_dict['resource_group']
                name = sql_server_dict['name']

                # Get Server Auditing Settings, Failover groups. azure ad administrators
                server_auditing_settings_dict = self.get_server_auditing_settings(sql_servers_conn, resource_group_name,
                                                                                  name)
                failover_group_list = self.list_failover_groups(sql_servers_conn, resource_group_name, name)
                transparent_data_encryption_dict = self.list_encryption_protectors(sql_servers_conn,
                                                                                   resource_group_name, name)
                azure_ad_admin_list = self.list_azure_ad_administrators(sql_servers_conn, resource_group_name, name)
                server_automatic_tuning_dict = self.get_server_automatic_tuning(sql_servers_conn, resource_group_name,
                                                                                name)
                databases_list = self.list_databases(sql_servers_conn=sql_servers_conn,
                                                     sql_monitor_conn=sql_servers_monitor_conn,
                                                     resource_group_name=resource_group_name, server_name=name,
                                                     server_admin_name=sql_server_dict.get('administrator_login'))
                elastic_pools_list = self.list_elastic_pools(sql_servers_conn, resource_group_name, name)
                deleted_databases_list = self.list_deleted_databases(sql_servers_conn, resource_group_name, name)
                virtual_network_rules_list = self.list_virtual_network_rules(sql_servers_conn, resource_group_name,
                                                                             name)
                firewall_rules_list = self.list_firewall_rules(sql_servers_conn, resource_group_name, name)

                sql_server_dict.update({
                    'azure_ad_administrators': azure_ad_admin_list,
                    'server_auditing_settings': server_auditing_settings_dict,
                    'failover_groups': failover_group_list,
                    'server_automatic_tuning': server_automatic_tuning_dict,
                    'databases': databases_list,
                    'elastic_pools': elastic_pools_list,
                    'deleted_databases': deleted_databases_list,
                    'virtual_network_rules': virtual_network_rules_list,
                    'firewall_rules': firewall_rules_list,
                    'encryption_protectors': transparent_data_encryption_dict
                })

                if sql_server_dict.get('azure_ad_administrators') is not None:
                    sql_server_dict.update({
                        'azure_ad_admin_name': self.get_azure_ad_admin_name(sql_server_dict['azure_ad_administrators'])
                    })

                if sql_server_dict.get('private_endpoint_connections') is not None:
                    sql_server_dict.update({
                        'private_endpoint_connections': self.get_private_endpoint_connections(sql_server_dict[
                                                                                                  'private_endpoint_connections'])
                    })

                # switch tags form
                tags = sql_server_dict.get('tags', {})
                _tags = self.convert_tag_format(tags)
                sql_server_dict.update({
                    'tags': _tags
                })

                sql_server_data = SQLServer(sql_server_dict, strict=False)
                sql_server_resource = SQLServerResource({
                    'data': sql_server_data,
                    'region_code': sql_server_data.location,
                    'reference': ReferenceModel(sql_server_data.reference()),
                    'tags': _tags,
                    'name': sql_server_data.name,
                    'account': sql_server_data.subscription_id
                })
                sql_server_responses.append(SQLServerResponse({'resource': sql_server_resource}))
                # _LOGGER.debug(f'[SQL SERVER INFO] {sql_server_resource.to_primitive()}')

                # Must set_region_code method for region collection
                self.set_region_code(sql_server_data['location'])

            except Exception as e:
                _LOGGER.error(f'[list_instances] {sql_server_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Database', 'SQLServer',
                                                                                sql_server_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** SQL Servers Finished {time.time() - start_time} Seconds **')

        return sql_server_responses, error_responses

    def list_elastic_pools(self, sql_servers_conn, rg_name, server_name):
        elastic_pools_list = list()
        elastic_pools = sql_servers_conn.list_elastic_pools_by_server(resource_group=rg_name, server_name=server_name)

        for elastic_pool in elastic_pools:
            elastic_pool_dict = self.convert_nested_dictionary(elastic_pool)

            # Get Databases list by elastic pool
            elastic_pool_dict['databases'] = self.get_databases_by_elastic_pools(sql_servers_conn,
                                                                                 elastic_pool_dict['name'], rg_name,
                                                                                 server_name)

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

    def get_databases_by_elastic_pools(self, sql_servers_conn, elastic_pool_name, rg_name, server_name):
        databases_obj = sql_servers_conn.list_databases_by_elastic_pool(elastic_pool_name, rg_name, server_name)
        databases_list = list()
        for database in databases_obj:
            database_dict = self.convert_nested_dictionary(database)
            databases_list.append(database_dict)

        return databases_list

    def list_deleted_databases(self, sql_servers_conn, rg_name, server_name):
        deleted_databases_obj = sql_servers_conn.list_restorable_dropped_databases_by_server(resource_group=rg_name,
                                                                                             server_name=server_name)
        deleted_databases_list = list()
        for deleted_database in deleted_databases_obj:
            deleted_database_dict = self.convert_nested_dictionary(deleted_database)
            deleted_databases_list.append(deleted_database_dict)

        return deleted_databases_list

    def list_firewall_rules(self, sql_servers_conn, rg_name, server_name):
        firewall_obj = sql_servers_conn.list_firewall_rules_by_server(resource_group=rg_name, server_name=server_name)
        firewall_list = list()
        for firewall in firewall_obj:
            firewall_rule_dict = self.convert_nested_dictionary(firewall)
            firewall_list.append(firewall_rule_dict)

        return firewall_list

    def list_virtual_network_rules(self, sql_servers_conn, rg_name, server_name):
        virtual_network_rule_obj = sql_servers_conn.list_virtual_network_rules_by_server(resource_group=rg_name,
                                                                                         server_name=server_name)
        virtual_network_rules_list = list()

        for virtual_network_rule in virtual_network_rule_obj:
            virtual_network_rule_dict = self.convert_nested_dictionary(virtual_network_rule)

            if virtual_network_rule_dict.get('id') is not None:  # Get Virtual Network's name
                virtual_network_rule_dict.update({
                    'virtual_network_name_display': virtual_network_rule_dict['virtual_network_subnet_id'].split('/')[
                        8],
                    'subscription_id': virtual_network_rule_dict['id'].split('/')[2],
                    'resource_group': virtual_network_rule_dict['id'].split('/')[4]
                })
            virtual_network_rules_list.append(virtual_network_rule_dict)

        return virtual_network_rules_list

    def list_encryption_protectors(self, sql_servers_conn, rg_name, server_name):
        encryption_protectors_list = list()
        encryption_protectors_obj = sql_servers_conn.list_encryption_protectors(resource_group=rg_name,
                                                                                server_name=server_name)

        for encryption_protector in encryption_protectors_obj:
            encryption_protectors_dict = self.convert_nested_dictionary(encryption_protector)
            encryption_protectors_list.append(encryption_protectors_dict)

        return encryption_protectors_list

    def list_azure_ad_administrators(self, sql_servers_conn, rg_name, server_name):
        ad_admin_list = list()  # return list
        ad_admin_obj = sql_servers_conn.list_server_azure_ad_administrators(resource_group=rg_name,
                                                                            server_name=server_name)

        for ad_admin in ad_admin_obj:
            ad_admin_list.append(self.convert_dictionary(ad_admin))

        return ad_admin_list

    def get_server_automatic_tuning(self, sql_servers_conn, rg_name, server_name):
        server_automatic_tuning_obj = sql_servers_conn.get_server_automatic_tuning(rg_name, server_name)
        server_automatic_tuning_dict = self.convert_nested_dictionary(server_automatic_tuning_obj)
        server_automatic_tuning_dict.update({
            'options': self.get_server_automatic_tuning_options(server_automatic_tuning_dict['options'])
        })

        return server_automatic_tuning_dict

    def get_server_automatic_tuning_options(self, options_dict):
        options_list = list()
        created_index_dict = self.convert_nested_dictionary(options_dict['createIndex'])
        drop_index_dict = self.convert_nested_dictionary(options_dict['dropIndex'])
        force_plan_dict = self.convert_nested_dictionary(options_dict['forceLastGoodPlan'])

        created_index_dict.update({
            'tuning_type': 'createIndex'
        })
        drop_index_dict.update({
            'tuning_type': 'dropIndex'
        })
        force_plan_dict.update({
            'tuning_type': 'forceLastGoodPlan'
        })

        options_list.append(created_index_dict)
        options_list.append(drop_index_dict)
        options_list.append(force_plan_dict)

        return options_list

    def get_server_auditing_settings(self, sql_servers_conn, rg_name, server_name):
        server_auditing_settings_obj = sql_servers_conn.get_server_auditing_settings(rg_name, server_name)
        server_auditing_settings_dict = self.convert_nested_dictionary(server_auditing_settings_obj)

        return server_auditing_settings_dict

    def list_failover_groups(self, sql_servers_conn, rg_name, server_name):
        failover_groups_list = list()
        failover_groups_obj = sql_servers_conn.list_failover_groups(rg_name, server_name)
        for failover in failover_groups_obj:
            failover_dict = self.convert_nested_dictionary(failover)

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
                    'grace_period_display': failover_dict['read_write_endpoint'].get(
                        'failover_with_data_loss_grace_period_minutes')
                })

            failover_groups_list.append(failover_dict)

        return failover_groups_list

    def list_data_masking_rules(self, sql_servers_conn, rg_name, server_name, database_name):
        data_masking_rules_list = list()
        data_masking_rule_obj = sql_servers_conn.list_data_masking_rules_by_database(resource_group=rg_name,
                                                                                     server_name=server_name,
                                                                                     database_name=database_name)

        for data_masking_rule in data_masking_rule_obj:
            data_masking_dict = self.convert_nested_dictionary(data_masking_rule)
            data_masking_rules_list.append(data_masking_dict)

        return data_masking_rules_list

    def list_databases(self, sql_servers_conn, sql_monitor_conn, resource_group_name, server_name, server_admin_name):
        databases_list = list()  # todo : list() , []
        databases = sql_servers_conn.list_databases_by_server(resource_group_name=resource_group_name,
                                                              server_name=server_name)

        for database in databases:
            database_dict = self.convert_nested_dictionary(database)
            if database_dict.get('sku'):
                if database_dict.get('name') != 'master':  # No pricing tier for system database
                    database_dict.update({
                        'pricing_tier_display': self.get_pricing_tier_display(database_dict['sku']),
                        'service_tier_display': database_dict['sku'].get('tier')
                    })

            if db_id := database_dict.get('id'):
                database_dict.update({
                    'server_name': db_id.split('/')[8],
                    'subscription_id': db_id.split('/')[2],
                    'resource_group': db_id.split('/')[4],
                    'azure_monitor': {'resource_id': db_id}
                })

            if compute_tier := database_dict.get('kind'):
                database_dict.update({
                    'compute_tier': self.get_db_compute_tier(compute_tier)
                })

            if database_dict.get('max_size_bytes'):
                database_dict.update({
                    'max_size_gb': database_dict['max_size_bytes'] / 1073741824  # 2의 30승
                })

            # Get Sync Groups by databases
            database_dict.update({
                'sync_group': self.get_sync_group_by_databases(sql_servers_conn, resource_group_name, server_name,
                                                               database_dict['name']),
            })

            if database_dict['sync_group']:
                database_dict.update({
                    'sync_group_display': self.get_sync_group_display(database_dict['sync_group'])
                })

            # Get Sync Agents by servers
            database_dict.update({
                'sync_agent': self.get_sync_agent_by_servers(sql_servers_conn, resource_group_name, server_name)
            })

            if database_dict['sync_agent']:
                database_dict.update({
                    'sync_agent_display': self.get_sync_agent_display(database_dict['sync_agent'])
                })
            '''
            # Get Data masking rules
            database_dict.update({
                'data_masking_rules': self.list_data_masking_rules(self, sql_servers_conn, rg_name, server_name, database_dict['name'])
            })
            '''

            # Get Diagnostic Settings
            database_dict.update({
                'diagnostic_settings_resource': self.list_diagnostics_settings(sql_monitor_conn,
                                                                               database_dict['id'])
            })

            # Get Database Replication Type
            database_dict.update({
                'replication_link': self.list_replication_link(sql_servers_conn, resource_group_name, server_name,
                                                               database_dict['name'])
            })

            # Get azure_ad_admin name
            if server_admin_name is not None:
                database_dict.update({
                    'administrator_login': server_admin_name
                })

            # switch tags form
            tags = database_dict.get('tags', {})
            _tags = self.convert_tag_format(tags)
            database_dict.update({
                'tags': _tags
            })

            databases_list.append(database_dict)

        return databases_list

    def get_sync_agent_by_servers(self, sql_servers_conn, rg_name, server_name):
        sync_agent_list = list()
        sync_agent_obj = sql_servers_conn.list_sync_agents_by_server(rg_name, server_name)

        for sync_agent in sync_agent_obj:
            sync_agent_dict = self.convert_nested_dictionary(sync_agent)
            sync_agent_list.append(sync_agent_dict)

        return sync_agent_list

    def list_diagnostics_settings(self, sql_monitor_conn, resource_uri):
        diagnostic_settings_list = list()
        diagnostic_settings_objs = sql_monitor_conn.list_diagnostic_settings(resource_uri=resource_uri)

        for diagnostic_setting in diagnostic_settings_objs:
            diagnostic_setting_dict = self.convert_nested_dictionary(diagnostic_setting)
            diagnostic_settings_list.append(diagnostic_setting_dict)

        return diagnostic_settings_list

    def list_replication_link(self, sql_servers_conn, rg_name, server_name, database_name):
        replication_link_list = list()
        replication_link_obj = sql_servers_conn.list_replication_link(rg_name, server_name, database_name)

        for replication_link in replication_link_obj:
            replication_link_dict = self.convert_nested_dictionary(replication_link)
            replication_link_list.append(replication_link_dict)

        return replication_link_list

    def get_sync_group_by_databases(self, sql_servers_conn, resource_group_name, server_name, database_name):
        sync_group_obj = sql_servers_conn.list_sync_groups_by_databases(resource_group=resource_group_name,
                                                                        server_name=server_name,
                                                                        database_name=database_name)
        sync_group_list = list()
        for sync_group in sync_group_obj:
            sync_group_dict = self.convert_nested_dictionary(sync_group)
            sync_group_list.append(sync_group_dict)
        return sync_group_list

    @staticmethod
    def get_private_endpoint_connections(private_endpoint_connection_list):
        for pec in private_endpoint_connection_list:
            if pec.get('id') is not None:
                pec.update({
                    'connection_id': pec['id'].split('/')[10]
                })

            if pec.get('properties') is not None:
                pec.update({
                    'private_endpoint_name': pec['properties'].get('private_endpoint').get('id').split('/')[8],
                    'description': pec['properties'].get('private_link_service_connection_state').get('description'),
                    'status': pec['properties'].get('private_link_service_connection_state').get('status')
                })

        return private_endpoint_connection_list

    @staticmethod
    def get_per_db_settings(per_database_settings_dict):
        per_db_settings = f"{str(per_database_settings_dict['min_capacity'])} - " \
                          f"{str(per_database_settings_dict['max_capacity'])} vCores"
        return per_db_settings

    @staticmethod
    def get_failover_secondary_server(partner_servers):
        secondary_server = None

        for partner_server in partner_servers:
            if partner_server['replication_role'] == 'Secondary':
                secondary_server = partner_server['id'].split('/')[8]

        return secondary_server

    @staticmethod
    def get_azure_ad_admin_name(azure_ad_administrators_list):
        az_admin_name = ''

        for az_admin in azure_ad_administrators_list:
            if az_admin.get('login') is not None:
                az_admin_name = az_admin.get('login')

        return az_admin_name

    @staticmethod
    def get_db_compute_tier(kind):
        if 'serverless' in kind:
            compute_tier = 'Serverless'
        else:
            compute_tier = 'Provisioned'

        return compute_tier

    @staticmethod
    def get_sync_agent_display(sync_agent_list):
        sync_agent_display_list = list()
        for sync_agent in sync_agent_list:
            sync_display = f"{sync_agent['name']} / {sync_agent['state']}"
            sync_agent_display_list.append(sync_display)

        return sync_agent_display_list

    @staticmethod
    def get_pricing_tier_display(sku_dict):
        pricing_tier = None
        if sku_dict.get('capacity') is not None:
            pricing_tier = f'{str(sku_dict["tier"])} : {str(sku_dict["family"])} , {str(sku_dict["capacity"])} vCores'

        return pricing_tier

    @staticmethod
    def get_sync_group_display(sync_group_list):
        sync_group_display_list = list()
        for sync_group in sync_group_list:
            sync_display = f"{sync_group['name']} / {sync_group['conflict_resolution_policy']} / {sync_group['sync_state']}"
            sync_group_display_list.append(sync_display)

        return sync_group_display_list
