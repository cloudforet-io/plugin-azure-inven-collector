from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.sqldatabase import *
from spaceone.inventory.model.sqldatabase.cloud_service import *
from spaceone.inventory.connector.sql import SqlConnector
from spaceone.inventory.connector.subscription import SubscriptionConnector
from spaceone.inventory.model.sqldatabase.cloud_service_type import CLOUD_SERVICE_TYPES
from datetime import datetime
import time


class SqlDatabaseManager(AzureManager):
    connector_name = 'SqlConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Sql Databases START **")
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
        subscription_info = params['subscription_info']

        sql_databases_conn: SqlConnector = self.locator.get_connector(self.connector_name, **params)
        sql_databases = []
        for sql_database in sql_databases_conn.list_databases():
            sql_databases_dict = self.convert_dictionary(sql_database)
            sku_dict = self.convert_dictionary(sql_database.sku)

            # update disk_data dict
            sql_databases_dict.update({
                'resource_group': self.get_resource_group_from_id(sql_databases_dict['id']),  # parse resource_group from ID
                'subscription_id': subscription_info['subscription_id'],
                'subscription_name': subscription_info['subscription_name'],
            })

            # switch tags form
            tags = sql_databases_dict.get('tags', {})
            _tags = self.convert_tag_format(tags)
            sql_databases_dict.update({
                'tags': _tags
            })

            sql_databases_data = SqlDatabase(sql_databases_dict, strict=False)

            sql_databases_resource = SqlDatabaseResource({
                'data': sql_databases_data,
                'region_code': sql_databases_data.location,
                'reference': ReferenceModel(sql_databases_data.reference()),
                'tags':  _tags
            })

            # Must set_region_code method for region collection
            self.set_region_code(sql_databases_data['location'])

            sql_databases.append(SqlDatabaseResponse({'resource': sql_databases_resource}))

        print(f'** Sql Databases Finished {time.time() - start_time} Seconds **')
        return sql_databases

    @staticmethod
    def get_resource_group_from_id(disk_id):
        resource_group = disk_id.split('/')[4].lower()
        return resource_group

