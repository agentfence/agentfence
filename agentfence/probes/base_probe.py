from abc import ABC
from typing import Optional, List
import logging
from agentfence.result import ProbeResult
from agentfence.connectors.base_agent import BaseAgent
from agentfence.evaluators.base_evaluator import BaseEvaluator
from agentfence.evaluators.llm_evaluator import LLMEvaluator


class BaseProbe(ABC):
    """
    Abstract base class for security probes.
    """

    def __init__(self, name: str, description: str = "", payload: Optional[str] = None,
                 evaluator: Optional[BaseEvaluator] = None):
        """
        Initializes the BaseProbe.

        Args:
            name (str): The name of the probe.
            description (str, optional): A description of the probe. Defaults to "".
            payload (Optional[str], optional): A payload to use for the probe. Defaults to None.
            evaluator(Optional[BaseEvaluator], optional): The evaluator to use. Defaults to None.
        """
        self.name = name
        self.description = description
        self.payload = payload
        self.last_result: ProbeResult = None
        self.logger = logging.getLogger(__name__)
        self.evaluator = evaluator if evaluator is not None else LLMEvaluator()

    def get_response(self, agent: BaseAgent, payload: str) -> str:
        """
        Gets the agent's response for a given payload.

        Args:
            agent (BaseAgent): The agent to probe.
            payload (str): The payload to send to the agent.

        Returns:
            str: The agent's response.
        """
        return agent.send_message(payload)

    def run(self, agent: BaseAgent) -> ProbeResult:
        """
        Runs the probe against the given agent.

        Args:
            agent (BaseAgent): The agent to probe.

        Returns:
            ProbeResult: The result of the probe.
        """
        try:
            response = None  # initialize response
            payloads: List[str] = self.create_payloads() if not self.payload else [self.payload]
            for payload in payloads:
                self.info(f"Attempting probe with payload: '{payload}'")
                response = self.get_response(agent, payload)
                expected_behavior = self.get_expected_behavior(payload)
                is_positive = self.evaluator.judge(payload, response, expected_behavior)
                if is_positive:
                    self.info(f"Probe successful: payload: '{payload}'")
                    return self.default_result(success=True,
                                               details=f"Probe detected.",
                                               evidence=response)
                else:
                    self.debug(f"Payload failed: {payload}. Response: {response}")

            self.info(f"All probe attempts failed")
            return self.default_result(success=False,
                                       details=f"No probe detected.",
                                       evidence=response)

        except Exception as e:
            self.error(f"Error during probe execution: {e}")
            return self.default_result(success=False, details=f"Error during probe execution: {e}")

    def get_expected_behavior(self, payload: str) -> str:
        return "The agent should indicate a successful probe"

    def create_payloads(self) -> List[str]:
        return []

    def default_result(self, success: bool, details: str, evidence: str = None) -> ProbeResult:
        """
        Creates and returns a ProbeResult object.

        Args:
            success (bool): True if the probe succeeded, False otherwise.
            details (str): Details about the probe result.
            evidence (Optional[str]): Evidence related to the probe result.

        Returns:
            ProbeResult: A ProbeResult object.
        """
        self.last_result = ProbeResult(success=success, details=details, evidence=evidence)
        return self.last_result

    def info(self, message: str) -> None:
        """
        Logs an informational message.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)

    def error(self, message: str) -> None:
        """
        Logs an error message.

        Args:
            message (str): The message to log.
        """
        self.logger.error(message)
