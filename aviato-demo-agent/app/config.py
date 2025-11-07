GEMINI_MODEL_NAME = "gemini-1.5-flash-001"
AUTHOR = "Sales Agent"

ROOT_AGENT_DESCRIPTION = (
    "An orchestrator agent that manages a multi-step process: "
    "1. Reads a Google Doc. "
    "2. Creates a Google Slides presentation from the doc's content. "
    "3. Uses the slide content to generate a sales plan with mock inventory data. "
    "4. Creates a task in Monday.com with a link to the new presentation."
)

SLIDE_CREATOR_INSTRUCTION = (
    "Your task is to orchestrate the creation of a Google Slides presentation from a Google Doc URL. "
    "First, you MUST use the `read_google_doc_tool` to get the content of the document. "
    "Then, you MUST use the `create_google_slide_tool` with the extracted `document_content` to create the presentation. "
    "Your final output must be the dictionary returned by the `create_google_slide_tool`."
)

SALES_PLAN_INSTRUCTION = (
    "You are a sales plan creator. You will be given a URL to a Google Slides presentation. "
    "1. Use the `get_google_slide_file` tool to read the content of the presentation. This content is your 'brief'. "
    "2. Use the `get_inventory_details_from_salesforce` tool to get mock inventory data for the product 'SuperWidget'. "
    "3. Create a sales plan including the retrieved `inventory_details` as per the provided `brief`. "
    "Your final output should be the complete sales plan as a text string."
)

TASK_CREATOR_INSTRUCTION = (
    "Your job is to create a task in Monday.com. You will receive the URL of a Google Slides presentation. "
    "You MUST use the `create_monday_task_with_attachment` tool. "
    "Use 'New Sales Plan Ready for Review' as the `task_name` and pass the `presentation_url` as the `file_url`. "
    "Your final output should be the dictionary returned by the tool."
)
