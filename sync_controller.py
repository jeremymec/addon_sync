from sync import Sync, SyncStatus
from datetime import datetime
from notify import NotificationSender
import json
from sync_model import Status
from pathlib import Path

class SyncController:

    def __init__(self, model):
        self.model = model
        self.read_config()
        self.notifcation_sender = NotificationSender()
        self.sync = Sync(Path(self.path_to_wow), self.repo_url)

    def read_config(self):
        f = open('config.json', 'r') 
        config_data = json.load(f)
        self.path_to_wow = config_data['WowFolder']
        self.repo_url = config_data['RepoURL']

    def update_addons(self):
        self.model.set_status(Status.SYNCING.value)
        result = self.sync.sync()
        if result['status'] == SyncStatus.UPLOADED_TO_CLOUD:
            self.notifcation_sender.create_notification("Addon Sync", "Your addons have been uploaded to the cloud")
        elif result['status'] == SyncStatus.UPDATED_FROM_CLOUD:
            self.notifcation_sender.create_notification("Addon Sync", "The latest version of your addons have been downloaded")
        self.model.set_last_checked(datetime.now())
        self.model.set_status(Status.NORMAL.value)

if __name__ == "__main__":
    from sync_model import SyncModel; model = SyncModel()
    SyncController(model)