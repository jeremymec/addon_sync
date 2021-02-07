from enum import Enum, auto


class SyncStatus(Enum):
    INITIALIZING = auto()
    ERROR = auto()
    UPDATED_FROM_CLOUD = auto()
    UPLOADED_TO_CLOUD = auto()
    NO_CHANGE = auto()
    MERGE_CONFLICT = auto()
