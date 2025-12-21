import subprocess
import tempfile
import os
from pathlib import Path
import uuid
from datetime import datetime


def apply_fix(state: dict, repo_path: str = ".", mcp_tools: list = None) -> dict:
    """
    Apply the proposed fix in a temporary Git branch and optionally run MCP tools.

    Args:
        state (dict): Agent state containing 'proposed_fix_diff' and 'affected_files'.
        repo_path (str): Path to the repository where fixes are applied.
        mcp_tools (list): List of MCP tools to run (e.g., ["black", "bandit"]).

    Returns:
        dict: Updated state with keys:
            - 'fix_applied' (bool)
            - 'apply_errors' (list[str])
            - 'applied_branch' (str)
            - 'timestamp' (ISO string)
    """

    state["fix_applied"] = False
    state["apply_errors"] = []
    state["applied_branch"] = None
    state["timestamp"] = datetime.utcnow().isoformat()

    if mcp_tools is None:
        mcp_tools = ["black", "bandit"]


    proposed_diff = state.get("proposed_fix_diff")
    affected_files = state.get("affected_files", [])

    if not proposed_diff:
        state["apply_errors"].append("No proposed fix diff provided.")
        return state

    try:
        branch_name = f"selfheal-{uuid.uuid4().hex[:8]}"
        state["applied_branch"] = branch_name

        subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)

        patch_file = Path(repo_path) / f"{branch_name}.diff"
        patch_file.write_text(proposed_diff)

        result = subprocess.run(
            ["git", "apply", str(patch_file)],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            state["apply_errors"].append(f"Patch failed: {result.stderr}")
            subprocess.run(["git", "checkout", "-"], cwd=repo_path)
            subprocess.run(["git", "branch", "-D", branch_name], cwd=repo_path)
            return state

        for tool in mcp_tools:
            try:
                subprocess.run([tool, repo_path], check=True)
            except subprocess.CalledProcessError as e:
                state["apply_errors"].append(f"{tool} failed: {e}")

        state["fix_applied"] = True

    except Exception as e:
        state["apply_errors"].append(str(e))

    return state