from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.cosmos_db import CosmosDBConnector
from spaceone.inventory.model.cosmosdb.cloud_service import *
from spaceone.inventory.model.cosmosdb.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.cosmosdb.data import *
from spaceone.inventory.error.custom import *
import time
import ipaddress
import logging

_LOGGER = logging.getLogger(__name__)


class CosmosDBManager(AzureManager):
    connector_name = 'CosmosDBConnector'
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
        _LOGGER.debug(f'** CosmosDB START **')

        start_time = time.time()

        secret_data = params['secret_data']
        subscription_info = params['subscription_info']
        cosmos_db_conn: CosmosDBConnector = self.locator.get_connector(self.connector_name, **params)
        cosmos_db_accounts = []
        cosmos_db_accounts_list = cosmos_db_conn.list_all_cosmos_db_accounts()

        for cosmos_db_account in cosmos_db_accounts_list:
            cosmos_db_account_dict = self.convert_nested_dictionary(self, cosmos_db_account)

            # update application_gateway_dict
            cosmos_db_account_dict.update({
                'resource_group': self.get_resource_group_from_id(cosmos_db_account_dict['id']),
                # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            if cosmos_db_account_dict.get('capabilities') is not None:
                cosmos_db_account_dict.update({
                    'capability_display': self.get_capability_type(cosmos_db_account_dict['capabilities'])
                })

            if cosmos_db_account_dict.get('virtual_network_rules') is not None:
                cosmos_db_account_dict.update({
                    'virtual_network_display': self.get_virtual_networks(cosmos_db_account_dict['virtual_network_rules'])
                })

            if cosmos_db_account_dict.get('private_endpoint_connections') is not None:
                for private_connection in cosmos_db_account_dict['private_endpoint_connections']:
                    private_connection.update({
                        'private_endpoint': self.get_private_endpoint_name(private_connection['private_endpoint']),
                        'name': self.get_private_connection_name(private_connection['id'])
                    })
            if cosmos_db_account_dict.get('cors') is not None:
                cosmos_db_account_dict.update({
                    'cors_display': self.get_cors_display(cosmos_db_account_dict['cors'])
                })

            if cosmos_db_account_dict.get('name') is not None:
                cosmos_db_account_dict.update({
                    'keys': self.get_keys(self, cosmos_db_conn, cosmos_db_account_dict['name'], cosmos_db_account_dict['resource_group']),
                    'sql_databases': self.get_sql_resources(self, cosmos_db_conn, cosmos_db_account_dict['name'], cosmos_db_account_dict['resource_group'])
                })

            _LOGGER.debug(f'[COSMOS DB INFO] {cosmos_db_account_dict}')
            cosmos_db_account_data = DatabaseAccountGetResults(cosmos_db_account_dict, strict=False)
            cosmos_db_resource = CosmosDBResource({
                'data': cosmos_db_account_data,
                'region_code': cosmos_db_account_data.location,
                'reference': ReferenceModel(cosmos_db_account_data.reference()),
                'name': cosmos_db_account_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(cosmos_db_account_data['location'])
            cosmos_db_accounts.append(CosmosDBResponse({'resource': cosmos_db_resource}))

        _LOGGER.debug(f'** CosmosDB Finished {time.time() - start_time} Seconds **')

        return cosmos_db_accounts

    @staticmethod
    def get_capability_type(capabilities):
        if capabilities:
            capability_str_list = []
            for capability in capabilities:
                capability_str_list.append(capability.get('name'))

            if 'EnableServerless' in capability_str_list:
                return 'Serverless'
            else:
                return 'Provisioned Throughput'

    @staticmethod
    def get_virtual_networks(virtual_network_rules):
        virtual_network_rules_display = []
        try:
            for virtual_network in virtual_network_rules:
                virtual_network_name = virtual_network['id'].split('/')[8]
                virtual_network_rules_display.append(virtual_network_name)

                return virtual_network_rules_display

        except ValueError as e:
            _LOGGER.error(ERROR_GET_RESOURCE_NAME_FROM_ID(field='CosmosDB Virtual Networks'))

    @staticmethod
    def get_private_endpoint_name(private_endpoint):
        if private_endpoint.get('id') is not None:
            try:
                private_endpoint.update({
                    'name': private_endpoint['id'].split('/')[8]
                })
                return private_endpoint
            except IndexError as e:
                _LOGGER.error(ERROR_GET_RESOURCE_NAME_FROM_ID(field='CosmosDB Private Endpoint'))

    @staticmethod
    def get_private_connection_name(private_connection_id):
        try:
            private_connection_name = private_connection_id.split('/')[10]
            return private_connection_name
        except IndexError as e:
            _LOGGER.error(ERROR_GET_RESOURCE_NAME_FROM_ID(field='CosmosDB Private Connection Name'))

    @staticmethod
    def get_cors_display(cors_list):
        cors_display = []
        try:
            for cors in cors_list:
                cors_display.append(cors.get('allowed_origins', ''))
            return cors_display

        except ValueError as e:
            _LOGGER.error(ERROR_GET_ADDITIONAL_RESOURCE_INFO())

    @staticmethod
    def get_keys(self, cosmos_db_conn, account_name, resource_group):
        try:
            keys_obj = cosmos_db_conn.list_keys(account_name=account_name, resource_group_name=resource_group)
            key_dict = self.convert_nested_dictionary(self, keys_obj)
            return key_dict

        except ConnectionError as e:
            _LOGGER.error(ERROR_CONNECTOR(Connector='Cosmos DB'))

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
