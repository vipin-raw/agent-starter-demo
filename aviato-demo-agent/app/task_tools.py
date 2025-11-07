import logging
from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)

async def create_monday_task_with_attachment(task_name: str, file_url: str) -> dict:
    """
    MOCK: Creates a task in Monday.com with a file attachment.
    In a real implementation, this would use the Monday.com SDK.
    """
    logger.info(f"MOCK: Creating Monday.com task '{task_name}' with attachment: {file_url}")
    # A real implementation would use the monday-sdk-python library here.
    # It would require an API key, board_id, and group_id.
    task_id = "mock_task_12345"
    return {"status": "success", "task_id": task_id, "task_url": f"https://mock.monday.com/boards/123/pulses/{task_id}"}

monday_task_creator_tool = FunctionTool(create_monday_task_with_attachment)