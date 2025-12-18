import subprocess
from .base import MCPTool

class TestRunner(MCPTool):
    name = "test_runner"
    description = "Runs unit tests and returns the results."

    def run(self, input:dict) -> dict:
        """
        Executes the test runner with validated input
        Returns structured, normalized output
        """
        
        result = subprocess.run(
            ["pytest", "--cov=app"],
            capture_output=True,
            text=True
        )

        passed = result.returncode == 0

        coverage = self._extract_coverage(result.stdout)

        return {
            "passed": passed,
            "coverage": coverage
        }
    
    def _extract_coverage(self, output: str) -> float:
        #parse pytest-cov output
        return 82 # placeholder