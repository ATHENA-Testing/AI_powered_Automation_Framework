"""
Git Manager for Python Automation Framework
Handles Git operations including status checks, commits, and pushes.
"""

import git
from git import Repo, InvalidGitRepositoryError
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

from src.config_manager import ConfigManager
from src.logger import log, LoggerMixin

class GitManager(LoggerMixin):
    """
    Manages Git operations for the automation framework.
    """

    def __init__(self, config: ConfigManager):
        """
        Initializes the GitManager.

        Args:
            config: An instance of ConfigManager for accessing configuration settings.
        """
        self.config = config
        self.auto_commit = self.config.get_boolean("GIT", "auto_commit")
        self.auto_push = self.config.get_boolean("GIT", "auto_push")
        self.commit_message_template = self.config.get("GIT", "commit_message_template")
        
        # Get the project root directory
        self.project_root = Path(__file__).parent.parent
        self.repo = None
        
        self._initialize_repo()
        self.logger.info("GitManager initialized")

    def _initialize_repo(self):
        """
        Initializes or loads the Git repository.
        """
        try:
            # Try to load existing repository
            self.repo = Repo(self.project_root)
            self.logger.info(f"Loaded existing Git repository at {self.project_root}")
        except InvalidGitRepositoryError:
            # Initialize new repository if none exists
            self.logger.info(f"No Git repository found. Initializing new repository at {self.project_root}")
            self.repo = Repo.init(self.project_root)
            
            # Create initial .gitignore
            gitignore_path = self.project_root / ".gitignore"
            if not gitignore_path.exists():
                gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# Screenshots
screenshots/
*.png
*.jpg
*.jpeg

# Temporary files
*.tmp
*.temp

# OS
.DS_Store
Thumbs.db

