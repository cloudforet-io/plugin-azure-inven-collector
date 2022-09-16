MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
FILTER_FORMAT = []


CLOUD_SERVICE_GROUP_MAP = {
    'ApplicationGateways': 'ApplicationGatewaysManager',
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
    'VirtualNetworks': 'VirtualNetworksManager',
    'VMScaleSets': 'VmScaleSetsManager',
    'VirtualMachines': 'VirtualMachinesManager',
}
