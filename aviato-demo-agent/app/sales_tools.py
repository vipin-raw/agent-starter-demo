import logging
from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)

async def get_inventory_details_from_salesforce(product_name: str) -> dict:
    """
    MOCK: Fetches inventory details for a given product from Salesforce.
    In a real implementation, this would connect to the Salesforce API.
    """
    logger.info(f"MOCK: Fetching inventory for product: {product_name}")
    # This is mock data. A real implementation would use the simple-salesforce library.
    mock_inventory = {
        "SuperWidget": {"stock": 1500, "price_usd": 49.99, "warehouse_location": "Nevada"},
        "MegaGadget": {"stock": 800, "price_usd": 199.99, "warehouse_location": "Georgia"},
    }
    return {"status": "success", "inventory_details": mock_inventory.get(product_name, {"stock": 0, "price_usd": 0, "error": "Product not found"})}

salesforce_inventory_tool = FunctionTool(get_inventory_details_from_salesforce)