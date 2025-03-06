import requests
import uuid
import json
import logging
from typing import Dict, Optional
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from agentfence.connectors.base_agent import BaseAgent


class DialogflowCXAgentWrapper(BaseAgent):
    """
    A wrapper class for interacting with a Dialogflow CX agent.
    """

    def __init__(self,
                 project_id, agent_id, credentials_file,
                 location_id="us-central1", agent_environment='draft'):
        """
        Initializes the DialogflowCXAgentWrapper.

        Args:
            project_id (str): Your Dialogflow project ID.
            agent_id (str): The ID of your Dialogflow agent.
            credentials_file (str): The path to your service account credentials file.
            location_id (str, optional): The location of your agent. Defaults to "us-central1".
            agent_environment (str, optional): The Dialogflow environment ID. If not provided the draft will be used.
        """
        super().__init__(provider="dialogflow", model="cx",
                         hello_message="Hi, I'm your Google travel assistant. I can help you search for points of interest, get travel inspiration, or book a hotel. What can I help you with today?")
        self.project_id = project_id
        self.agent_id = agent_id
        self.credentials_file = credentials_file
        self.location_id = location_id
        self.agent_environment = agent_environment
        self.base_url = f"https://{self.location_id}-dialogflow.googleapis.com/v3"
        self.access_token = self._get_access_token(self.credentials_file)
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)  # Default level

    def _get_access_token(self, credentials_file):
        """Gets an access token from the service account key file."""
        creds = service_account.Credentials.from_service_account_file(credentials_file)
        creds = creds.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
        request = Request()
        creds.refresh(request)
        return creds.token

    def _build_session_path(self):
        """
        Builds the session path based on the presence of agent_environment.

        Returns:
            str: The session path for detectIntent requests.
        """
        if self.agent_environment:
            return f"{self.base_url}/projects/{self.project_id}/locations/{self.location_id}/agents/{self.agent_id}/environments/{self.agent_environment}/sessions/{str(uuid.uuid4())}"
        else:
            flow_version = "$LATEST"
            return f"{self.base_url}/projects/{self.project_id}/locations/{self.location_id}/agents/{self.agent_id}/flows/00000000-0000-0000-0000-000000000000/versions/{flow_version}/sessions/{str(uuid.uuid4())}"

    def send_message(self, message: str, context: Optional[Dict] = None) -> str:
        """
        Sends a text message to the Dialogflow CX agent and returns the response.

        Args:
            message (str): The text message to send.

        Returns:
            str: The response message from the Dialogflow CX agent.
        """
        session_path = self._build_session_path()
        detect_intent_path = f"{session_path}:detectIntent"
        payload = {
            "session": session_path,
            "queryInput": {
                "text": {
                    "text": message,
                },
                "languageCode": "en"
            }
        }

        self.logger.debug("--------------------")
        self.logger.debug("DEBUG: Request Details:")
        self.logger.debug(f"  URL: {detect_intent_path}")
        self.logger.debug(f"  Headers: {self.headers}")
        self.logger.debug(f"  Payload: {json.dumps(payload, indent=2)}")
        self.logger.debug("--------------------")

        response = requests.post(detect_intent_path, headers=self.headers, json=payload)

        self.logger.debug("--------------------")
        self.logger.debug("DEBUG: Response Details:")
        self.logger.debug(f"  Status Code: {response.status_code}")
        self.logger.debug(f"  Response Headers: {response.headers}")
        self.logger.debug(f"  Response Content: {response.content.decode('utf-8')}")
        self.logger.debug("--------------------")

        response.raise_for_status()
        response_json=response.json()

        # Extract the actual text from the response
        query_result = response_json.get("queryResult", {})
        response_messages = query_result.get("responseMessages", [])

        for msg in response_messages:
            text_message = msg.get("text", {}).get("text")
            if text_message:
                return text_message[0]  # Return the first text response

        return "" # return empty string if no text is found.

