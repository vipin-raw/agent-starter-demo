import os

import google.auth
from google.adk.agents import Agent, SequentialAgent, LlmAgent
import app.config as config
from app.tools.google_doc_tool import google_doc_reader_tool
from app.tools.slide_tool import google_slide_creator_tool, google_slide_file_tool
from app.tools.sales_tools import salesforce_inventory_tool
from app.tools.task_tools import monday_task_creator_tool

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


markup_agent = LlmAgent(
    name="slide_creation_agent",
    model=config.GEMINI_MODEL_NAME,
    instruction=config.SLIDE_CREATOR_INSTRUCTION,
    tools=[
        google_doc_reader_tool,
        google_slide_creator_tool,
    ],
    output_key="slide_creation_result",
)

sales_plan_agent = LlmAgent(
    name="sales_plan_agent",
    model=config.GEMINI_MODEL_NAME,
    instruction=config.SALES_PLAN_INSTRUCTION,
    tools=[
        google_slide_file_tool,
        salesforce_inventory_tool,
    ],
    output_key="sales_plan_output",
)

task_creator_agent = LlmAgent(
    name="task_creator_agent",
    model=config.GEMINI_MODEL_NAME,
    instruction=config.TASK_CREATOR_INSTRUCTION,
    tools=[
        monday_task_creator_tool,
    ],
    output_key="monday_task_result",
)

root_agent = SequentialAgent(
    name="root_agent",
    description=config.ROOT_AGENT_DESCRIPTION,
    sub_agents=[
        markup_agent,
        sales_plan_agent,
        task_creator_agent,
    ],
)

#test deployment
