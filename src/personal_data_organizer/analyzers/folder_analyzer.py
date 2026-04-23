from dataclasses import dataclass
import os
from pathlib import Path
from personal_data_organizer.services import GitService
from personal_data_organizer.types import Recomendation

@dataclass
class FolderAnalysis:

    """ Data class to hold folder analysis results. """
    path: Path
    size: int
    file_count: int
    is_empty: bool

    # Detect if the folder is a software engineering project
    is_git_repo: bool
    has_uncommitted_changes: bool
    has_unpushed_commits: bool
    remote_url: str

    # Detect type of project (e.g., Python, JavaScript, etc.)
    has_node_modules: bool
    has_venv: bool
    has_pycache: bool
    has_readme: bool

    # Recomendations based on analysis
    recommendations: Recomendation



class FolderAnalyzer:

    """ Analyze folders to determinate what to do with them. """\
    
    def __init__(self, path: Path):
        self.path = path.resolve()

    def analyze(self) -> FolderAnalysis:
        """ Analyze the folder and return a FolderAnalysis object. """
        size = self.get_folder_size()
        file_count = self.get_file_count()
        is_empty = self.is_empty()

        is_git_repo = self.is_git_repository()
        has_uncommitted_changes = self.has_uncommitted_changes() if is_git_repo else False
        has_unpushed_commits = self.has_unpushed_commits() if is_git_repo else False
        remote_url = self.get_remote_url() if is_git_repo else ""

        has_node_modules = (self.path / "node_modules").exists()
        has_venv = (self.path / "venv").exists() or (self.path / ".venv").exists()
        has_pycache = any((self.path / d).exists() for d in ["__pycache__", "build", "dist"])
        has_readme = any((self.path / f).exists() for f in ["README.md", "README.txt", "README"])

        recommendations = self.generate_recommendations(
            size, file_count, is_empty, is_git_repo, has_uncommitted_changes,
            has_unpushed_commits, remote_url, has_node_modules, has_venv,
            has_pycache, has_readme
        )

        return FolderAnalysis(
            path=self.path,
            size=size,
            file_count=file_count,
            is_empty=is_empty,
            is_git_repo=is_git_repo,
            has_uncommitted_changes=has_uncommitted_changes,
            has_unpushed_commits=has_unpushed_commits,
            remote_url=remote_url,
            has_node_modules=has_node_modules,
            has_venv=has_venv,
            has_pycache=has_pycache,
            has_readme=has_readme,
            recommendations=recommendations
        )


    def get_folder_size(self) -> int:
        """ Calculate the total size of the folder. """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
    
    def get_file_count(self) -> int:
        """ Calculate the total number of files in the folder. """
        return sum(len(filenames) for dirpath, dirnames, filenames in os.walk(self.path))

    def is_empty(self) -> bool:
        """ Check if the folder is empty. """
        return self.get_file_count() == 0
    
    def is_git_repository(self) -> bool:
        """ Check if the folder is a git repository. """
        return (self.path / ".git").exists()
    
    def has_uncommitted_changes(self) -> bool:
        """ Check if there are uncommitted changes in the git repository. """
        status = GitService.get_git_status(str(self.path))
        return "nothing to commit" not in status.lower()
    
    def has_unpushed_commits(self) -> bool:
        """ Check if there are unpushed commits in the git repository. """
        status = GitService.get_git_status(str(self.path))
        if "Your branch is ahead of" in status:
            return True
        return False
    
    def get_remote_url(self) -> str:
        """ Get the remote URL of the git repository. """
        return GitService.get_git_remote_url(str(self.path))
    
    def generate_recommendations(self, size: int, file_count: int, is_empty: bool,
                                 is_git_repo: bool, has_uncommitted_changes: bool,
                                 has_unpushed_commits: bool, remote_url: str,
                                 has_node_modules: bool, has_venv: bool,
                                 has_pycache: bool, has_readme: bool) -> Recomendation:
        """ Generate recommendations based on the analysis. """
        # Empty folders can be deleted
        if is_empty:
            return Recomendation.DELETE
        
        # Git repo with remote (already on cloud)
        if is_git_repo and remote_url:
            if has_uncommitted_changes:
                return Recomendation.REVIEW_UNCOMMITTED  # Don't auto-commit
            if has_unpushed_commits:
                return Recomendation.PUSH_THEN_DELETE  # Safe: commits are ready
            # Clean, synced with remote
            return Recomendation.DELETE_LOCAL_COPY  # Safe to delete
        
        # Git repo without remote (not on cloud)
        if is_git_repo and not remote_url:
            return Recomendation.UPLOAD_TO_GITHUB  # Need to create repo first
        
        # Not a git repo but has dependencies
        if has_node_modules or has_venv or has_pycache:
            return Recomendation.CLEAN_DEPENDENCIES
        
        # Not a git repo, no README
        if not has_readme:
            return Recomendation.REVIEW_UNDOCUMENTED  # Might be garbage
        
        return Recomendation.KEEP