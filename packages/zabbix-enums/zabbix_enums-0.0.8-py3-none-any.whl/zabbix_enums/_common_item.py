from enum import IntEnum
from ._common import DiscoveryFlag, EntityStatus


ItemFlag = DiscoveryFlag
ItemStatus = EntityStatus


class ItemValueType(IntEnum):
    NUMERIC_FLOAT = 0
    CHARACTER = 1
    LOG = 2
    NUMERIC_UNSIGNED = 3
    TEXT = 4


class ItemState(IntEnum):
    NORMAL = 0
    NOT_SUPPORTED = 1
