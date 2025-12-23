from datetime import datetime, timezone

def abort(state: dict) -> dict:
    """
    Abort execution due to low confidence or unsafe conditions.
    """

    state["aborted"] = True
    state["status"] = "aborted"

    state["abort_reason"] = state.get(
        "abort_reason",
        "Confidence below minimum threshold for safe automation"
    )

    state["aborted_at"] = datetime.now(timezone.utc).isoformat()

    return state