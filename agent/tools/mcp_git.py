from github import Github
from .base import MCPTool
import os

class GitTool(MCPTool):
    name = "git_ops"
    description = "Tool for interacting with Git repositories."

    def run(self, input:dict) -> dict:
        action = input["action"]

        if action == "create_pr":
            return self._create_pr(input)

        raise ValueError(f"Unsupported action: {action}")
    
    def _create_pr(self, input:dict) -> dict:
        token = os.getenv("GITHUB_TOKEN")
        gh = Github(token)

        repo = gh.get_repo(input["repo"])

        pr = repo.create_pull(
            title=input["title"],
            body=input["body"],
            head=input["branch"],
            base="main"
        )

        return {
            "pr_url": pr.html_url,
        }