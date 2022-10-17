import time
import logging
from spaceone.core.utils import *
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.cosmos_db import CosmosDBConnector
from spaceone.inventory.model.cosmos_db.cloud_service import *
from spaceone.inventory.model.cosmos_db.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.cosmos_db.data import *

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
                    CloudServiceResponse (list) : dictionary of azure cosmosdb data resource information
                    ErrorResourceResponse (list) : list of error resource information


                """
        _LOGGER.debug(f'** CosmosDB START **')

        start_time = time.time()
        subscription_info = params['subscription_info']
        cosmos_db_conn: CosmosDBConnector = self.locator.get_connector(self.connector_name, **params)

        cosmos_db_account_responses = []
        error_responses = []

        cosmos_db_accounts_list = cosmos_db_conn.list_all_cosmos_db_accounts()

        for cosmos_db_account in cosmos_db_accounts_list:
            cosmos_db_account_id = ''

            try:
                cosmos_db_account_dict = self.convert_nested_dictionary(cosmos_db_account)
                cosmos_db_account_id = cosmos_db_account_dict.get('id')

                # update cosmosdb_dict
                cosmos_db_account_dict.update({
                    'resource_group': self.get_resource_group_from_id(cosmos_db_account_dict['id']),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': cosmos_db_account_id}
                })

                if cosmos_db_account_dict.get('capabilities') is not None:
                    cosmos_db_account_dict.update({
                        'capability_display': self.get_capability_type(cosmos_db_account_dict['capabilities'])
                    })

                if cosmos_db_account_dict.get('virtual_network_rules') is not None:
                    cosmos_db_account_dict.update({
                        'virtual_network_display': self.get_virtual_networks(
                            cosmos_db_account_dict['virtual_network_rules'])
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
                        'keys': self.get_keys(cosmos_db_conn, cosmos_db_account_dict['name'],
                                              cosmos_db_account_dict['resource_group']),
                        'sql_databases': self.get_sql_resources(cosmos_db_conn, cosmos_db_account_dict['name'],
                                                                cosmos_db_account_dict['resource_group'])
                    })

                # _LOGGER.debug(f'[COSMOS DB INFO]{cosmos_db_account_dict}')
                cosmos_db_account_data = DatabaseAccountGetResults(cosmos_db_account_dict, strict=False)
                cosmos_db_resource = CosmosDBResource({
                    'data': cosmos_db_account_data,
                    'tags': cosmos_db_account_dict.get('tags', {}),
                    'region_code': cosmos_db_account_data.location,
                    'reference': ReferenceModel(cosmos_db_account_data.reference()),
                    'name': cosmos_db_account_data.name,
                    'account': cosmos_db_account_data.subscription_id,
                    'instance_type': cosmos_db_account_data.database_account_offer_type,
                    'launched_at': datetime_to_iso8601(cosmos_db_account_data.system_data.created_at)
                })

                # Must set_region_code method for region collection
                self.set_region_code(cosmos_db_account_data['location'])
                cosmos_db_account_responses.append(CosmosDBResponse({'resource': cosmos_db_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {cosmos_db_account_id} {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'Database', 'AzureCosmosDB',
                                                                       cosmos_db_account_id)
                error_responses.append(error_response)

        _LOGGER.debug(f'** CosmosDB Finished {time.time() - start_time} Seconds **')

        return cosmos_db_account_responses, error_responses

    def get_keys(self, cosmos_db_conn, account_name, resource_group):
        keys_obj = cosmos_db_conn.list_keys(account_name=account_name, resource_group_name=resource_group)
        key_dict = self.convert_nested_dictionary(keys_obj)
        return key_dict

    def get_sql_resources(self, cosmos_db_conn, account_name, resource_group):
        sql_resources = []
        sql_resources_obj = cosmos_db_conn.list_sql_resources(account_name=account_name,
                                                              resource_group_name=resource_group)

        for sql in sql_resources_obj:
            sql_dict = self.convert_nested_dictionary(sql)
            sql_resources.append(sql_dict)
        return sql_resources

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

        for virtual_network in virtual_network_rules:
            virtual_network_name = virtual_network['id'].split('/')[8]
            virtual_network_rules_display.append(virtual_network_name)

            return virtual_network_rules_display

    @staticmethod
    def get_private_endpoint_name(private_endpoint):
        if private_endpoint.get('id') is not None:
            private_endpoint.update({
                'name': private_endpoint['id'].split('/')[8]
            })
            return private_endpoint

    @staticmethod
    def get_private_connection_name(private_connection_id):
        private_connection_name = private_connection_id.split('/')[10]
        return private_connection_name

    @staticmethod
    def get_cors_display(cors_list):
        cors_display = []

        for cors in cors_list:
            cors_display.append(cors.get('allowed_origins', ''))
        return cors_display
