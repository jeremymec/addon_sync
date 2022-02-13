
from git_service import GitService, InitRepoResult
from sync_status import SyncStatus


class Sync:
    def __init__(self, git_service, base_path, remote_path):
        self.git_service = git_service

    @staticmethod
    def create_sync(base_path, remote_path, objects_tracked):

        service_create_result = GitService.create_service(
            base_path, remote_path, objects_tracked)

        git_service = service_create_result["service"]

        result = service_create_result["result"]
        status = None

        if result == InitRepoResult.UPLOAD_TO_BLANK_REPO:
            status = SyncStatus.UPLOADED_TO_CLOUD
        elif result == InitRepoResult.CLONE_REPO:
            status = SyncStatus.UPDATED_FROM_CLOUD

        sync = Sync(git_service, base_path, remote_path)
        return {"sync": sync, "status": status}

    def force_local_sync(self):
        self.git_service.use_local()

        self.git_service.commit_local_changes()

        self.git_service.push_changes_to_remote()

        return {"status": SyncStatus.UPLOADED_TO_CLOUD}

    def force_remote_sync(self):
        self.git_service.use_remote()

        self.git_service.commit_local_changes()

        self.git_service.push_changes_to_remote()

        return {"status": SyncStatus.UPLOADED_TO_CLOUD}

    def sync(self):

        local_changes = self.git_service.commit_local_changes()
        print(local_changes)

        pull_result = self.git_service.pull_remote_changes()

        if pull_result == SyncStatus.MERGE_CONFLICT:
            return {"status": SyncStatus.MERGE_CONFLICT}

        self.git_service.push_changes_to_remote()

        if local_changes == SyncStatus.UPLOADED_TO_CLOUD:
            return {"status": SyncStatus.UPLOADED_TO_CLOUD}
        else:
            return {"status": pull_result}
