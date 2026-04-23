import subprocess

class GitService:
    """ Service to interact with Git repositories. """

    @staticmethod
    def get_git_status(repo_path: str) -> str:
        """ Get the status of the Git repository. """
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "status"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
        
    @staticmethod
    def get_git_remote_url(repo_path: str) -> str:
        """ Get the remote URL of the Git repository. """
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "remote", "get-url", "origin"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"