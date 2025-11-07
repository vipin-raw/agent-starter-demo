import json
from google.adk.tools import FunctionTool
import app.config as config
import requests

@FunctionTool
def query_inventory(industry: str, budget: float) -> str:
    """
    Gets available ad inventory slots from the Custom Inventory MCP.
    Args:
        industry: The prospect's industry (for targeting).
        budget: The prospect's budget (for filtering).
    Returns:
        A JSON string of available ad slots, pricing, and schedules.
    """
    print(f"[Tool] Querying inventory for industry: {industry}, budget: {budget}")

    # --- For POC: Return Dummy Data ---
    #
    dummy_inventory = {
        "available_slots": [
            {"slot_id": "HP-Banner-01", "name": "Homepage Top Banner", "cost": 15000, "schedule": "Full Week"},
            {"slot_id": "Finance-Sidebar-03", "name": "Finance Section Sidebar", "cost": 10000, "schedule": "Mon-Fri"},
            {"slot_id": "HP-Video-01", "name": "Homepage Video Preroll", "cost": 25000, "schedule": "Weekend"}
        ],
        "total_cost": 50000
    }
    return json.dumps(dummy_inventory)

    # --- For Production: Call the real MCP ---
    # ... (Add real API call logic here) ...
    # return response.text

# Expose the tool
query_inventory_tool = query_inventory