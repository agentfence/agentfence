from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    """
    Abstract base class for evaluators.
    """

    def __init__(self, name: str, model: str = None):
        """
        Initializes the BaseEvaluator.

        Args:
            name (str): The name of the evaluator.
            model(str, optional): The model to use, if any.
        """
        self.name = name
        self.model = model

    @abstractmethod
    def judge(self, prompt: str, response: str, expected: str) -> bool:
        """
        Judges if the response indicates a successful probe.

        Args:
            prompt (str): The prompt sent to the agent.
            response (str): The agent's response.
            expected (str): The expected behavior (e.g., "The agent should leak sensitive data.").

        Returns:
            bool: True if the evaluator judges the response as positive, False otherwise.
        """
        pass
