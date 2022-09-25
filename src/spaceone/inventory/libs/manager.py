from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.libs.schema.region import RegionResource, RegionResponse
from spaceone.inventory.libs.schema.resource import RegionResourceResponse
from spaceone.inventory.libs.schema.resource import ErrorResourceResponse
from spaceone.inventory.error.custom import *
from collections.abc import Iterable
import json
import logging


_LOGGER = logging.getLogger(__name__)

REGION_INFO = {
    'eastus': {'name': 'US East (Virginia)', 'tags': {'latitude': '37.3719', 'longitude': '-79.8164', 'continent': 'north_america'}},
    'eastus2': {'name': 'US East 2 (Virginia)', 'tags': {'latitude': '36.6681', 'longitude': '-78.3889', 'continent': 'north_america'}},
    'westus': {'name': 'US West (California)', 'tags': {'latitude': '37.783', 'longitude': '-122.417', 'continent': 'north_america'}},
    'westus2': {'name': 'US West 2 (Washington)', 'tags': {'latitude': '47.233', 'longitude': '-119.852', 'continent': 'north_america'}},
    'centralus': {'name': 'US Central (Iowa)', 'tags': {'latitude': '41.5908', 'longitude': '-93.6208', 'continent': 'north_america'}},
    'southcentralus': {'name': 'US South Central (Texas)',
                       'tags': {'latitude': '29.4167', 'longitude': '-98.5', 'continent': 'north_america'}},
    'northcentralus': {'name': 'US North Central (Illinois)',
                       'tags': {'latitude': '41.8819', 'longitude': '-87.6278', 'continent': 'north_america'}},
    'westcentralus': {'name': 'US West Central (Wyoming)',
                      'tags': {'latitude': '40.890', 'longitude': '-110.234', 'continent': 'north_america'}},
    'canadacentral': {'name': 'Canada Central (Toronto)',
                      'tags': {'latitude': '43.653', 'longitude': '-79.383', 'continent': 'north_america'}},
    'canadaeast': {'name': 'Canada East (Quebec)',
                   'tags': {'latitude': '46.817', 'longitude': '-71.217', 'continent': 'north_america'}},
    'southafricanorth': {'name': 'South Africa North (Johannesburg)',
                         'tags': {'latitude': '-25.731340', 'longitude': '28.218370', 'continent': 'africa'}},
    'southafricawest': {'name': 'South Africa West (Cape Town)',
                        'tags': {'latitude': '-34.075691', 'longitude': '18.843266', 'continent': 'africa'}},
    'eastasia': {'name': 'Asia Pacific East (Hong Kong)',
                 'tags': {'latitude': '22.267', 'longitude': '114.188', 'continent': 'asia_pacific'}},
    'centralindia': {'name': 'Asia Pacific Central India (Pune)',
                     'tags': {'latitude': '18.5822', 'longitude': '73.9197', 'continent': 'asia_pacific'}},
    'southindia': {'name': 'Asia Pacific South India (Chennai)',
                   'tags': {'latitude': '12.9822', 'longitude': '80.1636', 'continent': 'asia_pacific'}},
    'westindia': {'name': 'Asia Pacific West India (Mumbai)',
                  'tags': {'latitude': '19.088', 'longitude': '72.868', 'continent': 'asia_pacific'}},
    'southeastasia': {'name': 'Asia Pacific South East (Singapore)',
                      'tags': {'latitude': '1.283', 'longitude': '103.833', 'continent': 'asia_pacific'}},
    'japaneast': {'name': 'Asia Pacific Japan East (Tokyo, Saitama)',
                  'tags': {'latitude': '35.68', 'longitude': '139.77', 'continent': 'asia_pacific'}},
    'japanwest': {'name': 'Asia Pacific Japan West (Osaka)',
                  'tags': {'latitude': '34.6939', 'longitude': '135.5022', 'continent': 'asia_pacific'}},
    'koreacentral': {'name': 'Asia Pacific Korea Central (Seoul)',
                     'tags': {'latitude': '37.5665', 'longitude': '126.9780', 'continent': 'asia_pacific'}},
    'koreasouth': {'name': 'Asia Pacific Korea South (Busan)',
                   'tags': {'latitude': '35.1796', 'longitude': '129.0756', 'continent': 'asia_pacific'}},
    'australiaeast': {'name': 'Asia Pacific Australia East (New South Wales)',
                      'tags': {'latitude': '-33.86', 'longitude': '151.2094', 'continent': 'asia_pacific'}},
    'australiacentral': {'name': 'Asia Pacific Australia Central (Canberra)',
                         'tags': {'latitude': '-35.3075', 'longitude': '149.1244', 'continent': 'asia_pacific'}},
    'australiacentral2': {'name': 'Asia Pacific Australia Central 2 (Canberra)',
                          'tags': {'latitude': '-35.3075', 'longitude': '149.1244', 'continent': 'asia_pacific'}},
    'australiasoutheast': {'name': 'Asia Pacific Australia South East (Victoria)',
                           'tags': {'latitude': '-37.8136', 'longitude': '144.9631', 'continent': 'asia_pacific'}},
    'northeurope': {'name': 'North Europe (Ireland)', 'tags': {'latitude': '53.3478', 'longitude': '-6.2597', 'continent': 'europe'}},
    'norwayeast': {'name': 'North Europe (Norway East)',
                   'tags': {'latitude': '59.913868', 'longitude': '10.752245', 'continent': 'europe'}},
    'norwaywest': {'name': 'North Europe (Norway West)',
                   'tags': {'latitude': '58.969975', 'longitude': '5.733107', 'continent': 'europe'}},
    'germanywestcentral': {'name': 'Europe Germany West Central (Frankfurt)',
                           'tags': {'latitude': '50.110924', 'longitude': '8.682127', 'continent': 'europe'}},
    'germanynorth': {'name': 'Europe Germany North (Berlin)',
                     'tags': {'latitude': '53.073635', 'longitude': '8.806422', 'continent': 'europe'}},
    'switzerlandnorth': {'name': 'Europe Switzerland North (Zurich)',
                         'tags': {'latitude': '47.451542', 'longitude': '8.564572', 'continent': 'europe'}},
    'switzerlandwest': {'name': 'Europe Switzerland West (Geneva)',
                        'tags': {'latitude': '46.204391', 'longitude': '6.143158', 'continent': 'europe'}},
    'swedencentral': {'name': 'Sweden Central', 'tags': {'latitude': '60.67488', 'longitude': '17.14127', 'continent': 'europe'}},
    'francecentral': {'name': 'Europe France Central (Paris)',
                      'tags': {'latitude': '46.3772', 'longitude': '2.3730', 'continent': 'europe'}},
    'francesouth': {'name': 'Europe France South (Marseille)',
                    'tags': {'latitude': '43.8345', 'longitude': '2.1972', 'continent': 'europe'}},
    'westeurope': {'name': 'West Europe (Netherlands)', 'tags': {'latitude': '52.3667', 'longitude': '4.9', 'continent': 'europe'}},
    'uksouth': {'name': 'UK South (London)', 'tags': {'latitude': '50.941', 'longitude': '-0.799', 'continent': 'europe'}},
    'ukwest': {'name': 'UK West (Cardiff)', 'tags': {'latitude': '53.427', 'longitude': '-3.084', 'continent': 'europe'}},
    'uaenorth': {'name': 'Middle East UAE North (Dubai)',
                 'tags': {'latitude': '25.266666', 'longitude': '55.316666', 'continent': 'middle_east'}},
    'uaecentral': {'name': 'Middle East UAE Central (Abu Dhabi)',
                   'tags': {'latitude': '24.466667', 'longitude': '54.366669', 'continent': 'middle_east'}},
    'brazilsouth': {'name': 'South America Brazil South (Sao Paulo State)',
                    'tags': {'latitude': '-23.55', 'longitude': '-46.633', 'continent': 'south_america'}},
    'brazilsoutheast': {'name': 'South America Brazil South East (Rio)',
                        'tags': {'latitude': '-22.90278', 'longitude': '-43.2075', 'continent': 'south_america'}}
}


