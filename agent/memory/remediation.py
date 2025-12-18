from .vector_store import VectorStore
import uuid

store = VectorStore()

def store_successful_fix(signature, fix_type, files, confidence, delta):
    store.remediation.add(
        documents=[signature],
        metadatas=[{
            "fix_type": fix_type,
            "files": files,
            "confidence": confidence,
            "delta": delta,
            "outcome": "merged"
        }],
        ids=[str(uuid.uuid4())]
    )

def retrieve_similar_fixes(signature, top_k=3):
    return store.remediation.query(
        query_texts=[signature],
        n_results=top_k
    )

def store_failure(signature, attempted_fix, reason, confidence, context):
    store.failures.add(
        documents=[signature],
        metadatas=[{
            "attempted_fix": attempted_fix,
            "reason": reason,
            "confidence": confidence,
            "context": context
        }],
        ids=[str(uuid.uuid4())]
    )

    