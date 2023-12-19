import os
import subprocess

from bluemoon.utils.logly import logly

class Updater:
    def __init__(self):
        # Retrieve values from environment variables
        self.repo_url = os.environ.get("REPO_URL")
        self.branch_name = os.environ.get("BRANCH_NAME")
        self.autoupdate = os.environ.get("AUTOUPDATE", "True").lower() == "true"
        self.repo_dir = os.path.abspath(os.path.dirname(__file__))

        # Initialize autoupdate to True if not provided in environment variables
        if self.autoupdate is None:
            self.autoupdate = True

    def initialize_repo(self):
        if not self.repo_url:
            logly.warn("Repository URL is not provided. Set the REPO_URL environment variable.")
            return

        # Check if the repository exists
        if not os.path.exists(os.path.join(self.repo_dir, ".git")):
            # If it doesn't exist, initialize a new repository, add the remote, and fetch
            try:
                subprocess.run(["git", "init", self.repo_dir], check=True)
                subprocess.run(["git", "remote", "add", "origin", self.repo_url], cwd=self.repo_dir, check=True)
                subprocess.run(["git", "fetch", "--depth=1", "--no-tags"], cwd=self.repo_dir, check=True)
            except subprocess.CalledProcessError as e:
                logly.error(f"Error initializing repository: {e}")
                self.autoupdate = False
                return

            logly.info("Repository initialized successfully.")

    def git_reset(self):
        try:
            # Reset local branch to the latest commit on the remote branch, handling unrelated histories
            subprocess.run(["git", "fetch", "--all"], cwd=self.repo_dir, check=True)
            subprocess.run(["git", "reset", "--hard", f"origin/{self.branch_name}"], cwd=self.repo_dir, check=True)
            logly.info("successfully updated to the latest version")
        except subprocess.CalledProcessError as e:
            logly.error(f"Error resetting local branch: {e}")

    def run_update(self):
        if not self.repo_url:
            logly.error("Repository URL is not provided. Set the REPO_URL environment variable.")
            return

        if self.autoupdate:
            # Initialize the repository
            self.initialize_repo()

            # Check for updates
            if os.path.exists(os.path.join(self.repo_dir, ".git")):
                try:
                    # Reset local branch to the latest commit on the remote branch
                    self.git_reset()
                except Exception as e:
                    logly.warn(f'Checking and update failed. Error: {e}')
                    self.autoupdate = False
            else:
                logly.warn("Repository not initialized. Update skipped.")

            if self.autoupdate:
                logly.info('Checking and Autoupdate succeeded.')
            else:
                logly.info('Checking and update skipped.')

# If you want to run this script independently for testing, uncomment the next lines
# updater = Updater()
# updater.run_update()
