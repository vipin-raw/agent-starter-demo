

import os
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import secretmanager
from google.adk.tools import FunctionTool

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
logger = logging.getLogger(__name__)

def get_google_doc_content(document_id: str) -> str:
    """
    Retrieves all text content from a Google Doc using a service account.
    """
    logger.info(f"Attempting to retrieve content for Google Doc ID: {document_id}")
    SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    SECRET_NAME = "GOOGLE_SLIDES_SA_KEY"  # Reusing the same service account

    try:
        sm_client = secretmanager.SecretManagerServiceClient()
        secret_path = f"projects/{PROJECT_ID}/secrets/{SECRET_NAME}/versions/latest"
        secret_response = sm_client.access_secret_version(name=secret_path)
        sa_key_json = secret_response.payload.data.decode("UTF-8")
        sa_info = json.loads(sa_key_json)

        credentials = service_account.Credentials.from_service_account_info(sa_info, scopes=SCOPES)
        service = build('docs', 'v1', credentials=credentials)

        document = service.documents().get(documentId=document_id).execute()
        content = document.get('body').get('content')
        
        text = ""
        for value in content:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += elem.get('textRun', {}).get('content', '')
        return text
    except Exception as e:
        logger.error(f"Failed to retrieve Google Doc content for ID '{document_id}'. Error: {e}", exc_info=True)
        raise ValueError(f"Could not retrieve content from Google Docs. Ensure the document is shared with the service account.") from e

async def read_google_doc_tool(file_url: str) -> dict:
    """
    Reads content from a Google Doc URL and returns it as text.
    """
    logger.info(f"Executing read_google_doc_tool for URL: {file_url}")
    document_id = file_url.split('/d/')[1].split('/')[0]
    content = get_google_doc_content(document_id)
    return {"status": "success", "document_content": content}

google_doc_reader_tool = FunctionTool(read_google_doc_tool)

