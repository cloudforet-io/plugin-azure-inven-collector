from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, NumberType


class Tags(Model):
    key = StringType()
    value = StringType()


class UltraSSDEnabled(Model):  # belongs to VmScaleSet
    ultra_ssd_enabled = BooleanType(serialize_when_none=False)


class AdditionalCapabilities(Model):
    ultra_ssd_enabled = BooleanType(serialize_when_none=False)


class AdditionalUnattendedContent(Model):  # belongs to VmScaleSet
    component_name = StringType(choices='Microsoft-Windows-Shell-Setup', serialize_when_none=False)
    content = StringType(serialize_when_none=False)
    pass_name = StringType(choices='OobeSystem', serialize_when_none=False)
    setting_name = StringType(choices=('AutoLogon', 'FirstLogonCommands'), serialize_when_none=False)


class ApiEntityReference(Model):  # belongs to VmScaleSet
    id = StringType(serialize_when_none=False)


class AutomaticOSUpgradePolicy(Model):  # belongs to VmScaleSet >> UpgradePolicy
    disable_automatic_rollback = BooleanType(default=False)
    enable_automatic_os_upgrade = BooleanType(default=False)


class AutomaticRepairsPolicy(Model):  # belongs to VmScaleSet
    enabled = BooleanType(default=False)
    grace_period = StringType(serialize_when_none=False)


class BillingProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    max_price = NumberType(serialize_when_none=False)


class BootDiagnostics(Model):
    # belongs to the VmScaleSet >> VirtualMachineScaleSetVMProfile >> DiagnosticsProfile
    enabled = BooleanType(serialize_when_none=False)
    storage_uri = StringType(serialize_when_none=False)


class DiagnosticsProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    boot_diagnostics = ModelType(BootDiagnostics, serialize_when_none=False)


class DiffDiskOptions(Model):  # belongs to VmScaleSet >> DiffDiskSettings
    local = StringType(serialize_when_none=False)


class DiffDiskSettings(Model):
    option = ModelType(DiffDiskOptions, serialize_when_none=False)
    placement = StringType(choices=('CacheDisk', 'ResourceDisk'), serialize_when_none=False)


class DiskEncryptionSetParameters(Model):
    id = StringType(serialize_when_none=False)


class ImageReference(Model):
    exact_version = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    offer = StringType(serialize_when_none=False)
    publisher = StringType(serialize_when_none=False)
    sku = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)


class SshPublicKey(Model):  # belongs to VmScaleSet >> LinuxConfiguration >> SshConfiguration
    key_data = StringType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)


class SshConfiguration(Model):  # belongs to VmScaleSet >> LinuxConfiguration
    public_keys = ListType(SshPublicKey, serialize_when_none=False)


