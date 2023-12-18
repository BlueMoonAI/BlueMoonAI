import os
import subprocess
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
        self.repo_dir = os.path.abspath(os.path.dirname(__file__))

        # Initialize autoupdate to True if not provided in environment variables
        if self.autoupdate is None:
            self.autoupdate = True

    def initialize_repo(self):
        if not self.repo_url:
            print("Repository URL is not provided. Set the REPO_URL environment variable.")
            return

        # Check if the repository exists
        if not os.path.exists(os.path.join(self.repo_dir, ".git")):
            # If it doesn't exist, initialize a new repository, add the remote, and fetch
            try:
                subprocess.run(["git", "init", self.repo_dir], check=True)
                subprocess.run(["git", "remote", "add", "origin", self.repo_url], cwd=self.repo_dir, check=True)
                subprocess.run(["git", "fetch", "--depth=1", "--no-tags"], cwd=self.repo_dir, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error initializing repository: {e}")
                self.autoupdate = False
                return

            print("Repository initialized successfully.")

    def git_pull(self):
        try:
            subprocess.run(["git", "pull", "--ff-only"], cwd=self.repo_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'git pull': {e}")
            raise

    def check_for_updates(self):
        if self.autoupdate:
            try:
                # Fetch the latest changes
                subprocess.run(["git", "fetch", "--depth=1", "--no-tags"], cwd=self.repo_dir, check=True)

                # Get the local and remote commit hashes
                local_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                                            cwd=self.repo_dir, text=True).strip()
                remote_commit_hash = subprocess.check_output(["git", "rev-parse", f"origin/{self.branch_name}"],
                                                             cwd=self.repo_dir, text=True).strip()

                # Check if the local branch is behind the remote branch
                if local_commit_hash != remote_commit_hash:
                    print(f"Checking for updates... (Local version: {self.local_version}, Remote version: Unknown)")

                    # Perform 'git pull' to get the latest updates
                    print("Pulling the latest updates...")
                    self.git_pull()

                    # Update the local version using the latest commit hash
                    update_local_version(remote_commit_hash)
                    print("Local version successfully changed.")
                else:
                    print("Checking successful. Already up-to-date. No new commits available.")
            except Exception as e:
                print(f"Error checking for updates: {e}")

    def run_update(self):
        if not self.repo_url:
            print("Repository URL is not provided. Set the REPO_URL environment variable.")
            return

        if self.autoupdate:
            # Initialize the repository
            self.initialize_repo()

            # Check for updates
            if os.path.exists(os.path.join(self.repo_dir, ".git")):
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
