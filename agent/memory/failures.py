from .vector_store import VectorStore
import uuid

store = VectorStore()

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

    