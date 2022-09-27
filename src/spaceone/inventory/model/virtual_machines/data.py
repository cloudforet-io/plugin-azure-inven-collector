from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, BooleanType, IntType
from spaceone.inventory.libs.schema.resource import AzureCloudService, AzureTags
from spaceone.inventory.libs.schema.region import RegionResource


# Activity Log
class ActivityLog(Model):
    resource_uri = StringType()


# Azure
class Azure(Model):
    ultra_ssd_enabled = BooleanType(default=False)
    write_accelerator_enabled = BooleanType(default=False)
    boot_diagnostics = BooleanType(default=True)
    priority = StringType(choices=('Regular', 'Low', 'Spot'), default='Regular')
    tags = ListType(ModelType(AzureTags))


# Compute
class SecurityGroups(Model):
    display = StringType()
    id = StringType()
    name = StringType()


class ComputeTags(Model):
    vm_id = StringType()


class Compute(Model):
    keypair = StringType()
    az = StringType()
    instance_state = StringType(choices=('STARTING', 'RUNNING', 'STOPPING', 'STOPPED', 'DEALLOCATING', 'DEALLOCATED'))
    instance_type = StringType()
    launched_at = DateTimeType()
    instance_id = StringType(default='')
    instance_name = StringType(default='')
    security_groups = ListType(ModelType(SecurityGroups))
    image = StringType()
    account = StringType(default='')
    tags = ModelType(ComputeTags, default={})


# Disk
class DiskTags(Model):
    disk_name = StringType()
    caching = StringType(choices=('None', 'ReadOnly', 'ReadWrite'))
    storage_account_type = StringType(choices=('Standard_LRS', 'Premium_LRS', 'StandardSSD_LRS', 'UltraSSD_LRS'))
    disk_encryption_set = StringType(choices=('PMK', 'CMK'), default='PMK')
    iops = IntType()
    throughput_mbps = IntType()
    disk_id = StringType()


class Disk(Model):
    device_index = IntType()
    device = StringType(default='')
    disk_type = StringType(choices=('os_disk', 'data_disk'))
    size = FloatType()
    tags = ModelType(DiskTags, default={})


# Hardware
class Hardware(Model):
    core = IntType(default=0)
    memory = FloatType(default=0.0)


# Load Balancer
class LoadBalancerTags(Model):
    lb_id = StringType()


class LoadBalancer(Model):
    type = StringType(choices=('application', 'network'))
    endpoint = StringType()
    port = ListType(IntType())
    name = StringType()
    protocol = ListType(StringType())
    scheme = StringType(choices=('internet-facing', 'internal'))
    tags = ModelType(LoadBalancerTags, default={})


# Nic
class NICTags(Model):
    name = StringType()
    etag = StringType()
    enable_accelerated_networking = BooleanType(default=False)
    enable_ip_forwarding = BooleanType(default=False)


class NIC(Model):
    device_index = IntType()
    device = StringType(default="")
    nic_type = StringType(default="")
    ip_addresses = ListType(StringType(), default=[])
    cidr = StringType()
    mac_address = StringType(default="")
    public_ip_address = StringType()
    tags = ModelType(NICTags, default={})


# OS
class OS(Model):
    os_distro = StringType()
    os_arch = StringType(default='x86_64')
    details = StringType()
    os_type = StringType(choices=('LINUX', 'WINDOWS'))


# Resource Group
class ResourceGroup(Model):
    resource_group_name = StringType()
    resource_group_id = StringType()


# Security Group
class SecurityGroup(Model):
    protocol = StringType()
    remote = StringType()
    remote_cidr = StringType(serialize_when_none=False)
    remote_id = StringType(serialize_when_none=False)
    security_group_name = StringType()
    security_group_id = StringType()
    description = StringType(default="")
    direction = StringType(choices=("inbound", "outbound"))
    port_range_min = IntType(serialize_when_none=False)
    port_range_max = IntType(serialize_when_none=False)
    port = StringType(serialize_when_none=False)
    priority = IntType(serialize_when_none=False)
    action = StringType(choices=("allow", "deny"))


# Subnet
class Subnet(Model):
    subnet_name = StringType()
    subnet_id = StringType()
    cidr = StringType()


# Subscription
class Subscription(Model):
    subscription_id = StringType()
    subscription_name = StringType()
    tenant_id = StringType()
    tenant_name = StringType(serialize_when_none=False)
    domain = StringType(serialize_when_none=False)


# VMSS
class VMSS(Model):
    scale_set_name = StringType()
    capacity = IntType()
    admin_username = StringType()
    unique_id = StringType()


# VNet
class VNet(Model):
    vnet_id = StringType()
    vnet_name = StringType()
    cidr = StringType()


class VirtualMachine(AzureCloudService):  # Main Class
    os = ModelType(OS)
    azure = ModelType(Azure)
    hardware = ModelType(Hardware)
    security_group = ListType(ModelType(SecurityGroup))
    compute = ModelType(Compute)
    load_balancer = ListType(ModelType(LoadBalancer))
    vnet = ModelType(VNet)
    subnet = ModelType(Subnet)
    vmss = ModelType(VMSS, serialize_when_none=False)
    activity_log = ModelType(ActivityLog, serialize_when_none=False)
    primary_ip_address = StringType(default='')
    disks = ListType(ModelType(Disk))
    nics = ListType(ModelType(NIC))
    subscription = ModelType(Subscription)
    resource_group = ModelType(ResourceGroup)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
