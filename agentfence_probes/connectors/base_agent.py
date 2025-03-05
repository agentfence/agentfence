from abc import ABC, abstractmethod
from typing import Dict, Optional, List
import logging


class BaseAgent(ABC):
    """
    Abstract base class for AI agent wrappers.
    """

    def __init__(self, provider: str, model: str, system_instructions: str = "", tools: Optional[List] = None,
                 hello_message: str = "Hello, I am an AI assistant."):
        """
        Initializes the BaseAgent.

        Args:
            provider (str): The AI provider (e.g., "openai", "anthropic").
            model (str): The LLM model name (e.g., "gpt-3.5-turbo").
            system_instructions (str): The initial system instructions for the agent.
            tools (Optional[List]): A list of tools the agent can use.
            hello_message (str): A message for the agent to use when introducing itself.
        """
        self.provider = provider
        self.model = model
        self.system_instructions = system_instructions
        self.tools = tools if tools is not None else []  # Initialize to an empty list if None
        self.hello_message = hello_message
        self.conversation_history: list = []
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def send_message(self, message: str, context: Optional[Dict] = None) -> str:
        """
        Sends a message to the AI agent and returns the response.

        Args:
            message (str): The message to send to the agent.
            context (Optional[Dict]): Optional context to provide to the agent.

        Returns:
            str: The agent's response.
        """
        pass

    def query(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Sends a message to the AI agent and returns the response.
        it also stores the interaction for memory manipulation detection.
        Args:
            prompt (str): The message to send to the agent.
            context (Optional[Dict]): Optional context to provide to the agent.

        Returns:
            str: The agent's response.
        """
        # Store interaction for memory manipulation detection
        self.conversation_history.append({
            "prompt": prompt,
            "context": context
        })

        return self.send_message(prompt, context)

    def clear_conversation_history(self):
        self.conversation_history = []

    def introduce_self(self):
        """
        Returns the agent's introduction message.
        """
        if not self.hello_message:
            self.hello_message = self.send_message("introduce yourself")

        return self.hello_message