from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.postgresql_server import PostgreSQLServerConnector
from spaceone.inventory.model.postgresqlserver.cloud_service import *
from spaceone.inventory.model.postgresqlserver.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.postgresqlserver.data import *
from spaceone.inventory.error.custom import *
import time
import ipaddress
import logging

_LOGGER = logging.getLogger(__name__)


class PostgreSQLServerManager(AzureManager):
    connector_name = 'PostgreSQLServerConnector'
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
                    CloudServiceResponse (dict) : dictionary of azure cosmosdb data resource information

                """
        _LOGGER.debug(f'** Postgre SQL Servers START **')

        start_time = time.time()

        subscription_info = params['subscription_info']
        postgre_sql_conn: PostgreSQLServerConnector = self.locator.get_connector(self.connector_name, **params)
        postgre_sql_servers = []
        postgre_sql_servers_list = postgre_sql_conn.list_servers()

        for postgre_sql_server in postgre_sql_servers_list:
            postgre_sql_server_dict = self.convert_nested_dictionary(self, postgre_sql_server)

            # update application_gateway_dict
            postgre_sql_server_dict.update({
                'resource_group': self.get_resource_group_from_id(postgre_sql_server_dict['id']),
                # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            if postgre_sql_server_dict.get('name') is not None:
                resource_group = postgre_sql_server_dict['resource_group']
                server_name = postgre_sql_server_dict['name']
                postgre_sql_server_dict.update({
                    'firewall_rules': self.list_firewall_rules_by_server(self, postgre_sql_conn, resource_group, server_name),
                    'virtual_network_rules': self.list_virtual_network_rules_by_server(self, postgre_sql_conn, resource_group, server_name),
                    'replicas': self.list_replicas_by_server(self, postgre_sql_conn, resource_group, server_name),
                    'server_administrators': self.list_server_administrators(self, postgre_sql_conn, resource_group, server_name)
                })

            print(f'[POSTGRESQL SERVERS INFO] {postgre_sql_server_dict}')
            _LOGGER.debug(f'[POSTGRESQL SERVERS INFO] {postgre_sql_server_dict}')
            postgre_sql_server_data = Server(postgre_sql_server_dict, strict=False)
            postgre_sql_server_resource = SqlServerResource({
                'data': postgre_sql_server_data,
                'region_code': postgre_sql_server_data.location,
                'reference': ReferenceModel(postgre_sql_server_data.reference()),
                'name': postgre_sql_server_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(postgre_sql_server_data['location'])
            postgre_sql_servers.append(SqlServerResponse({'resource': postgre_sql_server_resource}))

        _LOGGER.debug(f'** PostgreSQL Finished {time.time() - start_time} Seconds **')

        return postgre_sql_servers

    @staticmethod
    def get_sql_resources(self, cosmos_db_conn, account_name, resource_group):
        try:
            sql_resources = []
            sql_resources_obj = cosmos_db_conn.list_sql_resources(account_name=account_name, resource_group_name=resource_group)

            for sql in sql_resources_obj:
                sql_dict = self.convert_nested_dictionary(self, sql)
                sql_resources.append(sql_dict)
            return sql_resources

        except ConnectionError as e:
            _LOGGER.error(ERROR_CONNECTOR(Connector='Cosmos DB'))

    @staticmethod
    def list_firewall_rules_by_server(self, postgresql_conn, resource_group, name):
        firewall_rules = []
        firewall_rules_obj = postgresql_conn.list_firewall_rules_by_server(resource_group_name=resource_group, server_name=name)

        for firewall_rule in firewall_rules_obj:
            firewall_rule_dict = self.convert_nested_dictionary(self, firewall_rule)
            firewall_rules.append(firewall_rule_dict)

        return firewall_rules

    @staticmethod
    def list_virtual_network_rules_by_server(self, postgresql_conn, resource_group, name):
        virtual_network_rules = []
        virtual_network_rules_obj = postgresql_conn.list_virtual_network_rules_by_server(resource_group_name=resource_group, server_name=name)

        for virtual_network in virtual_network_rules_obj:
            virtual_network_dict = self.convert_nested_dictionary(self, virtual_network)
            if virtual_network_dict.get('virtual_network_subnet_id') is not None:
                virtual_network_dict.update({
                    'subnet_name': self.get_subnet_name(virtual_network_dict['virtual_network_subnet_id']),
                    'virtual_network_name_display': self.get_virtual_network_name(virtual_network_dict['virtual_network_subnet_id'])
                })
            virtual_network_rules.append(virtual_network_dict)

        return virtual_network_rules

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
    def list_replicas_by_server(self, postgresql_conn, resource_group, name):
        replicas_list = []
        replicas_obj = postgresql_conn.list_replicas_by_server(resource_group_name=resource_group, server_name=name)
        for replica in replicas_obj:
            replica_dict = self.convert_nested_dictionary(self, replica)
            if replica_dict.get('master_server_id') is not None:
                replica_dict.update({
                    'master_server_name': self.get_replica_master_server_name(replica_dict['master_server_id'])
                })

            replicas_list.append(replica_dict)
        return replicas_list

    @staticmethod
    def list_server_administrators(self, postgresql_conn, resource_group, name):
        server_administrators = []
        server_admin_obj = postgresql_conn.list_server_administrators(resource_group_name=resource_group, server_name=name)
        for server_admin in server_admin_obj:
            server_admin_dict = self.convert_nested_dictionary(self, server_admin)
            server_administrators.append(server_admin_dict)

        return server_administrators

    @staticmethod
    def get_replica_master_server_name(master_server_id):
        try:
            master_server_name = master_server_id.split('/')[8]
            return master_server_name
        except Exception as e:
            _LOGGER.error(f'[ERROR: Azure PostgreSQL Server Manager Get Master Server Name]: {e}')

