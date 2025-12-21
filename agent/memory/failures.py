from typing import Dict

def persist_failure_to_store(failure_store, failure_doc: Dict):
    """
    Persist a failure event to the failure memory vector store.
    """
    failure_store.add_documents([failure_doc])

def retrieve_similar_failures(failure_store, signature: str, top_k: int = 3):
    """
    Retrieve similar past failures from the failure memory vector store.
    """
    return failure_store.similarity_search(
        query=signature,
        k=top_k,
    )