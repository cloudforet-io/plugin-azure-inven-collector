import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
DISK
"""
disks_count_by_account_conf = os.path.join(current_dir, 'widget/disks_count_by_account.yaml')
disks_count_by_region_conf = os.path.join(current_dir, 'widget/disks_count_by_region.yaml')
disks_count_by_resource_group_conf = os.path.join(current_dir, 'widget/disks_count_by_resource_group.yaml')
disks_size_by_region_conf = os.path.join(current_dir, 'widget/disks_size_by_region.yaml')
disks_size_by_status_conf = os.path.join(current_dir, 'widget/disks_size_by_status.yaml')
disks_size_by_subscription_conf = os.path.join(current_dir, 'widget/disks_size_by_subscription.yaml')
disks_size_by_type_conf = os.path.join(current_dir, 'widget/disks_size_by_type.yaml')
disks_total_size_conf = os.path.join(current_dir, 'widget/disks_total_size.yaml')
disks_total_count_conf = os.path.join(current_dir, 'widget/disks_total_count.yaml')

cst_disks = CloudServiceTypeResource()
cst_disks.group = 'Disks'
cst_disks.name = 'Disk'
cst_disks.provider = 'azure'
cst_disks.labels = ['Compute', 'Storage']
cst_disks.service_code = 'Microsoft.Compute/disks'
cst_disks.is_major = True
cst_disks.is_primary = True
cst_disks.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-disk.svg',
    'spaceone:display_name': 'Disk'
}

cst_disks._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Storage Account Type', 'data.sku.name'),
        SizeField.data_source('Size', 'data.size'),
        EnumDyField.data_source('Disk State', 'data.disk_state', default_state={
            'safe': ['ActiveSAS', 'ActiveUpload', 'Attached', 'Reserved'],
            'warning': ['ReadyToUpload'],
            'available': ['Unattached']
        }),
        TextDyField.data_source('Owner', 'data.managed_by'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),

        # is_optional - Default
        TextDyField.data_source('Subscription ID', 'data.subscription_id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Zones', 'data.zones', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('Encryption Type', 'data.encryption.type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Networking', 'data.network_access_policy_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Max Shares', 'data.max_shares', options={
            'is_optional': True
        }),
        TextDyField.data_source('Time Created', 'data.time_created', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Tier', key='data.tier', data_type='string'),
        SearchField.set(name='Subscription ID', key='data.subscription_id', data_type='string'),
        SearchField.set(name='Subscription Name', key='data.subscription_name', data_type='string'),
        SearchField.set(name='Resource Group', key='data.resource_group', data_type='string'),
        SearchField.set(name='Location', key='data.location', data_type='string'),
        SearchField.set(name='Zone', key='data.zones', data_type='string'),
        SearchField.set(name='Storage Account Type', key='data.sku.name', data_type='string'),
        SearchField.set(name='Disk Size (Bytes)', key='data.disk_size_bytes', data_type='integer'),
        SearchField.set(name='Disk Size (GB)', key='data.disk_size_gb', data_type='integer'),
        SearchField.set(name='Disk IOPS', key='data.disk_iops_read_write', data_type='integer'),
        SearchField.set(name='OS Type', key='data.os_type', data_type='string'),
        SearchField.set(name='Provisioning State', key='data.provisioning_state', data_type='string'),
        SearchField.set(name='Time Created', key='data.time_created', data_type='datetime'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(disks_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(disks_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(disks_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(disks_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(disks_count_by_resource_group_conf)),
        ChartWidget.set(**get_data_from_yaml(disks_size_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(disks_size_by_status_conf)),
        ChartWidget.set(**get_data_from_yaml(disks_size_by_subscription_conf)),
        ChartWidget.set(**get_data_from_yaml(disks_size_by_type_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_disks})
]
