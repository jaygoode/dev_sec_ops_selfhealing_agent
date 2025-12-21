from langgraph.graph import StateGraph
from agent.confidence import calculate_confidence

graph = StateGraph(dict)
graph.add_node("run_scan", run_security_scan)
