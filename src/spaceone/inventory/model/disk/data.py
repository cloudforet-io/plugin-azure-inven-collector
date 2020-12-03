from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType


class Sku(Model):
    name = StringType(choices=('Standard_LRS', 'Premium_LRS', 'StandardSSD_LRS', 'UltraSSD_LRS'))
    tier = StringType(choices=('Premium', 'Standard'))


class ImageReference(Model):
    id = StringType()


class CreationData(Model):
    creation_option = StringType(choices=('Attach', 'Copy', 'Empty', 'FromImage', 'Import', 'Restore', 'Upload'))
    image_reference = ModelType(ImageReference)


class Properties(Model):
    os_type = StringType(choices=('Linux', 'Windows'), serialize_when_none=False)
    creation_data = ModelType(CreationData)


class SourceVault(Model):
    id = StringType()


class DiskEncryptionKey(Model):
    source_vault = ModelType(SourceVault)
    secret_url = StringType()


class KeyEncryptionKey(Model):
    sourceVault = ModelType(SourceVault)
    key_url = StringType()


class EncryptionSettingsCollection(Model):
    disk_encryption_key = ModelType(DiskEncryptionKey)
    key_encryption_key = ModelType(KeyEncryptionKey)


class Encryption(Model):
    type = StringType()


class Tags(Model):
    key = StringType()
    value = StringType()


class Disk(Model):
    name = StringType()
    id = StringType()
    type = StringType()
    resource_group = StringType()
    location = StringType()
    managed_by = StringType()
    sku = ModelType(Sku)
    zones = ListType(StringType(), serialize_when_none=False)
    disk_size_gb = IntType()
    disk_iops_read_write = IntType()
    disk_size_bytes = IntType()
    size = IntType()  # disk size for statistics
    encryption_settings_collection = ModelType(EncryptionSettingsCollection, serialize_when_none=False)
    encryption = ModelType(Encryption, serialize_when_none=False, choices=('EncryptionAtRestWithCustomerKey',
                                                                           'EncryptionAtRestWithPlatformAndCustomerKeys',
                                                                           'EncryptionAtRestWithPlatformKey'))
    time_created = DateTimeType()
    provisioning_state = StringType(choices=('Failed', 'Succeeded'), serialize_when_none=False)
    unique_id = StringType()
    disk_m_bps_read_write = IntType()
    disk_m_bps_read_only = StringType(serialize_when_none=False)
    disk_iops_read_only = StringType(serialize_when_none=False)
    disk_state = StringType(choices=('ActiveSAS', 'ActiveUpload', 'Attached', 'ReadyToUpload', 'Reserved', 'Unattached'))
    networkAccessPolicy = StringType(choices=('AllowAll', 'AllowPrivate', 'DenyAll'))
    tier = StringType(choices=('P1', 'P2', 'P3', 'P4', 'P6', 'P10', 'P15', 'P20',
                               'P30', 'P40', 'P50', 'P60', 'P70', 'P80'), serialize_when_none=False)
    # tags = ListType(ModelType(Tags), default=[])

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": ""
        }
