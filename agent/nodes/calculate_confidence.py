from typing import Dict

def calculate_confidence(state: Dict) -> Dict:
    """
    Calculate a deterministic confidence score for a security remediation action
    based on observed outcomes and historical evidence.

    This function evaluates the likelihood that an applied fix is safe to promote
    by analyzing the following factors:

    - Finding delta: A reduction in security findings increases confidence;
    no change or an increase reduces confidence.
    - Test results: Failed tests strongly penalize confidence; low coverage
    applies an additional penalty.
    - Historical success memory: The presence of similar previously successful
    fixes slightly boosts confidence.
    - Historical failure memory: The presence of similar past failures significantly
    penalizes confidence.
    - Change size: Larger change surfaces (more affected files) reduce confidence.

    The confidence score starts at 1.0 and is adjusted using fixed heuristic weights.
    The final value is clamped between 0.0 and 1.0. Any detected concerns are recorded
    as structured risk factors for auditability.

    Args:
        state (Dict): A dictionary containing execution state, including:
            - "finding_delta" (int): Difference in the number of security findings
            before and after remediation (negative indicates improvement).
            - "test_results" (Dict): Test outcomes containing:
                - "passed" (bool): Whether all tests passed
                - "coverage" (int): Test coverage percentage
            - "memory" (Dict): Historical experience data with:
                - "successful_fixes": Retrieved similar successful remediations
                - "failures": Retrieved similar failed attempts
            - "affected_files" (List[str]): Files modified by the remediation

    Returns:
        Dict: The updated state dictionary with:
            - "confidence" (float): Calculated confidence score (0.0–1.0)
            - "risk_factors" (List[str]): Identified risk signals affecting confidence
    """
    confidence = 1.0
    risk_factors = []


    #1. FINDING DELTA
    delta = state.get("finding_delta", 0)

    if delta < 0:
        confidence += 0.15
    elif delta == 0:
        confidence -= 0.10
        risk_factors.append("no_finding_reduction")
    else:
        confidence -= 0.30
        risk_factors.append("new_findings_introduced")

    #2. TEST RESULTS 
    tests = state.get("test_results", {})
    if not tests.get("passed", False):
        confidence -= 0.40
        risk_factors.append("tests_failed")

    coverage = tests.get("coverage", 0)
    if coverage < 80:
        confidence -= 0.10
        risk_factors.append("low_test_coverage")

    #3. MEMORY SIMILARITY
    memory = state.get("memory", {})
    fixes = memory.get("successful_fixes", {})

    if fixes.get("documents"):
        confidence += 0.10
    else:
        confidence -= 0.05
        risk_factors.append("no_prior_success")
    
    #4. FAILURE OVERLAP
    failures = memory.get("failures", {})
    if failures.get("documents"):
        confidence -= 0.25
        risk_factors.append("similar_past_failure")

    # 5. CHANGE SIZE HEURISTIC
    files_changed = len(state.get("affected_files", []))
    if files_changed > 3:
        confidence -= 0.10
        risk_factors.append("large_change_surface")

    # 6. CLAMP CONFIDENCE
    confidence = max(0.0, min(confidence, 1.0))

    state["confidence"] = round(confidence, 2)
    state["risk_factors"] = risk_factors

    return state