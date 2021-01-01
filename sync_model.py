from enum import Enum

class Status(Enum):
    INIT = "Starting Up..."
    SYNC_UP = "Uploading your addons to the cloud"
    NORMAL = "Everything up to date!"

class SyncModel:

    def __init__(self):
        self.observers = []
        self.status = Status.INIT

    def register_observer(self, observer):
        self.observers.append(observer)
    
    def update(self):
        for observer in self.observers:
            observer.update()
    
    def get_status(self):
        return self.status.value
    
    def set_status(self, status):
        self.status = status
        self.update()

if __name__ == "__main__":
    SyncModel()