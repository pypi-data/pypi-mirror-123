import json
from zesty.id_handler import create_zesty_id

GB_IN_BYTES = 1024**3


class BlockDevice():
    def __init__(
            self,
            size: int,
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
            volume_id: str = None,
            volume_type: str = None,
            device: str = None,
            ):
        self.size = size
        self.cloud_vendor = cloud_vendor
        if volume_id:
            self.volume_id = create_zesty_id(
                cloud=self.cloud_vendor,
                resource_id=volume_id
            )
        else:
            self.volume_id = volume_id
        self.btrfs_dev_id = btrfs_dev_id
        self.created = created
        self.dev_usage = dev_usage
        self.iops = iops
        self.lun = lun
        self.map = map
        self.iops_stats = iops_stats
        if device:
            self.device = device
        if parent:
            self.parent = parent

        if not unlock_ts:
            self.unlock_ts = 0
        else:
            self.unlock_ts = unlock_ts

        self.volume_type = volume_type
    
    def as_dict(self) -> dict:
        return_dict = json.loads(json.dumps(self, default=self.object_dumper))
        return {k: v for k, v in return_dict.items() if v is not None}

    @staticmethod
    def object_dumper(obj) -> dict:
        try:
            return obj.__dict__
        except AttributeError as e:
            if isinstance(obj, Decimal):
                return int(obj)
            print(f"Got exception in object_dumper value: {obj} | type : {type(obj)}")
            print(traceback.format_exc())
            return obj

    def serialize(self) -> dict:
        return self.as_dict()

    def __repr__(self) -> str:
        return '<VolumeID: {} | Size: {:.1f} GB | Usage: {:.1f} GB>'.format(
            self.volume_id,
            self.size/GB_IN_BYTES,
            self.dev_usage/GB_IN_BYTES
        )

