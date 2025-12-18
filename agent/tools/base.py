from abc import ABC, abstractmethod

class MCPTool(ABC):
    name:str
    description:str

    @abstractmethod
    def run(self, input:dict) -> dict:
        """
        Executes the tool with validated input
        Returns structured, normalized output
        """
        pass