from enum import Enum

class Status(Enum):
    INIT = "Starting Up..."
    SYNCING = "Syncing your addons with the cloud..."
    NORMAL = "Everything up to date!"
    CONFLICT = "There has been a merge conflict"
    CONFLICT_WAITING = "Waiting for how to resolve the conflict"

class SyncModel:

    def __init__(self):
        self.observers = []
        self.status = Status.INIT.value
        self.last_checked = None
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
        
if __name__ == "__main__":
    SyncModel()