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

                backend_address_pools = application_gateway_dict.get('backend_address_pools', [])
                url_path_maps = application_gateway_dict.get('url_path_maps', [])
                request_routing_rules = application_gateway_dict.get('request_routing_rules', [])
                rewrite_rule_sets = application_gateway_dict.get('rewrite_rule_sets', [])
                frontend_ip_configurations = application_gateway_dict.get('frontend_ip_configurations', [])
                ip_configurations = application_gateway_dict.get('gateway_ip_configurations', [])

                for frontend_ip_configuration_dict in frontend_ip_configurations:
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
                            'ip_address': f'{public_ip_address_dict.get("ip_address", "-")} ({public_ip_address_dict.get("name","")})',
                            'associated_listener': self.get_associated_listener(frontend_ip_configuration_dict, application_gateway_dict.get('http_listeners', []))
                        })

                for ip_configuration in ip_configurations:
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

                for rewrite_rule in rewrite_rule_sets:
                    rewrite_rule_id = rewrite_rule.get('id')
                    rewrite_config_rule_displays = self.list_rewrite_config_rule_display(rewrite_rule)
                    rewrite_rule.update({
                        'rewrite_rules_display': rewrite_config_rule_displays
                    })

                    rules_applied_list = self.list_rewrite_rule_rules_applied(rewrite_rule_id, request_routing_rules, url_path_maps)
                    rewrite_rule.update({
                        'rules_applied': rules_applied_list
                    })

                # Update request routing rules
                for request_routing_rule in request_routing_rules:
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

                for backend_address_pool in backend_address_pools:
                    backend_address_pool_associated_rules = self.get_backend_pool_associated_rules(backend_address_pool, url_path_maps, request_routing_rules)
                    backend_address_pool.update({
                        'associated_rules': backend_address_pool_associated_rules
                    })

                    backend_addresses = backend_address_pool.get('backend_addresses', [])
                    backend_addresses_display = [backend_address.get('fqdn') for backend_address in backend_addresses]
                    backend_address_pool.update({
                        'backend_addresses_display': backend_addresses_display
                    })

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
        associated_listener = []
        for http_listener in http_listeners_list:
            if http_listener.get('frontend_ip_configuration') is not None:
                if frontend_ip_configuration_dict['id'] in http_listener.get('frontend_ip_configuration', {}).get('id', ''):
                    associated_listener.append(http_listener.get('name'))
        return associated_listener

    @staticmethod
    def get_port(port_id, frontend_ports_list):
        port = 0
        for fe_port in frontend_ports_list:
            if port_id == fe_port.get('id'):
                port = fe_port.get('port')
                break
        return port

    @staticmethod
    def get_backend_pool_associated_rules(backend_address_pool, url_path_maps, request_routing_rules):
        backend_address_pool_associated_rules = []
        backend_address_pool_id = backend_address_pool.get('id')

        for url_path_map in url_path_maps:
            default_backend_address_pool = url_path_map.get('default_backend_address_pool')
            if default_backend_address_pool is not None and default_backend_address_pool.get(
                    'id') == backend_address_pool_id:
                backend_address_pool_associated_rules.append(url_path_map.get('name'))

        for request_routing_rule in request_routing_rules:
            request_backend_address_pool = request_routing_rule.get('backend_address_pool')
            if request_backend_address_pool is not None and request_backend_address_pool.get(
                    'id') == backend_address_pool_id:
                backend_address_pool_associated_rules.append(request_routing_rule.get('name'))
        return backend_address_pool_associated_rules

    @staticmethod
    def update_http_listeners_list(http_listeners_list, http_listener_id, http_applied_rules):
        for http_listener in http_listeners_list:
            if http_listener['id'] == http_listener_id:
                http_listener.update({
                    'associated_rules': http_applied_rules
                })

    @staticmethod
    def list_rewrite_config_rule_display(rewrite_rule):
        rewrite_config_rule_displays = []
        rewrite_rule_list = rewrite_rule.get('rewrite_rules', [])
        for rule in rewrite_rule_list:
            rewrite_config_rule_displays.append(str(rule.get('name')) + ", " + str(rule.get('rule_sequence')))
        return rewrite_config_rule_displays

    @staticmethod
    def list_rewrite_rule_rules_applied(rewrite_rule_id, request_routing_rules, url_path_maps):
        rules_applied_list = []
        for request_routing_rule in request_routing_rules:
            if request_routing_rule.get('rewrite_rule_set') is not None:
                if request_routing_rule['rewrite_rule_set'].get('id') == rewrite_rule_id:
                    rules_applied_list.append(request_routing_rule['name'])

        for url_path_map in url_path_maps:
            if url_path_map.get('default_rewrite_rule_set') is not None:
                if url_path_map['default_rewrite_rule_set'].get('id') == rewrite_rule_id:
                    rules_applied_list.append(url_path_map['name'])

            if url_path_map.get('path_rules') is not None:
                for path_rule in url_path_map['path_rules']:
                    if path_rule.get('rewrite_rule_set') is not None:
                        if path_rule['rewrite_rule_set'].get('id') == rewrite_rule_id:
                            rules_applied_list.append(url_path_map['name'])
        return rules_applied_list
