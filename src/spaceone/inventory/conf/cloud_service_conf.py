MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
FILTER_FORMAT = []


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
