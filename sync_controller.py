import json
from datetime import datetime
from pathlib import Path

from notify import NotificationSender
from sync import Sync, SyncStatus
from sync_model import Status, SyncEventType


class SyncController:
    def __init__(self, model):
        self.model = model
        self.read_config()
        self.notifcation_sender = NotificationSender()

    def init_sync(self):
        self.model.set_status(Status.INIT.value)
        sync_create_result = Sync.create_sync(Path(self.path_to_wow), self.repo_url)
        result = sync_create_result["status"]
        self.sync = sync_create_result["sync"]

        self.handle_result(result)

    def update_config_with_sync(self, action_type, action_time):
        f = open("config.json", "r")
        config_data = json.load(f)
        f.close()

        config_data["LastAction"] = action_type.name
        config_data["ActionTime"] = action_time.isoformat()

        with open("config.json", "w") as f:
            f.write(json.dumps(config_data))

    def read_config(self):
        f = open("config.json", "r")
        config_data = json.load(f)
        self.path_to_wow = config_data["WowFolder"]
        self.repo_url = config_data["RepoURL"]

        actionstring = config_data["LastAction"]
        timestring = config_data["ActionTime"]
        if actionstring == "UPLOAD":
            print("Add upload")
            self.model.add_sync_event(
                SyncEventType.UPLOAD, datetime.fromisoformat(timestring)
            )
        elif actionstring == "DOWNLOAD":
            self.model.add_sync_event(
                SyncEventType.DOWNLOAD, datetime.fromisoformat(timestring)
            )

        f.close()

    def ack_conflict(self):
        self.model.set_status(Status.CONFLICT_WAITING)

    def resolve_conflict_with_local(self):
        self.model.set_status(Status.SYNCING.value)
        result = self.sync.force_local_sync()

        self.handle_result(result["status"])

    def resolve_conflict_with_cloud(self):
        self.model.set_status(Status.SYNCING.value)
        result = self.sync.force_remote_sync()

        self.handle_result(result["status"])

    def update_addons(self):
        if self.model.get_status() == Status.CONFLICT_WAITING:
            print("Not updating due to current merge conflict")
            return

        self.model.set_status(Status.SYNCING.value)
        result = self.sync.sync()

        self.handle_result(result["status"])

    def handle_result(self, sync_status):
        if sync_status == SyncStatus.INITIALIZING:
            self.model.set_status(Status.INIT.value)
            return

        if sync_status == SyncStatus.MERGE_CONFLICT:
            self.model.set_status(Status.CONFLICT.value)
            return

        if sync_status == SyncStatus.UPLOADED_TO_CLOUD:
            self.update_config_with_sync(SyncEventType.UPLOAD, datetime.now())
            self.model.add_sync_event(SyncEventType.UPLOAD, datetime.now())
            self.notifcation_sender.create_notification(
                "Addon Sync", "Your addons have been uploaded to the cloud"
            )
        elif sync_status == SyncStatus.UPDATED_FROM_CLOUD:
            self.update_config_with_sync(SyncEventType.DOWNLOAD, datetime.now())
            self.model.add_sync_event(SyncEventType.DOWNLOAD, datetime.now())
            self.notifcation_sender.create_notification(
                "Addon Sync", "The latest version of your addons have been downloaded"
            )

        self.model.set_last_checked(datetime.now())
        self.model.set_status(Status.NORMAL.value)


if __name__ == "__main__":
    from sync_model import SyncModel

    model = SyncModel()
    SyncController(model)
