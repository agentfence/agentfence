import os
from openai import OpenAI
from typing import List, Dict, Optional

from agentfence.connectors.base_agent import BaseAgent


class OpenAIAgent(BaseAgent):
    """
    Concrete implementation of an agent wrapper for the OpenAI API.
    """

    def __init__(self, model: str, api_key: str = None, system_instructions: str = "",
                 tools: Optional[List] = None, hello_message: str = "Hello, I am an AI assistant."):
        """
        Initializes the OpenAIAgent.

        Args:
            model (str): The OpenAI model to use (e.g., "gpt-3.5-turbo", "gpt-4").
            api_key (str, optional): Your OpenAI API key. If not provided, it will be loaded from the OPENAI_API_KEY environment variable. Defaults to None.
            system_instructions (str): The initial system instructions for the agent.
            tools (Optional[List]): A list of tools the agent can use.
            hello_message (str): A message for the agent to use when introducing itself.
        """
        super().__init__(provider="openai", model=model, system_instructions=system_instructions, tools=tools,
                         hello_message=hello_message)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")  # Get API key from env if not provided
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=self.api_key)

    def send_message(self, message: str, context: Optional[Dict] = None) -> str:
        """
        Sends a message to the OpenAI API and returns the response.

        Args:
            message (str): The message to send to the agent.
            context (Optional[Dict]): Optional context to provide to the agent.

        Returns:
            str: The agent's response.
        """
        try:
            messages = []

            # Add system instructions at the start if they exist
            if self.system_instructions:
                messages.append({"role": "system", "content": self.system_instructions})

            # add context if there is one.
            if context:
                for role, content in context.items():
                    messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": message})

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
            )
            response = chat_completion.choices[0].message.content
            return response
        except Exception as e:
            raise RuntimeError(f"Error communicating with OpenAI API: {e}")
