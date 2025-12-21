from agent.tools.registry import TOOLS

def run_security_scan(state):
    tools = TOOLS["sast"]
    result = tools.run({"path": "app/"})

    state["scan_results"] = result
    state["findings"] = result.get("findings", [])

    return state

