# Copyright 2025 Google LLC
# ... (licenses) ...

import os
import google.auth
from google.adk.agents import Agent, SequentialAgent, LlmAgent
import app.config as config


# --- NEW IMPORTS FOR MCP ---
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters



# --- Import Your *Custom* Tools (NOT Salesforce or Monday) ---
from app.tools.rag import get_dynamic_rules_tool
from app.tools.inventory import query_inventory_tool
from app.tools.workspace import create_slide_deck_tool, create_media_sheet_tool


_, project_id = google.auth.default()
# ... (os.environ lines) ...

# --- 1. CONFIGURE SALESFORCE MCP TOOLSET (Already Done) ---
SALESFORCE_MCP_SERVER_URL = "https://api.salesforce.com/platform/mcp/v1-beta.2/platform/sobject-all"
salesforce_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y", "mcp-remote@0.1.18",
                SALESFORCE_MCP_SERVER_URL,
                "8080", # Salesforce proxy listens on port 8080
                "--static-oauth-client-info",
                f'{{"client_id":"{config.SALESFORCE_CONSUMER_KEY}","client_secret":""}}'
            ]
        )
    )
)

# --- 2. CONFIGURE MONDAY.COM MCP TOOLSET (The New Step) ---
# This uses the official "Hosted MCP" URL from the README
MONDAY_MCP_SERVER_URL = "https://mcp.monday.com/mcp"
monday_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y", "mcp-remote@0.1.18", # We use the same mcp-remote proxy
                MONDAY_MCP_SERVER_URL,
                "8081", # <-- !! MUST USE A DIFFERENT PORT (e.g., 8081) !!
                "--static-oauth-client-info",
                f'{{"client_id":"{config.MONDAY_CLIENT_ID}","client_secret":""}}'
                # The proxy will use http://localhost:8081/oauth/callback
            ]
        )
    )
)
# --- END OF MCP CONFIGURATION ---


sales_pitch_agent = LlmAgent(
    name="sales_pitch_agent",
    model=config.GEMINI_MODEL_NAME,

    # --- FINAL, UPDATED INSTRUCTION ---
    # The agent now knows about *native* Salesforce and Monday.com tools
    instruction=(
        "You are a NewsCorp advertising strategist. Your job is to create a "
        "complete, bookable pitch package using the exact data provided. "
        "Your goal is to generate a proactive sales pitch."
        "\n"
        "Here is the plan you MUST follow:"
        "1.  **GATHER DATA (Parallel):**"
        "    - **Salesforce:** You will be given a `prospect_name`. Use your "
        "      Salesforce tools (like `run_soql_query`) to find the Account. "
        "      Get the prospect's industry, budget, and key objective."
        "    - **Monday.com:** Use the `list_users_and_teams` tool to see who is on "
        "      the sales team. Use `get_board_schema` to find the 'Sales Backlog' board ID."
        "    - **Inventory:** Use the `query_inventory` tool to get available ad slots."
        "    - **RAG:** Use the `get_dynamic_rules` tool to get sales best practices."
        "2.  **STRATEGIZE (LLM Call):**"
        "    - You will then be called (by the system) with all this data."
        "    - Your job is to analyze all inputs and generate the final JSON output "
        "      containing `strategy_rationale`, `slide_content`, and `media_schedule_line_items`."
        "3.  **EXECUTE ACTIONS (Parallel):**"
        "    - Use `create_slide_deck` with the `slide_content`."
        "    - Use `create_media_sheet` with the `media_schedule_line_items`."
        "4.  **FINALIZE TASK:**"
        "    - Use your **Monday.com `create_item` tool** to create a follow-up task "
        "      on the 'Sales Backlog' board. The task name should be the prospect's name. "
        "      You must put the URLs for the slide and sheet in the task update."
        "5.  **RESPOND:**"
        "    - Return the final Google Slide and Google Sheet URLs to the user."
    ),

    # --- FINAL TOOLS LIST ---
    tools=[
        salesforce_tools,      # Natively provides `run_soql_query`, etc.
        monday_tools,          # Natively provides `create_item`, `get_board_schema`, etc.
        query_inventory_tool,  # Your custom tool
        get_dynamic_rules_tool,  # Your custom tool
        create_slide_deck_tool,  # Your custom tool
        create_media_sheet_tool, # Your custom tool
    ],
)

# ... (root_agent setup remains the same) ...
root_agent = SequentialAgent(
    name="root_agent",
    description=config.ROOT_AGENT_DESCRIPTION,
    sub_agents=[
       sales_pitch_agent
    ],
)
