from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, NumberType


class Tags(Model):
    key = StringType()
    value = StringType()


class UltraSSDEnabled(Model):  # belongs to the class VmScaleSet
    ultra_ssd_enabled = BooleanType(serialize_when_none=False)


class ComponentNames(Model):  # belongs to the class "VmScaleSet >> AdditionalUnattendedContent"
    microsoft_windows_shell_setup = StringType(serialize_when_none=False)


class AdditionalUnattendedContent(Model):  # belongs to the class VmScaleSet
    component_name = ModelType(ComponentNames, serialize_when_none=False)
    content = StringType(serialize_when_none=False)
    pass_name = StringType(serialize_when_none=False)
    setting_name = StringType(choices=('auto_logon', 'first_logon_commands'), serialize_when_none=False)


class ApiEntityReference(Model):  # belongs to the class VmScaleSet
    id = StringType(serialize_when_none=False)


class AutomaticOSUpgradePolicy(Model):  # belongs to the class VmScaleSet
    disable_automatic_rollback = BooleanType(default=False)
    enable_automatic_os_upgrade = BooleanType(default=False)


class AutomaticRepairsPolicy(Model):  # belongs to the class VmScaleSet
    enabled = BooleanType(default=False)
    grace_period = StringType(serialize_when_none=False)


class BillingProfile(Model):  # belongs to the class VmScaleSet
    max_price = NumberType(serialize_when_none=False)


class BootDiagnostics(Model):  # belongs to the class VmScaleSet
    enabled = BooleanType(serialize_when_none=False)
    storage_uri = StringType(serialize_when_none=False)


class VmScaleSet(Model):
    additional_capabilities = ModelType(UltraSSDEnabled, serialize_when_none=False)
    additional_unattended_content = ModelType(AdditionalUnattendedContent, serialize_when_none=False)
    api_entity_reference = ModelType(ApiEntityReference, serialize_when_none=False)
    automatic_os_upgrade_policy = ModelType(AutomaticOSUpgradePolicy, serialize_when_none=False)
    automatic_repairs_policy = ModelType(AutomaticRepairsPolicy, serialize_when_none=False)
    billing_profile = ModelType(BillingProfile, serialize_when_none=False)
    boot_diagnostics = ModelType(BootDiagnostics, serialize_when_none=False)
    caching_types = StringType(choices=('None', 'ReadOnly', 'ReadWrite'), default='None')
    #  ############### 12/14 ################
    id = StringType()
    type = StringType()
    resource_group = StringType()
    location = StringType()
    managed_by = StringType(default='')
    managed_by_extended = ListType(StringType, serialize_when_none=False)
    max_shares = IntType(serialize_when_none=False, default=0)
    zones = ListType(StringType(), serialize_when_none=False)
    disk_size_gb = IntType()
    disk_iops_read_write = IntType()
    disk_iops_read_only = BooleanType(serialize_when_none=False)
    disk_size_bytes = IntType()
    size = IntType()  # disk size for statistics
    hyper_v_generation = StringType(serialize_when_none=False)
    time_created = DateTimeType()
    os_type = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Failed', 'Succeeded'), serialize_when_none=False)
    unique_id = StringType()
    disk_m_bps_read_write = IntType()
    subscription_id = StringType()
    subscription_name = StringType()
    disk_m_bps_read_only = BooleanType(serialize_when_none=False)
    disk_state = StringType(
        choices=('ActiveSAS', 'ActiveUpload', 'Attached', 'ReadyToUpload', 'Reserved', 'Unattached'))
    network_access_policy = StringType(choices=('AllowAll', 'AllowPrivate', 'DenyAll'), serialize_when_none=False)
    network_access_policy_display = StringType()
    tier_display = StringType(default='')
    tags = ListType(ModelType(Tags), default=[])

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }
