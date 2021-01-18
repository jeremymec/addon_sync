from git_service import GitService
from sync_status import SyncStatus
from enum import Enum, auto
import sys

class Sync:

    def __init__(self, base_path, remote_path):
        self.git_service = GitService(base_path, remote_path)

    def sync(self, resolve_conflict_with_local = False, resolve_conflict_with_remote = False):

        if resolve_conflict_with_local:
            self.git_service.use_local()
        elif resolve_conflict_with_remote:
            self.git_service.use_remote()

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