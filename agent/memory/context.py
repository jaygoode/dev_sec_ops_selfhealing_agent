def derive_failure_context(state) -> dict:
    return {
        "runtime": state.get("runtime", "unknown"),
        "framework": state.get("framework", "unknown"),
        "service_type": state.get("service_type", "unknown"),
        "breaking_changes_allowed": state.get("breaking_changes_allowed", False)
    }