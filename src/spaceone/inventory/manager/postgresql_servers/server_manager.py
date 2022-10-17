import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.postgresql_servers import PostgreSQLServersConnector
from spaceone.inventory.model.postgresql_servers.cloud_service import *
from spaceone.inventory.model.postgresql_servers.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.postgresql_servers.data import *

_LOGGER = logging.getLogger(__name__)


class PostgreSQLServersManager(AzureManager):
    connector_name = 'PostgreSQLServersConnector'
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
                    CloudServiceResponse (list) : dictionary of azure postgresql servers data resource information
                    ErrorResourceResponse (list) : list of error resource information


                """
        _LOGGER.debug(f'** Postgre SQL Servers START **')

        start_time = time.time()

        subscription_info = params['subscription_info']
        postgre_sql_conn: PostgreSQLServersConnector = self.locator.get_connector(self.connector_name, **params)
        postgre_sql_server_responses = []
        error_responses = []
        postgre_sql_servers = postgre_sql_conn.list_servers()

        for postgre_sql_server in postgre_sql_servers:
            postgre_sql_server_id = ''

            try:
                postgre_sql_server_dict = self.convert_nested_dictionary(postgre_sql_server)
                postgre_sql_server_id = postgre_sql_server_dict['id']

                # update application_gateway_dict
                postgre_sql_server_dict.update({
                    'resource_group': self.get_resource_group_from_id(postgre_sql_server_id),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': postgre_sql_server_id}
                })

                if postgre_sql_server_dict.get('name') is not None:
                    resource_group = postgre_sql_server_dict['resource_group']
                    server_name = postgre_sql_server_dict['name']
                    postgre_sql_server_dict.update({
                        'firewall_rules': self.list_firewall_rules_by_server(postgre_sql_conn, resource_group,
                                                                             server_name),
                        'virtual_network_rules': self.list_virtual_network_rules_by_server(postgre_sql_conn,
                                                                                           resource_group, server_name),
                        'replicas': self.list_replicas_by_server(postgre_sql_conn, resource_group, server_name),
                        'server_administrators': self.list_server_administrators(postgre_sql_conn, resource_group,
                                                                                 server_name)
                    })

                postgre_sql_server_data = PostgreSQLServer(postgre_sql_server_dict, strict=False)
                postgre_sql_server_resource = PostgreSQLServerResource({
                    'data': postgre_sql_server_data,
                    'region_code': postgre_sql_server_data.location,
                    'reference': ReferenceModel(postgre_sql_server_data.reference()),
                    'tags': postgre_sql_server_dict.get('tags', {}),
                    'name': postgre_sql_server_data.name,
                    'account': postgre_sql_server_data.subscription_id,
                    'instance_type': postgre_sql_server_data.sku.tier,
                    'instance_size': float(postgre_sql_server_data.storage_profile.storage_mb)
                })

                # Must set_region_code method for region collection
                self.set_region_code(postgre_sql_server_data['location'])
                # _LOGGER.debug(f'[POSTGRESQL SERVERS INFO] {postgre_sql_server_resource.to_primitive()}')
                postgre_sql_server_responses.append(PostgreSQLServerResponse({'resource': postgre_sql_server_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {postgre_sql_server_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Database', 'PostgreSQLServer',
                                                                                postgre_sql_server_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** PostgreSQLServer Finished {time.time() - start_time} Seconds **')
        return postgre_sql_server_responses, error_responses

    def get_sql_resources(self, cosmos_db_conn, account_name, resource_group):
        sql_resources = []
        sql_resources_obj = cosmos_db_conn.list_sql_resources(account_name=account_name,
                                                              resource_group_name=resource_group)

        for sql in sql_resources_obj:
            sql_dict = self.convert_nested_dictionary(sql)
            sql_resources.append(sql_dict)
        return sql_resources

    def list_firewall_rules_by_server(self, postgresql_conn, resource_group, name):
        firewall_rules = []
        firewall_rules_obj = postgresql_conn.list_firewall_rules_by_server(resource_group_name=resource_group,
                                                                           server_name=name)

        for firewall_rule in firewall_rules_obj:
            firewall_rule_dict = self.convert_nested_dictionary(firewall_rule)
            firewall_rules.append(firewall_rule_dict)

        return firewall_rules

    def list_virtual_network_rules_by_server(self, postgresql_conn, resource_group, name):
        virtual_network_rules = []
        virtual_network_rules_obj = postgresql_conn.list_virtual_network_rules_by_server(
            resource_group_name=resource_group, server_name=name)

        for virtual_network in virtual_network_rules_obj:
            virtual_network_dict = self.convert_nested_dictionary(virtual_network)
            if virtual_network_dict.get('virtual_network_subnet_id') is not None:
                virtual_network_dict.update({
                    'subnet_name': self.get_subnet_name(virtual_network_dict['virtual_network_subnet_id']),
                    'virtual_network_name_display': self.get_virtual_network_name(
                        virtual_network_dict['virtual_network_subnet_id'])
                })
            virtual_network_rules.append(virtual_network_dict)

        return virtual_network_rules

    def list_replicas_by_server(self, postgresql_conn, resource_group, name):
        replicas_list = []
        replicas_obj = postgresql_conn.list_replicas_by_server(resource_group_name=resource_group, server_name=name)
        for replica in replicas_obj:
            replica_dict = self.convert_nested_dictionary(replica)
            if replica_dict.get('master_server_id') is not None:
                replica_dict.update({
                    'master_server_name': self.get_replica_master_server_name(replica_dict['master_server_id'])
                })

            replicas_list.append(replica_dict)
        return replicas_list

    def list_server_administrators(self, postgresql_conn, resource_group, name):
        server_administrators = []
        server_admin_obj = postgresql_conn.list_server_administrators(resource_group_name=resource_group,
                                                                      server_name=name)
        for server_admin in server_admin_obj:
            server_admin_dict = self.convert_nested_dictionary(server_admin)
            server_administrators.append(server_admin_dict)

        return server_administrators

    @staticmethod
    def get_subnet_name(subnet_id):
        subnet_name = ''
        if subnet_id:
            subnet_name = subnet_id.split('/')[10]
        return subnet_name

    @staticmethod
    def get_virtual_network_name(subnet_id):
        virtual_network_name = ''
        if subnet_id:
            virtual_network_name = subnet_id.split('/')[8]
        return virtual_network_name

    @staticmethod
    def get_replica_master_server_name(master_server_id):
        master_server_name = master_server_id.split('/')[8]
        return master_server_name
