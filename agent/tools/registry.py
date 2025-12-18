from .mcp_scanner import SASTScanner
from .mcp_git import GitTool
from .mcp_tests import TestRunner

TOOLS = {
    "sast": SASTScanner(),
    "git": GitTool(),
    "tests": TestRunner(),
}

