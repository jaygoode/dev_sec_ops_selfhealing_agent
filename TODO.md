add derive context function for remediation vector store as well?
 instead of adding context, maybe this?:
 Retrieval With Context Awareness (Advanced but Clean)

    You do not embed context.

    You filter on it.

    Example:

    store.failures.query(
        query_texts=[signature],
        n_results=2,
        where={"framework": "flask"}
    )


-understand the confidence model
-vectorize mcp tools results
-graph.add_node("run_scan", run_security_scan)  - need to use lambda and pass state?
-write .github/workflows/security-agent.yaml
-create_pr
-request_human_review
-abort
-finalize
-run_tests

do i need chain.invoke in graph.py? 







____________________________

build orchestrated worker project next

agents for unpredictable work patterns

workflows set code pattern flow
    -digia automations are workflows

agentic workflows like hybrid bigger solutions

learn langsmith 
context engineering
