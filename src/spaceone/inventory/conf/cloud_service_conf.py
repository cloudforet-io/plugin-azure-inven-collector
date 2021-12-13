MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
FILTER_FORMAT = []

CLOUD_SERVICE_GROUP_MAP = {
    'ApplicationGateway': 'ApplicationGatewayManager',
    'AzureCosmosDB': 'CosmosDBManager',
    'Disk': 'DiskManager',
    'KeyVault': 'KeyVaultManager',
    'LoadBalancer': 'LoadBalancerManager',
    'MySQLServer': 'MySQLServerManager',
    'SQLServer': 'SqlServerManager',
    'NATGateway': 'NATGatewayManager',
    'NetworkSecurityGroup': 'NetworkSecurityGroupManager',
    'PostgreSQLServer': 'PostgreSQLServerManager',
    'PublicIPAddress': 'PublicIPAddressManager',
    'Snapshot': 'SnapshotManager',
    'StorageAccount': 'StorageAccountManager',
    'VirtualNetwork': 'VirtualNetworkManager',
    'VMScaleSet': 'VmScaleSetManager'
}
