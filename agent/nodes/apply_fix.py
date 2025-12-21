import subprocess
import uuid
from pathlib import Path
import os
from datetime import datetime

def apply_fix(state: dict, repo_path: str = ".", mcp_tools: list = None) -> dict:
    state["fix_applied"] = False
    state["apply_errors"] = []
    state["applied_branch"] = None
    state["timestamp"] = datetime.now(datetime.timezone.utc).isoformat()

    if mcp_tools is None:
        mcp_tools = ["black", "bandit"]

    diff_text = state.get("proposed_fix_diff")
    affected_files = state.get("affected_files", [])

    if not diff_text:
        state["apply_errors"].append("No proposed_fix_diff found in state")
        return state

    try:
        branch_name = f"selfheal-{uuid.uuid4().hex[:8]}"
        state["applied_branch"] = branch_name
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)

        # Ensure affected files exist (for new files)
        for f in affected_files:
            file_path = Path(repo_path) / f
            if not file_path.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.touch()

        # Save patch file
        patch_file = Path(repo_path) / f"{branch_name}.diff"
        patch_file.write_text(diff_text)

        # Apply patch
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

        # Run MCP tools only on affected files
        for tool in mcp_tools:
            try:
                cmd = [tool] + [str(Path(repo_path)/f) for f in affected_files] if affected_files else [tool, repo_path]
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                state["apply_errors"].append(f"{tool} failed: {e}")

        state["fix_applied"] = True

    except Exception as e:
        state["apply_errors"].append(str(e))

    return state
