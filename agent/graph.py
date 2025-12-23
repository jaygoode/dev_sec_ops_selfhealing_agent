from langgraph.graph import StateGraph
from agent.memory.vector_store import VectorStore

from agent.nodes.run_scan import run_security_scan
from agent.nodes.retrieve_memory import retrieve_memory
from agent.nodes.apply_fix import apply_fix
from agent.nodes.calculate_confidence import calculate_confidence
from agent.nodes.persist_failure import persist_failure
from agent.nodes.persist_success import persist_success
# from agent.nodes.run_tests import run_tests
# from agent.nodes.create_pr import create_pr
# from agent.nodes.request_human_review import request_human_review
# from agent.nodes.abort import abort_run

# ─────────────────────────────
# Confidence routing (single gate)
# ─────────────────────────────

def route_by_confidence(state: dict) -> str:
    c = state["confidence"]
    
    if c >= 0.85:
        return "persist_success"
    elif c >= 0.70:
        return "review_pr"
    elif c >= 0.50:
        return "record_failure"
    else:
        return "abort"

# ─────────────────────────────
# Composition root
# ─────────────────────────────
vector_store = VectorStore()
graph = StateGraph(dict)

# ─────────────────────────────
# Nodes (dependency injected)
# ─────────────────────────────
graph.add_node("run_scan", run_security_scan)

graph.add_node(
    "retrieve_memory",
    lambda state: retrieve_memory(
        state,
        remediation_store=vector_store.remediations,
        failure_store=vector_store.failures,
    )
)

graph.add_node(
    "apply_fix",
    lambda state: apply_fix(
        state,
        repo_path="/path/to/your/repo", #TODO Make dynamic
        mcp_tools=["black", "bandit"]   #TODO Make configurable
    )
)
# graph.add_node("run_tests", run_tests)
graph.add_node("calculate_confidence",calculate_confidence)
graph.add_node(
    "persist_failure",
    lambda state: persist_failure(
        state,
        failure_store=vector_store.failures
    )
)
graph.add_node(
    "persist_success",
    lambda state: persist_success(
        state,
        remediation_store=vector_store.remediations
    )
)

# graph.add_node("create_pr", create_pr)
# graph.add_node("request_human_review", request_human_review)
# graph.add_node("persist_success", persist_success)
# graph.add_node("abort", abort_run)

# ─────────────────────────────
# Edges (execution order)
# ─────────────────────────────
graph.set_entry_point("run_scan")
graph.add_edge("run_scan", "retrieve_memory")
graph.add_edge("retrieve_memory", "apply_fix")
graph.add_edge("apply_fix", "run_tests")
graph.add_edge("run_tests", "calculate_confidence")



graph.add_conditional_edges(
    "calculate_confidence",
    route_by_confidence,
    {
        "persist_success": "persist_success",
        "review_pr": "request_human_review",
        "record_failure": "persist_failure",
        "abort": "abort",
    }
)

# ─────────────────────────────
# Connect persistence to persist_success or retry
# ─────────────────────────────
graph.add_edge("persist_success", "persist_success")
graph.add_edge("create_pr", "persist_success")
graph.add_edge("request_human_review", "persist_success")
graph.add_edge("persist_failure", "apply_fix")
graph.add_edge("abort", "abort")

