from datetime import datetime
from agent.memory.failures import persist_failure_to_store, retrieve_similar_failures
from agent.memory.context import derive_failure_context

def persist_failure(state: dict, failure_store, top_k: int = 5) -> dict:
    """
    Persist a failure to the vector store if it is not a duplicate of recent failures.

    Deduplication ensures that identical failed fixes are not stored multiple times.
    
    Args:
        state (dict): Current agent state containing finding signature, proposed fix, and context.
        failure_store: The failure vector store instance (injected via graph).
        top_k (int): Number of similar failures to retrieve for duplicate checking.

    Returns:
        dict: Updated state, with 'failure_logged' indicating if the failure was persisted.
    """

    signature = state.get("finding_signature")
    proposed_fix = state.get("proposed_fix_diff")

    # Retrieve similar failures to check for duplicates
    similar_failures = retrieve_similar_failures(failure_store, signature, top_k=top_k)

    for doc in similar_failures:
        if doc.get("fix_diff") == proposed_fix:
            # Duplicate found, do not persist again
            state["failure_logged"] = False
            return state

    # No duplicate, create failure document
    failure_doc = {
        "finding_signature": signature,
        "fix_diff": proposed_fix,
        "failure_reason": state.get("failure_reason", "confidence_gate_reject"),
        "confidence": state.get("confidence"),
        "context_metadata": derive_failure_context(state),
        "timestamp": datetime.utcnow().isoformat(),
    }

    # Persist failure to vector store
    persist_failure_to_store(failure_store, failure_doc)

    state["failure_logged"] = True
    return state
