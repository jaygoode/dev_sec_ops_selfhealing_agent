from agent.memory.remediation import retrieve_similar_remediations
from agent.memory.failures import retrieve_similar_failures

def retrieve_memory(
    state: dict,
    remediation_store,
    failure_store,
    top_k: int = 3,
) -> dict:
    signature = state["finding_signature"]

    successful_fixes = retrieve_similar_remediations(
        remediation_store=remediation_store,
        signature=signature,
        top_k=top_k,
    )

    failures = retrieve_similar_failures(
        failure_store=failure_store,
        signature=signature,
        top_k=top_k,
    )

    state["memory"] = {
        "successful_fixes": successful_fixes,
        "failures": failures,
    }

    return state
