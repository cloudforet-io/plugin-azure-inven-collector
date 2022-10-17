import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.mysql_servers import MySQLServersConnector
from spaceone.inventory.model.mysql_servers.cloud_service import *
from spaceone.inventory.model.mysql_servers.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.mysql_servers.data import *

_LOGGER = logging.getLogger(__name__)


class MySQLServersManager(AzureManager):
    connector_name = 'MySQLServersConnector'
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
                CloudServiceResponse (dict) : dictionary of mysql servers data resource information
                ErrorResourceResponse (list) : list of error resource information
        """

        _LOGGER.debug(f'** MySQL Servers START **')
        start_time = time.time()

        subscription_info = params['subscription_info']

        mysql_servers_conn: MySQLServersConnector = self.locator.get_connector(self.connector_name, **params)
        mysql_server_responses = []
        error_responses = []

        mysql_servers_obj_list = mysql_servers_conn.list_servers()

        for mysql_server in mysql_servers_obj_list:
            mysql_server_id = ''

            try:
                mysql_server_dict = self.convert_nested_dictionary(mysql_server)
                mysql_server_id = mysql_server_dict['id']

                mysql_server_dict.update({
                    'resource_group': self.get_resource_group_from_id(mysql_server_id),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': mysql_server_id}
                })

                if mysql_server_dict.get('name') is not None:
                    resource_group = mysql_server_dict.get('resource_group', '')
                    server_name = mysql_server_dict['name']
                    mysql_server_dict.update({
                        'firewall_rules': self.get_firewall_rules_by_server(mysql_servers_conn, resource_group, server_name),
                    })

                if mysql_server_dict.get('firewall_rules') is not None:
                    mysql_server_dict.update({
                        'allow_azure_services_access': self.get_azure_service_access(mysql_server_dict['firewall_rules'])
                    })

                if mysql_server_dict.get('storage_profile') is not None:
                    mysql_server_dict['storage_profile'].update({
                        'storage_gb': self.get_storage_gb(mysql_server_dict['storage_profile'].get('storage_mb', ''))
                    })

                mysql_server_data = MySQLServer(mysql_server_dict, strict=False)
                mysql_server_resource = MySQLServerResource({
                    'data': mysql_server_data,
                    'tags': mysql_server_dict.get('tags', {}),
                    'region_code': mysql_server_data.location,
                    'reference': ReferenceModel(mysql_server_data.reference()),
                    'name': mysql_server_data.name,
                    'account': mysql_server_data.subscription_id,
                    'instance_type': mysql_server_data.sku.tier
                })

                # Must set_region_code method for region collection
                self.set_region_code(mysql_server_data['location'])
                # _LOGGER.debug(f'[MYSQL SERVER INFO] {mysql_server_resource.to_primitive()}')
                mysql_server_responses.append(MySQLServerResponse({'resource': mysql_server_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {mysql_server_id} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Database', 'MySQLServer', mysql_server_id)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** MySQL Server Finished {time.time() - start_time} Seconds **')
        return mysql_server_responses, error_responses

    def get_firewall_rules_by_server(self, mysql_servers_conn, resource_group, server_name):
        firewall_rules = []
        firewall_rules_obj = mysql_servers_conn.list_firewall_rules_by_server(resource_group_name=resource_group, server_name=server_name)
        for firewall_rule in firewall_rules_obj:
            firewall_dict = self.convert_nested_dictionary(firewall_rule)
            firewall_rules.append(firewall_dict)

        return firewall_rules

    @staticmethod
    def get_azure_service_access(firewall_rules):
        firewall_rule_name_list = []

        for firewall_rule in firewall_rules:
            if firewall_rule.get('name') is not None:
                firewall_rule_name_list.append(firewall_rule['name'])

        if 'AllowAllWindowsAzureIps' in firewall_rule_name_list:
            return True

        return False

    @staticmethod
    def get_storage_gb(storage_mb):
        if storage_mb:
            storage_gb = int(storage_mb / 1024)
            return storage_gb
