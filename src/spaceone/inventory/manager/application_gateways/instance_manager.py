import time
import logging
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.application_gateways import ApplicationGatewaysConnector
from spaceone.inventory.model.application_gateways.cloud_service import *
from spaceone.inventory.model.application_gateways.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.application_gateways.data import *

_LOGGER = logging.getLogger(__name__)


class ApplicationGatewaysManager(AzureManager):
    connector_name = 'ApplicationGatewaysConnector'
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
                    CloudServiceResponse (list) : list of azure application gateway data resource information
                    ErrorResourceResponse (list) : list of error resource information
                """

        _LOGGER.debug(f'** Application Gateway START **')

        start_time = time.time()
        subscription_info = params['subscription_info']

        application_gateway_conn: ApplicationGatewaysConnector = self.locator.get_connector(self.connector_name, **params)
        application_gateways_responses = []
        error_responses = []

        application_gateways_list = application_gateway_conn.list_all_application_gateways()
        for application_gateway in application_gateways_list:
            application_gateway_id = ''

            try:
                application_gateway_dict = self.convert_nested_dictionary(application_gateway)
                application_gateway_id = application_gateway_dict['id']

                # update application_gateway_dict
                application_gateway_dict.update({
                    'resource_group': self.get_resource_group_from_id(application_gateway_id),
                    'subscription_id': subscription_info['subscription_id'],
                    'subscription_name': subscription_info['subscription_name'],
                    'azure_monitor': {'resource_id': application_gateway_id}
                })

                if application_gateway_dict.get('frontend_ip_configurations') is not None:
                    for frontend_ip_configuration_dict in application_gateway_dict['frontend_ip_configurations']:
                        if frontend_ip_configuration_dict.get('private_ip_address') is not None:
                            application_gateway_dict.update({
                                'private_ip_address': frontend_ip_configuration_dict['private_ip_address']
                            })
                            frontend_ip_configuration_dict.update({
                                'ip_type': 'Private',
                                'ip_address': frontend_ip_configuration_dict['private_ip_address']
                            })
                        elif frontend_ip_configuration_dict.get('public_ip_address') is not None:
                            public_ip_address_name = frontend_ip_configuration_dict['public_ip_address']['id'].split('/')[8]
                            public_ip_address_dict = self.get_public_ip_address(application_gateway_conn, application_gateway_dict['resource_group'], public_ip_address_name)
                            application_gateway_dict.update({
                                'public_ip_address': public_ip_address_dict
                            })
                            frontend_ip_configuration_dict.update({
                                'ip_type': 'Public',
                                'ip_address': public_ip_address_dict.get('ip_address', '-'),
                                'associated_listener': self.get_associated_listener(frontend_ip_configuration_dict, application_gateway_dict.get('http_listeners', []))
                            })

                if application_gateway_dict.get('gateway_ip_configurations') is not None:
                    for ip_configuration in application_gateway_dict['gateway_ip_configurations']:
                        application_gateway_dict.update({
                            'virtual_network': ip_configuration.get('subnet')['id'].split('/')[8],
                            'subnet': ip_configuration.get('subnet')['id'].split('/')[10]
                        })

                if application_gateway_dict.get('backend_http_settings_collection') is not None:
                    for backend_setting in application_gateway_dict['backend_http_settings_collection']:
                        if backend_setting.get('probe') is not None:
                            custom_probe = backend_setting['probe']['id'].split('/')[10]
                            backend_setting.update({
                                'custom_probe': custom_probe
                            })

                if application_gateway_dict.get('http_listeners') is not None:
                    custom_error_configurations_list = []

                    for http_listener in application_gateway_dict['http_listeners']:

                        # Update Port information
                        if http_listener.get('frontend_port') is not None:
                            frontend_port_id = http_listener['frontend_port']['id']
                            http_listener['frontend_port'].update({
                                'port': self.get_port(frontend_port_id, application_gateway_dict.get('frontend_ports', []))
                            })
                            http_listener.update({
                                'port': http_listener.get('frontend_port', {}).get('port', '')
                            })

                        # Update custom error configuration
                        if http_listener.get('custom_error_configurations') is not None:
                            for custom_error_conf in http_listener['custom_error_configurations']:
                                custom_error_conf.update({'listener_name': http_listener['name']})
                                custom_error_configurations_list.append(custom_error_conf)

                            application_gateway_dict.update({
                                'custom_error_configurations': custom_error_configurations_list
                            })
                if application_gateway_dict.get('rewrite_rule_sets'):
                    for rewrite_rule in application_gateway_dict['rewrite_rule_sets']:
                        rewrite_rule_list = rewrite_rule.get('rewrite_rules', [])
                        rewrite_rule_str_list = []
                        for rule in rewrite_rule_list:
                            rewrite_rule_str_list.append(str(rule.get('name')) + ", " + str(rule.get('rule_sequence')))

                        rewrite_rule.update({
                            'rewrite_rules_display': rewrite_rule_str_list
                        })

                # Update request routing rules
                if application_gateway_dict.get('request_routing_rules') is not None:
                    for request_routing_rule in application_gateway_dict['request_routing_rules']:
                        if request_routing_rule.get('http_listener') is not None:
                            request_routing_rule.update({
                                'http_listener_name': request_routing_rule['http_listener']['id'].split('/')[10]
                            })
                            # Find http listener attached to this rule, and put rule's name to http_listeners dict
                            http_applied_rules_list = []
                            http_listener_id = request_routing_rule['http_listener']['id']

                            for request_routing_rule in application_gateway_dict.get('request_routing_rules', []):
                                if http_listener_id in request_routing_rule.get('http_listener').get('id', ''):
                                    http_applied_rules_list.append(request_routing_rule['name'])

                                self.update_http_listeners_list(application_gateway_dict['http_listeners'], http_listener_id, http_applied_rules_list)

                        # Find rewrite rule set attached to this rule, and put rule's name to rewrite rule dict
                        if request_routing_rule.get('rewrite_rule_set') is not None:
                            rewrite_rule_id = request_routing_rule['rewrite_rule_set']['id']
                            applied_rules_list = []

                            for request_routing_rule in application_gateway_dict.get('request_routing_rules', []):
                                if rewrite_rule_id in request_routing_rule.get('rewrite_rule_set', {}).get('id', ''):
                                    applied_rules_list.append(request_routing_rule['name'])

                                self.update_rewrite_ruleset_dict(application_gateway_dict['rewrite_rule_sets'], rewrite_rule_id, applied_rules_list)

                        # Find backend address pool attached to this rule, and put rule's name to backend address pool dict
                        if request_routing_rule.get('backend_address_pool') is not None:
                            backend_address_pool_id = request_routing_rule['backend_address_pool']['id']

                            rule_name_list = []
                            for request_routing_rule in application_gateway_dict['request_routing_rules']:
                                if backend_address_pool_id in request_routing_rule['backend_address_pool']['id']:
                                    rule_name_list.append(request_routing_rule['name'])

                            self.update_backend_pool_dict(application_gateway_dict['backend_address_pools'], backend_address_pool_id, rule_name_list)

                application_gateway_data = ApplicationGateway(application_gateway_dict, strict=False)
                application_gateway_resource = ApplicationGatewayResource({
                    'data': application_gateway_data,
                    'tags': application_gateway_dict.get('tags', {}),
                    'region_code': application_gateway_data.location,
                    'reference': ReferenceModel(application_gateway_data.reference()),
                    'name': application_gateway_data.name,
                    'instance_type': application_gateway_data.sku.name,
                    'account': application_gateway_data.subscription_id
                })
                # _LOGGER.debug(f'[APPLICATION GATEWAYS INFO] {application_gateway_resource.to_primitive()}')

                # Must set_region_code method for region collection
                self.set_region_code(application_gateway_data['location'])
                application_gateways_responses.append(ApplicationGatewayResponse({'resource': application_gateway_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_instances] {application_gateway_id} {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'Network', 'ApplicationGateway', application_gateway_id)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Application Gateway Finished {time.time() - start_time} Seconds **')
        return application_gateways_responses, error_responses

    def get_public_ip_address(self, application_gateway_conn, resource_group_name, pip_name):
        public_ip_address_obj = application_gateway_conn.get_public_ip_addresses(resource_group_name, pip_name)
        public_ip_address_dict = self.convert_nested_dictionary(public_ip_address_obj)

        # _LOGGER.debug(f'[Public IP Address]{public_ip_address_dict}')

        return public_ip_address_dict

    @staticmethod
    def get_associated_listener(frontend_ip_configuration_dict, http_listeners_list):
        associated_listener = ''
        for http_listener in http_listeners_list:
            if http_listener.get('frontend_ip_configuration') is not None:
                if frontend_ip_configuration_dict['id'] in http_listener.get('frontend_ip_configuration', {}).get('id', ''):
                    associated_listener = http_listener.get('name', '-')
                else:
                    associated_listener = '-'

        return associated_listener

    @staticmethod
    def get_port(port_id, frontend_ports_list):
        port = 0
        for fe_port in frontend_ports_list:
            if port_id in fe_port['id']:
                port = fe_port.get('port', 0)
                return port
            else:
                return port

    @staticmethod
    def update_backend_pool_dict(backend_pool_list, backend_pool_id, request_rules):
        for backend_pool in backend_pool_list:
            if backend_pool['id'] == backend_pool_id:
                backend_pool.update({
                    'associated_rules': request_rules
                })

    @staticmethod
    def update_rewrite_ruleset_dict(rewrite_rule_sets_list, rewrite_rule_id, applied_rules_list):
        for rewrite_rule in rewrite_rule_sets_list:
            if rewrite_rule['id'] == rewrite_rule_id:
                rewrite_rule.update({
                    'rules_applied': applied_rules_list
                })

    @staticmethod
    def update_http_listeners_list(http_listeners_list, http_listener_id, http_applied_rules):
        for http_listener in http_listeners_list:
            if http_listener['id'] == http_listener_id:
                http_listener.update({
                    'associated_rules': http_applied_rules
                })
