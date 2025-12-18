import subprocess
import json
from .base import MCPTool

class SASTScanner(MCPTool):
    name = "sast_scanner"
    description = "Static Application Security Testing (SAST) tool for scanning source code for vulnerabilities."

    def run(self, input:dict) -> dict:
        """
        Executes the SAST tool with validated input
        Returns structured, normalized output
        """
        target_path = input.get("path", "app/")

        result = subprocess.run(
            ["semgrep", "--config=auto", "--json", target_path],
            capture_output=True,
            text=True
        )

        raw = json.loads(result.stdout)

        findings = []

        for r in raw.get("results", []):
            findings.append({
                "severity": r.get("extra", {}).get("severity", "UNKNOWN"),
                "file": r.get("path", ""),
                "rule": r.get("check_id", ""),
                "line": r.get("start", {}).get("line", 0)
            })

        return {
            "tool": "sast",
            "findings": findings
        }