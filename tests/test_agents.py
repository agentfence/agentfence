import pytest
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from agentfence.connectors.openai_agent import OpenAIAgent
from agentfence.connectors.langgraph_agent import LangGraphAgent
from agentfence.connectors.dialogflow_agent import DialogflowCXAgentWrapper

# Load environment variables
load_dotenv()


@tool
def get_weather(city: str):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]


@pytest.fixture
def openai_agent():
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL") or 'gpt-3.5-turbo'
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    if not model:
        raise ValueError("OPENAI_MODEL is not set in the environment variables.")
    agent = OpenAIAgent(
        model=model,
        api_key=api_key,
        system_instructions="You are a helpful travel assistant.",
        hello_message="Hi, I'm your helpful travel assistant."
    )
    return agent


@pytest.fixture
def langgraph_agent():
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    system_instructions = """
    You are a helpful weather assistant.
    When ask about the weather you must use the weather tool.
    """
    react_agent = create_react_agent(model, tools=tools)
    agent = LangGraphAgent(react_agent, system_instructions=system_instructions, tools=tools)
    return agent


@pytest.fixture
def dialogflow_agent():
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
    agent_id = os.getenv("DIALOGFLOW_AGENT_ID")
    credentials_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    agent_environment = os.getenv("DIALOGFLOW_AGENT_ENVIRONMENT")
    if not credentials_file:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set in the environment variables.")
    if not project_id:
        raise ValueError("DIALOGFLOW_PROJECT_ID is not set in the environment variables.")
    if not agent_id:
        raise ValueError("DIALOGFLOW_AGENT_ID is not set in the environment variables.")
    if not agent_environment:
        raise ValueError("DIALOGFLOW_AGENT_ENVIRONMENT is not set in the environment variables.")

    agent = DialogflowCXAgentWrapper(
        project_id=project_id,
        agent_id=agent_id,
        credentials_file=credentials_file,
        agent_environment=agent_environment,
    )
    return agent


def test_openai_agent_send_message(openai_agent):
    response = openai_agent.send_message("Hello!")
    assert response is not None


def test_openai_agent_query(openai_agent):
    response = openai_agent.query("Hello!")
    assert response is not None


def test_langgraph_agent_send_message(langgraph_agent):
    response = langgraph_agent.send_message("Hello!")
    assert response is not None


def test_langgraph_agent_query(langgraph_agent):
    response = langgraph_agent.query("Hello!")
    assert response is not None


def test_dialogflow_agent_send_message(dialogflow_agent):
    response = dialogflow_agent.send_message("Hello!")
    assert response is not None


def test_dialogflow_agent_query(dialogflow_agent):
    response = dialogflow_agent.query("Hello!")
    assert response is not None
