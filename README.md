# plugin-azure-cloud-services

![Microsoft Azure Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-cloud-services.svg)
**Plugin to collect Microsoft Azure Cloud Services**


> SpaceONE's [plugin-azure-cloud-services](https://github.com/spaceone-dev/plugin-azure-cloud-services) is a convenient tool to 
get cloud service data from Azure Cloud Services. 


Find us also at [Dockerhub](https://hub.docker.com/r/spaceone/azure-cloud-services)
> Latest stable version : 1.2.3

Please contact us if you need any further information. 
<support@spaceone.dev>


## Contents

* Table of Contents
    * [Virtual Machines](#Azure_VM_(Instance))
    * [Virtual Machine Scale Sets](#Virtual_Machine_Scale_Sets)
    * [Disks](#disks)
    * [Snapshots](#Snapshots)
    * [Load Balancer](#Load_Balancer)
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


#### [Load Balancer](https://docs.microsoft.com/en-us/rest/api/load-balancer/loadbalancers/listall)
- Load Balancer
    - Scope 
        - https://docs.microsoft.com/en-us/rest/api/load-balancer/loadbalancers/listall
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/subnets/get

    - Permissions
        - Microsoft.Network/loadBalancers/*/read
        - Microsoft.Network/virtualNetworks/subnets/*/read		

            




