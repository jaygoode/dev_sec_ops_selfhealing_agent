from .vector_store import VectorStore
import uuid

store = VectorStore()

def store_successful_remediation(signature, remediation_type, files, confidence, delta):
    #TODO do we want to add context here as well?
    store.remediation.add(
        documents=[signature],
        metadatas=[{
            "remediation_type": remediation_type,
            "files": files,
            "confidence": confidence,
            "delta": delta,
            "outcome": "merged"
        }],
        ids=[str(uuid.uuid4())]
    )

def retrieve_similar_remediations(signature, top_k=3):
    return store.remediation.query(
        query_texts=[signature],
        n_results=top_k
    )

