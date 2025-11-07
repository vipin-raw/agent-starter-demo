# Model name (as discussed)
GEMINI_MODEL_NAME = "gemini-1.5-pro-001" # Or "gemini-1.5-flash-001"

# Root agent description
ROOT_AGENT_DESCRIPTION = (
    "A Proactive Sales Pitch Agent. The user will provide a 'prospect_name'. "
    "The agent will then fetch data from Salesforce, an Inventory system, "
    "and Monday.com, generate a Google Slide deck and a Google Sheet, "
    "and create a follow-up task in Monday.com."
)

# --- NEW ENDPOINTS FOR YOUR TOOLS ---

# --- NEW SALESFORCE MCP CONFIG ---
SALESFORCE_CONSUMER_KEY = "3MVG97L7PWbPq6Uw5fuwkN3EomRT_0V.4HO_L31z7PR1w_Ru7Di.10UDbKqhAgKMLyhyMQRHJC87m9Uljtib"

# Custom Inventory MCP [cite: 27]
INVENTORY_MCP_ENDPOINT = "https://your-inventory-mcp-url.com/api/query"
INVENTORY_API_KEY = "your-secret-api-key"

MONDAY_CLIENT_ID = "499ef7ad315b392ceeabcc27607ffa1a"

# Vertex AI Search (RAG) [cite: 28]
RAG_PROJECT_ID = "your-gcp-project-id"
RAG_LOCATION = "global"
RAG_DATASTORE_ID = "your-rag-datastore-id"

# Google Workspace / OAuth (for Vipin)
GOOGLE_OAUTH_CLIENT_ID = "your-oauth-client-id.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET = "your-client-secret"
GOOGLE_SLIDE_TEMPLATE_ID = "id-of-your-template-slide-deck" #
GOOGLE_SHEET_TEMPLATE_ID = "id-of-your-template-media-schedule" #