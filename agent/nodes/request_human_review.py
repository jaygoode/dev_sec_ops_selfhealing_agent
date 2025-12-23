import subprocess
import tempfile
import os
import requests
from datetime import datetime, timezone


def request_human_review(state: dict, repo_path: str) -> dict:
    """
    Create a draft PR and request human review for a medium-confidence fix.
    """

    diff = state["proposed_fix_diff"]
    signature = state["finding_signature"]
    confidence = state["confidence"]
    reasoning = state.get("fix_reasoning", "")
    branch_name = f"review-fix/{signature[:40]}"
    base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(diff)
        diff_path = temp_file.name

    subprocess.run(
        ["git", "apply", diff_path],
        cwd=repo_path,
        check=True
    )

    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)

    commit_msg = f"[REVIEW] Auto-fix for {signature} with confidence {confidence:.2f}"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_path, check=True)
    subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=repo_path, check=True)

    repo = os.environ["GITHUB_REPO"]
    token = os.environ["GITHUB_TOKEN"]

    pr_payload = {
        "title": f"[REVIEW] Auto-fix: {signature}",
        "head": branch_name,
        "base": base_branch,
        "draft": True,
        "body": (
            "⚠️ **Human review required**\n\n"
            f"Confidence score: {confidence:.2f}\n\n"
            f"LLM reasoning:\n{reasoning}\n\n"
            f"Generated at: {datetime.now(timezone.utc).isoformat()}"
        ),
    }

    resp = requests.post(
        f"https://api.github.com/repos/{repo}/pulls",
        json=pr_payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10,
    )
    resp.raise_for_status()
    pr_url = resp.json()["html_url"]
    issue_number = resp.json()["number"]

    requests.post(
        f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels",
        json={"labels": ["security", "needs-review", "ai-generated"]},
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10,
    )

    state["pr_url"] = pr_url
    state["review_requested"] = True

    return state
