MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
FILTER_FORMAT = []

ASSET_URL = 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure'

CLOUD_SERVICE_GROUP_MAP = {
    'ApplicationGateways': 'ApplicationGatewaysManager',
    'ContainerInstances': 'ContainerInstancesManager',
    'CosmosDB': 'CosmosDBManager',
    'Disks': 'DisksManager',
    'KeyVaults': 'KeyVaultsManager',
    'LoadBalancers': 'LoadBalancersManager',
    'MySQLServers': 'MySQLServersManager',
    'SQLServers': 'SQLServersManager',
    'SQLDatabases': 'SQLDatabasesManager',
    'NATGateways': 'NATGatewaysManager',
    'NetworkSecurityGroups': 'NetworkSecurityGroupsManager',
    'PostgreSQLServers': 'PostgreSQLServersManager',
    'PublicIPAddresses': 'PublicIPAddressesManager',
    'Snapshots': 'SnapshotsManager',
    'StorageAccounts': 'StorageAccountsManager',
    'VirtualMachines': 'VirtualMachinesManager',
    'VirtualNetworks': 'VirtualNetworksManager',
    'VMScaleSets': 'VmScaleSetsManager',
    'WebPubSubService': 'WebPubSubServiceManager',
}
