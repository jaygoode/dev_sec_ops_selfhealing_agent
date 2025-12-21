import subprocess
import tempfile
import os
from pathlib import Path

def apply_fix(state: dict) -> dict:
    """
    Apply the proposed fix to the codebase.

    Args:
        state (dict): Must contain 'proposed_fix_diff' and optionally 'affected_files'

    Returns:
        dict: Updated state with 'fix_applied' and 'apply_errors'
    """
    state["fix_applied"] = False
    state["apply_errors"] = []

    diff_text = state.get("proposed_fix_diff")
    if not diff_text:
        state["apply_errors"].append("No proposed fix diff provided.")
        return state
    
    try:
        temp_dir = tempfile.mkdtemp()
        for f in state.get("affected_files", []):
            target_file = Path(f)
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.touch()

        diff_file_path = Path(temp_dir) / "patch.diff"
        diff_file_path.write_text(diff_text)

        result = subprocess.run(
            ["patch", "-p1", "-i", str(diff_file_path)],
            cwd=os.getcwd(),
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            state["apply_errors"].append(result.stderr)
            return state

        mcp_tools = state.get("mcp_tools", ["black", "bandit"])
        for tool in mcp_tools:
            try:
                subprocess.run([tool, "."], check=True)
            except subprocess.CalledProcessError as e:
                state["apply_errors"].append(f"{tool} failed: {e}")

        state["fix_applied"] = True
    except Exception as e:
        state["apply_errors"].append(str(e))
    
    return state