from agent.memory.remediation import retrieve_similar_remediations
from agent.memory.failures import retrieve_similar_failures
from pathlib import Path
import json
from ollama import Ollama


def generate_fix(state: dict, remediation_store, failure_store, model_name:str) -> dict:
    """
    Generate a proposed code fix (patch) for a security or test finding.

    Args:
        state (dict): Current state containing 'finding_signature' and optionally
                      context such as 'scanner_output' or 'test_results'.
        remediation_store: Vector store for successful remediations.
        failure_store: Vector store for previous failures.
        llm_client: LLM interface to generate code fixes.

    Returns:
        dict: Updated state with keys:
            - 'proposed_fix_diff': generated diff/patch
            - 'affected_files': list of files touched
            - 'fix_reasoning': explanation of fix
    """
    signature = state.get("finding_signature")
    if not signature:
        state["proposed_fix_diff"] = None
        state["affected_files"] = []
        state["fix_reasoning"] = "No finding_signature provided."
        return state
    
    similar_success = retrieve_similar_remediations(remediation_store, signature, top_k=3)
    similar_failures = retrieve_similar_failures(failure_store, signature, top_k=3)

    memory_context = {
        "successes": [doc for doc in similar_success],
        "failures": [doc for doc in similar_failures]
    }

    prompt = f"""
            You are an AI code remediation assistant.
            A security finding has been detected with signature: {signature}

            Context:
            Successes: {memory_context['successes']}
            Failures: {memory_context['failures']}

            Please output a JSON object with the following keys:
            - "diff": a unified diff string for the fix
            - "files": list of affected files
            - "reasoning": explanation of your fix
            Only return JSON, do not include any other text.
            """
    
    #TODO use schema with structured output parsing
    client = Ollama(model_name)
    raw_response = client.chat(prompt)

    try:
        parsed = json.loads(raw_response)
        proposed_fix_diff = parsed.get("diff")
        affected_files = parsed.get("files", [])
        fix_reasoning = parsed.get("reasoning", "")
    except Exception as e:
        proposed_fix_diff = None
        affected_files = []
        fix_reasoning = f"Error generating fix: {str(e)}"

    state["proposed_fix_diff"] = proposed_fix_diff
    state["affected_files"] = affected_files
    state["fix_reasoning"] = fix_reasoning

    return state