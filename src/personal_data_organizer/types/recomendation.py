from enum import Enum 

class Recomendation(Enum):
    KEEP = "keep"
    DELETE = "delete"
    DELETE_LOCAL_COPY = "delete_local_copy"  # Safe: already on GitHub
    PUSH_THEN_DELETE = "push_then_delete"  # Safe: just push commits
    REVIEW_UNCOMMITTED = "review_uncommitted"  # Manual: check changes first
    UPLOAD_TO_GITHUB = "upload_to_github"  # Manual: create repo
    CLEAN_DEPENDENCIES = "clean_dependencies"  # Auto: delete node_modules/venv
    REVIEW_UNDOCUMENTED = "review_undocumented"  # Manual: no README