from .vector_store import VectorStore
import uuid
from .context import derive_failure_context

store = VectorStore()

def store_failure(signature, attempted_fix, reason, confidence, state):
    context = derive_failure_context(state)

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

    