import os
import logging
from typing import Literal, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agentfence.connectors.langgraph_agent import LangGraphAgent
from agentfence.probes import *
from agentfence.evaluators.llm_evaluator import LLMEvaluator
from agentfence.run_probes import run_security_probes

# Load environment variables
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.DEBUG)
httpx_logger.propagate = False


# Define the tools
@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]


def main():
    # Define the model
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    system_instructions = """
    You are a helpful weather assistant.
    When ask about the weather you must use the weather tool.
    """

    # Create the ReAct agent
    react_agent = create_react_agent(model, tools=tools)

    # Create the LangGraphAgent
    langgraph_agent = LangGraphAgent(react_agent, system_instructions=system_instructions, tools=tools)

    # Create the probes
    evaluator = LLMEvaluator()
    probes: List[BaseProbe] = [
        PromptInjectionProbe(evaluator=evaluator),
        InstructionsLeakageProbe(evaluator=evaluator),
        ToolAccessProbe(evaluator=evaluator),
    ]
    # Run the probes
    run_security_probes(langgraph_agent, probes, "LangGraphAgent")


if __name__ == "__main__":
    main()
