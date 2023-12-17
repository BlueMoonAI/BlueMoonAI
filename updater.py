import os
import subprocess

import pygit2
from packaging.version import Version
import json


def update_local_version(new_version):
    try:
        version_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "version.json")

        with open(version_file_path, "r") as f:
            data = json.load(f)

        data["version"] = new_version

        with open(version_file_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Local version updated to {new_version}.")
    except Exception as e:
        print(f"Error updating local version: {e}")


class Updater:
    def __init__(self):
        # Retrieve values from environment variables
        self.repo_url = os.environ.get("REPO_URL")
        self.branch_name = os.environ.get("BRANCH_NAME")
        self.local_version = os.environ.get("LOCAL_VERSION")
        self.autoupdate = os.environ.get("AUTOUPDATE", "True").lower() == "true"
        self.repo = None

    def initialize_repo(self):
        if not self.repo_url:
            print("Repository URL is not provided. Set the REPO_URL environment variable.")
            return

        try:
            import pygit2
            pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

            # Attempt to open the repository
            self.repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))
        except pygit2.GitError:
            # If the repository doesn't exist, attempt to clone it
            try:
                self.repo = pygit2.clone_repository(self.repo_url, os.path.abspath(os.path.dirname(__file__)))
            except pygit2.GitError as e:
                print(f"Error initializing repository: {e}")
                self.autoupdate = False
                # If the URL is broken, display a message and exit
                print(f"Error initializing repository: {e}")
                return

            if not self.repo.is_empty:
                print(f"Repository initialized successfully.")
            else:
                print(f"Error initializing repository. The repository is empty or not reachable.")
                self.autoupdate = False

    def git_pull(self):
        try:
            subprocess.run(["git", "pull"], cwd=os.path.abspath(os.path.dirname(__file__)), check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'git pull': {e}")
            raise

    def check_for_updates(self):
        if self.autoupdate and self.repo:
            try:
                remote_name = "origin"
                remote = self.repo.remotes[remote_name]
                remote.fetch()

                # Get the remote commit information
                remote_reference = f"refs/remotes/{remote_name}/{self.branch_name}"
                remote_commit = self.repo.revparse_single(remote_reference)

                # Check the version.json in the remote tree
                remote_version = None
                try:
                    # Get the remote tree
                    remote_tree = self.repo.get(remote_commit.tree_id)

                    # Find the version.json entry in the tree
                    for entry in remote_tree:
                        if entry.name == "version.json":
                            # Get the blob associated with the file
                            remote_blob = self.repo.get(entry.id)

                            # Extract the version information
                            remote_data = json.loads(remote_blob.data.decode("utf-8"))
                            if "version" in remote_data:
                                remote_version = remote_data["version"]
                            break
                    else:
                        # If version.json is not found, perform 'git pull' to get the latest updates
                        print("version.json not found in the remote repository.")
                        print("Pulling the latest updates...")
                        self.git_pull()
                        return
                except Exception as e:
                    print(f"Error reading remote version: {e}")

                # Compare versions and perform an update if necessary
                if remote_version and Version(remote_version) > Version(self.local_version):
                    print(f"Checking for updates... (Local version: {self.local_version}, Remote version: {remote_version})")
                    merge_result, _ = self.repo.merge_analysis(remote_commit.id)

                    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                        print("Checking successful. Already up-to-date.")
                    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
                        local_branch_ref = f"refs/heads/{self.branch_name}"
                        local_branch = self.repo.lookup_reference(local_branch_ref)
                        local_branch.set_target(remote_commit.id)
                        self.repo.head.set_target(remote_commit.id)
                        self.repo.checkout_tree(self.repo.get(remote_commit.id))
                        self.repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
                        print("Checking successful. Fast-forward merge. Update successful.")
                        print(f"Updated to version {remote_version}.")

                        # Update the local version in version.json
                        update_local_version(remote_version)
                        print("Local version successfully changed.")
                else:
                    print("Checking successful. Already up-to-date.")
            except ImportError:
                print("PyGit2 module not installed. Install it using 'pip install pygit2'")
                self.autoupdate = False

    def run_update(self):
        if not self.repo_url:
            print("Repository URL is not provided. Set the REPO_URL environment variable.")
            return

        if self.autoupdate:
            # Initialize the repository
            self.initialize_repo()

            # Check for updates
            if self.repo:
                try:
                    self.check_for_updates()
                except Exception as e:
                    print(f'Checking failed. Error: {e}')
                    self.autoupdate = False
            else:
                print("Repository not initialized. Update skipped.")

            if self.autoupdate:
                print('Checking and Autoupdate succeeded.')
            else:
                print('Checking and update skipped.')

# If you want to run this script independently for testing, uncomment the next lines
# updater = Updater()
# updater.run_update()
