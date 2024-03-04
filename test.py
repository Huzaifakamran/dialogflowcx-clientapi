from google.oauth2 import service_account
from google.cloud.dialogflowcx_v3.services.agents.client import AgentsClient
from google.cloud.dialogflowcx_v3.services.sessions.client import SessionsClient
from google.cloud.dialogflowcx_v3.types.session import TextInput, QueryInput, DetectIntentRequest
import uuid

# Path to your service account key file
service_account_key_path = 'service_key.json'

# Load credentials from the service account key file
credentials = service_account.Credentials.from_service_account_file(service_account_key_path)

project_id = "<>"
agent_id = "<>"
location_id = "us-central1"
agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
session_id = str(uuid.uuid4())  # Convert UUID to string
texts = ["hi"]
language_code = "en-us"

def detect_intent_texts(agent, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")
    session_client = SessionsClient(credentials=credentials, client_options={'api_endpoint': 'us-central1-dialogflow.googleapis.com'})

    for text in texts:
        text_input = TextInput(text=text)
        query_input = QueryInput(text=text_input, language_code=language_code)
        request = DetectIntentRequest(
            session=session_path, query_input=query_input
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print("Payload",response)
        print(f"Query text: {response.query_result.text}")
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        print(f"Response text: {' '.join(response_messages)}\n")

detect_intent_texts(agent, session_id, texts, language_code)
