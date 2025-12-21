from typing import Dict

def persist_failure_to_store(failure_store, failure_doc: Dict):
    """
    Persist a failure event to the failure memory vector store.
    """
    failure_store.add_documents([failure_doc])