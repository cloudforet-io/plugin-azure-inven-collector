class VirtualMachineDiskManager:
    def get_disk_info(self, vm, list_disks):
        '''
        disk_data = {
            "device_index": 0,
            "device": "",
            "disk_type": "disk",
            "size": 100,
            "tags": {
                "disk_name": "",
                "caching": "None" | "ReadOnly" | "ReadWrite"
                "storage_account_type": "Standard_LRS" | "Premium_LRS" | "StandardSSD_LRS" | "UltraSSD_LRS"
                "disk_encryption_set": "PMK" | "CMK"
                "iops": 60,
                "throughput_mbps": 200
            }
        }
        '''

        disk_data = []
        index = 0

        os_disk = vm.storage_profile.os_disk
        volume_data = self.get_volume_data(os_disk, list_disks, index)
        volume_data.update({
            'disk_type': 'os_disk'
        })
        disk_data.append(volume_data)
        index += 1

        data_disks = vm.storage_profile.data_disks
        if data_disks:
            for data_disk in data_disks:
                volume_data_sub = self.get_volume_data(data_disk, list_disks, index)
                volume_data_sub.update({
                    'disk_type': 'data_disk'
                })
                disk_data.append(volume_data_sub)
                index += 1

        return disk_data

    def get_volume_data(self, disk, list_disks, index):
        volume_data = {
            'device_index': index,
            'size': disk.disk_size_gb * 1073741824 if disk.disk_size_gb is not None else 0,
            'tags': {
                'disk_name': disk.name if disk.name is not None else '',
                'caching': disk.caching if disk.caching is not None else '',
            }
        }

        if getattr(disk, 'managed_disk') and disk.managed_disk is not None:
            encryption = self.get_disk_encryption(disk)
            volume_data['tags'].update({'disk_encryption_set': encryption})
            if disk.managed_disk.id is not None:
                volume_data['tags'].update({'disk_id': disk.managed_disk.id})
            if disk.managed_disk.storage_account_type is not None:
                volume_data['tags'].update({'storage_account_type': disk.managed_disk.storage_account_type})

        map_disk = self.get_mapping_disk_info(disk, list_disks)

        if map_disk:
            volume_data['tags'].update({
                'iops': map_disk.disk_iops_read_write,
                'throughput_mbps': map_disk.disk_m_bps_read_write
            })
        return volume_data

    @staticmethod
    def get_mapping_disk_info(disk, list_disks):
        if list_disks:
            list_disks = []

        if getattr(disk, 'managed_disk') and disk.managed_disk:
            disk_name = disk.managed_disk.id.split('/')[-1]
            for disk_info in list_disks:
                if disk_info.name == disk_name:
                    return disk_info

        return None

    @staticmethod
    def get_disk_encryption(disk):
        if disk.managed_disk.disk_encryption_set:
            return 'CMK'
        else:
            return 'PMK'
