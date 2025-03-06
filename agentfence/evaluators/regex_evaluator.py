import re
from agentfence.evaluators.base_evaluator import BaseEvaluator


class RegexEvaluator(BaseEvaluator):
    """
    An evaluator that uses regular expressions to determine if a probe is successful.
    """

    def __init__(self, regex_pattern: str):
        """
        Initializes the RegexEvaluator.

        Args:
            regex_pattern (str): The regular expression pattern to match.
        """
        super().__init__(name="RegexEvaluator", model=None)
        self.regex_pattern = regex_pattern

    def judge(self, prompt: str, response: str, expected: str) -> bool:
        """
        Judges if the response indicates a successful probe based on regex matching.

        Args:
            prompt (str): The prompt sent to the agent.
            response (str): The agent's response.
            expected (str): The expected behavior if the probe is successful. (Not used in this evaluator).

        Returns:
            bool: True if the regex pattern is found in the response, False otherwise.
        """
        return bool(re.search(self.regex_pattern, response))
