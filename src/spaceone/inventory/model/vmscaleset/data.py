from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, NumberType


class Tags(Model):
    key = StringType()
    value = StringType()


class AdditionalCapabilities(Model):  # belongs to VmScaleSet
    ultra_ssd_enabled = BooleanType(serialize_when_none=False)


class AutomaticOSUpgradePolicy(Model):  # belongs to VmScaleSet >> UpgradePolicy
    disable_automatic_rollback = BooleanType(default=False, serialize_when_none=False)
    enable_automatic_os_upgrade = BooleanType(default=False, serialize_when_none=False)
    enable_automatic_os_upgrade_display = StringType(serialize_when_none=False)


class AutomaticRepairsPolicy(Model):  # belongs to VmScaleSet
    enabled = BooleanType(default=False)
    grace_period = StringType(serialize_when_none=False)


class ApiEntityReference(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    id = StringType(serialize_when_none=False)


class BillingProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    max_price = NumberType(serialize_when_none=False)


class BootDiagnostics(Model):
    # belongs to the VmScaleSet >> VirtualMachineScaleSetVMProfile >> DiagnosticsProfile
    enabled = BooleanType(serialize_when_none=False)
    storage_uri = StringType(serialize_when_none=False)


class DiffDiskOptions(Model):  # belongs to VmScaleSet >> DiffDiskSettings
    local = StringType(serialize_when_none=False)


class DiffDiskSettings(Model):
    option = ModelType(DiffDiskOptions, serialize_when_none=False)
    placement = StringType(choices=('CacheDisk', 'ResourceDisk'), serialize_when_none=False)


class DiagnosticsProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    boot_diagnostics = ModelType(BootDiagnostics, serialize_when_none=False)


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
    public_keys = ListType(ModelType(SshPublicKey), serialize_when_none=False)


class LinuxConfiguration(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetOSProfile
    disable_password_authentication = BooleanType(serialize_when_none=False)
    provision_vm_agent = BooleanType(serialize_when_none=False, default=True)
    ssh = ModelType(SshConfiguration, serialize_when_none=False)


class Plan(Model):  # belongs to VmScaleSet
    name = StringType(serialize_when_none=False)
    product = StringType(serialize_when_none=False)
    promotion_code = StringType(serialize_when_none=False)
    publisher = StringType(serialize_when_none=False)


class RollingUpgradePolicy(Model):  # belongs to VmScaleSet >> UpgradePolicy
    max_batch_instance_percent = IntType(default=20, serialize_when_none=False)
    max_unhealthy_instance_percent = IntType(default=20, serialize_when_none=False)
    max_unhealthy_upgraded_instance_percent = IntType(default=20, serialize_when_none=False)
    pause_time_between_batches = StringType(default='PT0S', serialize_when_none=False)


class ScaleInPolicy(Model):  # belongs to VmScaleSet
    rules = ListType(StringType, serialize_when_none=False)


class TerminateNotificationProfile(Model):  # belongs to VmScaleSet >> ScheduledEventsProfile
    enable = BooleanType(serialize_when_none=False)
    not_before_timeout = StringType(default='PT5M', serialize_when_none=False)


class ScheduledEventsProfile(Model):  # belongs to VmScaleSet
    terminate_notification_profile = ModelType(TerminateNotificationProfile, serialize_when_none=False)


class SecurityProfile(Model):  # belongs to VmScaleSet
    encryption_at_host = BooleanType(default=False, serialize_when_none=False)


class Sku(Model):  # belongs to VmScaleSet
    capacity = IntType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    tier = StringType(choices=('Standard', 'Basic', '', None), default='Standard', serialize_when_none=False)


class SubResource(Model):  # belongs to VmScaleSet
    id = StringType(serialize_when_none=False)


class InGuestPatchMode(Model):  # belongs to  VmScaleSet >> PatchSettings
    in_guest_patch_mode = StringType(choices=('AutomaticByOS', 'Manual', 'AutomaticByPlatform', '', None), serialize_when_none=False)


class PatchSettings(Model):  # belongs to  VmScaleSet
    patch_mode = ModelType(InGuestPatchMode, serialize_when_none=False)


class AdditionalUnattendedContent(Model):  # belongs to VmScaleSet
    component_name = StringType(choices=('Microsoft-Windows-Shell-Setup', ''), serialize_when_none=False)
    content = StringType(serialize_when_none=False)
    pass_name = StringType(choices=('OobeSystem', '', None), serialize_when_none=False)
    setting_name = StringType(choices=('AutoLogon', 'FirstLogonCommands', '', None), serialize_when_none=False)


class WinRMListener(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> WindowsConfiguration >> WinRMConfiguration
    certificate_url = StringType(serialize_when_none=False)
    protocol_types = StringType(choices=('http', 'https'), serialize_when_none=False)


class WinRMConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> WindowsConfiguration
    listeners = ListType(ModelType(WinRMListener), serialize_when_none=False)


class WindowsConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    additional_unattended_content = ListType(ModelType(AdditionalUnattendedContent), serialize_when_none=False)
    enable_automatic_updates = BooleanType(serialize_when_none=False)
    patch_settings = ModelType(PatchSettings, serialize_when_none=False)
    provision_vm_agent = BooleanType(serialize_when_none=False)
    time_zone = StringType(serialize_when_none=False)
    win_rm = ModelType(WinRMConfiguration, serialize_when_none=False)


class UpgradePolicy(Model):  # belongs to VmScaleSet
    automatic_os_upgrade_policy = ModelType(AutomaticOSUpgradePolicy, serialize_when_none=False)
    mode = StringType(choices=('Manual', 'Automatic', 'Rolling', None, ''), serialize_when_none=False)
    rolling_upgrade_policy = ModelType(RollingUpgradePolicy, serialize_when_none=False)


class VirtualMachineScaleSetIdentity(Model):  # belongs to VmScaleSet
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    type = StringType(choices=('None', 'SystemAssigned', ' SystemAssigned,UserAssigned', 'UserAssigned', '', None),
                      serialize_when_none=False)


class VirtualMachineScaleSetExtension(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetExtensionProfile
    id = StringType()
    name = StringType()
    auto_upgrade_minor_version = BooleanType(serialize_when_none=False)
    enable_automatic_upgrade = BooleanType(serialize_when_none=False)
    force_update_tag = StringType(serialize_when_none=False)
    protected_settings = StringType(serialize_when_none=False)
    provisioned_after_extensions = ListType(StringType, serialize_when_none=False)
    provisioning_state = StringType(serialize_when_none=False)
    publisher = StringType(serialize_when_none=False)
    settings = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    type_handler_version = StringType(serialize_when_none=False)


class VirtualMachineScaleSetExtensionProfile(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    extensions = ListType(ModelType(VirtualMachineScaleSetExtension), serialize_when_none=False)
    extensions_time_budget = StringType(serialize_when_none=False)  # ISO 8601 format


class VirtualMachineScaleSetNetworkConfigurationDNSSettings(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetNetworkProfile
    #            >> VirtualMachineScaleSetNetworkConfiguration
    dns_servers = ListType(StringType, serialize_when_none=False)


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
    ip_tags = ListType(ModelType(VirtualMachineScaleSetIpTag), serialize_when_none=False)
    public_ip_address_version = StringType(choices=('IPv4', 'IPv6'), default='IPv4', serialize_when_none=False)
    public_ip_prefix = ModelType(SubResource, serialize_when_none=False)


class VirtualMachineScaleSetIPConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    #                       >> VirtualMachineScaleSetNetworkProfile >> VirtualMachineScaleSetNetworkConfiguration
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    application_gateway_backend_address_pools = ListType(ModelType(SubResource), serialize_when_none=False)
    application_security_groups = ListType(ModelType(SubResource), serialize_when_none=False)
    load_balancer_backend_address_pools = ListType(ModelType(SubResource), serialize_when_none=False)
    load_balancer_inbound_nat_pools = ListType(ModelType(SubResource), serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)
    private_ip_address_version = StringType(choices=('IPv4', 'IPv6'), default='IPv4', serialize_when_none=False)
    public_ip_address_configuration = ModelType(VirtualMachineScaleSetPublicIPAddressConfiguration,
                                                serialize_when_none=False)
    subnet = ModelType(ApiEntityReference, serialize_when_none=False)


class VirtualMachineScaleSetNetworkConfiguration(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetNetworkProfile
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    dns_settings = ModelType(VirtualMachineScaleSetNetworkConfigurationDNSSettings, serialize_when_none=False)
    enable_accelerated_networking = BooleanType(serialize_when_none=False)
    enable_ip_forwarding = BooleanType(serialize_when_none=False)
    ip_configurations = ListType(ModelType(VirtualMachineScaleSetIPConfiguration), serialize_when_none=False)
    network_security_group = ModelType(SubResource, serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)


class VaultCertificate(Model):
    # belongs to VmScaleSet >> >> VirtualMachineScaleSetVMProfile >> VaultSecretGroup
    certificate_store = StringType(serialize_when_none=False)
    certificate_uri = StringType(serialize_when_none=False)


class VaultSecretGroup(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    source_vault = ModelType(SubResource, serialize_when_none=False)
    vault_certificates = ListType(ModelType(VaultCertificate), serialize_when_none=False)


class VirtualMachineScaleSetNetworkProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    health_probe = ModelType(ApiEntityReference, serialize_when_none=False)
    network_interface_configurations = ListType(ModelType(VirtualMachineScaleSetNetworkConfiguration),
                                                serialize_when_none=False)


class VirtualMachineScaleSetOSProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    admin_username = StringType(serialize_when_none=False)
    admin_password = StringType(serialize_when_none=False)
    computer_name_prefix = StringType(serialize_when_none=False)
    custom_data = StringType(serialize_when_none=False, default='')
    linux_configuration = ModelType(LinuxConfiguration, serialize_when_none=False)
    secrets = ListType(ModelType(VaultSecretGroup), serialize_when_none=False)
    windows_configuration = ModelType(WindowsConfiguration, serialize_when_none=False)


class DiskEncryptionSetParameters(Model):
    id = StringType(serialize_when_none=False)


class VirtualMachineScaleSetManagedDiskParameters(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    # >> VirtualMachineScaleSetStorageProfile >> VirtualMachineScaleSetDataDisk
    disk_encryption_set = ModelType(DiskEncryptionSetParameters, serialize_when_none=False)
    storage_account_type = StringType(serialize_when_none=False)


class VirtualMachineScaleSetDataDisk(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetStorageProfile
    name = StringType(serialize_when_none=False)
    caching = StringType(choices=('None', 'ReadOnly', 'ReadWrite', '', None), serialize_when_none=False)
    create_option = StringType(choices=('Attach', 'Empty', 'FromImage', None, ''), default='Empty', serialize_when_none=False)
    disk_iops_read_write = IntType(serialize_when_none=False)
    disk_m_bps_read_write = IntType(serialize_when_none=False)
    disk_size_gb = IntType(serialize_when_none=False)
    lun = IntType(serialize_when_none=False)
    managed_disk = ModelType(VirtualMachineScaleSetManagedDiskParameters, serialize_when_none=False)
    write_accelerator_enabled = BooleanType(serialize_when_none=False)


class VirtualHardDisk(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetStorageProfile
    #            >> VirtualMachineScaleSetOSDisk
    uri = StringType(serialize_when_none=False)


class VirtualMachineScaleSetOSDisk(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile >> VirtualMachineScaleSetStorageProfile
    name = StringType()
    caching = StringType(choices=('None', 'ReadOnly', 'ReadWrite'), default='None', serialize_when_none=False)
    create_option = StringType(choices=('Attach', 'Empty', 'FromImage'), default='Empty', serialize_when_none=False)
    diff_disk_settings = ModelType(DiffDiskSettings, serialize_when_none=False)
    disk_size_gb = IntType(serialize_when_none=False)
    image = ModelType(VirtualHardDisk, serialize_when_none=False)
    managed_disk = ModelType(VirtualMachineScaleSetManagedDiskParameters, serialize_when_none=False)
    os_type = StringType(choices=('Linux', 'Windows'), serialize_when_none=False)
    vhd_containers = ListType(StringType, serialize_when_none=False)
    write_accelerator_enabled = BooleanType(serialize_when_none=False)


class VirtualMachineScaleSetStorageProfile(Model):  # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    data_disks = ListType(ModelType(VirtualMachineScaleSetDataDisk), serialize_when_none=False)
    image_reference = ModelType(ImageReference, serialize_when_none=False)
    os_disk = ModelType(VirtualMachineScaleSetOSDisk, serialize_when_none=False)


class VirtualMachineScaleSetVMProfile(Model):  # belongs to VmScaleSet
    billing_profile = ModelType(BillingProfile, serialize_when_none=False)
    diagnostics_profile = ModelType(DiagnosticsProfile, serialize_when_none=False)
    eviction_policy = StringType(choices=('Deallocate', 'Delete', '', None), serialize_when_none=False)
    extension_profile = ModelType(VirtualMachineScaleSetExtensionProfile, serialize_when_none=False)
    license_type = StringType(choices=('Windows_Client', 'Windows_Server', 'RHEL_BYOS', 'SLES_BYOS', '', None), serialize_when_none=False)
    network_profile = ModelType(VirtualMachineScaleSetNetworkProfile, serialize_when_none=False)
    os_profile = ModelType(VirtualMachineScaleSetOSProfile, serialize_when_none=False)
    priority = StringType(choices=('Low', 'Regular', 'Spot', '', None), serialize_when_none=False)
    scheduled_events_profile = ModelType(ScheduledEventsProfile, serialize_when_none=False)
    security_profile = ModelType(SecurityProfile, serialize_when_none=False)
    storage_profile = ModelType(VirtualMachineScaleSetStorageProfile, serialize_when_none=False)


###### vm instances class

class InstanceViewStatus(Model):
    code = StringType(serialize_when_none=False)
    display_status = StringType(serialize_when_none=False)
    level = StringType(choices = ('Error', 'Info', 'Warning'), serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    time = StringType(serialize_when_none=False)


class VirtualMachineExtensionInstanceView(Model):
    name = StringType(serialize_when_none=False)
    statuses = ListType(ModelType(InstanceViewStatus))
    substatuses = ListType(ModelType(InstanceViewStatus))
    type = StringType(serialize_when_none=False)
    type_handler_version = StringType(serialize_when_none=False)


class VirtualMachineExtension(Model):
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    auto_upgrade_minor_version = BooleanType(serialize_when_none=False)
    enable_automatic_upgrade = BooleanType(serialize_when_none=False)
    force_update_tag = StringType(serialize_when_none=False)
    instance_view = ModelType(VirtualMachineExtensionInstanceView)
    protected_settings = StringType(serialize_when_none=False)
    provisioning_state = StringType(serialize_when_none=False)
    publisher = StringType(serialize_when_none=False)
    settings = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    type_handler_version = StringType(serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)


class KeyVaultSecretReference(Model):
    secret_url = StringType(serialize_when_none=False)
    source_vault = ModelType(SubResource, serialize_when_none=False)


class KeyVaultKeyReference(Model):
    key_url = StringType(serialize_when_none=False)
    source_vault = ModelType(SubResource, serialize_when_none=False)


class DiskEncryptionSettings(Model):
    disk_encryption_key = ModelType(KeyVaultSecretReference, serialize_when_none=False)
    enabled = BooleanType(serialize_when_none=False)
    key_encryption_key = ModelType(KeyVaultKeyReference, serialize_when_none=False)


class ManagedDiskParameters(Model):
    # belongs to VmScaleSet >> VirtualMachineScaleSetVMProfile
    # >> VirtualMachineScaleSetStorageProfile >> VirtualMachineScaleSetDataDisk
    disk_encryption_set = ModelType(DiskEncryptionSetParameters, serialize_when_none=False)
    storage_account_type = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)


class OSDisk(Model):
    name = StringType(serialize_when_none=False)
    caching = StringType(choices=('None', 'ReadOnly', 'ReadWrite'), default='None', serialize_when_none=False)
    create_option = StringType(choices=('Attach', 'Empty', 'FromImage'), default='Empty', serialize_when_none=False)
    diff_disk_settings = ModelType(DiffDiskSettings, serialize_when_none=False)
    disk_size_gb = IntType(serialize_when_none=False)
    encryption_settings = ModelType(DiskEncryptionSettings, serialize_when_none=False)
    image = ModelType(VirtualHardDisk, serialize_when_none=False)
    managed_disk = ModelType(ManagedDiskParameters, serialize_when_none=False)
    os_type = StringType(choices=('Linux', 'Windows'), serialize_when_none=False)
    vhd = ModelType(VirtualHardDisk, serialize_when_none=False)
    write_accelerator_enabled = BooleanType(serialize_when_none=False)


class DataDisk(Model):
    caching = StringType(choices=('None', 'ReadOnly', 'ReadWrite', '', None), serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    create_option = StringType(choices=('Attach', 'Empty', 'FromImage', None, ''), default='Empty',
                               serialize_when_none=False)
    disk_iops_read_write = IntType(serialize_when_none=False)
    disk_m_bps_read_write = IntType(serialize_when_none=False)
    disk_size_gb = IntType(serialize_when_none=False)
    lun = IntType(serialize_when_none=False)
    managed_disk = ModelType(ManagedDiskParameters, serialize_when_none=False)
    write_accelerator_enabled = BooleanType(serialize_when_none=False)
    image = ModelType(VirtualHardDisk, serialize_when_none=False)
    to_be_detached = BooleanType(serialize_when_none=False)
    vhd = ModelType(VirtualHardDisk, serialize_when_none=False)


class StorageProfile(Model):
    data_disks = ListType(ModelType(DataDisk), serialize_when_none=False)
    image_reference = ModelType(ImageReference, serialize_when_none=False)
    os_disk = ModelType(OSDisk, serialize_when_none=False)


class VirtualMachineScaleSetVMProtectionPolicy(Model):
    protect_from_scale_in = BooleanType(serialize_when_none=False)
    protect_from_scale_set_actions = BooleanType(serialize_when_none=False)


class OSProfile(Model):  # belongs to VirtualMachineScaleSetVM
    admin_username = StringType(serialize_when_none=False)
    admin_password = StringType(serialize_when_none=False)
    allow_extension_operations = BooleanType(serialize_when_none=False)
    computer_name = StringType(serialize_when_none=False)
    custom_data = StringType(serialize_when_none=False)
    linux_configuration = ModelType(LinuxConfiguration, serialize_when_none=False)
    windows_configuration = ModelType(WindowsConfiguration, serialize_when_none=False)
    require_guest_provision_signal = BooleanType(serialize_when_none=False)
    secrets = ListType(ModelType(VaultSecretGroup), serialize_when_none=False)


class HardwareProfile(Model):  # belongs to VMScaleSet >> vm instances
    vm_size = StringType(serialize_when_none=False)


class NetworkInterfaceReference(Model):
    id = StringType(serialize_when_none=False)
    primary = BooleanType(serialize_when_none=False)


class NetworkProfile(Model):  # belongs to VirtualMachineScaleSetVM
    network_interfaces = ListType(ModelType(NetworkInterfaceReference), serialize_when_none=False)


class VirtualMachineScaleSetVMNetworkProfileConfiguration(Model):
    network_interface_configurations = ListType(ModelType(VirtualMachineScaleSetNetworkConfiguration), serialize_when_none=False)


class VirtualMachineScaleSetVM(Model):  # data model for actual instances
    id = StringType()
    instance_id = IntType()
    location = StringType()
    name = StringType()
    plan = ModelType(Plan, serialize_when_none=False)
    additional_capabilities = ModelType(AdditionalCapabilities, serialize_when_none=False)
    available_set = ModelType(SubResource, serialize_when_none=False)
    diagnostics_profile = ModelType(DiagnosticsProfile, serialize_when_none=False)
    hardware_profile = ModelType(HardwareProfile, serialize_when_none=False)
    latest_model_applied = BooleanType(default=True, serialize_when_none=False)
    licence_type = StringType(serialize_when_none=False)
    model_definition_applied = StringType(serialize_when_none=False)
    network_profile = ModelType(NetworkProfile, serialize_when_none=False)
    network_profile_configuration = ModelType(VirtualMachineScaleSetVMNetworkProfileConfiguration, serialize_when_none=False)
    os_profile = ModelType(OSProfile, serialize_when_none=False)
    protection_policy = ModelType(VirtualMachineScaleSetVMProtectionPolicy, serialize_when_none=False)
    provisioning_state = StringType(serialize_when_none=False)
    security_profile = ModelType(SecurityProfile, serialize_when_none=False)
    storage_profile = ModelType(StorageProfile, serialize_when_none=False)
    vm_id = StringType(serialize_when_none=False)
    resources = ListType(ModelType(VirtualMachineExtension), serialize_when_none=False)
    sku = ModelType(Sku, serialize_when_none=False)
    tags = ModelType(Tags, serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)


class VirtualMachineScaleSet(Model):
    id = StringType(serialize_when_none=False)
    subscription_id = StringType(serialize_when_none=False)
    subscription_name = StringType(serialize_when_none=False)
    resource_group = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    identity = ModelType(VirtualMachineScaleSetIdentity, serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    plan = ModelType(Plan, serialize_when_none=False)
    additional_capabilities = ModelType(AdditionalCapabilities, serialize_when_none=False)
    automatic_repairs_policy = ModelType(AutomaticRepairsPolicy, serialize_when_none=False)
    automatic_repairs_policy_display = StringType(serialize_when_none=False)
    do_not_run_extensions_on_overprovisioned_v_ms = BooleanType(serialize_when_none=False)
    host_group = ModelType(SubResource, serialize_when_none=False)
    overprovision = BooleanType(default=True, serialize_when_none=False)
    platform_fault_domain_count = IntType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Failed', 'Succeeded'), serialize_when_none=False)
    proximity_placement_group = ModelType(SubResource, serialize_when_none=False)
    proximity_placement_group_display = StringType(serialize_when_none=False)
    scale_in_policy = ModelType(ScaleInPolicy, serialize_when_none=False)
    single_placement_group = BooleanType(serialize_when_none=False)
    unique_id = StringType(serialize_when_none=False)
    upgrade_policy = ModelType(UpgradePolicy, serialize_when_none=False)
    virtual_machine_profile = ModelType(VirtualMachineScaleSetVMProfile, serialize_when_none=False)
    zone_balance = BooleanType(serialize_when_none=False)
    sku = ModelType(Sku, serialize_when_none=False)
    tags = ListType(ModelType(Tags), default=[], serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)
    vm_instances = ListType(ModelType(VirtualMachineScaleSetVM), serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
