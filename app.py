from fastapi import FastAPI
from google.cloud import workflows_v1
from google.cloud.workflows_v1.types import ExecuteWorkflowRequest
import google.auth

app = FastAPI()

@app.get("/")
def greet():
    # Define your workflow details
    project_id = 'writing-practice-app'
    location = 'europe-central2'
    workflow_name = 'call-private-endpoint'

    # Construct the fully qualified workflow path
    workflow_path = f'projects/{project_id}/locations/{location}/workflows/{workflow_name}'

    # Obtain the default credentials
    credentials, _ = google.auth.default()

    # Initialize the Workflows client
    client = workflows_v1.ExecutionsClient(credentials=credentials)

    # Execute the workflow
    response = client.create_execution(request=ExecuteWorkflowRequest(name=workflow_path))

    # Print the execution response
    print(f'Execution started: {response.name}')
    return response.name


@app.get("/dupa/{id}/jasia")
def greet_with_id(id: int):
    return f"Hello {id}"
