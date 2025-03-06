import os
from typing import List
from dotenv import load_dotenv

from agentfence.evaluators.llm_evaluator import LLMEvaluator
from agentfence.connectors.dialogflow_agent import DialogflowCXAgentWrapper
from agentfence.probes import *
from agentfence.run_probes import run_security_probes


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get the Dialogflow CX credentials from the environment variables
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

    # Create the Dialogflow CX agent wrapper
    agent = DialogflowCXAgentWrapper(
        project_id=project_id,
        agent_id=agent_id,
        credentials_file=credentials_file,
        agent_environment=agent_environment,
    )
    # Create the security probes
    evaluator = LLMEvaluator()
    probes: List[BaseProbe] = [
        PromptInjectionProbe(evaluator=evaluator),
        InstructionsLeakageProbe(evaluator=evaluator),
        ToolAccessProbe(evaluator=evaluator),
        DataExtractionProbe(evaluator=evaluator),
        DataExtractionProbe(target_info="customer data", evaluator=evaluator),
        SecretLeakageProbe(evaluator=evaluator),
        RoleConfusionProbe(evaluator=evaluator),
        JailbreakProbe(evaluator=evaluator),
        HarmfulLanguageProbe(evaluator=evaluator),
    ]
    # Run the probes
    run_security_probes(agent, probes, "DialogflowAgent")


if __name__ == "__main__":
    main()
