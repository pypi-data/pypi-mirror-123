import json
import time
from typing import Dict

from zesty.id_handler import create_zesty_id, create_zesty_filesystem_id

from ..actions import ZBSAction
from .BlockDevice import BlockDevice

GB_IN_BYTES = 1024**3


class FileSystem:
    """
    This object interacts with DynamoDB representing a FileSystem.

    As per the data model migration ZES-2884,
    these will be backwards compatible and awkward in appearance until
    the code is brought up to date.
    """
    def __init__(
            self,
            fs_id: str,
            fs_type: str,
            mount_path: str,
            account_id: str = None,
            account_uuid: str = None,
            agent_update_required: bool = None,
            btrfs_version: str = None,
            cloud_vendor: str = 'Amazon',
            cycle_period: int = None,
            devices: dict = {},
            existing_actions: Dict[str, ZBSAction] = None,
            expiredAt: int = None,
            fs_cost: float = None,
            fs_size: int = None,
            fs_usage: int = None,
            has_unallocated_space: bool = None,
            inodes: dict = {},
            instance_id: str = None,
            instance_type: str = None,
            is_ephemeral: bool = None,
            is_partition: bool = None,
            is_zesty_disk: bool = None,
            label: str = None,
            last_update: int = None,
            LV: str = None,
            lvm_path: str = None,
            org_id: str = None,
            partition_id: str = None,
            partition_number: int = None,
            platform: str = None,
            potential_savings: float = None,
            region: str = None,
            space: dict = {},
            tags: dict = None,
            update_data_ts: int = 0,
            VG: str = None,
            wrong_fs_alert: bool = None,
            zesty_disk_iops: int = None,
            zesty_disk_vol_type: str = None
            ):
        self.fs_id = create_zesty_filesystem_id(
            cloud=cloud_vendor,
            fs_id=fs_id
        )
        self.fs_type = fs_type
        self.inodes = inodes
        self.mount_path = mount_path
        self.space = space
        self.account_id = account_id
        self.account_uuid = account_uuid
        self.agent_update_required = agent_update_required
        self.btrfs_version = btrfs_version
        self.cloud_vendor = cloud_vendor
        self.cycle_period = cycle_period
        self.devices = devices
        for dev in self.devices:
            self.devices[dev] = BlockDevice(
                **self.devices.get(dev, {}),
                cloud_vendor=cloud_vendor
            )
        self.existing_actions = existing_actions
        self.expiredAt = expiredAt
        self.fs_cost = fs_cost
        self.fs_size = fs_size
        self.fs_usage = fs_usage
        self.has_unallocated_space = has_unallocated_space
        self.inodes = inodes
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.is_ephemeral = is_ephemeral
        self.is_partition = is_partition
        self.is_zesty_disk = is_zesty_disk
        self.label = label
        if last_update:
            self.last_update = last_update
        else:
            self.last_update = int(time.time()) - 60
        self.LV = LV
        self.lvm_path = lvm_path
        self.org_id = org_id
        self.partition_id = partition_id
        self.partition_number = partition_number
        self.platform = platform
        self.potential_savings = potential_savings
        self.region = region
        self.space = space
        self.tags = tags
        self.update_data_ts = update_data_ts
        self.VG = VG
        self.wrong_fs_alert = wrong_fs_alert
        self.zesty_disk_iops = zesty_disk_iops
        self.zesty_disk_vol_type = zesty_disk_vol_type

    def asdict(self) -> dict:
        return_dict = json.loads(json.dumps(self, default=self.object_dumper))
        return {k: v for k, v in return_dict.items() if v is not None}

    @staticmethod
    def object_dumper(obj) -> dict:
        try:
            return obj.__dict__
        except:
            pass

    def __repr__(self) -> str:
        return f"FileSystem:{self.fs_id}"
