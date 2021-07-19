import time
import logging
import concurrent.futures
from spaceone.inventory.libs.manager import AzureManager
from spaceone.inventory.manager.subscription_manager import SubscriptionManager
from spaceone.core.service import *


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
SUPPORTED_SCHEDULES = ['hours']
FILTER_FORMAT = []


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = [
            # set MS Azure cloud service manager
            'DiskManager',
            'SnapshotManager',
            'VmScaleSetManager',
            'LoadBalancerManager',
            'SqlServerManager',
            'VirtualNetworkManager',
            'ApplicationGatewayManager',
            'PublicIPAddressManager',
            'NetworkSecurityGroupManager',
            'NATGatewayManager'
        ]

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES,
            'supported_schedules': SUPPORTED_SCHEDULES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        print(f'[PARAMS in COLLECTOR SERVICE] {params}')
        options = params['options']
        secret_data = params.get('secret_data', {})
        if secret_data != {}:
            azure_manager = AzureManager()
            active = azure_manager.verify({}, secret_data)

        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        start_time = time.time()

        params.update({
            'subscription_info': self.get_subscription_info(params)
        })

        print("[ EXECUTOR START: Azure Cloud Service ]")
        '''
        # TODO: Thread per cloud services
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            # print("[ EXECUTOR START ]")
            future_executors = []

            for execute_manager in self.execute_managers:
                print(f'@@@ {execute_manager} @@@')
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, params))

            try:
                for future in concurrent.futures.as_completed(future_executors):
                    for result in future.result():
                        yield result.to_primitive()

            except Exception as e:
                _LOGGER.error(f'failed to result {e}')
        '''

        for manager in self.execute_managers:
            print(f'@@@ {manager} @@@')
            _manager = self.locator.get_manager(manager)

            for resource in _manager.collect_resources(params):
                yield resource.to_primitive()

        print(f'TOTAL TIME : {time.time() - start_time} Seconds')

    def get_subscription_info(self, params):
        subscription_manager: SubscriptionManager = self.locator.get_manager('SubscriptionManager')
        return subscription_manager.get_subscription_info(params)
