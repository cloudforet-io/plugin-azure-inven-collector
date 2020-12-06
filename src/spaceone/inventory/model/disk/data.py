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
    logical_sector_size = ModelType(IntType, serialize_when_none=False)
    source_resource_id = StringType(serialize_when_none=False)
    source_unique_id = StringType(serialize_when_none=False)
    source_uri = StringType(serialize_when_none=False)
    storage_account_id = StringType(serialize_when_none=False)
    upload_size_bytes = IntType(serialize_when_none=False)


class SourceVault(Model):
    id = StringType()


class DiskEncryptionKey(Model):
    source_vault = ModelType(SourceVault)
    secret_url = StringType()


class KeyEncryptionKey(Model):
    source_vault = ModelType(SourceVault)
    key_url = StringType()


class EncryptionSettingsCollection(Model):
    disk_encryption_key = ModelType(DiskEncryptionKey)
    key_encryption_key = ModelType(KeyEncryptionKey)


class Encryption(Model):
    disk_encryption_set_id = StringType(serialize_when_none=False)
    type = StringType(choices=('EncryptionAtRestWithCustomerKey', 'EncryptionAtRestWithPlatformAndCustomerKeys',
                               'EncryptionAtRestWithPlatformKey'),
                      default='EncryptionAtRestWithPlatformKey')


class OsType(Model):
    Linux = StringType(serialize_when_none=False),
    Windows = StringType(serialize_when_none=False)


class ShareInfoElement(Model):
    vmUri = StringType(serialize_when_none=False)


class Tags(Model):
    key = StringType()
    value = StringType()


# 예제일뿐...
class Lock(Model):
    name = StringType()
    type = StringType()
    scope = StringType()
    notes = ListType(StringType())


class Disk(Model):
    name = StringType()
    id = StringType()
    type = StringType()
    resource_group = StringType()
    location = StringType()
    managed_by = StringType(serialize_when_none=False)
    managed_by_extended = ListType(StringType, serialize_when_none=False)
    max_shares = IntType(serialize_when_none=False)
    sku = ModelType(Sku)
    zones = ListType(StringType(), serialize_when_none=False)
    disk_size_gb = IntType()
    disk_iops_read_write = IntType()
    disk_iops_read_only = BooleanType(serialize_when_none=False)
    disk_size_bytes = IntType()
    size = IntType()  # disk size for statistics
    encryption_settings_collection = ModelType(EncryptionSettingsCollection, serialize_when_none=False)
    encryption = ModelType(Encryption, serialize_when_none=False),
    hyper_v_generation = StringType()
    time_created = DateTimeType()
    creation_data = ModelType(CreationData)
    os_type = ModelType(OsType, serialize_when_none=False)
    provisioning_state = StringType(choices=('Failed', 'Succeeded'), serialize_when_none=False)
    share_info = ListType(ShareInfoElement, serialize_when_none=False)
    unique_id = StringType()
    disk_m_bps_read_write = IntType()
    subscription_id = StringType()
    subscription_name = StringType()
    locks = ListType(ModelType(Lock))
    disk_m_bps_read_only = BooleanType(serialize_when_none=False)
    disk_state = StringType(choices=('ActiveSAS', 'ActiveUpload', 'Attached', 'ReadyToUpload', 'Reserved', 'Unattached'))
    disk_state_display = StringType()
    networkAccessPolicy = StringType(choices=('AllowAll', 'AllowPrivate', 'DenyAll'))
    tier = StringType(choices=('P1', 'P2', 'P3', 'P4', 'P6', 'P10', 'P15', 'P20',
                               'P30', 'P40', 'P50', 'P60', 'P70', 'P80', 'E1', 'E2', 'E3', 'E4', 'E6', 'E10', 'E15',
                               'E20', 'E30', 'E40', 'E50', 'S4', 'S6', 'S10', 'S15', 'S20', 'S30', 'S40', 'S50',
                               'S60', 'S70', 'S80'), serialize_when_none=False)
    tags = ListType(ModelType(Tags), default=[])

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }