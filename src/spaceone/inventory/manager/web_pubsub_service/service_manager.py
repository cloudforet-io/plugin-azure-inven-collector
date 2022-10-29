import copy
import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.core.utils import *
from spaceone.inventory.model.web_pubsub_service.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.connector.web_pubsub_service.connector import WebPubSubServiceConnector
from spaceone.inventory.model.web_pubsub_service.cloud_service import *
from spaceone.inventory.model.web_pubsub_service.data import *

_LOGGER = logging.getLogger(__name__)


class WebPubSubServiceManager(AzureManager):
    connector_name = 'WebPubSubServiceConnector'
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
                CloudServiceResponse (list) : list of azure web pubsub service data resource information
                ErrorResourceResponse (list) : list of error resource information
        """

        _LOGGER.debug(f'** Web PubSub Service START **')
        start_time = time.time()
        subscription_info = params['subscription_info']
        web_pubsub_responses = []
        error_responses = []

        web_pubsub_service_conn: WebPubSubServiceConnector = self.locator.get_connector(self.connector_name, **params)
        web_pubsub_services = web_pubsub_service_conn.list_by_subscription()

        for web_pubsub_service in web_pubsub_services:
            web_pubsub_service_id = ''
            try:
                web_pubsub_service_dict = self.convert_nested_dictionary(web_pubsub_service)
                web_pubsub_service_id = web_pubsub_service_dict['id']
                resource_group_name = self.get_resource_group_from_id(web_pubsub_service_id)
                resource_name = web_pubsub_service_dict['name']

                # Update data info in Container Instance's Raw Data

                # Make private endpoint name
                if private_endpoints := web_pubsub_service_dict.get('private_endpoint_connections', []):
                    for private_endpoint in private_endpoints:
                        private_endpoint['private_endpoint'][
                            'private_endpoint_name_display'] = self.get_resource_name_from_id(
                            private_endpoint['private_endpoint']['id'])

                # Collect Web PubSub Hub resource
                web_pubsub_hubs = web_pubsub_service_conn.list_hubs(resource_group_name=resource_group_name,
                                                                    resource_name=resource_name)

                _hub_responses, _hub_errors = self._collect_web_pubsub_hub(web_pubsub_hubs, subscription_info, web_pubsub_service_dict['location'])
                web_pubsub_responses.extend(_hub_responses)
                error_responses.extend(_hub_errors)

                # Add Web PubSub Hub info in data
                web_pubsub_hub_datas = [WebPubSubHub(self.convert_nested_dictionary(hub), strict=False) for hub in
                                        web_pubsub_hubs]

                # Add Web PubSub Key info in data
                web_pubsub_key = web_pubsub_service_conn.list_keys(resource_group_name=resource_group_name,
                                                                   resource_name=resource_name)

                web_pubsub_service_dict.update({
                    'resource_group': resource_group_name,
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': web_pubsub_service_id},
                    'web_pubsub_hubs': web_pubsub_hub_datas,
                    'web_pubsub_hub_count_display': len(web_pubsub_hub_datas),
                    'web_pubsub_key': WebPubSubKey(self.convert_nested_dictionary(web_pubsub_key), strict=False)
                })

                web_pubsub_service_data = WebPubSubService(web_pubsub_service_dict, strict=False)

                # Update resource info of Container Instance
                web_pubsub_service_resource = WebPubSubServiceResource({
                    'name': resource_name,
                    'account': web_pubsub_service_dict['subscription_id'],
                    'data': web_pubsub_service_data,
                    'tags': web_pubsub_service_dict.get('tags', {}),
                    'region_code': web_pubsub_service_data.location,
                    'reference': ReferenceModel(web_pubsub_service_data.reference())
                })

                self.set_region_code(web_pubsub_service_data['location'])
                # web_pubsub_responses.append(WebPubSubServiceResponse({'resource': web_pubsub_service_resource}))
            except Exception as e:
                _LOGGER.error(f'[list_instances] {web_pubsub_service_id} {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'Service', 'WebPubSubService',
                                                                       web_pubsub_service_id)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Web PubSub Service Finished {time.time() - start_time} Seconds **')
        return web_pubsub_responses, error_responses

    def _collect_web_pubsub_hub(self, web_pubsub_hubs, subscription_info, location):
        web_pubsub_hub_responses = []
        error_responses = []
        for web_pubsub_hub in web_pubsub_hubs:
            web_pubsub_hub_id = ''
            try:
                web_pubsub_hub_id = web_pubsub_hub.id
                resource_group_name = self.get_resource_group_from_id(web_pubsub_hub_id)

                web_pubsub_hub_dict = self.convert_nested_dictionary(web_pubsub_hub)
                web_pubsub_hub_dict.update({
                    'location': location,
                    'resource_group': resource_group_name,
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': web_pubsub_hub_id},
                    'web_pubsub_svc_name': self.get_web_pubsub_name_from_id(web_pubsub_hub_id),
                    'web_pubsub_hub_evnet_handler_count_display': len(web_pubsub_hub_dict.get('properties', {}).get('event_handlers', []))
                })
                web_pubsub_hub_data = WebPubSubHub(web_pubsub_hub_dict, strict=False)
                web_pubsub_hub_resource = WebPubSubHubResource({
                    'name': web_pubsub_hub_data.name,
                    'account': web_pubsub_hub_dict['subscription_id'],
                    'data': web_pubsub_hub_data,
                    'tags': web_pubsub_hub_dict.get('tags', {}),
                    'region_code': web_pubsub_hub_data.location,
                    'reference': ReferenceModel(web_pubsub_hub_data.reference())
                })
                web_pubsub_hub_responses.append(WebPubSubHubResponse({'resource': web_pubsub_hub_resource}))
            except Exception as e:
                print(e)
                _LOGGER.error(f'[list_instances] {web_pubsub_hub_id} {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'Hub', 'WebPubSubService', web_pubsub_hub_id)
                error_responses.append(error_response)
        return web_pubsub_hub_responses, error_responses

    @staticmethod
    def get_resource_name_from_id(dict_id):
        resource_name = dict_id.split('/')[-1]
        return resource_name

    @staticmethod
    def get_web_pubsub_name_from_id(dict_id):
        svc_name = dict_id.split('/')[-3]
        return svc_name


