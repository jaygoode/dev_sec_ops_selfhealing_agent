def retrieve_memory(
    state: dict,
    remediation_store,
    failure_store,
    top_k: int = 3,
) -> dict:
    """
    Retrieve relevant historical remediation and failure memory
    for the current security finding.
    """

    signature = state["finding_signature"]

    successful_fixes = remediation_store.similarity_search(
        query=signature,
        k=top_k,
    )

    failures = failure_store.similarity_search(
        query=signature,
        k=top_k,
    )

    state["memory"] = {
        "successful_fixes": successful_fixes,
        "failures": failures,
    }

    return state