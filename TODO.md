add derive context function for remediation vector store as well?
 instead of adding context, maybe this?:
 Retrieval With Context Awareness (Advanced but Clean)

    You do not embed context.

    You filter on it.

    Example:

    store.failures.query(
        query_texts=[signature],
        n_results=2,
        where={"framework": "flask"}
    )


understand the confidence model
