import json
from google.adk.tools import FunctionTool
import app.config as config
# You will need:
# 'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib'
# Add these to requirements.txt

@FunctionTool
def create_slide_deck(slide_content: str) -> str:
    """
    Creates a new Google Slide deck from a template and populates it.
    Args:
        slide_content: A JSON string (or list) of slide titles and bodies.
                       Example: '[{"title": "...", "body": "..."}, ...]'
    Returns:
        The URL of the newly created Google Slide deck.
    """
    print(f"[Tool] Creating Google Slide deck...")

    # --- For POC: Return Dummy URL ---
    # [cite: 48]
    dummy_url = "https://docs.google.com/presentation/d/1_abc-123_EXAMPLE/edit"
    return dummy_url

    # --- For Production (Vipin's Task) ---
    #
    # 1. Handle Google OAuth (this is the complex part, similar to sharepoint_tool.py)
    # 2. Copy the template slide (config.GOOGLE_SLIDE_TEMPLATE_ID)
    # 3. Parse the slide_content (it's a list of dicts)
    # 4. Loop through the list, create new slides, and populate them
    # 5. Make the new slide deck shareable
    # 6. Return the URL

@FunctionTool
def create_media_sheet(media_schedule_line_items: str) -> str:
    """
    Creates a new Google Sheet from a template and populates it.
    Args:
        media_schedule_line_items: A JSON string (or list) of line items.
                                   Example: '[{"item": "...", "cost": ...}, ...]'
    Returns:
        The URL of the newly created Google Sheet.
    """
    print(f"[Tool] Creating Google Media Sheet...")

    # --- For POC: Return Dummy URL ---
    # [cite: 48]
    dummy_url = "https://docs.google.com/spreadsheets/d/1_xyz-789_EXAMPLE/edit"
    return dummy_url

    # --- For Production (Vipin's Task) ---
    # 1. Handle Google OAuth
    # 2. Copy the template sheet (config.GOOGLE_SHEET_TEMPLATE_ID)
    # 3. Parse the media_schedule_line_items
    # 4. Write the data to the new sheet
    # 5. Make the new sheet shareable
    # 6. Return the URL

# Expose the tools
create_slide_deck_tool = create_slide_deck
create_media_sheet_tool = create_media_sheet