from datetime import datetime
from agent.memory.failures import persist_failure_to_store
from agent.memory.context import derive_failure_context

def persist_failure(state: dict, failure_store) -> dict:
    failure_doc = {
        "finding_signature": state["finding_signature"],
        "fix_diff": state["proposed_fix_diff"],
        "failure_reason": state.get("failure_reason", "confidence_gate_reject"),
        "confidence": state.get("confidence"),
        "context_metadata": derive_failure_context(state),
        "timestamp": datetime.utcnow().isoformat(),
    }

    persist_failure_to_store(failure_store, failure_doc)

    state["failure_logged"] = True
    return state