class AzureManager(BaseManager):
    connector_name = None
    cloud_service_types = []
    response_schema = None
    collected_region_codes = []

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: AzureConnector = self.locator.get_connector('AzureConnector', secret_data=secret_data)
        params = {'secret_data': secret_data}
        connector.verify(**params)

    def collect_cloud_service_type(self, params):
        options = params.get('options', {})

        for cloud_service_type in self.cloud_service_types:
            if 'service_code_mappers' in options:
                svc_code_maps = options['service_code_mappers']
                if getattr(cloud_service_type.resource, 'service_code') and \
                        cloud_service_type.resource.service_code in svc_code_maps:
                    cloud_service_type.resource.service_code = svc_code_maps[cloud_service_type.resource.service_code]

            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        total_resources = []

        try:
            total_resources.extend(self.collect_cloud_service_type(params))
            resources, error_resources = self.collect_cloud_service(params)

            total_resources.extend(resources)
            total_resources.extend(error_resources)

            regions = self.collect_region()
            total_resources.extend(regions)

        except Exception as e:
            error_resource_response = self.generate_error_response(e, self.cloud_service_types[0].resource.group, self.cloud_service_types[0].resource.name)
            total_resources.append(error_resource_response)
            _LOGGER.error(f'[collect] {e}', exc_info=True)

        return total_resources

    def collect_region(self):
        results = []
        try:
            for region_code in self.collected_region_codes:
                if region := self.match_region_info(region_code):
                    results.append(RegionResourceResponse({'resource': region}))

        except Exception as e:
            _LOGGER.error(f'[collect] {e}', exc_info=True)

            if type(e) is dict:
                error_resource_response = ErrorResourceResponse({
                    'message': json.dumps(e),
                    'resource': {'resource_type': 'inventory.Region'}
                })
            else:
                error_resource_response = ErrorResourceResponse({
                    'message': str(e),
                    'resource': {'resource_type': 'inventory.Region'}
                })
            results.append(error_resource_response)

        return results

    def set_region_code(self, region):
        if region not in REGION_INFO:
            region = 'global'

        if region not in self.collected_region_codes:
            self.collected_region_codes.append(region)

    @staticmethod
    def convert_tag_format(tags):
        convert_tags = []

        if tags:
            for k, v in tags.items():
                convert_tags.append({
                    'key': k,
                    'value': v
                })

        return convert_tags

    @staticmethod
    def match_region_info(region_code):
        match_region_info = REGION_INFO.get(region_code)

        if match_region_info:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': region_code
            })
            return RegionResource(region_info, strict=False)

        return None

    @staticmethod
    def convert_dictionary(obj):
        return vars(obj)

    # def convert_nested_dictionary(self, cloud_svc_object):
    #     cloud_svc_dict = self.convert_dictionary(cloud_svc_object)
    #     for k, v in cloud_svc_dict.items():
    #         if isinstance(v, object):  # object
    #             if 'azure' in str(type(v)):  # 1) if cloud_svc_object is azure defined model class
    #                 cloud_svc_dict[k] = self.convert_nested_dictionary(v)
    #             elif isinstance(v, list):  # 2) if cloud_svc_object is list
    #                 cloud_svc_converse_list = list()
    #                 for list_obj in v:  # if cloud_svc object's child value is Azure defined model class or dict class
    #                     if hasattr(list_obj, '__dict__') or 'azure' in str(type(list_obj)):
    #                         cloud_svc_converse_dict = self.convert_nested_dictionary(list_obj)
    #                         cloud_svc_converse_list.append(cloud_svc_converse_dict)
    #                     else:  # if cloud_svc_object's child value is simple list
    #                         cloud_svc_converse_list.append(list_obj)
    #
    #                     cloud_svc_dict[k] = cloud_svc_converse_list
    #
    #             elif hasattr(v, '__dict__'):  # if cloud_svc_object is not a list type, just a dict
    #                 cloud_svc_converse_dict = self.convert_nested_dictionary(v)
    #                 cloud_svc_dict[k] = cloud_svc_converse_dict
    #
    #     return cloud_svc_dict

    def convert_nested_dictionary(self, cloud_svc_object):
        cloud_svc_dict = {}
        if hasattr(cloud_svc_object, '__dict__'):  # if cloud_svc_object is not a dictionary type but has dict method
            cloud_svc_dict = cloud_svc_object.__dict__
        elif not isinstance(cloud_svc_object, list):  # if cloud_svc_object is one of type like int, float, char, ...
            return cloud_svc_object

        # if cloud_svc_object is dictionary type
        for key, value in cloud_svc_dict.items():
            if 'azure' in str(type(value)):
                cloud_svc_dict[key] = self.convert_nested_dictionary(value)
            elif isinstance(value, list):
                value_list = []
                for v in value:
                    value_list.append(self.convert_nested_dictionary(v))
                cloud_svc_dict[key] = value_list

        return cloud_svc_dict

    @staticmethod
    def get_resource_group_from_id(dict_id):
        resource_group = dict_id.split('/')[4]
        return resource_group

    @staticmethod
    def generate_error_response(e, cloud_service_group, cloud_service_type):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({'message': json.dumps(e),
                                                             'resource': {'cloud_service_group': cloud_service_group,
                                                                          'cloud_service_type': cloud_service_type}})
        else:
            error_resource_response = ErrorResourceResponse({'message': str(e),
                                                             'resource': {'cloud_service_group': cloud_service_group,
                                                                          'cloud_service_type': cloud_service_type}})
        return error_resource_response

    @staticmethod
    def generate_resource_error_response(e, cloud_service_group, cloud_service_type, resource_id):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({'message': json.dumps(e),
                                                             'resource': {'cloud_service_group': cloud_service_group,
                                                                          'cloud_service_type': cloud_service_type,
                                                                          'resource_id': resource_id}})
        else:
            error_resource_response = ErrorResourceResponse({'message': str(e),
                                                             'resource': {'cloud_service_group': cloud_service_group,
                                                                          'cloud_service_type': cloud_service_type,
                                                                          'resource_id': resource_id}})
        return error_resource_response
