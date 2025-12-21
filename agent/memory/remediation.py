from typing import Dict

def persist_successful_remediation(remediation_store, remediation_doc: Dict):
    """
    Persist a successful remediation to the remediation memory store.
    """
    remediation_store.add_documents([remediation_doc])


def retrieve_similar_remediations(
    remediation_store,
    signature: str,
    top_k: int = 3,
):
    """
    Retrieve similar successful remediations from memory.
    """
    return remediation_store.similarity_search(
        query=signature,
        k=top_k,
    )