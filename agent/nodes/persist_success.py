from datetime import datetime
from agent.memory.remediation import persist_successful_remediation

def persist_success(state: dict, remediation_store) -> dict:
    """
    Persist a successful remediation after a high-confidence fix.
    """
    remediation_doc = {
        "finding_signature": state["finding_signature"],
        "fix_diff": state["proposed_fix_diff"],
        "files": state.get("affected_files", []),
        "confidence": state.get("confidence"),
        "delta": state.get("finding_delta"),
        "outcome": "merged",
        "timestamp": datetime.now().isoformat(),
    }

    persist_successful_remediation(remediation_store, remediation_doc)

    state["success_logged"] = True
    return state