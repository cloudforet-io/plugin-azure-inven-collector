# plugin-azure-cloud-services

![Microsoft Azure Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-cloud-services.svg)
**Plugin to collect Microsoft Azure Cloud Services**


> SpaceONE's [plugin-azure-cloud-services](https://github.com/spaceone-dev/plugin-azure-cloud-services) is a convenient tool to 
get cloud service data from Azure Cloud Services. 


Find us also at [Dockerhub](https://hub.docker.com/r/spaceone/azure-cloud-services)
> Latest stable version : 1.2.14

Please contact us if you need any further information. 
<support@spaceone.dev>


## Contents

|Cloud Service Type|Cloud Service|
|---|---|
|Network|[Application Gateways](#Application_Gateways)|
|Database|[CosmosDBs](#cosmos_dbs)|
|Compute|[Disks](#disks)|
|KeyVault|[KeyVaults](#key_vaults)|
|Network|[Load Balancers](#Load_Balancer)|
|Database|[MySQL Servers](#my_sql_server)|
|Network|[NAT Gateways](#NAT_Gateways)|
|Network|[Network Security Groups](#Network_security_groups)|
|Database|[PostgreSQL Servers](#postgre_sql_servers)|
|Network|[Public IP Address](#public_ip_addresses)|
|Compute|[Snapshots](#Snapshots)|
|Database|[SQL Servers](#SQL_Servers)|
|Database|[SQL Databases](#SQL_databases)|
|Storage|[Storage Account](#storage_accounts)|
|Network|[Virtual Network](#virtual_networks)|
|Compute|[VM ScaleSets](#vm_scale_sets)|
    
---
## SETTING
You should insert information about account in SpaceONE's **Service Account** initially.
* Base Information
	* `name`
	* `Tenant ID`
	* `Subscription ID`
	* `Tag`

* Credentials
	* `Tenant ID`
	* `Subscription ID`
	* `Client Secret`
	* `Client ID`
---

## Authentication Overview
Registered service account on SpaceONE must have certain permissions to collect cloud service data 
Please, set authentication privilege for followings:

### Custom roles for SpaceONE collector
SpaceONE collector requires several privileges for collecting resources. <br>
Please create custom roles in Azure portal, and assign following roles to SpaceONE collector apps before collect resources.
For information on creating custom roles in Azure, see the [Microsoft custom role document](https://docs.microsoft.com/en-us/azure/role-based-access-control/custom-roles). <br>
```
{
    "properties": {
        "roleName": "spaceone_collector_role",
        "description": "",
        "assignableScopes": [
            "/subscriptions/3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.Network/applicationGateways/read",
                    "Microsoft.Network/applicationGateways/privateEndpointConnections/read",
                    "Microsoft.Network/applicationGateways/privateLinkConfigurations/read",
                    "Microsoft.Network/applicationGateways/privateLinkResources/read",
                    "Microsoft.Network/publicIPAddresses/read",
                    "Microsoft.Network/publicIPAddresses/dnsAliases/read",
                    "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/logDefinitions/read",
                    "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/metricDefinitions/read",
                    "Microsoft.DocumentDB/databaseAccounts/services/read",
                    "Microsoft.DocumentDB/databaseAccounts/read",
                    "Microsoft.DocumentDB/databaseAccounts/listKeys/action",
                    "Microsoft.DocumentDB/databaseAccounts/privateLinkResources/read",
                    "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/read",
                    "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/clientEncryptionKeys/read",
                    "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/read",
                    "Microsoft.DocumentDB/databaseAccounts/tables/read",
                    "Microsoft.Compute/disks/read",
                    "Microsoft.KeyVault/vaults/read",
                    "Microsoft.KeyVault/vaults/keys/read",
                    "Microsoft.KeyVault/vaults/providers/Microsoft.Insights/diagnosticSettings/Read",
                    "Microsoft.KeyVault/vaults/privateEndpointConnections/read",
                    "Microsoft.KeyVault/vaults/privateEndpointConnectionProxies/read",
                    "Microsoft.KeyVault/vaults/secrets/read",
                    "Microsoft.Network/loadBalancers/read",
                    "Microsoft.Network/loadBalancers/backendAddressPools/read",
                    "Microsoft.Network/loadBalancers/backendAddressPools/backendPoolAddresses/read",
                    "Microsoft.Network/loadBalancers/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Network/loadBalancers/frontendIPConfigurations/read",
                    "Microsoft.Network/loadBalancers/frontendIPConfigurations/loadBalancerPools/read",
                    "Microsoft.Network/loadBalancers/inboundNatPools/read",
                    "Microsoft.Network/loadBalancers/inboundNatRules/read",
                    "Microsoft.Network/loadBalancers/loadBalancingRules/read",
                    "Microsoft.Network/loadBalancers/providers/Microsoft.Insights/logDefinitions/read",
                    "Microsoft.Network/loadBalancers/outboundRules/read",
                    "Microsoft.Network/loadBalancers/networkInterfaces/read",
                    "Microsoft.Network/loadBalancers/probes/read",
                    "Microsoft.Network/loadBalancers/virtualMachines/read",
                    "Microsoft.Network/networkInterfaces/loadBalancers/read",
                    "Microsoft.Network/virtualNetworks/subnets/joinLoadBalancer/action",
                    "Microsoft.Network/virtualNetworks/joinLoadBalancer/action",
                    "Microsoft.DBforMySQL/flexibleServers/read",
                    "Microsoft.DBforMySQL/flexibleServers/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.DBforMySQL/servers/read",
                    "Microsoft.DBforMySQL/servers/administrators/read",
                    "Microsoft.DBforMySQL/servers/advisors/read",
                    "Microsoft.DBforMySQL/servers/privateEndpointConnectionProxies/read",
                    "Microsoft.DBforMySQL/servers/keys/read",
                    "Microsoft.DBforMySQL/servers/privateEndpointConnections/read",
                    "Microsoft.DBforMySQL/servers/privateLinkResources/read",
                    "Microsoft.DBforMySQL/servers/configurations/read",
                    "Microsoft.DBforMySQL/servers/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.DBforMySQL/servers/providers/Microsoft.Insights/metricDefinitions/read",
                    "Microsoft.DBforMySQL/servers/firewallRules/read",
                    "Microsoft.DBforMySQL/servers/databases/read",
                    "Microsoft.DBforMySQL/servers/replicas/read",
                    "Microsoft.DBforMySQL/servers/performanceTiers/read",
                    "Microsoft.DBforMySQL/servers/recoverableServers/read",
                    "Microsoft.DBforMySQL/servers/virtualNetworkRules/read",
                    "Microsoft.Network/natGateways/read",
                    "Microsoft.Network/natGateways/join/action",
                    "microsoft.network/vpnGateways/natRules/read",
                    "microsoft.network/virtualNetworkGateways/natRules/read",
                    "Microsoft.Network/publicIPAddresses/read",
                    "Microsoft.Network/publicIPAddresses/dnsAliases/read",
                    "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Network/publicIPPrefixes/read",
                    "Microsoft.Network/virtualNetworks/subnets/read",
                    "Microsoft.Network/networkSecurityGroups/read",
                    "Microsoft.Network/networkSecurityGroups/defaultSecurityRules/read",
                    "Microsoft.Network/networksecuritygroups/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Network/networkSecurityGroups/securityRules/read",
                    "Microsoft.Network/networkInterfaces/read",
                    "Microsoft.Network/networkInterfaces/effectiveNetworkSecurityGroups/action",
                    "Microsoft.Network/virtualNetworks/subnets/read",
                    "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
                    "Microsoft.Network/virtualNetworks/subnets/join/action",
                    "Microsoft.DBforPostgreSQL/servers/read",
                    "Microsoft.DBforPostgreSQL/servers/administrators/read",
                    "Microsoft.DBforPostgreSQL/servers/advisors/read",
                    "Microsoft.DBforPostgreSQL/servers/privateEndpointConnectionProxies/read",
                    "Microsoft.DBforPostgreSQL/servers/keys/read",
                    "Microsoft.DBforPostgreSQL/servers/privateEndpointConnections/read",
                    "Microsoft.DBforPostgreSQL/servers/privateLinkResources/read",
                    "Microsoft.DBforPostgreSQL/servers/configurations/read",
                    "Microsoft.DBforPostgreSQL/servers/firewallRules/read",
                    "Microsoft.DBforPostgreSQL/servers/databases/read",
                    "Microsoft.DBforPostgreSQL/servers/replicas/read",
                    "Microsoft.DBforPostgreSQL/servers/recoverableServers/read",
                    "Microsoft.DBforPostgreSQL/servers/securityAlertPolicies/read",
                    "Microsoft.DBforPostgreSQL/servers/virtualNetworkRules/read",
                    "Microsoft.Network/publicIPAddresses/read",
                    "Microsoft.Network/publicIPAddresses/join/action",
                    "Microsoft.Network/publicIPAddresses/dnsAliases/read",
                    "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Network/publicIPAddresses/read",
                    "Microsoft.Network/publicIPAddresses/join/action",
                    "Microsoft.Network/publicIPAddresses/dnsAliases/read",
                    "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Storage/deletedAccounts/read",
                    "Microsoft.Storage/storageAccounts/read",
                    "Microsoft.Storage/storageAccounts/privateEndpointConnections/read",
                    "Microsoft.Storage/storageAccounts/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Storage/storageAccounts/blobServices/read",
                    "Microsoft.Storage/storageAccounts/blobServices/containers/read",
                    "Microsoft.Storage/storageAccounts/tableServices/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Storage/storageAccounts/privateLinkResources/read",
                    "Microsoft.Storage/storageAccounts/objectReplicationPolicies/read",
                    "Microsoft.Storage/storageAccounts/encryptionScopes/read",
                    "Microsoft.Compute/virtualMachineScaleSets/read",
                    "Microsoft.Compute/virtualMachineScaleSets/networkInterfaces/read",
                    "Microsoft.Compute/virtualMachineScaleSets/publicIPAddresses/read",
                    "Microsoft.Compute/virtualMachineScaleSets/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Compute/virtualMachineScaleSets/extensions/read",
                    "Microsoft.Compute/virtualMachineScaleSets/extensions/roles/read",
                    "Microsoft.Compute/virtualMachineScaleSets/instanceView/read",
                    "Microsoft.Compute/virtualMachineScaleSets/osUpgradeHistory/read",
                    "Microsoft.Compute/virtualMachineScaleSets/skus/read",
                    "Microsoft.Compute/virtualMachineScaleSets/rollingUpgrades/read",
                    "Microsoft.Compute/virtualMachineScaleSets/providers/Microsoft.Insights/metricDefinitions/read",
                    "Microsoft.Compute/virtualMachineScaleSets/vmSizes/read",
                    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/read",
                    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/extensions/read",
                    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/instanceView/read",
                    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/networkInterfaces/read",
                    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/networkInterfaces/ipConfigurations/read",
                    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/networkInterfaces/ipConfigurations/publicIPAddresses/read",
                    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/runCommands/read",
                    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/providers/Microsoft.Insights/metricDefinitions/read",
                    "Microsoft.Network/dnsForwardingRulesets/virtualNetworkLinks/read",
                    "Microsoft.Network/loadBalancers/virtualMachines/read",
                    "Microsoft.Network/networkInterfaces/join/action",
                    "Microsoft.Network/privateDnsZones/read",
                    "Microsoft.Network/privateDnsZones/virtualNetworkLinks/read",
                    "Microsoft.Network/locations/virtualNetworkAvailableEndpointServices/read",
                    "Microsoft.Network/virtualNetworks/read",
                    "Microsoft.Network/locations/supportedVirtualMachineSizes/read",
                    "Microsoft.Network/virtualNetworks/bastionHosts/default/action",
                    "Microsoft.Network/virtualNetworks/dnsForwardingRulesets/read",
                    "Microsoft.Network/virtualNetworks/dnsResolvers/read",
                    "Microsoft.Network/virtualNetworks/checkIpAddressAvailability/read",
                    "Microsoft.Network/virtualNetworks/privateDnsZoneLinks/read",
                    "Microsoft.Network/virtualNetworks/usages/read",
                    "Microsoft.Network/virtualNetworks/virtualNetworkPeerings/read",
                    "Microsoft.Network/virtualNetworks/remoteVirtualNetworkPeeringProxies/read",
                    "Microsoft.Network/virtualNetworks/subnets/read",
                    "Microsoft.Network/virtualNetworks/subnets/contextualServiceEndpointPolicies/read",
                    "Microsoft.Network/virtualNetworks/subnets/resourceNavigationLinks/read",
                    "Microsoft.Network/virtualNetworks/subnets/serviceAssociationLinks/read",
                    "Microsoft.Network/virtualNetworks/subnets/serviceAssociationLinks/details/read",
                    "Microsoft.Network/virtualNetworks/subnets/virtualMachines/read",
                    "Microsoft.Network/virtualNetworks/virtualMachines/read",
                    "Microsoft.Network/virtualNetworks/customViews/read",
                    "Microsoft.Network/virtualNetworks/providers/Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Network/virtualNetworkGateways/read",
                    "microsoft.network/virtualNetworkGateways/natRules/read",
                    "Microsoft.Network/virtualNetworkGateways/providers/Microsoft.Insights/diagnosticSettings/read",
                    "microsoft.network/virtualnetworkgateways/connections/read",
                    "Microsoft.Network/connections/read",
                    "Microsoft.Network/virtualNetworkTaps/read",
                    "Microsoft.Network/virtualNetworkTaps/networkInterfaceTapConfigurationProxies/read",
                    "Microsoft.Network/virtualRouters/read",
                    "Microsoft.Network/virtualRouters/providers/Microsoft.Insights/metricDefinitions/read",
                    "Microsoft.Network/virtualRouters/peerings/read"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": []
            }
        ]
    }
}
```
### Additional custom roles for SpaceONE collector
Some of cloud services require several additional IAM settings for collecting resources. <br>
#### KeyVaults
For collecting Azure ```KeyVaults``` resources, you need to assign a Key Vault access policy to SpaceONE collector App in Azure portal.
For information on assigning access policy, see [Microsoft key vault access policy document](https://docs.microsoft.com/en-us/azure/key-vault/general/assign-access-policy?tabs=azure-portal).

#### CosmosDB
For collecting key lists in ```CosmosDB``` azure resources, you need to assign an access policy to SpaceONE collector App in Azure portal.
For information on creating custom roles in Azure, see the [Microsoft custom role document](https://docs.microsoft.com/en-us/azure/role-based-access-control/custom-roles). <br>

```
{
    "properties": {
        "roleName": "YOUR_ROLE_NAME_FOR_LIST_KEYS_IN_COSMOSDB",
        "description": "",
        "assignableScopes": [
            "/subscriptions/YOUR_SUBSCRIPTION_ID"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.DocumentDB/databaseAccounts/listKeys/action"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": []
            }
        ]
    }
}
```

#### [Virtual Machines](https://docs.microsoft.com/ko-kr/rest/api/compute/virtualmachines/list)
      
- Azure VM (Instance)

    - Scope
        - https://docs.microsoft.com/ko-kr/rest/api/compute/virtualmachines/listall
        - https://docs.microsoft.com/ko-kr/rest/api/compute/virtualmachines/get
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/virtualnetworks/list
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/publicipaddresses/list
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/virtualnetworks
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/networkinterfaces
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/networksecuritygroups
		
    - Permissions
        - Microsoft.Compute/*/read
        - Microsoft.Resources/*/read
        - Microsoft.Network/networkInterfaces/read	
        - Microsoft.Network/publicIPAddresses/read
        - Microsoft.Network/networkSecurityGroups/read
        - Microsoft.Network/loadBalancers/read
	
  
#### [Virtual Machine Scale Sets](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesets/listall)
- Virtual Machine Scale Sets
    - Scope
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesets/listall
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesetvms/list

    - Permissions
        ```
        "Microsoft.Compute/virtualMachineScaleSets/read",
        "Microsoft.Compute/virtualMachineScaleSets/networkInterfaces/read",
        "Microsoft.Compute/virtualMachineScaleSets/publicIPAddresses/read",
        "Microsoft.Compute/virtualMachineScaleSets/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Compute/virtualMachineScaleSets/extensions/read",
        "Microsoft.Compute/virtualMachineScaleSets/extensions/roles/read",
        "Microsoft.Compute/virtualMachineScaleSets/instanceView/read",
        "Microsoft.Compute/virtualMachineScaleSets/osUpgradeHistory/read",
        "Microsoft.Compute/virtualMachineScaleSets/skus/read",
        "Microsoft.Compute/virtualMachineScaleSets/rollingUpgrades/read",
        "Microsoft.Compute/virtualMachineScaleSets/providers/Microsoft.Insights/metricDefinitions/read",
        "Microsoft.Compute/virtualMachineScaleSets/vmSizes/read",
        "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/read",
        "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/extensions/read",
        "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/instanceView/read",
        "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/networkInterfaces/read",
        "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/networkInterfaces/ipConfigurations/read",
        "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/networkInterfaces/ipConfigurations/publicIPAddresses/read",
        "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/runCommands/read",
        "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/providers/Microsoft.Insights/metricDefinitions/read"
        ```
        
#### [Virtual Network](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/virtual-networks/list-all)
- Virtual Network
    - Scope
        - https://docs.microsoft.com/en-us/rest/api/virtualnetwork/virtual-networks/list-all

    - Permissions
      ```
        "Microsoft.Network/dnsForwardingRulesets/virtualNetworkLinks/read",
        "Microsoft.Network/loadBalancers/virtualMachines/read",
        "Microsoft.Network/networkInterfaces/join/action",
        "Microsoft.Network/privateDnsZones/read",
        "Microsoft.Network/privateDnsZones/virtualNetworkLinks/read",
        "Microsoft.Network/locations/virtualNetworkAvailableEndpointServices/read",
        "Microsoft.Network/virtualNetworks/read",
        "Microsoft.Network/locations/supportedVirtualMachineSizes/read",
        "Microsoft.Network/virtualNetworks/bastionHosts/default/action",
        "Microsoft.Network/virtualNetworks/dnsForwardingRulesets/read",
        "Microsoft.Network/virtualNetworks/dnsResolvers/read",
        "Microsoft.Network/virtualNetworks/checkIpAddressAvailability/read",
        "Microsoft.Network/virtualNetworks/privateDnsZoneLinks/read",
        "Microsoft.Network/virtualNetworks/usages/read",
        "Microsoft.Network/virtualNetworks/virtualNetworkPeerings/read",
        "Microsoft.Network/virtualNetworks/remoteVirtualNetworkPeeringProxies/read",
        "Microsoft.Network/virtualNetworks/subnets/read",
        "Microsoft.Network/virtualNetworks/subnets/contextualServiceEndpointPolicies/read",
        "Microsoft.Network/virtualNetworks/subnets/resourceNavigationLinks/read",
        "Microsoft.Network/virtualNetworks/subnets/serviceAssociationLinks/read",
        "Microsoft.Network/virtualNetworks/subnets/serviceAssociationLinks/details/read",
        "Microsoft.Network/virtualNetworks/subnets/virtualMachines/read",
        "Microsoft.Network/virtualNetworks/virtualMachines/read",
        "Microsoft.Network/virtualNetworks/customViews/read",
        "Microsoft.Network/virtualNetworks/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Network/virtualNetworkGateways/read",
        "microsoft.network/virtualNetworkGateways/natRules/read",
        "Microsoft.Network/virtualNetworkGateways/providers/Microsoft.Insights/diagnosticSettings/read",
        "microsoft.network/virtualnetworkgateways/connections/read",
        "Microsoft.Network/connections/read",
        "Microsoft.Network/virtualNetworkTaps/read",
        "Microsoft.Network/virtualNetworkTaps/networkInterfaceTapConfigurationProxies/read",
        "Microsoft.Network/virtualRouters/read",
        "Microsoft.Network/virtualRouters/providers/Microsoft.Insights/metricDefinitions/read",
        "Microsoft.Network/virtualRouters/peerings/read",
        "Microsoft.Sql/operations/read",
        "Microsoft.Sql/checkNameAvailability/action",
        "Microsoft.Sql/servers/read",
        "Microsoft.Sql/servers/outboundFirewallRules/read",
        "Microsoft.Sql/servers/jobAgents/read",
        "Microsoft.Sql/servers/databases/read",
        "Microsoft.Sql/servers/jobAgents/targetGroups/read",
        "Microsoft.Sql/servers/databases/geoBackupPolicies/read",
        "Microsoft.Sql/servers/databases/azureAsyncOperation/read",
        "Microsoft.Sql/servers/databases/extensions/read",
        "Microsoft.Sql/servers/databases/extensions/importExtensionOperationResults/read",
        "Microsoft.Sql/servers/databases/operationResults/read",
        "Microsoft.Sql/servers/databases/operations/read",
        "Microsoft.Sql/servers/databases/skus/read",
        "Microsoft.Sql/servers/databases/usages/read",
        "Microsoft.Sql/servers/databases/transparentDataEncryption/read",
        "Microsoft.Sql/servers/databases/transparentDataEncryption/operationResults/read",
        "Microsoft.Sql/servers/databases/ledgerDigestUploads/read",
        "Microsoft.Sql/servers/databases/syncGroups/read",
        "Microsoft.Sql/servers/databases/syncGroups/hubSchemas/read",
        "Microsoft.Sql/servers/databases/syncGroups/logs/read",
        "Microsoft.Sql/servers/databases/syncGroups/refreshHubSchemaOperationResults/read",
        "Microsoft.Sql/servers/databases/syncGroups/syncMembers/read",
        "Microsoft.Sql/servers/databases/syncGroups/syncMembers/refreshSchemaOperationResults/read",
        "Microsoft.Sql/servers/databases/syncGroups/syncMembers/schemas/read",
        "Microsoft.Sql/servers/databases/auditRecords/read",
        "Microsoft.Sql/servers/databases/auditingSettings/read",
        "Microsoft.Sql/servers/databases/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Sql/servers/databases/replicationLinks/read",
        "Microsoft.Sql/servers/databases/restorePoints/read",
        "Microsoft.Sql/servers/databases/securityMetrics/read",
        "Microsoft.Sql/servers/databases/serviceTierAdvisors/read",
        "Microsoft.Sql/servers/databases/securityAlertPolicies/read",
        "Microsoft.Sql/servers/databases/extendedAuditingSettings/read",
        "Microsoft.Sql/servers/databases/backupShortTermRetentionPolicies/read",
        "Microsoft.Sql/servers/elasticPools/read",
        "Microsoft.Sql/servers/elasticPools/databases/read",
        "Microsoft.Sql/servers/elasticPools/operations/read",
        "Microsoft.Sql/servers/elasticPools/skus/read",
        "Microsoft.Sql/servers/elasticPools/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Sql/servers/elasticPools/elasticPoolActivity/read",
        "Microsoft.Sql/servers/elasticPools/metrics/read",
        "Microsoft.Sql/servers/elasticPools/metricDefinitions/read",
        "Microsoft.Sql/servers/elasticPools/providers/Microsoft.Insights/metricDefinitions/read",
        "Microsoft.Sql/servers/elasticPools/advisors/read",
        "Microsoft.Sql/servers/elasticPools/elasticPoolDatabaseActivity/read",
        "Microsoft.Sql/servers/failoverGroups/read",
        "Microsoft.Sql/servers/privateEndpointConnections/read",
        "Microsoft.Sql/servers/privateEndpointConnectionProxies/read",
        "Microsoft.Sql/servers/privateLinkResources/read",
        "Microsoft.Sql/servers/dnsAliases/read",
        "Microsoft.Sql/servers/operationResults/read",
        "Microsoft.Sql/servers/operations/read",
        "Microsoft.Sql/servers/virtualNetworkRules/read",
        "Microsoft.Sql/servers/syncAgents/read",
        "Microsoft.Sql/servers/syncAgents/linkedDatabases/read",
        "Microsoft.Sql/servers/disasterRecoveryConfiguration/read",
        "Microsoft.Sql/servers/ipv6FirewallRules/read",
        "Microsoft.Sql/servers/replicationLinks/read",
        "Microsoft.Sql/servers/restorableDroppedDatabases/read",
        "Microsoft.Sql/servers/auditingSettings/read",
        "Microsoft.Sql/servers/automaticTuning/read",
        "Microsoft.Sql/servers/firewallRules/read",
        "Microsoft.Sql/servers/administrators/read",
        "Microsoft.Sql/locations/databaseOperationResults/read",
        "Microsoft.Sql/locations/elasticPoolOperationResults/read",
        "Microsoft.Sql/locations/privateEndpointConnectionAzureAsyncOperation/read",
        "Microsoft.Sql/locations/privateEndpointConnectionOperationResults/read",
        "Microsoft.Sql/locations/instanceFailoverGroups/read",
        "Microsoft.Sql/locations/longTermRetentionBackups/read",
        "Microsoft.Sql/locations/longTermRetentionBackupOperationResults/read",
        "Microsoft.Sql/locations/transparentDataEncryptionAzureAsyncOperation/read",
        "Microsoft.Sql/locations/transparentDataEncryptionOperationResults/read",
        "Microsoft.Sql/locations/timeZones/read",
        "Microsoft.Sql/locations/auditingSettingsOperationResults/read",
        "Microsoft.Sql/locations/firewallRulesAzureAsyncOperation/read",
        "Microsoft.Sql/locations/serverAdministratorOperationResults/read"
      ```	
        

#### [Disks](https://docs.microsoft.com/en-ca/rest/api/compute/disks/list)
- Disks
    - Scope
        - https://docs.microsoft.com/en-ca/rest/api/compute/disks/list
    
    - Permissions
       ```
       "Microsoft.Compute/disks/read"
       ```


#### [Snapshots](https://docs.microsoft.com/en-us/rest/api/compute/snapshots/list)
- Snapshots
    - Scope
        - https://docs.microsoft.com/en-us/rest/api/compute/snapshots/list
    
    - Permissions
      ```
       "Microsoft.Compute/snapshots/read",
       "Microsoft.Compute/snapshots/beginGetAccess/action"
      ```

#### [SQL Servers](https://docs.microsoft.com/en-us/rest/api/sql/2021-02-01-preview/servers)
- SQL Servers
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/sql/2021-02-01-preview/servers

    - Permissions
        - Microsoft.Sql/servers/*/read

#### [Load Balancers](https://docs.microsoft.com/en-us/rest/api/load-balancer/loadbalancers/listall)
- Load Balancer
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/load-balancer/loadbalancers/listall
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/subnets/get

    - Permissions
        ```
        "Microsoft.Network/loadBalancers/read",
        "Microsoft.Network/loadBalancers/backendAddressPools/read",
        "Microsoft.Network/loadBalancers/backendAddressPools/backendPoolAddresses/read",
        "Microsoft.Network/loadBalancers/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Network/loadBalancers/frontendIPConfigurations/read",
        "Microsoft.Network/loadBalancers/frontendIPConfigurations/loadBalancerPools/read",
        "Microsoft.Network/loadBalancers/inboundNatPools/read",
        "Microsoft.Network/loadBalancers/inboundNatRules/read",
        "Microsoft.Network/loadBalancers/loadBalancingRules/read",
        "Microsoft.Network/loadBalancers/providers/Microsoft.Insights/logDefinitions/read",
        "Microsoft.Network/loadBalancers/outboundRules/read",
        "Microsoft.Network/loadBalancers/networkInterfaces/read",
        "Microsoft.Network/loadBalancers/probes/read",
        "Microsoft.Network/loadBalancers/virtualMachines/read",
        "Microsoft.Network/networkInterfaces/loadBalancers/read",
        "Microsoft.Network/virtualNetworks/subnets/joinLoadBalancer/action",
        "Microsoft.Network/virtualNetworks/joinLoadBalancer/action"
        ```

#### [Public IP Addresses](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/public-ip-addresses/list-all)
- Public IP Address
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/virtualnetwork/public-ip-addresses/list-all

    - Permissions
      ```
        "Microsoft.Network/publicIPAddresses/read",
        "Microsoft.Network/publicIPAddresses/join/action",
        "Microsoft.Network/publicIPAddresses/dnsAliases/read",
        "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/diagnosticSettings/read"
      ```


#### [NetworkSecurityGroups](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/network-security-groups/list-all)
- Network Security Group
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/virtualnetwork/network-security-groups/list-all

    - Permissions
      ```
        "Microsoft.Network/networkSecurityGroups/read",
        "Microsoft.Network/networkSecurityGroups/defaultSecurityRules/read",
        "Microsoft.Network/networksecuritygroups/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Network/networkSecurityGroups/securityRules/read",
        "Microsoft.Network/networkInterfaces/read",
        "Microsoft.Network/networkInterfaces/effectiveNetworkSecurityGroups/action",
        "Microsoft.Network/virtualNetworks/subnets/read",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ```

#### [Application Gateways](https://docs.microsoft.com/en-us/rest/api/application-gateway/application-gateways/list-all)
- Application Gateways
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/application-gateway/application-gateways/list-all

    - Permissions
      ```
        "Microsoft.Network/applicationGateways/read",
        "Microsoft.Network/applicationGateways/privateEndpointConnections/read",
        "Microsoft.Network/applicationGateways/privateLinkConfigurations/read",
        "Microsoft.Network/applicationGateways/privateLinkResources/read",
        "Microsoft.Network/publicIPAddresses/read",
        "Microsoft.Network/publicIPAddresses/dnsAliases/read",
        "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/logDefinitions/read",
        "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/metricDefinitions/read"
      ```

#### [NAT Gateways](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/nat-gateways/list-all)
- NAT Gateways
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/virtualnetwork/nat-gateways/list-all

    - Permissions
      ```
        "Microsoft.Network/natGateways/read",
        "Microsoft.Network/natGateways/join/action",
        "microsoft.network/vpnGateways/natRules/read",
        "microsoft.network/virtualNetworkGateways/natRules/read",
        "Microsoft.Network/publicIPAddresses/read",
        "Microsoft.Network/publicIPAddresses/dnsAliases/read",
        "Microsoft.Network/publicIPAddresses/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Network/publicIPPrefixes/read",
        "Microsoft.Network/virtualNetworks/subnets/read"
      ```

#### [Storage Accounts](https://docs.microsoft.com/en-us/rest/api/storagerp/storage-accounts/list#blobrestorerange)
- Storage Accounts
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/storagerp/storage-accounts/list
    - Permissions
      ```
        "Microsoft.Storage/deletedAccounts/read",
        "Microsoft.Storage/storageAccounts/read",
        "Microsoft.Storage/storageAccounts/privateEndpointConnections/read",
        "Microsoft.Storage/storageAccounts/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Storage/storageAccounts/blobServices/read",
        "Microsoft.Storage/storageAccounts/blobServices/containers/read",
        "Microsoft.Storage/storageAccounts/tableServices/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.Storage/storageAccounts/privateLinkResources/read",
        "Microsoft.Storage/storageAccounts/objectReplicationPolicies/read",
        "Microsoft.Storage/storageAccounts/encryptionScopes/read"
      ```


#### [MySQL Servers]()
- MySQL Servers
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/storagerp/storage-accounts/list
    - Permissions
        ```
        "Microsoft.DBforMySQL/flexibleServers/read",
        "Microsoft.DBforMySQL/flexibleServers/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.DBforMySQL/servers/read",
        "Microsoft.DBforMySQL/servers/administrators/read",
        "Microsoft.DBforMySQL/servers/advisors/read",
        "Microsoft.DBforMySQL/servers/privateEndpointConnectionProxies/read",
        "Microsoft.DBforMySQL/servers/keys/read",
        "Microsoft.DBforMySQL/servers/privateEndpointConnections/read",
        "Microsoft.DBforMySQL/servers/privateLinkResources/read",
        "Microsoft.DBforMySQL/servers/configurations/read",
        "Microsoft.DBforMySQL/servers/providers/Microsoft.Insights/diagnosticSettings/read",
        "Microsoft.DBforMySQL/servers/providers/Microsoft.Insights/metricDefinitions/read",
        "Microsoft.DBforMySQL/servers/firewallRules/read",
        "Microsoft.DBforMySQL/servers/databases/read",
        "Microsoft.DBforMySQL/servers/replicas/read",
        "Microsoft.DBforMySQL/servers/performanceTiers/read",
        "Microsoft.DBforMySQL/servers/recoverableServers/read",
        "Microsoft.DBforMySQL/servers/virtualNetworkRules/read"
        ```
    
    - SpaceONE Inventory Collector only supports ``Single Servers`` type. 

#### [PostgreSQL Servers](https://docs.microsoft.com/en-us/rest/api/postgresql/flexibleserver(preview)/servers/list)
- PostgreSQL Servers
    - Scope
        - https://docs.microsoft.com/en-us/rest/api/postgresql/flexibleserver(preview)/servers/list
    - Permissions
      ```
        "Microsoft.DBforPostgreSQL/servers/read",
        "Microsoft.DBforPostgreSQL/servers/administrators/read",
        "Microsoft.DBforPostgreSQL/servers/advisors/read",
        "Microsoft.DBforPostgreSQL/servers/privateEndpointConnectionProxies/read",
        "Microsoft.DBforPostgreSQL/servers/keys/read",
        "Microsoft.DBforPostgreSQL/servers/privateEndpointConnections/read",
        "Microsoft.DBforPostgreSQL/servers/privateLinkResources/read",
        "Microsoft.DBforPostgreSQL/servers/configurations/read",
        "Microsoft.DBforPostgreSQL/servers/firewallRules/read",
        "Microsoft.DBforPostgreSQL/servers/databases/read",
        "Microsoft.DBforPostgreSQL/servers/replicas/read",
        "Microsoft.DBforPostgreSQL/servers/recoverableServers/read",
        "Microsoft.DBforPostgreSQL/servers/securityAlertPolicies/read",
        "Microsoft.DBforPostgreSQL/servers/virtualNetworkRules/read"
      ``` 

---
## Options

### Cloud Service Type : Specify what to collect

If cloud_service_types is added to the list elements in options, only the specified cloud service type is collected.
By default, if cloud_service_types is not specified in options, all services are collected.

The cloud_service_types items that can be specified are as follows.

<pre>
<code>
{
    "cloud_service_types": [
       'ApplicationGateway',
        'AzureCosmosDB',
        'Disk',
        'KeyVault',
        'LoadBalancer',
        'SQLServer',
        'MySQLServer',
        'NATGateway',
        'NetworkSecurityGroup,
        'PostgreSQLServer',
        'PublicIPAddress',
        'Snapshot',
        'StorageAccount',
        'VirtualNetwork',
        'VMScaleSet' 
    ]
}
</code>
</pre>

How to update plugin information using spacectl is as follows.
First, create a yaml file to set options.

<pre>
<code>
> cat update_collector.yaml
---
collector_id: collector-xxxxxxx
options:
  cloud_service_types:
    - VMScaleSet
    - VirtualNetwork
</code>
</pre>

Update plugin through spacectl command with the created yaml file.

<pre><code>
> spacectl exec update_plugin inventory.Collector -f update_collector.yaml
</code></pre>

## Release Note
### Ver 1.2.14
* [Add feature for Usage Overview of cloud services](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/174)
### Ver 1.2.13
* [Add feature to specify the Cloud Service Type and collect it.](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/162)
* [Add fields to cloud services model(account, instance_type, instance_size, launched_at)](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/159) 
* [Add ErrorResources to collect error messages as resources](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/157)

### Ver 1.2.12
* [Add ```PostgreSQL``` Servers cloud service](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/154)

### Ver 1.2.10
* [Add CosmosDB Syntax bug](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/152/commits)
* [Add ```CosmosDB cloud``` service](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/commit/c50693a222555611cb1fb27b2ce222543e1cf174)
* [Update CI workflow](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/142)

### Ver 1.2.8
* [Add ```MySQL Servers``` cloud service](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/136)


### Ver 1.2.7
* [Add ```Key Vaults``` cloud service](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/123)

### Ver 1.2.6
* Add ```Storage Accounts``` cloud service

### Ver 1.2.5
* Add ```NAT Gateways``` cloud service

### Ver 1.2.4
* Add ```Network Security Groups``` cloud service

### Ver 1.2.3
* Add ```Virtual Networks```, ```Application Gateways```, ```Public IP Address``` cloud service


