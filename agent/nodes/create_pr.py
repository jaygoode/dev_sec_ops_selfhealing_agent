import subprocess
import tempfile
import os
import requests
from datetime import datetime, timezone


def create_pr(state: dict, repo_path: str) -> dict:
    """
    Creates a pull request with the proposed fix.
    """
    
    diff = state["proposed_fix_diff"]
    signature = state["finding_signature"]
    confidence = state["confidence"]
    branch_name = f"auto-fix/{signature[:40]}"
    base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
    
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_diff_file:
        temp_diff_file.write(diff)
        temp_diff_file_path = temp_diff_file.name
        
        subprocess.run(
            ["git", "apply", temp_diff_file_path],
            cwd=repo_path,
            check=True
        )
        
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    
    commit_message = f"Auto-fix for {signature} with confidence {confidence:.2f}"
    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
    subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=repo_path, check=True)
    
    repo = os.getenv("GITHUB_REPOSITORY")
    token = os.getenv("GITHUB_TOKEN")
    
    pr_payload = {
        "title": f"Auto-fix: {signature}",
        "head": branch_name,
        "base": base_branch,
        "body": (
            f"This PR proposes an automatic fix for the issue identified by signature {signature}.\n\n"
            f"Confidence Level: {confidence:.2f}\n\n"
            f"Generated at: {datetime.now().isoformat()}"
        )
    }
    
    response = requests.post(
        f"https://api.github.com/repos/{repo}/pulls",
        json=pr_payload,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        },
        timeout=10
    )
    
    response.raise_for_status()
    
    state["pr_url"] = response.json().get("html_url")
    state["pr_created"] = True
    
    return state