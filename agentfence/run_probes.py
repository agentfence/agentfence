import logging
from typing import List
from dotenv import load_dotenv

from agentfence.connectors.base_agent import BaseAgent
from agentfence.probes.base_probe import BaseProbe


def run_security_probes(agent: BaseAgent, probes: List[BaseProbe], agent_name: str):
    """
    Runs a set of security probes against an AI agent.

    Args:
        agent: The AI agent to test.
        probes: A list of security probes to run.
        agent_name: The name of the agent.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Set up basic logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger(__name__)

    # Configure the httpx logger to log to DEBUG
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.DEBUG)
    httpx_logger.propagate = False

    # Print the agent's introduction
    logger.info(agent.introduce_self())

    # Run each probe and print results
    logger.info(f"🔍 Running security probes on {agent_name}...")
    logger.info("-" * 50)

    for probe in probes:
        logger.info(f"Running {probe.name}...")
        result = probe.run(agent)

        logger.info(f"Status: {'✅ Passed' if not result.success else '❌ Failed'}")
        logger.info(f"Details: {result.details}")
        if result.evidence:
            logger.info(f"Evidence: {result.evidence}")
        logger.info("-" * 50)

    # Generate a security report
    logger.info("📊 Security Report Summary:")
    vulnerabilities = [p for p in probes if p.last_result.success]
    logger.info(f"Total Probes Run: {len(probes)}")
    logger.info(f"Vulnerabilities Found: {len(vulnerabilities)}")

    if vulnerabilities:
        logger.info("Detailed Findings:")
        for v in vulnerabilities:
            logger.info(f"- {v.name}: {v.last_result.details}")
