from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from pprint import pprint
from spaceone.inventory.connector.mysql_server import MySQLServerConnector
from spaceone.inventory.model.mysqlserver.cloud_service import *
from spaceone.inventory.model.mysqlserver.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.mysqlserver.data import *
from spaceone.inventory.error.custom import *
import time
import logging

_LOGGER = logging.getLogger(__name__)


class MySQLServerManager(AzureManager):
    connector_name = 'MySQLServerConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** MySQL Servers START **")
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
        subscription_info = params['subscription_info']

        mysql_servers_conn: MySQLServerConnector = self.locator.get_connector(self.connector_name, **params)
        mysql_servers = []
        mysql_servers_obj_list = mysql_servers_conn.list_servers()

        for mysql_server in mysql_servers_obj_list:
            mysql_server_dict = self.convert_nested_dictionary(self, mysql_server)
            mysql_server_dict.update({
                'resource_group': self.get_resource_group_from_id(mysql_server_dict['id']),  # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            _LOGGER.debug(f'[MYSQL SERVER INFO] {mysql_server_dict}')
            mysql_server_data = MySQLServer(mysql_server_dict, strict=False)
            mysql_server_resource = MySQLServerResource({
                'data': mysql_server_data,
                'region_code': mysql_server_data.location,
                'reference': ReferenceModel(mysql_server_data.reference()),
                'name': mysql_server_data.name
            })

            # Must set_region_code method for region collection
            self.set_region_code(mysql_server_data['location'])
            mysql_servers.append(MySQLServerResponse({'resource': mysql_server_resource}))

        _LOGGER.debug(f'** MySQL Server Finished {time.time() - start_time} Seconds **')
        return mysql_servers

    @staticmethod
    def get_resource_group_from_id(dict_id):
        try:
            resource_group = dict_id.split('/')[4]
            return resource_group
        except IndexError:
            raise ERROR_PARSE_ID_FROM_RESOURCE_GROUP



