from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import AzureConnector
from spaceone.inventory.libs.schema.region import RegionResource, RegionResponse
from collections.abc import Iterable
import json

REGION_INFO = {
    'eastus': {'name': 'US East (Virginia)', 'tags': {'latitude': '37.3719', 'longitude': '-79.8164'}},
    'eastus2': {'name': 'US East 2 (Virginia)', 'tags': {'latitude': '36.6681', 'longitude': '-78.3889'}},
    'westus': {'name': 'US West (California)', 'tags': {'latitude': '37.783', 'longitude': '-122.417'}},
    'westus2': {'name': 'US West 2 (Washington)', 'tags': {'latitude': '47.233', 'longitude': '-119.852'}},
    'centralus': {'name': 'US Central (Iowa)', 'tags': {'latitude': '41.5908', 'longitude': '-93.6208'}},
    'southcentralus': {'name': 'US South Central (Texas)',
                       'tags': {'latitude': '29.4167', 'longitude': '-98.5'}},
    'northcentralus': {'name': 'US North Central (Illinois)',
                       'tags': {'latitude': '41.8819', 'longitude': '-87.6278'}},
    'westcentralus': {'name': 'US West Central (Wyoming)',
                      'tags': {'latitude': '40.890', 'longitude': '-110.234'}},
    'canadacentral': {'name': 'Canada Central (Toronto)',
                      'tags': {'latitude': '43.653', 'longitude': '-79.383'}},
    'canadaeast': {'name': 'Canada East (Quebec)',
                   'tags': {'latitude': '46.817', 'longitude': '-71.217'}},
    'southafricanorth': {'name': 'South Africa North (Johannesburg)',
                         'tags': {'latitude': '-25.731340', 'longitude': '28.218370'}},
    'southafricawest': {'name': 'South Africa West (Cape Town)',
                        'tags': {'latitude': '-34.075691', 'longitude': '18.843266'}},
    'eastasia': {'name': 'Asia Pacific East (Hong Kong)',
                 'tags': {'latitude': '22.267', 'longitude': '114.188'}},
    'centralindia': {'name': 'Asia Pacific Central India (Pune)',
                     'tags': {'latitude': '18.5822', 'longitude': '73.9197'}},
    'southindia': {'name': 'Asia Pacific South India (Chennai)',
                   'tags': {'latitude': '12.9822', 'longitude': '80.1636'}},
    'westindia': {'name': 'Asia Pacific West India (Mumbai)',
                  'tags': {'latitude': '19.088', 'longitude': '72.868'}},
    'southeastasia': {'name': 'Asia Pacific South East (Singapore)',
                      'tags': {'latitude': '1.283', 'longitude': '103.833'}},
    'japaneast': {'name': 'Asia Pacific Japan East (Tokyo, Saitama)',
                  'tags': {'latitude': '35.68', 'longitude': '139.77'}},
    'japanwest': {'name': 'Asia Pacific Japan West (Osaka)',
                  'tags': {'latitude': '34.6939', 'longitude': '135.5022'}},
    'koreacentral': {'name': 'Asia Pacific Korea Central (Seoul)',
                     'tags': {'latitude': '37.5665', 'longitude': '126.9780'}},
    'koreasouth': {'name': 'Asia Pacific Korea South (Busan)',
                   'tags': {'latitude': '35.1796', 'longitude': '129.0756'}},
    'australiaeast': {'name': 'Asia Pacific Australia East (New South Wales)',
                      'tags': {'latitude': '-33.86', 'longitude': '151.2094'}},
    'australiacentral': {'name': 'Asia Pacific Australia Central (Canberra)',
                         'tags': {'latitude': '-35.3075', 'longitude': '149.1244'}},
    'australiacentral2': {'name': 'Asia Pacific Australia Central 2 (Canberra)',
                          'tags': {'latitude': '-35.3075', 'longitude': '149.1244'}},
    'australiasoutheast': {'name': 'Asia Pacific Australia South East (Victoria)',
                           'tags': {'latitude': '-37.8136', 'longitude': '144.9631'}},
    'northeurope': {'name': 'North Europe (Ireland)', 'tags': {'latitude': '53.3478', 'longitude': '-6.2597'}},
    'norwayeast': {'name': 'North Europe (Norway East)',
                   'tags': {'latitude': '59.913868', 'longitude': '10.752245'}},
    'norwaywest': {'name': 'North Europe (Norway West)',
                   'tags': {'latitude': '58.969975', 'longitude': '5.733107'}},
    'germanywestcentral': {'name': 'Europe Germany West Central (Frankfurt)',
                           'tags': {'latitude': '50.110924', 'longitude': '8.682127'}},
    'germanynorth': {'name': 'Europe Germany North (Berlin)',
                     'tags': {'latitude': '53.073635', 'longitude': '8.806422'}},
    'switzerlandnorth': {'name': 'Europe Switzerland North (Zurich)',
                         'tags': {'latitude': '47.451542', 'longitude': '8.564572'}},
    'switzerlandwest': {'name': 'Europe Switzerland West (Geneva)',
                        'tags': {'latitude': '46.204391', 'longitude': '6.143158'}},
    'francecentral': {'name': 'Europe France Central (Paris)',
                      'tags': {'latitude': '46.3772', 'longitude': '2.3730'}},
    'francesouth': {'name': 'Europe France South (Marseille)',
                    'tags': {'latitude': '43.8345', 'longitude': '2.1972'}},
    'westeurope': {'name': 'West Europe (Netherlands)', 'tags': {'latitude': '52.3667', 'longitude': '4.9'}},
    'uksouth': {'name': 'UK South (London)', 'tags': {'latitude': '50.941', 'longitude': '-0.799'}},
    'ukwest': {'name': 'UK West (Cardiff)', 'tags': {'latitude': '53.427', 'longitude': '-3.084'}},
    'uaenorth': {'name': 'Middle East UAE North (Dubai)',
                 'tags': {'latitude': '25.266666', 'longitude': '55.316666'}},
    'uaecentral': {'name': 'Middle East UAE Central (Abu Dhabi)',
                   'tags': {'latitude': '24.466667', 'longitude': '54.366669'}},
    'brazilsouth': {'name': 'South America Brazil South (Sao Paulo State)',
                    'tags': {'latitude': '-23.55', 'longitude': '-46.633'}},
    'brazilsoutheast': {'name': 'South America Brazil South East (Rio)',
                        'tags': {'latitude': '-22.90278', 'longitude': '-43.2075'}},
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
        connector.verify()

    def collect_cloud_service_type(self):
        for cloud_service_type in self.cloud_service_types:
            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        resources = []

        resources.extend(self.collect_cloud_service_type())
        resources.extend(self.collect_cloud_service(params))
        resources.extend(self.collect_region())

        return resources

    def collect_region(self):
        results = []
        for region_code in self.collected_region_codes:
            if region := self.match_region_info(region_code):
                results.append(RegionResponse({'resource': region}))

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

    @staticmethod
    def convert_nested_dictionary(self, vm_object):
        vm_dict = self.convert_dictionary(vm_object)
        for k, v in vm_dict.items():
            if isinstance(v, object):  # object
                if 'azure' in str(type(v)):  # 1) if vm_object is azure defined model class
                    vm_dict[k] = self.convert_nested_dictionary(self, v)
                elif isinstance(v, list):  # 2) if vm_object is list
                    vm_converse_list = list()
                    for list_obj in v:  # if vm object's child value is Azure defined model class or dict class
                        if hasattr(list_obj, '__dict__') or 'azure' in str(type(list_obj)):
                            vm_converse_dict = self.convert_nested_dictionary(self, list_obj)
                            vm_converse_list.append(vm_converse_dict)
                        else:  # if vm object's child value is simple list
                            vm_converse_list.append(list_obj)

                        vm_dict[k] = vm_converse_list

                elif hasattr(v, '__dict__'):  # if vm_object is not a list type, just a dict
                    vm_converse_dict = self.convert_nested_dictionary(self, v)
                    vm_dict[k] = vm_converse_dict

        return vm_dict
