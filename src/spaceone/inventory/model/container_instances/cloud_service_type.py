import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

container_instances_count_by_account_conf = os.path.join(current_dir, 'widget/container_instances_count_by_account.yaml')
container_instances_count_by_region_conf = os.path.join(current_dir, 'widget/container_instances_count_by_region.yaml')
container_instances_count_by_subscription_conf = os.path.join(current_dir, 'widget/container_Instances_count_by_subscription.yaml')
container_instances_total_container_conf = os.path.join(current_dir, 'widget/container_instances_total_container_count.yaml')
container_instances_total_count_conf = os.path.join(current_dir, 'widget/container_instances_total_count.yaml')
container_instances_total_gpu_conf = os.path.join(current_dir, 'widget/container_instances_total_gpu_count.yaml')
container_instances_total_memory_conf = os.path.join(current_dir, 'widget/container_instances_total_memory_size.yaml')
container_instances_total_vcpu_conf = os.path.join(current_dir, 'widget/container_instances_total_vcpu_count.yaml')

cst_container_instances = CloudServiceTypeResource()
cst_container_instances.name = 'Container'
cst_container_instances.group = 'ContainerInstances'
cst_container_instances.service_code = 'Microsoft.ContainerInstance/containerGroups'
cst_container_instances.labels = ['Container']
cst_container_instances.is_major = True
cst_container_instances.is_primary = True
cst_container_instances.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/azure/azure-container-instances.svg',
}


cst_container_instances._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Status', 'data.instance_view.state',  default_state={
            'safe': ['RUNNING'],
            'warning': ['PENDING', 'REBOOTING', 'SHUTTING-DOWN', 'STOPPING', 'STARTING',
                        'PROVISIONING', 'STAGING', 'DEALLOCATING', 'REPAIRING'],
            'alert': ['STOPPED', 'DEALLOCATED', 'SUSPENDED'],
            'disable': ['TERMINATED']}),
        TextDyField.data_source('Resource Group', 'data.resource_group'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('OS type', 'data.os_type'),
        TextDyField.data_source('Total Containers', 'data.container_count_display'),
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Subscription Name', 'data.subscription_name'),
        TextDyField.data_source('Provisioning State', 'data.provisioning_state', options={
            'is_optional': True
        }),
        TextDyField.data_source('Restart Policy', 'data.restart_policy', options={
            'is_optional': True
        }),
        TextDyField.data_source('IP Address', 'data.ip_address.ip', options={
            'is_optional': True
        }),
        TextDyField.data_source('IP Address Type', 'data.ip_address.type', options={
            'is_optional': True
        }),
        TextDyField.data_source('FQDN', 'data.ip_address.fqdn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Start Time', 'data.start_time', options={
            'is_optional': True})
    ],
    search=[
        SearchField.set(name='Container Group Name', key='name'),
        SearchField.set(name='Status', key='data.instance_view.state'),
        SearchField.set(name='Resource Group', key='data.resource_group'),
        SearchField.set(name='OS type', key='data.os_type'),
        SearchField.set(name='Total Containers', key='data.container_count_display'),
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription_name'),
        SearchField.set(name='Provisioning State', key='data.provisioning_state'),
        SearchField.set(name='Restart Policy', key='data.restart_policy'),
        SearchField.set(name='IP Address', key='data.ip_address.ip'),
        SearchField.set(name='FQDN', key='data.ip_address.fqdn'),
        SearchField.set(name='Start Time', key='data.start_time'),
        SearchField.set(name='Location', key='data.location')
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(container_instances_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(container_instances_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(container_instances_count_by_subscription_conf)),
        CardWidget.set(**get_data_from_yaml(container_instances_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(container_instances_total_container_conf)),
        CardWidget.set(**get_data_from_yaml(container_instances_total_vcpu_conf)),
        CardWidget.set(**get_data_from_yaml(container_instances_total_memory_conf)),
        CardWidget.set(**get_data_from_yaml(container_instances_total_gpu_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_container_instances}),
]