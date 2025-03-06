from typing import Any, Optional


class ProbeResult:
    """
    Represents the result of running a probe against an AI agent.
    """

    def __init__(self, success: bool, details: str = "", evidence: Optional[Any] = None):
        """
        Initializes the ProbeResult.

        Args:
            success (bool): True if the probe succeeded in finding a vulnerability, False otherwise.
            details (str): A description of the result or the vulnerability found.
            evidence (Optional[Any]): Any evidence supporting the finding (e.g., the agent's response).
        """
        self.success = success
        self.details = details
        self.evidence = evidence

    def __str__(self) -> str:
        return f"Success: {self.success}, Details: {self.details}, Evidence: {self.evidence}"

    def __repr__(self) -> str:
        return self.__str__()
