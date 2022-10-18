from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType
from spaceone.inventory.model.container_instances.data import ContainerInstance
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, SizeField

'''
CONTAINER_INSTANCES
'''

# TAB - Default
container_instances_info_meta = ItemDynamicLayout.set_fields('Container Instances', fields=[
    TextDyField.data_source('Name', 'name'),
    EnumDyField.data_source('Status', 'data.instance_view.state', default_state={
        'safe': ['RUNNING'],
        'warning': ['PENDING', 'REBOOTING', 'SHUTTING-DOWN', 'STOPPING', 'STARTING',
                    'PROVISIONING', 'STAGING', 'DEALLOCATING', 'REPAIRING'],
        'alert': ['STOPPED', 'DEALLOCATED', 'SUSPENDED'],
        'disable': ['TERMINATED']}),
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Resource Group', 'data.resource_group'),
    TextDyField.data_source('Region', 'region_code'),
    TextDyField.data_source('Subscription', 'data.subscription_name'),
    TextDyField.data_source('Subscription ID', 'account'),
    TextDyField.data_source('SKU', 'data.sku'),
    TextDyField.data_source('OS type', 'data.os_type'),
    TextDyField.data_source('Container count', 'data.container_count_display'),
    TextDyField.data_source('IP Address', 'data.ip_address.ip'),
    TextDyField.data_source('IP Address Type', 'data.ip_address.type'),
    TextDyField.data_source('FQDN', 'data.ip_address.fqdn'),
    TextDyField.data_source('DNS name label', 'data.ip_address.auto_generated_domain_name_label_scope'),
    TextDyField.data_source('DNS name label scope reuse', 'data.ip_address.dns_name_label'),
    ListDyField.data_source('Ports', 'data.ip_address.ports.port', options={'delimiter': '<br>'}),
    TextDyField.data_source('Start Time', 'data.start_time')

])

# TAB -Container
container_instances_info_container = TableDynamicLayout.set_fields('Containers', root_path='data', fields=[
    TextDyField.data_source('Name', 'containers.name'),
    TextDyField.data_source('Container Instance Name', 'name'),
    TextDyField.data_source('Image', 'containers.image'),
    TextDyField.data_source('State', 'containers.instance_view.current_state.state'),
    TextDyField.data_source('Container Start time', 'containers.instance_view.current_state.start_time'),
    TextDyField.data_source('Restart count', 'containers.instance_view.restart_count'),
    TextDyField.data_source('CPU cores', 'containers.resources.requests.cpu', options={
        'translation_id': 'PAGE_SCHEMA.CPU_CORE',
    }),
    TextDyField.data_source('Memory', 'containers.resources.requests.memory_in_gb', options={
        'translation_id': 'PAGE_SCHEMA.MEMORY',
    }),
    TextDyField.data_source('GPU SKU', 'containers.resources.requests.gpu.sku'),
    TextDyField.data_source('GPU count', 'containers.resources.requests.gpu.count'),
    ListDyField.data_source('Commands', 'containers.command', options={'delimiter': '<br>'}),
])

# TAB - Volume
container_instances_info_volumes = TableDynamicLayout.set_fields('Volumes', root_path='data', fields=[
    TextDyField.data_source('Name', 'volumes.name'),
    TextDyField.data_source('Container Instance Name', 'name'),
    TextDyField.data_source('Volume type', 'containers.volume_mounts.name'),
    TextDyField.data_source('Mount path', 'containers.volume_mounts.mount_path')

])

container_instances_meta = CloudServiceMeta.set_layouts(
    [container_instances_info_meta, container_instances_info_container, container_instances_info_volumes]
)


class ContainerResource(CloudServiceResource):
    cloud_service_group = StringType(default='ContainerInstances')


class ContainerInstanceResource(ContainerResource):
    cloud_service_type = StringType(default='Container')
    data = ModelType(ContainerInstance)
    _metadata = ModelType(CloudServiceMeta, default=container_instances_meta, serialized_name='metadata')
    name = StringType(serialize_when_none=False)
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class ContainerInstanceResponse(CloudServiceResponse):
    resource = PolyModelType(ContainerInstanceResource)
