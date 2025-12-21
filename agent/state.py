

class AgentState(TypedDict):
    repo: str
    branch: str
    scan_results: dict
    findings: list
    affected_files: list
    proposed_fix: dict
    test_results: dict
    finding_delta: int
    confidence: float
    decision: str

