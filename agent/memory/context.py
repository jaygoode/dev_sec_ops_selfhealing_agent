def derive_failure_context(state) -> dict:
    return {
        "runtime": state.get("runtime", "unknown"),
        "framework": state.get("framework", "unknown"),
        "service_type": state.get("service_type", "unknown"),
        "breaking_changes_allowed": state.get("breaking_changes_allowed", False)
    }

#TODO is this better? or what do i want for data
# def derive_failure_context(state: dict) -> dict:
#     return {
#         "language": state.get("language"),
#         "framework": state.get("framework"),
#         "scanner": state.get("scanner"),
#         "severity": state.get("severity"),
#     }