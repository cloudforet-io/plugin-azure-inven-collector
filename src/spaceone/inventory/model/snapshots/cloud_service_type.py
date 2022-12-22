import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import ASSET_URL

current_dir = os.path.abspath(os.path.dirname(__file__))

snapshots_count_by_account_conf = os.path.join(current_dir, 'widget/snapshots_count_by_account.yaml')
snapshots_count_by_region_conf = os.path.join(current_dir, 'widget/snapshots_count_by_region.yaml')
snapshots_count_by_resource_group_conf = os.path.join(current_dir, 'widget/snapshots_count_by_resource_group.yaml')
snapshots_count_by_subscription_conf = os.path.join(current_dir, 'widget/snapshots_count_by_subscription.yaml')
snapshots_total_count_conf = os.path.join(current_dir, 'widget/snapshots_total_count.yaml')
snapshots_total_size_conf = os.path.join(current_dir, 'widget/snapshots_total_size.yaml')


cst_snapshots = CloudServiceTypeResource()
cst_snapshots.name = 'Instance'
cst_snapshots.group = 'Snapshots'
cst_snapshots.service_code = 'Microsoft.Compute/snapshots'
cst_snapshots.labels = ['Compute', 'Storage']
cst_snapshots.is_primary = True
cst_snapshots.is_major = True
cst_snapshots.tags = {
    'spaceone:icon': f'{ASSET_URL}/azure-disk-snapshot.svg',
}

cst_snapshots._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Source disk', 'data.source_disk_name'),
        TextDyField.data_source('Snapshot type', 'data.incremental_display'),
        SizeField.data_source('Source disk size', 'data.disk_size_bytes'),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Subscription', 'data.subscription_name'),
        DateTimeDyField.data_source('Launched', 'data.time_created'),

        # is_optional fields - Default
        TextDyField.data_source('Subscription ID', 'account', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encryption Type', 'data.encryption.type_display', options={
            'is_optional': True
        }),
        TextDyField.data_source('Network Access Policy', 'data.network_access_policy_display', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Storage Account Type', key='instance_type'),
        SearchField.set(name='Snapshot Type', key='data.incremental_display'),
        SearchField.set(name='Disk Size (Bytes)', key='data.disk_size_bytes'),
        SearchField.set(name='Disk Size (GB)', key='instance_size', data_type='float'),
        SearchField.set(name='Encryption', key='data.encryption.type_display'),
        SearchField.set(name='Network Access Policy', key='data.network_access_policy'),
        SearchField.set(name='Provisioning State', key='data.provisioning_state'),
        SearchField.set(name='Launched', key='data.time_created', data_type='datetime')
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(snapshots_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshots_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshots_count_by_resource_group_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshots_count_by_subscription_conf)),
        CardWidget.set(**get_data_from_yaml(snapshots_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(snapshots_total_size_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_snapshots}),
]