class LinuxConfiguration(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetOSProfile
    disable_password_authentication = BooleanType(serialize_when_none=False)
    provision_vm_agent = BooleanType(serialize_when_none=False, default=True)
    ssh = ModelType(SshConfiguration, serialize_when_none=False)


class InGuestPatchMode(Model):  # belongs to  VmScaleSet >> PatchSettings
    in_guest_patch_mode = StringType(choices=('AutomaticByOS', 'Manual', 'AutomaticByPlatform'))


class PatchSettings(Model):  # belongs to  VmScaleSet
    patch_mode = ModelType(InGuestPatchMode, serialize_when_none=False)


class Plan(Model):  # belongs to VmScaleSet
    name = StringType(serialize_when_none=False)
    product = StringType(serialize_when_none=False)
    promotion_code = StringType(serialize_when_none=False)
    publisher = StringType(serialize_when_none=False)


class ResourceIdentityType(Model):
    resource_identity_type = StringType(choices=('None', 'SystemAssigned', 'SystemAssigned, UserAssigned',
                                                 'UserAssigned'), serialize_when_none=False)


class RollingUpgradePolicy(Model):  # belongs to VmScaleSet >> UpgradePolicy
    max_batch_instance_percent = IntType(default=20)
    max_unhealthy_instance_percent = IntType(default=20)
    max_unhealthy_upgraded_instance_percent = IntType(default=20)
    pause_time_between_batches = StringType(default='PT0S')


class ScaleInPolicy(Model):  # belongs to VmScaleSet
    rules = ListType(StringType, choices=('Default', 'OldestVM', 'NewestVM'), default='Default')


class TerminateNotificationProfile(Model):  # belongs to VmScaleSet >> ScheduledEventsProfile
    enable = BooleanType(serialize_when_none=False)
    not_before_timeout = StringType(default='PT5M')


class ScheduledEventsProfile(Model):  # belongs to VmScaleSet
    terminate_notification_profile = ModelType(TerminateNotificationProfile, serialize_when_none=False)


class SecurityProfile(Model):  # belongs to VmScaleSet
    encryption_at_host = BooleanType(default=False, serialize_when_none=False)


class Sku(Model):  # belongs to VmScaleSet
    capacity = IntType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    tier = StringType(choices=('Standard', 'Basic'), default='Standard')


class SubResource(Model):  # belongs to VmScaleSet
    id = StringType(serialize_when_none=False)


class UpgradePolicy(Model):  # belongs to VmScaleSet
    automatic_os_upgrade_policy = ModelType(AutomaticOSUpgradePolicy, serialize_when_none=False)
    mode = StringType(choices=('Manual', 'Automatic', 'Rolling'), serialize_when_none=False)
    rolling_upgrade_policy = ModelType(RollingUpgradePolicy, serialize_when_none=False)


class WinRMListener(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> WindowsConfiguration >> WinRMConfiguration
    certificate_url = StringType(serialize_when_none=False)
    protocol_types = StringType(choices=('Http', 'Https'), serialize_when_none=False)


class WinRMConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> WindowsConfiguration
    listeners = ListType(WinRMListener, serialize_when_none=False)


class WindowsConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    additional_unattended_content = ModelType(AdditionalUnattendedContent, serialize_when_none=False)
    enable_automatic_updates = BooleanType(serialize_when_none=False)
    patch_settings = ModelType(PatchSettings, serialize_when_none=False)
    provision_vm_agent = BooleanType(serialize_when_none=False)
    time_zone = StringType(serialize_when_none=False)
    win_rm = ModelType(WinRMConfiguration, serialize_when_none=False)


class VaultCertificate(Model):
    # belongs to VmScaleSet >> >> VirtualMachineScaleSetVMProfile >> VaultSecretGroup
    certificate_store = StringType(serialize_when_none=False)
    certificate_uri = StringType(serialize_when_none=False)


class VaultSecretGroup(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    source_vault = ModelType(SubResource, serialize_when_none=False)
    vault_certificates = ListType(VaultCertificate, serialize_when_none=False)


class VirtualMachineScaleSetManagedDiskParameters(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    # >> VirtualMachineScaleSetStorageProfile >> VirtualMachineScaleSetDataDisk
    disk_encryption_set_parameters = ModelType(DiskEncryptionSetParameters, serialize_when_none=False)


class VirtualMachineScaleSetDataDisk(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetStorageProfile
    name = StringType()
    caching = StringType(choices=('None', 'ReadOnly', 'ReadWrite'), serialize_when_none=False)
    create_option = StringType(choices=('Attach', 'Empty', 'FromImage'), default='Empty')
    disk_iops_read_write = IntType(serialize_when_none=False)
    disk_mbps_read_write = IntType(serialize_when_none=False)
    disk_size_gb = IntType(serialize_when_none=False)
    lun = IntType(serialize_when_none=False)
    managed_disk = ModelType(VirtualMachineScaleSetManagedDiskParameters, serialize_when_none=False)
    os_type = StringType(choices=('Linux', 'Windows'), serialize_when_none=False)
    vhd_containers = ListType(StringType, serialize_when_none=False)
    write_accelerator_enabled = BooleanType(serialize_when_none=False)


class VirtualMachineScaleSetExtension(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetExtensionProfile
    id = StringType()
    name = StringType()
    auto_upgrade_minor_version = BooleanType(serialize_when_none=False)
    enable_automatic_upgrade = BooleanType(serialize_when_none=False)
    force_update_tag = StringType(serialize_when_none=False)
    provisioned_after_extensions = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(serialize_when_none=False)
    publisher = StringType(serialize_when_none=False)
    settings = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    type_handler_version = StringType(serialize_when_none=False)


class VirtualMachineScaleSetExtensionProfile(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    extensions = ListType(VirtualMachineScaleSetExtension, serialize_when_none=False)
    extensions_time_budget = StringType(serialize_when_none=False)  # ISO 8601 format


class VirtualMachineScaleSetIdentity(Model):  # belongs to VmScaleSet
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    type = ModelType(ResourceIdentityType, serialize_when_none=False)
    user_assigned_identities = StringType(serialize_when_none=False)


class VirtualMachineScaleSetPublicIPAddressConfigurationDnsSettings(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetNetworkProfile >>
    #            VirtualMachineScaleSetNetworkConfiguration >> VirtualMachineScaleSetIPConfiguration >>
    #            VirtualMachineScaleSetPublicIPAddressConfiguration
    domain_name_label = StringType(serialize_when_none=False)


class VirtualMachineScaleSetIpTag(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetNetworkProfile >>
    #            VirtualMachineScaleSetNetworkConfiguration >> VirtualMachineScaleSetIPConfiguration >>
    #            VirtualMachineScaleSetPublicIPAddressConfiguration
    ip_tag_type = StringType(serialize_when_none=False)
    tag = StringType(serialize_when_none=False)


class VirtualMachineScaleSetPublicIPAddressConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    #                       >> VirtualMachineScaleSetNetworkProfile >> VirtualMachineScaleSetNetworkConfiguration
    #                       >> VirtualMachineScaleSetIPConfiguration
    name = StringType()
    dns_settings = ModelType(VirtualMachineScaleSetPublicIPAddressConfigurationDnsSettings, serialize_when_none=False)
    idle_timeout_in_minutes = IntType(serialize_when_none=False)
    ip_tags = ListType(VirtualMachineScaleSetIpTag, serialize_when_none=False)
    public_ip_address_version = StringType(choices=('IPv4', 'IPv6'), default='IPv4')
    public_ip_prefix = ModelType(SubResource, serialize_when_none=False)


class VirtualMachineScaleSetIPConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    #                       >> VirtualMachineScaleSetNetworkProfile >> VirtualMachineScaleSetNetworkConfiguration
    id = StringType()
    name = StringType()
    application_gateway_backend_address_pools = ListType(SubResource, serialize_when_none=False)
    load_balancer_backend_address_pools = ListType(SubResource, serialize_when_none=False)
    load_balancer_inbound_nat_pools = ListType(SubResource, serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), default='IPv4')
    public_ip_address_configuration = ModelType(VirtualMachineScaleSetPublicIPAddressConfiguration,
                                                serialize_when_none=False)
    subnet = ModelType(ApiEntityReference, serialize_when_none=False)


class VirtualMachineScaleSetNetworkConfigurationDNSSettings(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetNetworkProfile
    #            >> VirtualMachineScaleSetNetworkConfiguration
    dns_servers = ListType(StringType, serialize_when_none=False)


class VirtualMachineScaleSetNetworkConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetNetworkProfile
    id = StringType()
    name = StringType()
    dns_settings = ModelType(VirtualMachineScaleSetNetworkConfigurationDNSSettings, serialize_when_none=False)
    enable_accelerated_networking = BooleanType(serialize_when_none=False)
    enable_ip_forwarding = BooleanType(serialize_when_none=False)
    ip_configurations = ListType(VirtualMachineScaleSetIPConfiguration, serialize_when_none=False)
    network_security_group = ModelType(SubResource, serialize_when_none=False)


class VirtualMachineScaleSetNetworkProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    health_probe = ModelType(ApiEntityReference, serialize_when_none=False)
    network_interface_configurations = ListType(VirtualMachineScaleSetNetworkConfiguration, serialize_when_none=False)


class VirtualHardDisk(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetStorageProfile
    #            >> VirtualMachineScaleSetOSDisk
    uri = StringType(serialize_when_none=False)


class VirtualMachineScaleSetOSDisk(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetStorageProfile
    name = StringType()
    caching = StringType(choices=('None', 'ReadOnly', 'ReadWrite'), default='None')
    create_option = StringType(choices=('Attach', 'Empty', 'FromImage'), default='Empty')
    diff_disk_settings = ModelType(DiffDiskSettings, serialize_when_none=False)
    disk_size_gb = IntType(serialize_when_none=False)
    image = ModelType(VirtualHardDisk, serialize_when_none=False)
    managed_disk = ModelType(VirtualMachineScaleSetManagedDiskParameters, serialize_when_none=False)
    os_type = StringType(choices=('Linux', 'Windows'), serialize_when_none=False)
    vhd_containers = ListType(StringType, serialize_when_none=False)
    write_accelerator_enabled = BooleanType(serialize_when_none=False)


class VirtualMachineScaleSetStorageProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    data_disks = ListType(VirtualMachineScaleSetDataDisk, serialize_when_none=False)
    image_reference = ModelType(ImageReference, serialize_when_none=False)
    os_disk = ModelType(VirtualMachineScaleSetOSDisk, serialize_when_none=False)


class VirtualMachineScaleSetOSProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    admin_password = StringType()
    admin_username = StringType()
    computer_name_prefix = StringType()
    custom_data = StringType(serialize_when_none=False)
    linux_configuration = ModelType(LinuxConfiguration, serialize_when_none=False)
    secrets = ListType(VaultSecretGroup, serialize_when_none=False)
    windows_configuration = ModelType(WindowsConfiguration, serialize_when_none=False)


class VirtualMachineScaleSetVMProfile(Model):  # belongs to VmScaleSet
    billing_profile = ModelType(BillingProfile, serialize_when_none=False)
    diagnostics_profile = ModelType(DiagnosticsProfile, serialize_when_none=False)
    eviction_policy = StringType(choices=('Deallocate', 'Delete'), serialize_when_none=False)
    extension_profile = ModelType(VirtualMachineScaleSetExtensionProfile, serialize_when_none=False)
    license_type = StringType(choices=('Windows_Client', 'Windows_Server', 'RHEL_BYOS', 'SLES_BYOS'))
    os_profile = ModelType(VirtualMachineScaleSetOSProfile, serialize_when_none=False)
    network_profile = ModelType(VirtualMachineScaleSetNetworkProfile, serialize_when_none=False)
    priority = ModelType(choices=('Low', 'Regular', 'Spot'), serialize_when_none=False)
    scheduled_events_profile = ModelType(ScheduledEventsProfile, serialize_when_none=False)
    security_profile = ModelType(SecurityProfile, serialize_when_none=False)
    storage_profile = ModelType(VirtualMachineScaleSetStorageProfile, serialize_when_none=False)


'''
class Vms(Model):
    name = StringType()
'''

class VmScaleSet(Model):

    # vm_instances = ListType(ModelType(Vms))  # ##vm list
    id = StringType()
    subscription_id = StringType()
    subscription_name = StringType()
    identity = ModelType(VirtualMachineScaleSetIdentity, serialize_when_none=False)
    resource_group = StringType()
    location = StringType()
    name = StringType()
    plan = ModelType(Plan, serialize_when_none=False)
    additional_capabilities = ModelType(AdditionalCapabilities, serialize_when_none=False)
    automatic_repairs_policy = ModelType(AutomaticRepairsPolicy, serialize_when_none=False)
    do_not_run_extensions_on_overprovisioned_vms = BooleanType(serialize_when_none=False)
    host_group = ModelType(SubResource, serialize_when_none=False)
    over_provision = BooleanType(default=True)
    platform_fault_domain_count = IntType(default=5)
    provisioning_state = StringType(choices=('Failed', 'Succeeded'), serialize_when_none=False)
    proximity_placement_group = ModelType(SubResource, serialize_when_none=False)
    scale_in_policy = ModelType(ScaleInPolicy, serialize_when_none=False)
    single_placement_group = BooleanType(serialize_when_none=False)
    storage_account_types = StringType(choices=('Premium_LRS', 'StandardSSD_LRS', 'Standard_LRS', 'UltraSSD_LRS'),
                                       serialize_when_none=False)
    unique_id = StringType()
    upgrade_policy = ModelType(UpgradePolicy, serialize_when_none=False)
    virtual_machine_profile = ModelType(VirtualMachineScaleSetVMProfile)
    zone_balance = BooleanType(serialize_when_none=False)
    sku = ModelType(Sku, serialize_when_none=False)
    tags = ListType(ModelType(Tags), default=[])
    zones = ListType(StringType(), serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
