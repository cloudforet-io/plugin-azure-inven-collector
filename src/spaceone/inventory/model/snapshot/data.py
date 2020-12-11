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
    creation_option = StringType(choices=('Attach', 'Copy', 'Empty', 'FromImage', 'Import', 'Restore', 'Upload'),
                                 serialize_when_none=False)
    image_reference = ModelType(ImageDiskReference, serialize_when_none=False)
    gallery_image_reference = ModelType(ImageDiskReference, serialize_when_none=False)
    logical_sector_size = IntType(serialize_when_none=False)
    source_resource_id = StringType()
    source_uri = StringType(serialize_when_none=False)
    source_unique_id = StringType(serialize_when_none=False)
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
    type_display = StringType()


class ShareInfoElement(Model):
    vm_uri = StringType(serialize_when_none=False)


class Tags(Model):
    key = StringType()
    value = StringType()


class Snapshot(Model):
    id = StringType()
    location = StringType()
    managed_by = StringType(serialize_when_none=False)
    resource_group = StringType()
    name = StringType()
    creation_data = ModelType(CreationData)
    disk_access_id = StringType(serialize_when_none=False)
    disk_iops_read_write = StringType(serialize_when_none=False)
    disk_m_bps_read_write = StringType(serialize_when_none=False)
    disk_size_bytes = IntType()
    disk_size_gb = IntType()
    disk_state = StringType(choices=('ActiveSAS', 'ActiveUpload', 'Attached', 'ReadyToUpload',
                                     'Reserved', 'Unattached'))
    encryption = ModelType(Encryption)
    encryption_settings_collection = ModelType(EncryptionSettingsCollection, serialize_when_none=False)
    hyper_v_generation = StringType(serialize_when_none=False)
    incremental = BooleanType()
    incremental_display = StringType(default='Full', serialize_when_none=False)
    network_access_policy = StringType(choices=('AllowAll', 'AllowPrivate', 'DenyAll'), serialize_when_none=False)
    network_access_policy_display = StringType(serialize_when_none=False)
    os_type = StringType(serialize_when_none=False)
    provisioning_state = StringType(choices=('Failed', 'Succeeded'), serialize_when_none=False)
    time_created = DateTimeType()
    unique_id = StringType()
    sku = ModelType(Sku)
    source_disk_name = StringType()
    subscription_id = StringType()
    subscription_name = StringType()
    tags = ListType(ModelType(Tags), default=[])
    tier_display = StringType(default='')
    type = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }