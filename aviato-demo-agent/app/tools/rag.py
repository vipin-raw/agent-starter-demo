import json
from google.adk.tools import FunctionTool
import app.config as config
# You will need to add 'google-cloud-discoveryengine' to requirements.txt
# from google.cloud import discoveryengine_v1alpha as discoveryengine

@FunctionTool
def get_dynamic_rules(industry: str, objective: str) -> str:
    """
    Gets dynamic rules, best practices, and audience info from Vertex AI Search (RAG).
    Args:
        industry: The prospect's industry.
        objective: The prospect's campaign objective.
    Returns:
        A plain text string of rules and insights.
    """
    print(f"[Tool] Getting RAG rules for: {industry}, {objective}")

    # --- For POC: Return Dummy Text ---
    #
    dummy_rules = (
        "**Best Practices for Financial Services:**\n"
        "1. Emphasize security, trust, and low-interest rates.\n"
        "2. Target Homepage banners for maximum brand awareness.\n"
        "3. Use video preroll to explain complex products (like new credit cards).\n"
        "**Target Audience Info:**\n"
        "- Adults 30-50, high-income bracket, interested in personal finance."
    )
    return dummy_rules

    # --- For Production: Call Vertex AI Search ---
    # ... (Add real RAG client logic here) ...
    # search_query = f"sales best practices for {industry} with objective {objective}"
    # ...
    # return rag_response_text

# Expose the tool
get_dynamic_rules_tool = get_dynamic_rules