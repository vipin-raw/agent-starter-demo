import json
import os
import logging
from typing import Dict, Any, List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import secretmanager
from google.cloud import storage
from google.adk.tools import FunctionTool

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

logger = logging.getLogger(__name__)

def get_google_slide_content(presentation_id: str) -> dict | None:
    """
    Retrieves all text content from a Google Slide presentation using a
    service account for authentication.
    """
    logger.info(f"Attempting to retrieve content for Google Slide ID: {presentation_id}")
    SCOPES = ["https://www.googleapis.com/auth/presentations.readonly"]
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    SECRET_NAME = "GOOGLE_SLIDES_SA_KEY" # The name of the secret in Secret Manager

    try:
        # 1. Fetch Service Account credentials from Secret Manager
        sm_client = secretmanager.SecretManagerServiceClient()
        secret_path = f"projects/{PROJECT_ID}/secrets/{SECRET_NAME}/versions/latest"
        secret_response = sm_client.access_secret_version(name=secret_path)
        sa_key_json = secret_response.payload.data.decode("UTF-8")
        sa_info = json.loads(sa_key_json)

        credentials = service_account.Credentials.from_service_account_info(sa_info, scopes=SCOPES)

        # 2. Build the Slides API service
        service = build('slides', 'v1', credentials=credentials)

        # 3. Call the Slides API to fetch the presentation
        presentation = service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        # 4. Extract text from all shapes in all slides
        all_text = []
        for slide in slides:
            for element in slide.get('pageElements', []):
                if 'shape' in element and 'text' in element['shape']:
                    text_elements = element['shape']['text'].get('textElements', [])
                    for text_element in text_elements:
                        if 'textRun' in text_element:
                            all_text.append(text_element['textRun'].get('content', ''))
        
        logger.info(f"Successfully extracted text from {len(slides)} slides.")
        return {
            "text_content": "".join(all_text),
            "slide_count": len(slides)
        }

    except Exception as e:
        logger.error(f"Failed to retrieve or parse Google Slide content for ID '{presentation_id}'. Error: {e}", exc_info=True)
        # This could be a permissions issue (slide not shared with SA) or invalid ID.
        raise ValueError(
            "Could not retrieve content from Google Slides. "
            "Please ensure the presentation ID is correct and that the slide has been "
            f"shared with the service account."
        ) from e


def create_presentation_from_text(title: str, sections: List[str]) -> str:
    """
    Creates a new Google Slides presentation from a list of text sections.
    Each section is placed on a new slide.
    Returns the URL of the new presentation.
    """
    logger.info(f"Creating new presentation titled: {title}")
    SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/presentations"]
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    SECRET_NAME = "GOOGLE_SLIDES_SA_KEY"

    try:
        sm_client = secretmanager.SecretManagerServiceClient()
        secret_path = f"projects/{PROJECT_ID}/secrets/{SECRET_NAME}/versions/latest"
        secret_response = sm_client.access_secret_version(name=secret_path)
        sa_key_json = secret_response.payload.data.decode("UTF-8")
        sa_info = json.loads(sa_key_json)

        credentials = service_account.Credentials.from_service_account_info(sa_info, scopes=SCOPES)
        slides_service = build('slides', 'v1', credentials=credentials)

        # Create a new presentation
        presentation = slides_service.presentations().create(body={'title': title}).execute()
        presentation_id = presentation.get('presentationId')

        # Add a slide for each section
        requests = []
        for i, section_text in enumerate(sections):
            slide_id = f"slide_{i}"
            requests.append({'createSlide': {'objectId': slide_id, 'insertionIndex': i + 1}})
            # This is a simplified text box creation. A real one would be more complex.
            requests.append({'createShape': {'objectId': f"shape_{i}", 'shapeType': 'TEXT_BOX', 'elementProperties': {'pageObjectId': slide_id}}})
            requests.append({'insertText': {'objectId': f"shape_{i}", 'text': section_text}})

        slides_service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': requests}).execute()

        presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
        logger.info(f"Successfully created presentation: {presentation_url}")
        return presentation_url

    except Exception as e:
        logger.error(f"Failed to create Google Slide presentation. Error: {e}", exc_info=True)
        raise ValueError("Could not create Google Slides presentation.") from e

async def get_google_slide_file(tool_context: Any, file_url: str) -> str:
    """
    Retrieves text content from a Google Slides presentation URL, 
    uploads it to Google Cloud Storage (GCS), and returns the GCS URI.
    This tool uses a service account and does not require user authentication.
    """
    logger.info(f"Starting get_google_slide_file for URL: {file_url}")

    if "docs.google.com/presentation/d/" not in file_url:
        error_msg = "Invalid URL. This tool only supports Google Slides presentation URLs (e.g., 'https://docs.google.com/presentation/d/...')."
        logger.error(error_msg)
        return {"status": "error", "error_message": error_msg}

    
    try:
        presentation_id = file_url.split('/d/')[1].split('/')[0]
        slide_data = get_google_slide_content(presentation_id)
        return {
            "status": "success",
            "slide_content": slide_data.get("text_content"),
            "page_count": slide_data.get("slide_count"),
            "source_type": "google_slide"
        }
    except Exception as e:
        logger.error(f"Google Slides processing failed: {e}", exc_info=True)
        return {"status": "error", "error_message": str(e)}

async def create_google_slide_tool(document_content: str) -> dict:
    """
    Creates a Google Slides presentation from the provided document content.
    It splits the content by sections to create individual slides.
    """
    logger.info("Executing create_google_slide_tool")
    sections = document_content.split("\n\n") # Simple split by double newline
    title = sections[0] if sections else "New Presentation"
    presentation_url = create_presentation_from_text(title, sections)
    return {"status": "success", "presentation_url": presentation_url}

google_slide_file_tool = FunctionTool(get_google_slide_file)
google_slide_creator_tool = FunctionTool(create_google_slide_tool)