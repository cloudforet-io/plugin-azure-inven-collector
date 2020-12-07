from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType


class Sku(Model):
    name = StringType(choices=('Standard_LRS', 'Premium_LRS', 'StandardSSD_LRS', 'UltraSSD_LRS'),
                      serialize_when_none=False)
    tier = StringType(choices=('Premium', 'Standard'), serialize_when_none=False)


class ImageDiskReference(Model):
    id = StringType(serialize_when_none=False)
    Lun = IntType(serialize_when_none=False)


class CreationData(Model):
    creation_option = StringType(choices=('Attach', 'Copy', 'Empty', 'FromImage', 'Import', 'Restore', 'Upload'))
    gallery_image_reference = ModelType(ImageDiskReference, serialize_when_none=False)
    image_reference = ModelType(ImageDiskReference, serialize_when_none=False)
    logical_sector_size = IntType(serialize_when_none=False)
    source_resource_id = StringType(serialize_when_none=False)
    source_unique_id = StringType(serialize_when_none=False)
    source_uri = StringType(serialize_when_none=False)
    storage_account_id = StringType(serialize_when_none=False)
    upload_size_bytes = IntType(serialize_when_none=False)


class SourceVault(Model):
    id = StringType(serialize_when_none=False)


class DiskEncryptionKey(Model):
    source_vault = ModelType(SourceVault, serialize_when_none=False)
    secret_url = StringType(serialize_when_none=False)


class KeyEncryptionKey(Model):
    source_vault = ModelType(SourceVault)
    key_url = StringType()


class EncryptionSettingsCollection(Model):
    disk_encryption_key = ModelType(DiskEncryptionKey, serialize_when_none=False)
    key_encryption_key = ModelType(KeyEncryptionKey, serialize_when_none=False)


class Encryption(Model):
    disk_encryption_set_id = StringType(default='', serialize_when_none=False)
    type = StringType(choices=('EncryptionAtRestWithCustomerKey', 'EncryptionAtRestWithPlatformAndCustomerKeys',
                               'EncryptionAtRestWithPlatformKey'),
                      default='EncryptionAtRestWithPlatformKey', serialize_when_none=False)


class ShareInfoElement(Model):
    vm_uri = StringType(serialize_when_none=False)


class Tags(Model):
    key = StringType()
    value = StringType()


class LockLevel(Model):
    can_not_delete = StringType()
    not_specified = StringType()
    read_only = StringType()


class ManagementLockObject(Model):
    id = StringType()
    name = StringType()
    level = ModelType(LockLevel)
    level_display = StringType()
    notes = StringType()
    properties_owners = ListType(StringType())
    type = StringType()


class Lock(Model):
    next_link = StringType()
    value = ModelType(ManagementLockObject)


class Disk(Model):
    name = StringType()
    id = StringType()
    type = StringType()
    resource_group = StringType()
    location = StringType()
    managed_by = StringType(serialize_when_none=False)
    managed_by_extended = ListType(StringType, serialize_when_none=False)
    max_shares = IntType(serialize_when_none=False, default=0)
    sku = ModelType(Sku)
    zones = ListType(StringType(), serialize_when_none=False)
    disk_size_gb = IntType()
    disk_iops_read_write = IntType()
    disk_iops_read_only = BooleanType(serialize_when_none=False)
    disk_size_bytes = IntType()
    size = IntType()  # disk size for statistics
    encryption_settings_collection = ModelType(EncryptionSettingsCollection)
    encryption = ModelType(Encryption)
    hyper_v_generation = StringType(serialize_when_none=False)
    time_created = DateTimeType()
    creation_data = ModelType(CreationData)
    os_type = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Failed', 'Succeeded'), serialize_when_none=False)
    share_info = ModelType(ShareInfoElement, serialize_when_none=False)
    unique_id = StringType()
    disk_m_bps_read_write = IntType()
    subscription_id = StringType()
    subscription_name = StringType()
    # locks = ListType(ModelType(Lock), serialize_when_none=False)
    disk_m_bps_read_only = BooleanType(serialize_when_none=False)
    disk_state = StringType(choices=('ActiveSAS', 'ActiveUpload', 'Attached', 'ReadyToUpload', 'Reserved', 'Unattached'))
    network_access_policy = StringType(choices=('AllowAll', 'AllowPrivate', 'DenyAll'), serialize_when_none=False)
    network_access_policy_display = StringType()
    tier_display = StringType(default='')
    tags = ListType(ModelType(Tags), default=[])

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }