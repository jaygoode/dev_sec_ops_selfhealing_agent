from langgraph.graph import StateGraph
from agent.confidence import calculate_confidence
from agent.nodes.run_scan import run_security_scan
from agent.nodes.retrieve_memory import retrieve_memory

graph = StateGraph(dict)
graph.add_node("run_scan", run_security_scan)
graph.add_node("retrieve_memory", retrieve_memory)
graph.add_node("calculate_confidence", calculate_confidence)
graph.add_node("apply_fix", apply_fix)
graph.add_node("run_tests", run_tests)
graph.add_node("create_pr", create_pr)
graph.add_node("request_human_review", request_human_review)
graph.add_node("abort", abort_run)

def confidence_gate(state:dict) -> str:
    c = state["confidence"]

    if c >= 0.85:
        return "auto_pr"
    elif c >= 0.70:
        return "review_pr"
    elif c >= 0.50:
        return "human_approval"
    else:
        return "abort"
    