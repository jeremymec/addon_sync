from sync import Sync, SyncStatus
from datetime import datetime
from notify import NotificationSender
import json
from sync_model import Status, SyncEventType
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

    def ack_conflict(self):
        self.model.set_status(Status.CONFLICT_WAITING)

    def resolve_conflict_with_local(self):
        self.model.set_status(Status.SYNCING.value)
        result = self.sync.force_local_sync()

        self.handle_result(result['status'])

    def resolve_conflict_with_cloud(self):
        self.model.set_status(Status.SYNCING.value)
        result = self.sync.force_remote_sync()
        
        self.handle_result(result['status'])

    def update_addons(self):
        if self.model.get_status() == Status.CONFLICT_WAITING:
            print('Not updating due to current merge conflict')
            return

        self.model.set_status(Status.SYNCING.value)
        result = self.sync.sync()

        self.handle_result(result['status'])

    def handle_result(self, sync_status):
        if sync_status == SyncStatus.MERGE_CONFLICT:
            self.model.set_status(Status.CONFLICT)
            return

        if sync_status == SyncStatus.UPLOADED_TO_CLOUD:
            self.model.add_sync_event(SyncEventType.UPLOAD, datetime.now())
            self.notifcation_sender.create_notification("Addon Sync", "Your addons have been uploaded to the cloud")
        elif sync_status == SyncStatus.UPDATED_FROM_CLOUD:
            self.model.add_sync_event(SyncEventType.DOWNLOAD, datetime.now())
            self.notifcation_sender.create_notification("Addon Sync", "The latest version of your addons have been downloaded")

        self.model.set_last_checked(datetime.now())
        self.model.set_status(Status.NORMAL.value)

if __name__ == "__main__":
    from sync_model import SyncModel; model = SyncModel()
    SyncController(model)