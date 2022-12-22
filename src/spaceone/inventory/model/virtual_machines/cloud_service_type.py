import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, \
    ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import ASSET_URL

current_dir = os.path.abspath(os.path.dirname(__file__))

virtual_machine_total_count_conf = os.path.join(current_dir, 'widget/virtual_machine_total_running_count.yaml')
virtual_machine_total_disk_size_conf = os.path.join(current_dir, 'widget/virtual_machine_total_disk_size.yaml')
virtual_machine_total_memory_size_conf = os.path.join(current_dir, 'widget/virtual_machine_total_memory_size.yaml')
virtual_machine_total_vcpu_count_conf = os.path.join(current_dir, 'widget/virtual_machine_total_vcpu_count.yaml')
virtual_machine_count_by_account_conf = os.path.join(current_dir, 'widget/virtual_machine_count_by_account.yaml')
virtual_machine_count_by_instance_type_conf = os.path.join(current_dir,
                                                           'widget/virtual_machine_count_by_instance_type.yaml')
virtual_machine_count_by_region_conf = os.path.join(current_dir, 'widget/virtual_machine_count_by_region.yaml')

cst_virtual_machine = CloudServiceTypeResource()
cst_virtual_machine.name = 'Instance'
cst_virtual_machine.group = 'VirtualMachines'
cst_virtual_machine.labels = ['Compute', 'Server']
cst_virtual_machine.is_major = True
cst_virtual_machine.is_primary = True
cst_virtual_machine.service_code = 'Microsoft.Compute/virtualMachines'
cst_virtual_machine.tags = {
    'spaceone:icon': f'{ASSET_URL}/azure-vm.svg',
}


