from ..memory.failures import store_failure
from ..memory.remediation import retrieve_similar_fixes

def retrieve_memory(state):
    signature = state["finding_signature"]

    fixes = retrieve_similar_fixes(signature)
    failures = store_failure(signature)

    state["memory"] = {
        "successful_fixes": fixes,
        "failures": failures
    }

    return state