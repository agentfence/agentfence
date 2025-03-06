from typing import Dict, Any, Optional, List
from langchain_core.runnables import Runnable
from agentfence.connectors.base_agent import BaseAgent
from langchain_core.messages import HumanMessage, BaseMessage
import logging

logger = logging.getLogger(__name__)


class AgentState:
    messages: List[BaseMessage]


class LangGraphAgent(BaseAgent):
    def __init__(self, agent: Runnable, system_instructions: str = "", tools: Optional[List] = None,
                 llm: Optional[Any] = None, max_iterations: int = 15,
                 hello_message: str = "Hello, I am a LangGraph agent, and I'm ready to assist you!"):
        super().__init__("langgraph", "langgraph", system_instructions=system_instructions, tools=tools,
                         hello_message=hello_message)
        self.agent = agent
        self.config = {"max_iterations": max_iterations, "tools": tools, "llm": llm}
        if system_instructions:
            self.config["system_instructions"] = system_instructions

    def send_message(self, message: str, context: Optional[Dict] = None) -> str:
        result = self.agent.invoke({"messages": [HumanMessage(message)]})
        return result['messages'][-1].content
