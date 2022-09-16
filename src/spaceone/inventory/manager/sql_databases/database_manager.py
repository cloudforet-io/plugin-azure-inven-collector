import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.sql_databases.cloud_service import *
from spaceone.inventory.model.sql_databases.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.sql_databases.data import *
from spaceone.inventory.connector.sql_databases import SQLDatabasesConnector
from spaceone.core.utils import *

_LOGGER = logging.getLogger(__name__)


class SQLDatabasesManager(AzureManager):
    connector_name = 'SQLDatabasesConnector'
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
        _LOGGER.debug(f'** SQL Databases START *')
        start_time = time.time()

        subscription_info = params['subscription_info']
        sql_databases_conn: SQLDatabasesConnector = self.locator.get_connector(self.connector_name, **params)

        sql_database_responses = []
        error_responses = []

        sql_servers = sql_databases_conn.list_servers()
        for sql_server in sql_servers:
            sql_database_id = ''
            try:
                sql_server_dict = self.convert_nested_dictionary(self, sql_server)

                # get resource_group_name and server_name from sql_server for sql_databases list
                server_name = sql_server_dict['name']
                resource_group_name = self.get_resource_group_from_id(sql_server_dict['id'])
                sql_databases = sql_databases_conn.list_databases(resource_group_name=resource_group_name, server_name=server_name)

                for sql_database in sql_databases:
                    sql_database_dict = self.convert_nested_dictionary(self, sql_database)

                    sql_database_id = sql_database_dict['id']
                    name = sql_database_dict['name']

                    sql_database_dict.update({
                        'resource_group': resource_group_name,
                        'subscription_id': subscription_info['subscription_id'],
                        'subscription_name': subscription_info['subscription_name'],
                        'azure_monitor': {'resource_id': sql_database_id}
                    })

                    # switch tags form
                    tags = sql_database_dict.get('tags', {})
                    _tags = self.convert_tag_format(tags)
                    sql_database_dict.update({
                        'tags': _tags
                    })

                    sql_database_data = SQLDatabase(sql_database_dict, strict=False)
                    sql_database_resource = SQLDatabaseResource({
                        'data': sql_database_data,
                        'region_code': sql_database_data.location,
                        'reference': ReferenceModel(sql_database_data.reference())
                    })
                    print('====================')
                    pprint.pprint(f'resource {sql_database_resource.to_primitive()}')
                    print('====================')
                sql_database_responses.append(SQLDatabaseResponse({'resource': sql_database_resource}))





            except Exception as e:
                _LOGGER.error(f'[list_instances] {sql_database_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Database', 'SQLDatabse', sql_database_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** SQL Databases Finished {time.time() - start_time} Seconds **')
        return sql_database_responses, error_responses


