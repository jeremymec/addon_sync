from git_service import GitService
from sync_status import SyncStatus
from enum import Enum, auto
import sys
import os
import json

class Sync:

    def __init__(self, base_path, remote_path):
        self.base_path = base_path
        self.remote_path = remote_path

        # Attempt to read sync_lock
        path_to_lockfile = os.path.join(self.base_path, 'sync_lock.json')
        try:
            with open(path_to_lockfile) as f:
                pass
        except IOError:
            self.create_lockfile(path_to_lockfile)

        self.git_service = GitService(self.base_path, self.remote_path)

    def create_lockfile(self, path):
        initial_lockfile_contents = {'Remote': self.remote_path}
        with open(path, 'w+') as f:
            f.write(json.dumps(initial_lockfile_contents))
        
        f.close()
        

    def force_local_sync(self):
        self.git_service.use_local()

        self.git_service.commit_local_changes()

        self.git_service.push_changes_to_remote()

        return {'status': SyncStatus.UPLOADED_TO_CLOUD}
    
    def force_remote_sync(self):
        self.git_service.use_remote()

        self.git_service.commit_local_changes()

        self.git_service.push_changes_to_remote()

        return {'status': SyncStatus.UPLOADED_TO_CLOUD}

    def sync(self):

        local_changes = self.git_service.commit_local_changes()
        print(local_changes)

        pull_result = self.git_service.pull_remote_changes()
        
        if (pull_result == SyncStatus.MERGE_CONFLICT):
            return {'status': SyncStatus.MERGE_CONFLICT}
    
        self.git_service.push_changes_to_remote()
        
        if local_changes == SyncStatus.UPLOADED_TO_CLOUD:
            return {'status': SyncStatus.UPLOADED_TO_CLOUD}
        else:
            return {'status': pull_result}