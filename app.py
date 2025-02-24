from fastapi import FastAPI
from google.cloud import workflows_v1
import os

from google.cloud.workflows import executions_v1
from google.cloud.workflows.executions_v1 import Execution

PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("LOCATION", "us-central1")
WORKFLOW_ID = os.getenv("WORKFLOW", "myFirstWorkflow")


def execute_workflow(project: str, location: str, workflow: str) -> Execution:
    # Set up API clients.
    execution_client = executions_v1.ExecutionsClient()
    workflows_client = workflows_v1.WorkflowsClient()

    # Construct the fully qualified location path.
    parent = workflows_client.workflow_path(project, location, workflow)

    # Execute the workflow.
    response = execution_client.create_execution(request={"parent": parent})
    print(f"Created execution: {response.name}")
    return response

app = FastAPI()

@app.get("/")
def greet():
    # Define your workflow details
    project_id = 'writing-practice-app'
    location = 'europe-central2'
    workflow_name = 'call-private-endpoint'

    response = execute_workflow(project_id, location, workflow_name)
    return response.name
   


@app.get("/dupa/{id}/jasia")
def greet_with_id(id: int):
    return f"Hello {id}"