# Framework specific
knowledgebase/
reports/
testcase_generator/
testscript_generator/
"""
                with open(gitignore_path, 'w') as f:
                    f.write(gitignore_content.strip())
                
                self.logger.info("Created .gitignore file")

    def get_status(self) -> str:
        """
        Gets the current Git repository status.

        Returns:
            String representation of the repository status.
        """
        try:
            if not self.repo:
                return "No Git repository initialized"
            
            status_lines = []
            
            # Get current branch
            try:
                current_branch = self.repo.active_branch.name
                status_lines.append(f"Current branch: {current_branch}")
            except:
                status_lines.append("Current branch: (detached HEAD)")
            
            # Get modified files
            modified_files = [item.a_path for item in self.repo.index.diff(None)]
            if modified_files:
                status_lines.append(f"Modified files ({len(modified_files)}):")
                for file in modified_files[:10]:  # Limit to first 10
                    status_lines.append(f"  - {file}")
                if len(modified_files) > 10:
                    status_lines.append(f"  ... and {len(modified_files) - 10} more")
            else:
                status_lines.append("No modified files")
            
            # Get untracked files
            untracked_files = self.repo.untracked_files
            if untracked_files:
                status_lines.append(f"Untracked files ({len(untracked_files)}):")
                for file in untracked_files[:10]:  # Limit to first 10
                    status_lines.append(f"  - {file}")
                if len(untracked_files) > 10:
                    status_lines.append(f"  ... and {len(untracked_files) - 10} more")
            else:
                status_lines.append("No untracked files")
            
            # Get staged files
            staged_files = [item.a_path for item in self.repo.index.diff("HEAD")]
            if staged_files:
                status_lines.append(f"Staged files ({len(staged_files)}):")
                for file in staged_files[:10]:  # Limit to first 10
                    status_lines.append(f"  - {file}")
                if len(staged_files) > 10:
                    status_lines.append(f"  ... and {len(staged_files) - 10} more")
            else:
                status_lines.append("No staged files")
            
            return "\n".join(status_lines)
            
        except Exception as e:
            self.logger.error(f"Error getting Git status: {e}")
            return f"Error getting Git status: {e}"

    def get_modified_files(self) -> List[str]:
        """
        Gets a list of modified files in the repository.

        Returns:
            List of modified file paths.
        """
        try:
            if not self.repo:
                return []
            
            modified_files = []
            
            # Get modified files (working directory changes)
            for item in self.repo.index.diff(None):
                modified_files.append(item.a_path)
            
            # Get untracked files
            modified_files.extend(self.repo.untracked_files)
            
            # Get staged files
            for item in self.repo.index.diff("HEAD"):
                if item.a_path not in modified_files:
                    modified_files.append(item.a_path)
            
            return sorted(modified_files)
            
        except Exception as e:
            self.logger.error(f"Error getting modified files: {e}")
            return []

    def add_files(self, file_paths: List[str]) -> None:
        """
        Adds files to the Git staging area.

        Args:
            file_paths: List of file paths to add.
        """
        try:
            if not self.repo:
                raise Exception("No Git repository initialized")
            
            for file_path in file_paths:
                self.repo.index.add([file_path])
            
            self.logger.info(f"Added {len(file_paths)} files to staging area")
            
        except Exception as e:
            self.logger.error(f"Error adding files to Git: {e}")
            raise

    def commit_files(self, file_paths: List[str], commit_message: str) -> str:
        """
        Commits specified files with a given message.

        Args:
            file_paths: List of file paths to commit.
            commit_message: Commit message.

        Returns:
            Commit hash.
        """
        try:
            if not self.repo:
                raise Exception("No Git repository initialized")
            
            # Add files to staging area
            self.add_files(file_paths)
            
            # Commit the changes
            commit = self.repo.index.commit(commit_message)
            
            self.logger.info(f"Committed {len(file_paths)} files with message: '{commit_message}'")
            self.logger.info(f"Commit hash: {commit.hexsha}")
            
            return commit.hexsha
            
        except Exception as e:
            self.logger.error(f"Error committing files: {e}")
            raise

    def commit_all_changes(self, commit_message: str) -> str:
        """
        Commits all changes in the repository.

        Args:
            commit_message: Commit message.

        Returns:
            Commit hash.
        """
        try:
            if not self.repo:
                raise Exception("No Git repository initialized")
            
            # Add all changes
            self.repo.git.add(A=True)
            
            # Commit the changes
            commit = self.repo.index.commit(commit_message)
            
            self.logger.info(f"Committed all changes with message: '{commit_message}'")
            self.logger.info(f"Commit hash: {commit.hexsha}")
            
            return commit.hexsha
            
        except Exception as e:
            self.logger.error(f"Error committing all changes: {e}")
            raise

    def push_changes(self, remote_name: str = "origin", branch_name: str = None) -> None:
        """
        Pushes committed changes to the remote repository.

        Args:
            remote_name: Name of the remote repository.
            branch_name: Name of the branch to push. If None, uses current branch.
        """
        try:
            if not self.repo:
                raise Exception("No Git repository initialized")
            
            # Get current branch if not specified
            if branch_name is None:
                try:
                    branch_name = self.repo.active_branch.name
                except:
                    branch_name = "main"  # Default to main if no active branch
            
            # Check if remote exists
            if remote_name not in [remote.name for remote in self.repo.remotes]:
                self.logger.warning(f"Remote '{remote_name}' not found. Available remotes: {[r.name for r in self.repo.remotes]}")
                raise Exception(f"Remote '{remote_name}' not configured")
            
            # Push changes
            origin = self.repo.remote(remote_name)
            origin.push(branch_name)
            
            self.logger.info(f"Successfully pushed changes to {remote_name}/{branch_name}")
            
        except Exception as e:
            self.logger.error(f"Error pushing changes: {e}")
            raise

    def auto_commit_on_success(self) -> str:
        """
        Performs an automatic commit when all tests pass successfully.

        Returns:
            Commit hash if successful.
        """
        try:
            if not self.auto_commit:
                raise Exception("Auto-commit is disabled in configuration")
            
            # Generate commit message with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = self.commit_message_template.format(timestamp=timestamp)
            
            # Commit all changes
            commit_hash = self.commit_all_changes(commit_message)
            
            # Auto-push if enabled
            if self.auto_push:
                try:
                    self.push_changes()
                    self.logger.info("Auto-push completed successfully")
                except Exception as e:
                    self.logger.warning(f"Auto-push failed: {e}")
            
            return commit_hash
            
        except Exception as e:
            self.logger.error(f"Auto-commit failed: {e}")
            raise

    def create_branch(self, branch_name: str) -> None:
        """
        Creates a new branch.

        Args:
            branch_name: Name of the new branch.
        """
        try:
            if not self.repo:
                raise Exception("No Git repository initialized")
            
            new_branch = self.repo.create_head(branch_name)
            self.logger.info(f"Created new branch: {branch_name}")
            
        except Exception as e:
            self.logger.error(f"Error creating branch: {e}")
            raise

    def switch_branch(self, branch_name: str) -> None:
        """
        Switches to a different branch.

        Args:
            branch_name: Name of the branch to switch to.
        """
        try:
            if not self.repo:
                raise Exception("No Git repository initialized")
            
            self.repo.git.checkout(branch_name)
            self.logger.info(f"Switched to branch: {branch_name}")
            
        except Exception as e:
            self.logger.error(f"Error switching branch: {e}")
            raise

    def get_commit_history(self, max_count: int = 10) -> List[Dict[str, Any]]:
        """
        Gets the commit history.

        Args:
            max_count: Maximum number of commits to retrieve.

        Returns:
            List of commit information dictionaries.
        """
        try:
            if not self.repo:
                return []
            
            commits = []
            for commit in self.repo.iter_commits(max_count=max_count):
                commits.append({
                    "hash": commit.hexsha[:8],
                    "message": commit.message.strip(),
                    "author": str(commit.author),
                    "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "files_changed": len(commit.stats.files)
                })
            
            return commits
            
        except Exception as e:
            self.logger.error(f"Error getting commit history: {e}")
            return []

    def add_remote(self, remote_name: str, remote_url: str) -> None:
        """
        Adds a remote repository.

        Args:
            remote_name: Name for the remote.
            remote_url: URL of the remote repository.
        """
        try:
            if not self.repo:
                raise Exception("No Git repository initialized")
            
            self.repo.create_remote(remote_name, remote_url)
            self.logger.info(f"Added remote '{remote_name}': {remote_url}")
            
        except Exception as e:
            self.logger.error(f"Error adding remote: {e}")
            raise

# Example Usage (for testing purposes)
if __name__ == "__main__":
    # Assuming config.ini is in the parent directory
    current_dir = Path(__file__).parent
    config_path = current_dir.parent / "config.ini"
    
    # Initialize ConfigManager with the correct path
    cfg_manager = ConfigManager(config_path=str(config_path))
    git_manager = GitManager(cfg_manager)

    print("\n--- Git Status ---")
    status = git_manager.get_status()
    print(status)

    print("\n--- Modified Files ---")
    modified_files = git_manager.get_modified_files()
    print("Modified files:", modified_files)

    print("\n--- Commit History ---")
    history = git_manager.get_commit_history(5)
    for commit in history:
        print(f"{commit['hash']} - {commit['message']} ({commit['date']})")

    print("\n--- Git Integration Demo Complete ---")

