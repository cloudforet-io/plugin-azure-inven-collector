<h1 align="center">Microsoft Azure Collector</h1>  

<br/>  
<div align="center" style="display:flex;">  
  <img width="245" src="https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-cloud-services.svg">
  <p> 
    <br>
    <img alt="Version"  src="https://img.shields.io/badge/version-2.0.8-blue.svg?cacheSeconds=2592000"  />    
    <a href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank"><img alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg" /></a> 
  </p> 
</div> 

#### Plugin to collect Microsoft Azure Cloud Services

> Cloudforet's [plugin-azure-cloud-services](https://github.com/cloudforet-io/plugin-azure-inven-collector) is a
> convenient tool to
> get cloud service data from Azure Cloud Services.


Find us also at [Dockerhub](https://hub.docker.com/r/cloudforet/plugin-azure-inven-collector)
> Latest stable version : 2.0.8

Please contact us if you need any further information.
<admin@cloudforet.io>

## Contents

| Cloud Service Type                                                       | Cloud Service                                               |
|--------------------------------------------------------------------------|-------------------------------------------------------------|
| Instance                                                                 | [Application Gateways](#application-gateways)               |
| Container                                                                | [Container Instances](#container-instances)                 |
| Container                                                                | [Container Registries](#container-registries)               |
| Instance                                                                 | [CosmosDB](#cosmos-db)                                      |
| Disk                                                                     | [Disks](#disks)                                             |
| Instance                                                                 | [KeyVaults](#key-vaults)                                    |
| Instance                                                                 | [Load Balancers](#load-balancers)                           |
| Server                                                                   | [MySQL Servers](#mysql-servers---deprecated)                |
| Server                                                                   | [MySQL Flexible Servers](#mysql-flexible-servers)           |
| Instance                                                                 | [NAT Gateways](#nat-gateways)                               |
| Instance                                                                 | [Network Security Groups](#network-security-groups)         |
| Server                                                                   | [PostgreSQL Servers](#postgresql-servers---deprecated)      |
| Server                                                                   | [PostgreSQL Flexible Servers](#postgresql-flexible-servers) |
| IPAddress                                                                | [Public IP Addresses](#public-ip-addresses)                 |
| Instance                                                                 | [Snapshots](#snapshots)                                     |
| Server                                                                   | [SQL Servers](#sql-servers)                                 |
| Database                                                                 | [SQL Databases](#sql-databases)                             |
| Storage                                                                  | [Storage Accounts](#storage-accounts)                       |
| Instance                                                                 | [Virtual Machines](#virtual-machines)                       |
| Instance                                                                 | [Virtual Networks](#virtual-networks)                       |
| ScaleSet                                                                 | [VM ScaleSets](#virtual-machine-scale-sets)                 |
| Service                                                                  | [Web PubSub Service](#web-pubsub-service)                   |
| Score<br>OperationalExcellence<br>Performance<br>Reliability<br>Security | [Advisor](#advisor)                                         |
| Instance                                                                 | [Functions](#functions)                                     |
| Instance                                                                 | [Kubernetes Service](#kubernetes-service) |


    
---

## SETTING

You should insert information about account in Cloudforet's **Service Account** initially.

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

## Azure Service Endpoint (in use)

There is an endpoints used to collect Azure resources information.

<pre>
https://management.azure.com
https://login.microsoftonline.com
https://*.vault.azure.net
</pre>

---

## Service list

The following is a list of services being collected and service code information.

| No. | Service name                | Service Code                                                      |
|-----|-----------------------------|-------------------------------------------------------------------|
| 1   | Application Gateways        | Microsoft.Network/applicationGateways                             |
| 2   | Cosmos DB                   | Microsoft.DocumentDB/databaseAccounts                             |
| 3   | Disks                       | Microsoft.Compute/disks                                           |
| 4   | Key Vaults                  | Microsoft.KeyVault/vaults                                         |
| 5   | Load Balancers              | Microsoft.Network/loadBalancers                                   |
| 6   | MySQL Servers               | Microsoft.DBforMySQL/servers                                      |
| 7   | MySQL Flexible Servers      | Microsoft.DBforMySQL/flexibleServers                              |
| 8   | SQL Servers                 | Microsoft.Sql/servers                                             |
| 9   | SQL Databases               | Microsoft.Sql/servers/databases                                   |
| 10  | NAT Gateways                | Microsoft.Network/natGateways                                     |
| 11  | Network Security Groups     | Microsoft.Network/networkSecurityGroups                           |
| 12  | PostgreSQL Servers          | Microsoft.DBforPostgreSQL/servers                                 |
| 13  | PostgreSQL Flexible Servers | Microsoft.DBforPostgreSQL/flexibleServers                         |
| 14  | Public IP Addresses         | Microsoft.Network/publicIPAddresses                               |
| 15  | Snapshots                   | Microsoft.Compute/snapshots                                       |
| 16  | Storage Accounts            | Microsoft.Storage/storageAccounts                                 |
| 17  | Virtual Machines            | Microsoft.Compute/virtualMachines                                 |
| 18  | Virtual Networks            | Microsoft.Network/virtualNetworks                                 |
| 19  | VM ScaleSets                | Microsoft.Compute/virtualMachineScaleSets                         |
| 20  | Container Instances         | Microsoft.ContainerInstance/containerGroups                       |
| 21  | Web PubSub Service          | Microsoft.SignalRService/WebPubSub                                |
| 22  | Advisor                     | Microsoft.Advisor/advisorScore<br>Microsoft.ResourceHealth/events |
| 23  | Container Registries        | Microsoft.ContainerRegistry/registries                            |
| 24  | Functions                   | Microsoft.Web/sites                                               |
| 25 | Kubernetes Service | Microsoft.ContainerService/ManagedClusters |


---

## Authentication Overview

Registered service account on Cloudforet must have certain permissions to collect cloud service data
Please, set authentication privilege for followings:

### Custom roles for collecting Azure cloud resources

Cloudforet Azure collector requires several privileges for collecting resources. <br>
Please create custom roles in Azure portal, and assign following roles to Cloudforet Azure collector apps before collect
resources.
For information on creating custom roles in Azure, see
the [Microsoft custom role document](https://docs.microsoft.com/en-us/azure/role-based-access-control/custom-roles). <br>

```
{
    "properties": {
        "roleName": "cloudforet_azure_collector_role",
        "description": "custom role for cloudforet azure collector",
        "assignableScopes": [
            "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
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
                    "Microsoft.DocumentDB/databaseAccounts/listKeys/action",
                    "Microsoft.ContainerInstance/containerGroups/read",
                    "Microsoft.SignalRService/WebPubSub/read",
                    "Microsoft.SignalRService/WebPubSub/hubs/read",
                    "Microsoft.SignalRService/webPubSub/listKeys/action",
                    "Microsoft.Insights/Metrics/Read",
                    "Microsoft.Sql/servers/read",
                    "Microsoft.Sql/servers/administrators/read",
                    "Microsoft.Sql/servers/databases/read",
                    "Microsoft.Sql/servers/automaticTuning/read",
                    "Microsoft.Sql/servers/databases/automaticTuning/read",
                    "Microsoft.Sql/servers/databases/auditingSettings/read",
                    "Microsoft.Sql/servers/auditingSettings/read",
                    "Microsoft.Sql/servers/failoverGroups/read",
                    "Microsoft.Sql/servers/encryptionProtector/read",
                    "Microsoft.Sql/servers/elasticPools/read",
                    "Microsoft.Sql/servers/elasticPools/databases/read",
                    "Microsoft.Sql/servers/restorableDroppedDatabases/read",
                    "Microsoft.Sql/servers/firewallRules/read",
                    "Microsoft.Sql/servers/virtualNetworkRules/read",
                    "Microsoft.Sql/servers/databases/syncGroups/read",
                    "Microsoft.Sql/servers/syncAgents/read",
                    "Microsoft.Sql/servers/databases/dataMaskingPolicies/rules/read",
                    "Microsoft.Sql/servers/databases/replicationLinks/read",
                    "Microsoft.Sql/servers/replicationLinks/read"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": []
            }
        ]
    }
}
```

### Additional custom roles for Cloudforet collector

Some of cloud services require several additional IAM settings for collecting resources. <br>

#### [Key Vaults](https://learn.microsoft.com/en-us/python/api/azure-mgmt-keyvault/azure.mgmt.keyvault?view=azure-python)

- KeyVaults

For collecting Azure ```KeyVaults``` resources, you need to assign a Key Vault access policy to SpaceONE collector App
in Azure portal.

For information on assigning access policy,
see [Microsoft key vault access policy document - legacy](https://docs.microsoft.com/en-us/azure/key-vault/general/assign-access-policy?tabs=azure-portal).<br>
If your ```KeyVaults``` has Azure RBAC model
see [Microsoft key vault access policy document](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview?WT.mc_id=Portal-Microsoft_Azure_KeyVault)

#### [Cosmos DB](https://learn.microsoft.com/en-us/python/api/azure-mgmt-cosmosdb/azure.mgmt.cosmosdb?view=azure-python)

- Cosmos DB

For collecting key lists in ```CosmosDB``` azure resources, you need to assign an access policy to SpaceONE collector
App in Azure portal.
For information on creating custom roles in Azure, see
the [Microsoft custom role document](https://docs.microsoft.com/en-us/azure/role-based-access-control/custom-roles). <br>

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

- Virtual Machines

    - Scope
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.resources.resourcemanagementclient?view=azure-python#azure-mgmt-resource-resources-resourcemanagementclient-resource-groups
            - resource_groups
                - list()
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.computemanagementclient?view=azure-python#azure-mgmt-compute-computemanagementclient-virtual-machines
            - virtual_machines
                - list_all()
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.networkmanagementclient?view=azure-python#azure-mgmt-network-networkmanagementclient-virtual-networks
            - virtual_networks
                - list_all()
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.networkmanagementclient?view=azure-python#azure-mgmt-network-networkmanagementclient-public-ip-addresses
            - public_ip_addresses
                - list_all()
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.networkmanagementclient?view=azure-python#azure-mgmt-network-networkmanagementclient-network-interfaces
            - network_interfaces
                - list_all()
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.networkmanagementclient?view=azure-python#azure-mgmt-network-networkmanagementclient-network-security-groups
            - network_security_groups
                - list_all()

    - Permissions
        ```
        - Microsoft.Compute/*/read
        - Microsoft.Resources/*/read
        - Microsoft.Network/networkInterfaces/read	
        - Microsoft.Network/publicIPAddresses/read
        - Microsoft.Network/networkSecurityGroups/read
        - Microsoft.Network/loadBalancers/read
        ```

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

#### [Virtual Networks](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/virtual-networks/list-all)

- Virtual Networks
    - Scope
        - https://docs.microsoft.com/en-us/rest/api/virtualnetwork/virtual-networks/list-all

- Permissions
  ```
    "Microsoft.Network/dnsForwardingRulesets/virtualNetworkLinks/read",
    "Microsoft.Network/virtualNetworks/listDnsResolvers/action",
    "Microsoft.Network/virtualNetworks/listDnsForwardingRulesets/action"
    "Microsoft.Network/loadBalancers/virtualMachines/read",
    "Microsoft.Network/networkInterfaces/join/action",
    "Microsoft.Network/privateDnsZones/read",
    "Microsoft.Network/privateDnsZones/virtualNetworkLinks/read",
    "Microsoft.Network/locations/virtualNetworkAvailableEndpointServices/read",
    "Microsoft.Network/virtualNetworks/read",
    "Microsoft.Network/locations/supportedVirtualMachineSizes/read",
    "Microsoft.Network/virtualNetworks/bastionHosts/default/action",
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
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-sql/azure.mgmt.sql.sqlmanagementclient?view=azure-python
            - servers
                - list()
            - databases
                - list_by_server()
                - list_by_elastic_pool()
            - server_azure_ad_administrators
                - list_by_server()
            - server_automatic_tuning
                - get()
            - server_blob_auditing_policies
                - get()
            - failover_groups
                - list_by_server()
            - list_encryption_protectors
                - list_by_server()
            - elastic_pools
                - list_by_server()
            - restorable_dropped_databases
                - list_by_server()
            - firewall_rules
                - list_by_server()
            - virtual_network_rules
                - list_by_server()
            - sync_groups
                - list_by_server()
            - sync_agents
                - list_by_server()
            - data_masking_policies
                - list_by_database()
            - replication_links
                - list_by_database()

    - Permissions
    ```
    "Microsoft.Sql/servers/read",
    "Microsoft.Sql/servers/administrators/read",
    "Microsoft.Sql/servers/databases/read",
    "Microsoft.Sql/servers/automaticTuning/read",
    "Microsoft.Sql/servers/databases/automaticTuning/read",
    "Microsoft.Sql/servers/databases/auditingSettings/read",
    "Microsoft.Sql/servers/auditingSettings/read",
    "Microsoft.Sql/servers/failoverGroups/read",
    "Microsoft.Sql/servers/encryptionProtector/read",
    "Microsoft.Sql/servers/elasticPools/read",
    "Microsoft.Sql/servers/elasticPools/databases/read",
    "Microsoft.Sql/servers/restorableDroppedDatabases/read",
    "Microsoft.Sql/servers/firewallRules/read",
    "Microsoft.Sql/servers/virtualNetworkRules/read",
    "Microsoft.Sql/servers/databases/syncGroups/read",
    "Microsoft.Sql/servers/syncAgents/read",
    "Microsoft.Sql/servers/databases/dataMaskingPolicies/rules/read",
    "Microsoft.Sql/servers/databases/replicationLinks/read",
    "Microsoft.Sql/servers/replicationLinks/read"
    ```

#### [SQL Databases](https://learn.microsoft.com/en-us/python/api/azure-mgmt-sql/azure.mgmt.sql.operations.databasesoperations?view=azure-python)

- SQL Databases
    - Scope
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-sql/azure.mgmt.sql.sqlmanagementclient?view=azure-python
            - servers
                - list()
            - databases
                - list_by_server()
            - sync_groups
                - list_by_database()
            - sync_agents
                - list_by_server()
            - replication_links
                - list_by_server()
            - database_blob_auditing_policies
                - get()
    - Permissions
      ```
      "Microsoft.Sql/servers/read",
      "Microsoft.Sql/servers/syncAgents/read",
      "Microsoft.Sql/servers/replicationLinks/read",
      "Microsoft.Sql/servers/databases/replicationLinks/read",
      "Microsoft.Sql/servers/databases/read",
      "Microsoft.Sql/servers/databases/auditingSettings/read",
      "Microsoft.Sql/servers/databases/syncGroups/read"
      ```

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

#### [Network Security Groups](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/network-security-groups/list-all)

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
        - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-storage/azure.mgmt.storage.storagemanagementclient?view=azure-python
            - storage_accounts
                - list()
            - blob_containers
                - list()
        - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-monitor/azure.mgmt.monitor.monitormanagementclient?view=azure-python
            - metrics
                - list()
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
        "Microsoft.Storage/storageAccounts/encryptionScopes/read",
        "Microsoft.Insights/Metrics/Read"
      ```

####

~~[MySQL Servers](https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.mysql.mysqlmanagementclient?view=azure-python)~~ (
Deprecated)

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

    - ~~SpaceONE Inventory Collector only supports ``Single Servers`` type.~~
    - [
      ``Azure Database for MySQL Single Servers``  is on the retirement path.](https://learn.microsoft.com/ko-kr/azure/mysql/migrate/whats-happening-to-mysql-single-server)

#### [MySQL Flexible Servers](https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.mysql_flexibleservers.mysqlmanagementclient?view=azure-python)

- MySQL Flexible Servers
    - Scope
        - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.mysql_flexibleservers.operations.serversoperations?view=azure-python
            - servers
                - list()
        - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.mysql_flexibleservers.operations.firewallrulesoperations?view=azure-python
            - firewall_rules
                - list_by_server()
    - Permissions
        ```
        "Microsoft.DBforMySQL/flexibleServers/read",
        "Microsoft.DBforMySQL/flexibleServers/firewallRules/read"
        ```

####

~~[PostgreSQL Servers](https://docs.microsoft.com/en-us/rest/api/postgresql/flexibleserver(preview)/servers/list)~~ (
Deprecated)

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

    - ~~SpaceONE Inventory Collector only supports ``Single Servers`` type.~~
    - [
      ``Azure Database for PostgreSQL Single Servers`` is on the retirement path.](https://learn.microsoft.com/ko-kr/azure/postgresql/single-server/whats-happening-to-postgresql-single-server)

#### [PostgreSQL Flexible Servers](https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.postgresql_flexibleservers.postgresqlmanagementclient?view=azure-python)

- PostgreSQL Servers
    - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.postgresql_flexibleservers.operations.serversoperations?view=azure-python
        - servers
            - list()
    - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.postgresql_flexibleservers.operations.firewallrulesoperations?view=azure-python
        - firewall_rules
            - list_by_server()
    - Permissions
      ```
        "Microsoft.DBforPostgreSQL/flexibleServers/read",
        "Microsoft.DBforPostgreSQL/flexibleServers/firewallRules/read"
      ```

#### [Container Instances](https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-containerinstance/azure.mgmt.containerinstance.containerinstancemanagementclient?view=azure-python)

- Container Instances
    - Scope
        - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-containerinstance/azure.mgmt.containerinstance.containerinstancemanagementclient?view=azure-python
            - container_groups
                - list()
    - Permissions
      ```
        "Microsoft.ContainerInstance/containerGroups/read"
      ``` 
      
#### [Container Registries](https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-containerregistry/azure.mgmt.containerregistry.containerregistrymanagementclient?view=azure-python)

- Container Registries
    - Scope
        - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-containerregistry/azure.mgmt.containerregistry.containerregistrymanagementclient?view=azure-python
            - registries
                - list()
                - get()
                - list_usages()
            - webhooks
                - list()
            - replications
                - list()
            - tasks
                - list()
            - connected_registries
                - list()
            - cache_rules
                - list()
            - tokens
                - list()
            - scope_maps
                - list()
    - Permissions
      ```
        "Microsoft.ContainerRegistry/registries/read",
        "Microsoft.ContainerRegistry/registries/listUsages/read",
        "Microsoft.ContainerRegistry/registries/webhooks/read",
        "Microsoft.ContainerRegistry/registries/replications/read",
        "Microsoft.ContainerRegistry/registries/tasks/read",
        "Microsoft.ContainerRegistry/registries/connectedRegistries/read",
        "Microsoft.ContainerRegistry/registries/cacheRules/read",
        "Microsoft.ContainerRegistry/registries/tokens/read",
        "Microsoft.ContainerRegistry/registries/scopeMaps/read",
        "Microsoft.Resources/subscriptions/resourceGroups/read"
      ```

#### [Web PubSub Service](https://learn.microsoft.com/en-us/python/api/overview/azure/web-pubsub?view=azure-python)

- Web PubSub Service
    - Scope
        - https://github.com/Azure/azure-sdk-for-python/tree/azure-mgmt-webpubsub_1.1.0b1/sdk/webpubsub/azure-mgmt-webpubsub/azure/mgmt/webpubsub/operations
            - web_pub_sub
                - list_by_subscription()
                - list_keys()
            - web_pub_sub_hubs
                - list()
    - Permissions
      ```
      "Microsoft.SignalRService/WebPubSub/read",
      "Microsoft.SignalRService/WebPubSub/hubs/read",
      "Microsoft.SignalRService/webPubSub/listKeys/action"
      ```

#### [Advisor](https://learn.microsoft.com/en-us/python/api/overview/azure/advisor?view=azure-python)

- Advisor
    - Scope
        - https://learn.microsoft.com/en-us/python/api/azure-mgmt-advisor/azure.mgmt.advisor.advisormanagementclient?view=azure-python
            - recommendations
                - list()
    - Permissions

#### [Functions](https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-web/azure.mgmt.web.websitemanagementclient?view=azure-python)

- Functions
    - Scope
        - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-web/azure.mgmt.web.websitemanagementclient?view=azure-python
            - web_apps
                - list()
                - get()
                - list_private_endpoint_connections()
                - list_hybrid_connections()
            - app_service_plans
                - get()
        - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-network/azure.mgmt.network.networkmanagementclient?view=azure-python
            - virtual_networks
                - get()
            - subnets
                - get()
    - Permissions
      ```
        "Microsoft.Web/*/read",
        "Microsoft.Network/virtualNetworks/read",
        "Microsoft.Network/virtualNetworks/subnets/read",
        "Microsoft.Network/privateEndpoints/read",
        "Microsoft.Network/publicIPAddresses/read",
        "Microsoft.Network/natGateways/read",
        "Microsoft.Network/networkSecurityGroups/read",
        "Microsoft.Network/routeTables/read",
        "Microsoft.Resources/*/read"
      ```
      
#### [Kubernetes Service](https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-containerservice/azure.mgmt.containerservice.containerserviceclient?view=azure-python)

- Kubernetes Service (AKS)
  - Scope
    - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-containerservice/azure.mgmt.containerservice.containerserviceclient?view=azure-python
      - managed_clusters  
        - list()
        - get()
        
    - https://learn.microsoft.com/ko-kr/python/api/azure-mgmt-resource/azure.mgmt.resource.resources.resourcemanagementclient?view=azure-python
      - locks
        - list_at_resource_level()
  - Permissions
   ```
    "Microsoft.ContainerService/managedClusters/read"
    "Microsoft.ContainerService/managedClusters/listClusterUserCredential/action"
    "Microsoft.Authorization/locks/*/read"
    "Microsoft.Resources/subscriptions/resourceGroups/read"
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
        'ApplicationGateways',
        'CosmosDB',
        'Disks',
        'KeyVaults',
        'LoadBalancers',
        'MySQLServers',
        'SQLServers',
        'SQLDatabases',
        'NATGateways',
        'NetworkSecurityGroups,
        'PostgreSQLServers',
        'PublicIPAddresses',
        'Snapshots',
        'StorageAccounts',
        'VirtualMachines',
        'VirtualNetworks',
        'VMScaleSets',
        'ContainerInstances',
        'WebPubSubService',
        "ContainerRegistries",
        "Functions",
        "KubernetesService"
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

### Service Code Mapper : Convert service code in Cloud Service Type what you want.

If `service_code_mappers` is added in options, You can replace the service code specified in the cloud service type.
The service code set by default can be checked in the Service List item of this document.

The `service_code_mappers` items that can be specified are as follows.

<pre>
<code>
{
    "service_code_mappers": {
        "Microsoft.Compute/disks": "Azure Virtual Disk",
        "Microsoft.Storage/storageAccounts": "Azure Storage Account",
    }
}
</code>
</pre>

### Custom Asset URL : Update ASSET_URL in Cloud Service Type.

If `custom_asset_url` is in options, You can change it to an asset_url that users will use instead of the default
asset_url.  
The default ASSET_URL in cloud_service_conf is
`https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure`

<pre>
<code>
{
    "custom_asset_url": "https://xxxxx.cloudforet.dev/icon/azure"
}
</code>
</pre>

---

## Release Note

| Version | Description                                                                                                                                                                                                                                                                                                                                                               | Affected Service                                    | Release Date |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|--------------|
| 2.0.10  | - Add Kubernetes Service (AKS)                                                                                                      | Kubernetes Service (AKS) | 2025.12.09   |
| 2.0.9   | - Add Azure Functions, Container Registries                                                                                                      | Functions, Container Registries | 2025.12.03   |
| 2.0.8   | - Add Azure Advisor service                                                                                                                                                                                                                                                                                                                                               |                                                     |              |
| 2.0.5   | - Add Azure Cognitive service                                                                                                                                                                                                                                                                                                                                             |                                                     |              |
| 2.0.0   | - [Migration to spaceone framework 2.0](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/91)                                                                                                                                                                                                                                                          | All Services                                        | 2024.08.22   |
| 1.7.0   | - Add metric data query for all services                                                                                                                                                                                                                                                                                                                                  | All Services                                        | 2024.07.02   |
| 1.6.18  | - [Fix Data Size too big error when collecting `StorageAccounts`](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/57)                                                                                                                                                                                                                                | Storage Accounts                                    | 2023.09.26   |
| 1.6.15  | - [Fix `SQL Databases` error 'mappingproxy' object does not support item assignment](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/77)                                                                                                                                                                                                             | SQL Databases                                       | 2023.08.04   | 
| 1.6.14  | - [Fix `Application Gateways` error with assigned managed identity](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/73)                                                                                                                                                                                                                              | Application Gateways                                | 2023.08.01   |
| 1.6.13  | - [Fix `Application Gateways` None type error](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/67)                                                                                                                                                                                                                                                   | Application Gateways                                | 2023.07.13   |
| 1.6.12  | - [Fix `Virtual Networks` modeling error](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/64)<br/>- [Fix `Disks` modeling error](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/60)<br>- [Fix error occurs when collecting `SQL server` and database](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/41) | Virtual Networks, Disks, SQL Servers, SQL Databases | 2023.07.05   |
| 1.6.9   | - [Fix CosmosDB location info](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/53)<br/>- [Add all Azure location info](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/52)                                                                                                                                                      | CosmosDB                                            | 2023.06.30   |

### Ver 1.6.14

* [Fix
  `Application Gateways` error with assigned managed identity](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/73)

### Ver 1.6.13

* [Fix `Application Gateways` None type error](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/67)

### Ver 1.6.12

* [Fix `Virtual Networks` modeling error](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/64)
* [Fix `Disks` modeling error](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/60)
* [Fix error occurs when collecting
  `SQL server` and database](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/41)

### Ver 1.6.9

* [Fix CosmosDB location info](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/53)
* [Add all Azure location info](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/52)

### Ver 1.6.7

* [Size of storage service(ex.disk, snapshot) display error at console](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/49)

### Ver 1.6.4

* [Error 'list index out of range' occur when collecting StorageAccounts](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/45)

### Ver 1.6.3

* [Fix error when collecting virtual machine](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/40)

### Ver 1.6.1

* [Collect the total size in use of the Azure
  ```Storage Account``` ](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/33)

### Ver 1.6.0

* [Add ```Web PubSub Service``` cloud service](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/21)

### Ver 1.5.0

* [Add ```Container Instances``` cloud service](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/14)

### Ver 1.4.0

* [Merge Azure vm plugin to Azure inventory collector](https://github.com/cloudforet-io/plugin-azure-inven-collector/issues/2)
* Split SQL Servers to SQL Servers and SQL Databases
* [Update Azure sdk version](https://github.com/cloudforet-io/plugin-azure-inven-collector/pull/4)
* Fix Snapshot collecting issue
* Change cloud_service_name and cloud_service_group

### Ver 1.3.0

* [Add feature for monitoring metrics](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/190)

### Ver 1.2.15

* [Add feature to convert service_code to what you want using options](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/186)

### Ver 1.2.14

* [Add feature for Usage Overview of cloud services](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/174)

### Ver 1.2.13

* [Add feature to specify the Cloud Service Type and collect it.](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/162)
* [Add fields to cloud services model(account, instance_type, instance_size, launched_at)](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/159)
* [Add ErrorResources to collect error messages as resources](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/issues/157)

### Ver 1.2.12

* [Add
  ```PostgreSQL Servers```  cloud service](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/154)

### Ver 1.2.10

* [Add CosmosDB Syntax bug](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/152/commits)
* [Add
  ```CosmosDB``` cloud service](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/commit/c50693a222555611cb1fb27b2ce222543e1cf174)
* [Update CI workflow](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/142)

### Ver 1.2.8

* [Add
  ```MySQL Servers``` cloud service](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/136)

### Ver 1.2.7

* [Add
  ```Key Vaults``` cloud service](https://github.com/spaceone-dev/plugin-azure-cloud-service-inven-collector/pull/123)

### Ver 1.2.6

* Add ```Storage Accounts``` cloud service

### Ver 1.2.5

* Add ```NAT Gateways``` cloud service

### Ver 1.2.4

* Add ```Network Security Groups``` cloud service

### Ver 1.2.3

* Add ```Virtual Networks```, ```Application Gateways```, ```Public IP Address``` cloud service


