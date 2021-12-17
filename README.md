# plugin-azure-cloud-services

![Microsoft Azure Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-cloud-services.svg)
**Plugin to collect Microsoft Azure Cloud Services**


> SpaceONE's [plugin-azure-cloud-services](https://github.com/spaceone-dev/plugin-azure-cloud-services) is a convenient tool to 
get cloud service data from Azure Cloud Services. 


Find us also at [Dockerhub](https://hub.docker.com/r/spaceone/azure-cloud-services)
> Latest stable version : 1.2.12

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
        - Microsoft.Compute/virtualMachineScaleSets/*/read	
        

#### [Disks](https://docs.microsoft.com/en-ca/rest/api/compute/disks/list)
- Disks
    - Scope
        - https://docs.microsoft.com/en-ca/rest/api/compute/disks/list
    
    - Permissions
        - Microsoft.Storage/*/read


#### [Snapshots](https://docs.microsoft.com/en-us/rest/api/compute/snapshots/list)
- Snapshots
    - Scope
        - https://docs.microsoft.com/en-us/rest/api/compute/snapshots/list
    
    - Permissions
        - Microsoft.Compute/snapshots/*/read	

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
        - Microsoft.Network/loadBalancers/*/read
        - Microsoft.Network/virtualNetworks/subnets/*/read		

#### [Public IP Addresses](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/public-ip-addresses/list-all)
- Public IP Address
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/virtualnetwork/public-ip-addresses/list-all

    - Permissions
        - Microsoft.Network/publicIPAddresses/*/read


#### [NetworkSecurityGroups](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/network-security-groups/list-all)
- Network Security Group
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/virtualnetwork/network-security-groups/list-all

    - Permissions
        - Microsoft.Network/networkSecurityGroups/read
        - Microsoft.Network/virtualNetworks/subnets/*/read	
        - Microsoft.Network/networkInterfaces/read

#### [Application Gateways](https://docs.microsoft.com/en-us/rest/api/application-gateway/application-gateways/list-all)
- Application Gateways
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/application-gateway/application-gateways/list-all

    - Permissions
        - Microsoft.Network/applicationGateways/read
        - Microsoft.Network/publicIPAddresses/read

#### [NAT Gateways](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/nat-gateways/list-all)
- NAT Gateways
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/virtualnetwork/nat-gateways/list-all

    - Permissions
        - Microsoft.Network/natGateways/read
        - Microsoft.Network/virtualNetworks/subnets/*/read	
        - Microsoft.Network/publicIPAddresses/read
        - Microsoft.Network/publicIPPrefixes/read

#### [Storage Accounts](https://docs.microsoft.com/en-us/rest/api/storagerp/storage-accounts/list#blobrestorerange)
- Storage Accounts
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/storagerp/storage-accounts/list
    - Permissions
        - Microsoft.Storage/storageAccounts/read


#### [MySQL Servers]()
- MySQL Servers
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/storagerp/storage-accounts/list
    - Permissions
        - Microsoft.Storage/storageAccounts/read
    
    - SpaceONE Inventory Collector only supports ``Single Servers`` type. 

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


