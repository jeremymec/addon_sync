from enum import Enum, auto
class Status(Enum):
    INIT = "Starting Up..."
    SYNCING = "Syncing your addons with the cloud..."
    NORMAL = "Everything up to date!"
    CONFLICT = "There has been a merge conflict"
    CONFLICT_WAITING = "Waiting for how to resolve the conflict"

class SyncEventType(Enum):
    UPLOAD = "uploaded"
    DOWNLOAD = "downloaded"

class SyncEvent():

    def __init__(self, sync_type, sync_time):
        self.sync_type = sync_type
        self.sync_time = sync_time
    
    def get_sync_type(self):
        return self.sync_type

    def get_sync_time(self):
        return self.sync_time


class SyncModel:

    def __init__(self):
        self.observers = []
        self.status = Status.INIT.value
        self.last_checked = None
        self.sync_events = []
        self.conflict = False

    def register_observer(self, observer):
        self.observers.append(observer)
    
    def update(self):
        for observer in self.observers:
            observer.update()
    
    def get_status(self):
        return self.status
    
    def set_status(self, status):
        self.status = status
        self.update()

    def get_last_checked(self):
        return self.last_checked

    def set_last_checked(self, time):
        self.last_checked = time
        self.update()

    def add_sync_event(self, sync_type, sync_time):
        self.sync_events.append(SyncEvent(sync_type, sync_time))
        self.update()
    
    def get_last_sync_event(self):
        try:
            return self.sync_events[-1]
        except IndexError:
            return None

    def get_sync_events(self):
        return self.sync_events.copy()

    
        
if __name__ == "__main__":
    SyncModel()