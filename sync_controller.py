from copy_addons import copy_addons
from remote import push_addons, clone_addons, addons_exist, update_addons
from notify import NotificationSender
import json
from sync_model import Status

class SyncController:

    def __init__(self, model):
        self.model = model
        self.read_config()
        self.notifcation_sender = NotificationSender()

    def read_config(self):
        f = open('config.json', 'r') 
        config_data = json.load(f)
        self.path_to_wow = config_data['WowFolder']
        self.repo_url = config_data['RepoURL']

    def clone_repo(self):
        self.model.set_status(Status.CLONE)
        clone_addons(self.repo_url)
        self.model.set_status(Status.NORMAL)

    def update_from_cloud(self):
        self.model.set_status(Status.SYNC_DOWN)
        update_addons()
        self.model.set_status(Status.NORMAL)

    def upstream_sync(self):
        self.model.set_status(Status.SYNC_UP)
        copy_addons(self.path_to_wow)
        push_addons()
        self.notifcation_sender.create_notification("Addon Sync", "Your addons have been uploaded to the cloud!")
        self.model.set_status(Status.NORMAL)

    def sync(self):
        if not addons_exist():
            self.clone_repo()

        self.update_from_cloud()

        