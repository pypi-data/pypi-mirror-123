from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, FLOAT, \
    JSON, VARCHAR

Base = declarative_base()


class ManagedFs(Base):
    __tablename__ = "managed_filesystems"

    account_uuid = Column(VARCHAR, index=True)
    account_id = Column(VARCHAR, index=True)
    agent_update_required = Column(BOOLEAN)
    btrfs_version = Column(VARCHAR, default=None)
    cloud = Column(VARCHAR, index=True)
    cycle_period = Column(VARCHAR)
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
            account_id: str,
            account_uuid: str,
            agent_update_required: bool,
            cloud: str,
            cycle_period: str,
            expiredAt: int,
            fs_id: str,
            instance_id: str,
            instance_type: str,
            last_update: int,
            mount_path: str,
            org_id: str,
            platform: str,
            region: str,
            wrong_fs_alert: bool,
            btrfs_version: str = None,
            devices: dict = {},
            existing_actions: dict = None,
            fs_cost: float = 0.0,
            fs_size: int = 0,
            fs_type: str = None,
            fs_usage: int = None,
            has_unallocated_space: bool = False,
            inodes: dict = {},
            is_ephemeral: bool = False,
            is_partition: bool = None,
            is_zesty_disk: bool = False,
            label: str = None,
            LV: str = None,
            lvm_path: str = None,
            partition_id: str = None,
            partition_number: int = None,
            potential_savings: float = 0.0,
            space: dict = {},
            tags: dict = {},
            VG: str = None,
            zesty_disk_iops: str = None,
            zesty_disk_vol_type: str = None
            ):
        self.account_id = account_id
        self.account_uuid = account_uuid
        self.agent_update_required = agent_update_required
        self.cloud = cloud
        self.cycle_period = cycle_period
        self.expiredAt = expiredAt
        self.fs_id = fs_id
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.last_update = last_update
        self.mount_path = mount_path
        self.org_id = org_id
        self.platform = platform
        self.region = region
        self.wrong_fs_alert = wrong_fs_alert
        self.btrfs_version = btrfs_version
        self.devices = devices
        self.existing_actions = existing_actions
        self.fs_cost = fs_cost
        self.fs_size = fs_size
        self.fs_type = fs_type
        self.fs_usage = fs_usage
        self.has_unallocated_space = has_unallocated_space
        self.inodes = inodes
        self.is_ephemeral = is_ephemeral
        self.is_partition = is_partition
        self.is_zesty_disk = is_zesty_disk
        self.label = label
        self.LV = LV
        self.lvm_path = lvm_path
        self.partition_id = partition_id
        self.partition_number = partition_number
        self.potential_savings = potential_savings
        self.space = space
        self.tags = tags
        self.VG = VG
        self.zesty_disk_iops = zesty_disk_iops
        self.zesty_disk_vol_type = zesty_disk_vol_type

    def __repr__(self) -> str:
        return f"{self.__tablename__}:{self.fs_id}"

    def asdict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
