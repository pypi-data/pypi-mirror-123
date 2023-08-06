import time
from typing import Dict

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, FLOAT, \
    JSON, VARCHAR

from .BlockDevice import BlockDevice
from ..actions import ZBSAction

Base = declarative_base()


class ManagedFs(Base):
    __tablename__ = "managed_filesystems"

    account_id = Column(VARCHAR, index=True)
    account_uuid = Column(VARCHAR, index=True)
    agent_update_required = Column(BOOLEAN)
    btrfs_version = Column(VARCHAR, default=None)
    cloud = Column(VARCHAR, index=True)
    cycle_period = Column(BIGINT)
    devices = Column(JSON)
    existing_actions = Column(JSON, default=None)
    expiredAt = Column(BIGINT)
    fs_cost = Column(FLOAT)
    fs_id = Column(VARCHAR, primary_key=True)
    fs_size = Column(BIGINT)
    fs_type = Column(VARCHAR)
    fs_usage = Column(BIGINT, default=None)
    has_unallocated_space = Column(BOOLEAN)
    inodes = Column(JSON)
    instance_id = Column(VARCHAR)
    instance_type = Column(VARCHAR)
    is_ephemeral = Column(BOOLEAN)
    is_partition = Column(BOOLEAN, default=None)
    is_zesty_disk = Column(BOOLEAN)
    label = Column(VARCHAR, default=None)
    last_update = Column(BIGINT)
    LV = Column(VARCHAR, default=None)
    lvm_path = Column(VARCHAR, default=None)
    mount_path = Column(VARCHAR)
    org_id = Column(VARCHAR, index=True)
    partition_id = Column(VARCHAR, default=None)
    partition_number = Column(BIGINT, default=None)
    platform = Column(VARCHAR)
    potential_savings = Column(FLOAT)
    region = Column(VARCHAR, index=True)
    space = Column(JSON)
    tags = Column(JSON)
    VG = Column(VARCHAR, default=None)
    wrong_fs_alert = Column(BOOLEAN)
    zesty_disk_iops = Column(VARCHAR, default=None)
    zesty_disk_vol_type = Column(VARCHAR, default=None)

    def __init__(
            self,
            fs_id: str,
            account_id: str = None,
            account_uuid: str = None,
            agent_update_required: bool = None,
            btrfs_version: str = None,
            cloud: str = None,
            cloud_vendor: str = None,
            cycle_period: int = None,
            delete_on_termination: bool = None,
            devices: dict = {},
            encrypted: bool = None,
            existing_actions: Dict[str, ZBSAction] = None,
            expiredAt: int = None,
            fs_cost: float = None,
            fs_devices_to_count: int = None,
            fs_size: int = None,
            fs_type: str = None,
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
            mount_path: str = None,
            name: str = None,
            org_id: str = None,
            partition_id: str = None,
            partition_number: int = None,
            platform: str = None,
            potential_savings: float = None,
            region: str = None,
            resizable: bool = None,
            space: dict = {},
            tags: dict = None,
            unallocated_chunk: int = None,
            VG: str = None,
            wrong_fs_alert: bool,
            zesty_disk_iops: str = None,
            zesty_disk_vol_type: str = None
            ):
        self.fs_id = fs_id
        self.account_id = account_id
        self.account_uuid = account_uuid
        self.agent_update_required = agent_update_required
        self.btrfs_version = btrfs_version
        if cloud is None and cloud_vendor is None:
            self.cloud = 'Amazon'
            self.cloud_vendor = 'Amazon'
        elif cloud:
            self.cloud = cloud
            self.cloud_vendor = cloud
        elif cloud_vendor:
            self.cloud = cloud_vendor
            self.cloud_vendor = cloud_vendor
        self.cycle_period = cycle_period
        self.delete_on_termination = delete_on_termination
        self.devices = devices
        for dev in self.devices:
            if isinstance(self.devices[dev], BlockDevice):
                self.devices[dev] = self.devices[dev].asdict()
            else:
                self.devices[dev] = self.devices.get(dev, {})
        self.encrypted = encrypted
        for action in existing_actions:
            self.existing_actions[action] = self.existing_actions[action].serialize()
        self.expiredAt = expiredAt
        self.fs_cost = fs_cost
        self.fs_devices_to_count = fs_devices_to_count
        self.fs_size = fs_size
        self.fs_type = fs_type
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
        self.mount_path = mount_path
        self.name = name
        self.org_id = org_id
        self.partition_id = partition_id
        self.partition_number = partition_number
        self.platform = platform
        self.potential_savings = potential_savings
        self.region = region
        self.resizable = resizable
        self.space = space
        self.tags = tags
        self.VG = VG
        self.wrong_fs_alert = wrong_fs_alert
        self.zesty_disk_iops = zesty_disk_iops
        self.zesty_disk_vol_type = zesty_disk_vol_type

    def __repr__(self) -> str:
        return f"{self.__tablename__}:{self.fs_id}"

    def asdict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
