## Overview

<img src="./GUIDE-img/azure-account.png" width="80%" height="80%">

To register an Azure service account in Cloudforet, you need the four settings information below.

- **Subscription ID**
- **Tenant ID**
- **Client ID**
- **Client Secret**


>💡 Before starting the setup guide, please make sure **Subscription ID** has been created.

See the Azure Subscription Guides [Azure Documentation](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/initial-subscriptions)
 


<img src="./GUIDE-img/summary(h2)-1.png" width="60%" height="60%">


<img src="./GUIDE-img/summary(h2)-2.png" width="60%" height="60%">

This setup guide will take a closer look at what the above-mentioned information means and where to obtain it.

<br>

### Subscription ID

Azure manages costs and resources in units of objects called subscriptions.
The **unique identifier** that distinguishes this is **Subscription ID**.

See the Subscription [Azure Documentation](https://docs.microsoft.com/en-us/azure/developer/intro/azure-developer-billing#what-is-an-azure-subscription)

<br>

### Tenant ID

**Tenant ID** is a **unique identifier** for your organization provided by Azure Active Directory (AD) or Microsoft Extra ID.
Azure AD is a cloud-based identity and access management service that you use to manage users on an organizational basis.
See the Azure AD [Azure Documentation](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis)

<br>

### Client ID

**Client ID** is the Application ID issued when creating an Azure app.
You use Azure App to manage credentials and IAM users for your applications.
See the Azure App [Azure Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

<br>

### Client Secret

This is the **Client Secret** key that can be obtained through Azure App registration.
Required when using Azure's API and issuing tokens to access resources.

<br>

We briefly discussed the concept of setup information required when registering a Cloudforet Azure service account.
Now, let's learn more about **how to actually obtain configuration information** in the next lesson.

<br>

## Overall Flow

Cloudforet supports the **[azure_client_secret]** method through issuing authentication keys for integration with Azure.
The method using **[azure_client_secret]** requires the following setting information.

- **Subscription ID**
- **Tenant ID**
- **Client ID**
- **Client Secret**

To obtain the above information, please proceed with the settings in the following order.

1. [App Registration](#1 App Registration)
2. [Generate Authentication key](#2 Generate Authentication key)
3. [Create Resource Group](#3 Create Resource Group)
4. [Assign Role](#4 Assign Role)

<br>
<br>

## 1 App Registration

You can obtain **[Client ID]** settings information in Azure through app registration.
If there is already a registered app, it can be omitted.

(1) Log in to [Azure Portal](https://portal.azure.com/#home).

(1-1) Enter ‘app registrations’ in the search box and click [App registrations].

<img src="./GUIDE-img/create-application(h2)-1.png" width="80%" height="80%">

(1-2) Click the [New Registration] button.

<img src="./GUIDE-img/create-application(h2)-2.png" width="80%" height="80%">

(2) Enter application registration information.

(2-1) Click [Accounts in this organizational directory only].
You can click [Selection Guide] to select an account that can access the API that suits your organization's structure.

(2-2) Click the [Register] button.

<img src="./GUIDE-img/create-application(h2)-3.png" width="80%" height="80%">

(3) You can check **[Client ID]** and **[Tenant ID]** setting information in the [Basic Information] menu.

<img src="./GUIDE-img/create-application(h2)-4.png" width="80%" height="80%">

<br>
<br>

## 2 Generate authentication key

Authentication keys contain **credentials** information to access Azure resources.
You can obtain **[Client Secret]** setting information by creating an authentication key.

(1) Go to [Azure Portal](https://portal.azure.com/#home).
(1-1) Enter ‘app registration’ in the search box and click [app registration] in the service list.

<img src="./GUIDE-img/create-key(h2)-1.png" width="80%" height="80%">

(2) Click the application for which you want to create an authentication key.

<img src="./GUIDE-img/create-key(h2)-2.png" width="80%" height="80%">

(3) Click the [Certificate & Secret > Client Secret] tab and then click the [New Client Secret] button.

<img src="./GUIDE-img/create-key(h2)-3.png" width="80%" height="80%">

(3-1) Enter the description information and click the [Add] button.

<img src="./GUIDE-img/create-key(h2)-4.png" width="80%" height="80%">

(3-2) Since you cannot see the generated password value again when moving the page, **note** the encryption key information.
The information in the [Value] column corresponds to the **[Client Secret]** setting information.

<img src="./GUIDE-img/create-key(h2)-5.png" width="80%" height="80%">

<br>
<br>

## 3 Create Resource Group

A resource group is a group for managing resources being used in Azure.
You can have a 1:N relationship with your subscription.

> If you have already created a resource group, skip this step.

(1) Go to [Azure Portal](https://portal.azure.com/#home).
(1-1) Enter ‘resource group’ in the search box and click [Resource Group] in the service list.

<img src="./GUIDE-img/create-resource-group(h2)-1.png" width="80%" height="80%">

(2) Click the [Create] button.

<img src="./GUIDE-img/create-resource-group(h2)-2.png" width="80%" height="80%">

(3) After entering the project information, click the [Review + Create] button.
(3-1) Then click the [Create] button.

<img src="./GUIDE-img/create-resource-group(h2)-3.png" width="80%" height="80%">

<br>
<br>

## 4 Assign Role

[Role](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-definitions) is a collection of access permissions to Azure resources.
The Azure plugin requires a role setup with appropriate permissions to collect resource information.

The collector plugin does not require any permissions other than read permission.
The permission information required for each plugin is as follows.

| Plugin                                   | URL |
|------------------------------------------| --- |
| Microsoft Azure Cloud Service Collector  | https://github.com/cloudforet-io/plugin-azure-inven-collector#authentication-overview |

The process of granting permission in Azure for the plugin to collect resources is as follows:

1. Assign roles to subscriptions
2. Grant roles to resource groups

(1) This is the process of assigning roles to subscriptions.

(1-1) Go to [Azure Portal](https://portal.azure.com/#home).

(1-2) Enter ‘Subscription’ in the search box and click [Subscription] in the service list.

<img src="./GUIDE-img/create-role(h2)-1.png" width="80%" height="80%">

(1-3) Click the subscription you want to grant a role to.

<img src="./GUIDE-img/create-role(h2)-2.png" width="80%" height="80%">

(1-4) Click the [Access Control (IAM) > Add > Add Role Assignment] button.

<img src="./GUIDE-img/create-role(h2)-3.png" width="80%" height="80%">

(1-5) Click the [Reader] role and then click the [Next] button.

<img src="./GUIDE-img/create-role(h2)-4.png" width="80%" height="80%">

(1-6) Click the [Select Member] button to select an application as a member.

(1-7) After adding members, click the [Select] button.
Click the Review + Assign button when it becomes active.

<img src="./GUIDE-img/create-role(h2)-5.png" width="80%" height="80%">

>💡 Please select the application with the corresponding role.

<img src="./GUIDE-img/create-role(h2)-5-1.png" width="80%" height="80%">
<br>

(2) This is the process of assigning roles to resource groups.

If you only want to collect resources from a specific resource group that belongs to your subscription, you must grant a role to that resource group.
If you have assigned a role to your subscription, you can skip this step.

(2-1) Log in to [Azure Portal](https://portal.azure.com/#home).

(2-2) Enter ‘resource group’ in the search box and click [Resource Group] in the service list.

<img src="./GUIDE-img/create-role(h2)-6.png" width="80%" height="80%">

(2-3) Click the resource group you want to grant permission to.
<img src="./GUIDE-img/create-role(h2)-7.png" width="80%" height="80%">

(2-4) Click the [Access Control (IAM) > Add > Add Role Assignment] button to start setting access permissions.

<img src="./GUIDE-img/create-role(h2)-8.png" width="80%" height="80%">

(2-5) Select the [Reader] permission and click the [Next] button.

<img src="./GUIDE-img/create-role(h2)-9.png" width="80%" height="80%">

(2-6) Select [User, Group, Service Principal] and then click [Select Members].

(2-7) Check [Selected members] and click the [Select] button.

The [Review + Assignment] button becomes activated and click it.

<img src="./GUIDE-img/create-role(h2)-10.png" width="80%" height="80%">

> 💡 Selected members must have access to the selected resource group.


<img src="./GUIDE-img/create-role(h2)-10-1.png" width="80%" height="80%">
<br>
<br>