cst_virtual_machine._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Instance State', 'data.compute.instance_state', default_state={
            'safe': ['RUNNING'],
            'warning': ['PENDING', 'REBOOTING', 'SHUTTING-DOWN', 'STOPPING', 'STARTING',
                        'PROVISIONING', 'STAGING', 'DEALLOCATING', 'REPAIRING'],
            'alert': ['STOPPED', 'DEALLOCATED', 'SUSPENDED'],
            'disable': ['TERMINATED']}
        ),
        TextDyField.data_source('Cloud Service ID', 'cloud_service_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Instance Type', 'data.compute.instance_type'),
        TextDyField.data_source('Core', 'data.hardware.core'),
        TextDyField.data_source('Memory', 'data.hardware.memory'),
        TextDyField.data_source('Instance ID', 'data.compute.instance_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key Pair', 'data.compute.keypair', options={
            'is_optional': True
        }),
        TextDyField.data_source('Image', 'data.compute.image', options={
            'is_optional': True
        }),

        TextDyField.data_source('Availability Zone', 'data.compute.az'),
        TextDyField.data_source('OS Type', 'data.os.os_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('OS', 'data.os.os_distro'),
        TextDyField.data_source('OS Architecture', 'data.os.os_arch', options={
            'is_optional': True
        }),
        TextDyField.data_source('Primary IP', 'data.primary_ip_address'),
        ListDyField.data_source('Public DNS', 'data.nics', options={
            'sub_key': 'tags.public_dns',
            'is_optional': True
        }),
        ListDyField.data_source('Public IP', 'data.nics', options={
            'sub_key': 'public_ip_address',
            'is_optional': True
        }),
        TextDyField.data_source('All IP', 'ip_addresses', options={
            'is_optional': True
        }),
        TextDyField.data_source('MAC Address', 'data.nics.mac_address', options={
            'is_optional': True
        }),
        TextDyField.data_source('CIDR', 'data.vnet.cidr', options={
            'is_optional': True
        }),
        TextDyField.data_source('VNet ID', 'data.vnet.vnet_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('VNet Name', 'data.vnet.vnet_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet ID', 'data.subnet.subnet_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Name', 'data.subnet.subnet_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancer Name', 'data.load_balancer.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancer DNS', 'data.load_balancer.endpoint', options={
            'is_optional': True
        }),
        TextDyField.data_source('Ultra SSD Enabled', 'data.azure.ultra_ssd_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('Write Accelerator Enabled', 'data.azure.write_accelerator_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('Boot Diagnostics', 'data.azure.boot_diagnostics', options={
            'is_optional': True
        }),
        TextDyField.data_source('Priority', 'data.azure.priority', options={
            'is_optional': True
        }),
        TextDyField.data_source('Auto Scaling Group', 'data.auto_scaling_group.name', options={
            'is_optional': True
        }),
        TextDyField.data_source('CPU Utilization', 'data.monitoring.cpu.utilization.avg', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Average)'
        }),
        TextDyField.data_source('Memory Usage', 'data.monitoring.memory.usage.avg', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Average)'
        }),
        TextDyField.data_source('Disk Read IOPS', 'data.monitoring.disk.read_iops.avg', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Average)'
        }),
        TextDyField.data_source('Disk Write IOPS', 'data.monitoring.disk.write_iops.avg', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Average)'
        }),
        SizeField.data_source('Disk Read Throughput', 'data.monitoring.disk.read_throughput.avg', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Average)'
        }),
        SizeField.data_source('Disk Write Throughput', 'data.monitoring.disk.write_throughput.avg', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Average)'
        }),
        TextDyField.data_source('Network Received PPS', 'data.monitoring.network.received_pps.avg', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Average)'
        }),
        TextDyField.data_source('Network Send PPS', 'data.monitoring.network.sent_pps.avg', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Average)'
        }),
        SizeField.data_source('Network Received Throughput', 'data.monitoring.network.received_throughput.avg',
                              options={
                                  'default': 0,
                                  'is_optional': True,
                                  'field_description': '(Daily Average)'
                              }),
        SizeField.data_source('Network Sent Throughput', 'data.monitoring.network.sent_throughput.avg',
                              options={
                                  'default': 0,
                                  'is_optional': True,
                                  'field_description': '(Daily Average)'
                              }),
        TextDyField.data_source('CPU Utilization', 'data.monitoring.cpu.utilization.max', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Max)'
        }),
        TextDyField.data_source('Memory Usage', 'data.monitoring.memory.usage.max', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Max)'
        }),
        TextDyField.data_source('Disk Read IOPS', 'data.monitoring.disk.read_iops.max', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Max)'
        }),
        TextDyField.data_source('Disk Write IOPS', 'data.monitoring.disk.write_iops.max', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Max)'
        }),
        SizeField.data_source('Disk Read Throughput', 'data.monitoring.disk.read_throughput.max', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Max)'
        }),
        SizeField.data_source('Disk Write Throughput', 'data.monitoring.disk.write_throughput.max', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Max)'
        }),
        TextDyField.data_source('Network Received PPS', 'data.monitoring.network.received_pps.max', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Max)'
        }),
        TextDyField.data_source('Network Send PPS', 'data.monitoring.network.sent_pps.max', options={
            'default': 0,
            'is_optional': True,
            'field_description': '(Daily Max)'
        }),
        SizeField.data_source('Network Received Throughput', 'data.monitoring.network.received_throughput.max',
                              options={
                                  'default': 0,
                                  'is_optional': True,
                                  'field_description': '(Daily Max)'
                              }),
        SizeField.data_source('Network Sent Throughput', 'data.monitoring.network.sent_throughput.max',
                              options={
                                  'default': 0,
                                  'is_optional': True,
                                  'field_description': '(Daily Max)'
                              }),
        TextDyField.data_source('Subscription ID', 'account'),
        TextDyField.data_source('Launched', 'launched_at', options={'is_optional': True}),
    ],
    search=[
        SearchField.set(name='Subscription ID', key='account'),
        SearchField.set(name='Subscription Name', key='data.subscription.subscription_name'),
        SearchField.set(name='Resource Group', key='data.resource_group.resource_group_name'),
        SearchField.set(name='IP Address', key='ip_addresses'),
        SearchField.set(name='Instance ID', key='data.compute.instance_id'),
        SearchField.set(name='Instance State', key='data.compute.instance_state'),
        SearchField.set(name='Instance Type', key='data.compute.instance_type'),
        SearchField.set(name='Key Pair', key='data.compute.keypair'),
        SearchField.set(name='Image', key='data.compute.image'),
        SearchField.set(name='Availability Zone', key='data.compute.az'),
        SearchField.set(name='OS Type', key='data.os.os_type'),
        SearchField.set(name='OS Architecture', key='data.os.os_arch'),
        SearchField.set(name='MAC Address', key='data.nics.mac_address'),
        SearchField.set(name='Public IP Address', key='data.nics.public_ip_address'),
        SearchField.set(name='Public DNS', key='data.nics.tags.public_dns'),
        SearchField.set(name='VNet ID', key='data.vnet.vnet_id'),
        SearchField.set(name='VNet Name', key='data.vnet.vnet_name'),
        SearchField.set(name='Subnet ID', key='data.subnet.subnet_id'),
        SearchField.set(name='Subnet Name', key='data.subnet.subnet_name'),
        SearchField.set(name='ELB Name', key='data.load_balancer.name'),
        SearchField.set(name='ELB DNS', key='data.load_balancer.endpoint'),
        SearchField.set(name='Auto Scaling Group', key='data.auto_scaling_group.name'),
        SearchField.set(name='Core', key='data.hardware.core', data_type='integer'),
        SearchField.set(name='Memory', key='data.hardware.memory', data_type='float'),
        SearchField.set(name='Management State', key='state'),
        SearchField.set(name='Cloud Service Group', key='cloud_service_group'),
        SearchField.set(name='Cloud Service Type', key='cloud_service_type'),
        SearchField.set(name='Service Account', key='collection_info.service_accounts',
                        reference='identity.ServiceAccount'),
        SearchField.set(name='Launched', key='data.launched_at'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(virtual_machine_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(virtual_machine_total_vcpu_count_conf)),
        CardWidget.set(**get_data_from_yaml(virtual_machine_total_memory_size_conf)),
        CardWidget.set(**get_data_from_yaml(virtual_machine_total_disk_size_conf)),
        ChartWidget.set(**get_data_from_yaml(virtual_machine_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(virtual_machine_count_by_instance_type_conf)),
        ChartWidget.set(**get_data_from_yaml(virtual_machine_count_by_account_conf)),
    ]
)
CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_virtual_machine}),
]
