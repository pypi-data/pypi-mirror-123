from zesty.id_handler import create_zesty_id

GB_IN_BYTES = 1024**3


class BlockDevice():
    def __init__(
            self,
            size: int,
            volume_id: str,
            btrfs_dev_id: str = None,
            cloud_vendor: str = 'Amazon',
            created: str = None,
            dev_usage: str = None,
            iops: str = None,
            lun: str = None,
            map: str = None,
            iops_stats: dict = {},
            parent: str = None,
            unlock_ts: int = 0,
            volume_type: str = None,
            ):
        self.size = size
        self.cloud_vendor = cloud_vendor
        self.volume_id = create_zesty_id(
            cloud=self.cloud_vendor,
            resource_id=volume_id
        )
        self.btrfs_dev_id = btrfs_dev_id
        self.created = created
        self.dev_usage = dev_usage
        self.iops = iops
        self.lun = lun
        self.map = map
        self.iops_stats = iops_stats
        if parent:
            self.parent = parent
        self.unlock_ts = unlock_ts
        self.volume_type = volume_type

    def __repr__(self) -> str:
        return '<VolumeID: {} | Size: {:.1f} GB | Usage: {:.1f} GB>'.format(
            self.volume_id,
            self.size/GB_IN_BYTES,
            self.dev_usage/GB_IN_BYTES
        )
