from copy_addons import copy_addons
from updater import push_addons_to_git
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

    def upstream_sync(self):
        self.model.set_status(Status.SYNC_UP)
        copy_addons(self.path_to_wow)
        push_addons_to_git()
        self.notifcation_sender.create_notification("Addon Sync", "Your addons have been uploaded to the cloud!")
        self.model.set_status(Status.NORMAL)

    def sync(self):
        self.upstream_sync()