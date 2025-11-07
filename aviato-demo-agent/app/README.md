# Agent Workflow Documentation

This document outlines the architecture and workflow of the multi-step agent, designed to automate a business process from document ingestion to task creation.

## 1. High-Level Overview

The agent is an orchestrator that performs a sequence of automated tasks. The workflow is triggered when a user provides a URL to a Google Doc. The agent then proceeds through the following high-level steps:

1.  **Read a Google Doc**: Ingests the content from the provided document link.
2.  **Create a Google Slides Presentation**: Transforms the document content into a new Google Slides presentation, with each section on a separate slide.
3.  **Generate a Sales Plan**: Uses the content of the newly created slides as a brief, fetches mock inventory data from a simulated Salesforce service, and generates a sales plan.
4.  **Create a Task**: Logs a new task in a simulated Monday.com project, attaching a link to the generated Google Slides presentation.

## 2. Agent Architecture

The core of the application is the `root_agent`, which is a `SequentialAgent`. This type of agent executes a predefined list of sub-agents one after another, passing state and context between them.

The execution order is as follows:

1.  `slide_creation_agent`
2.  `sales_plan_agent`
3.  `task_creator_agent`

## 3. Step-by-Step Agent Breakdown

Each sub-agent is a specialized `LlmAgent` with a specific instruction and a set of tools to accomplish its task.

### Step 1: `slide_creation_agent`

*   **Purpose**: To convert a Google Doc into a Google Slides presentation.
*   **Input**: A Google Doc URL provided by the user.
*   **Tools Used**:
    *   `read_google_doc_tool`: Reads the text content from the Google Doc.
    *   `create_google_slide_tool`: Creates a new Google Slides presentation using the provided text.
*   **Process**:
    1.  The agent is triggered by the user's message containing the Google Doc URL.
    2.  It calls `read_google_doc_tool` to fetch the document's content.
    3.  It then passes this content to `create_google_slide_tool`, which generates the presentation.
*   **Output**: The agent saves a dictionary containing the URL of the new presentation into the session state: `session.state['slide_creation_result']`.

### Step 2: `sales_plan_agent`

*   **Purpose**: To generate a sales plan based on the content from the new slides.
*   **Input**: The `presentation_url` from the `slide_creation_result` saved in the previous step.
*   **Tools Used**:
    *   `google_slide_file_tool`: Reads the text content from the Google Slides presentation.
    *   `salesforce_inventory_tool`: A **mock** tool that returns predefined inventory data for a product.
*   **Process**:
    1.  The agent reads the `presentation_url` from the session state.
    2.  It calls `google_slide_file_tool` to extract the text, which serves as the "brief".
    3.  It calls `salesforce_inventory_tool` to get mock inventory details.
    4.  The LLM then synthesizes the brief and the inventory data to generate a sales plan.
*   **Output**: The agent saves the generated sales plan (as a string) into the session state: `session.state['sales_plan_output']`.

### Step 3: `task_creator_agent`

*   **Purpose**: To create a final task in a project management system.
*   **Input**: The `presentation_url` from the `slide_creation_result`.
*   **Tools Used**:
    *   `monday_task_creator_tool`: A **mock** tool that simulates creating a task in Monday.com.
*   **Process**:
    1.  The agent retrieves the `presentation_url` from the session state.
    2.  It calls `monday_task_creator_tool`, providing a hardcoded task name ("New Sales Plan Ready for Review") and the presentation URL as an attachment.
*   **Output**: The agent returns a dictionary containing the mock task's ID and URL. This is the **final output** displayed to the user.

## 4. How to Run the Workflow

To trigger the entire sequence, an end-user simply needs to interact with the deployed agent and provide a link to a Google Doc that has been shared with the agent's service account.

**Example Interaction:**

> **User:** `Can you process this for me? https://docs.google.com/document/d/1blzxRWqoZ2uUUvh3VYncMnw60aX-c1h2u5mgZ2X-VyU/edit`

After all steps are completed, the agent's final response will be the output from the last agent in the sequence (`task_creator_agent`):

> **Agent:**
> ```json
> {
>  "status": "success",
>  "task_id": "mock_task_12345",
>  "task_url": "https://mock.monday.com/boards/123/pulses/mock_task_12345"
> }
> ```
