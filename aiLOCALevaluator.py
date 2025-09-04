# Following these steps https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/agent-evaluate-sdk

import os
from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

import json, os
from azure.ai.evaluation import IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator 
from azure.ai.evaluation import RelevanceEvaluator, CoherenceEvaluator, CodeVulnerabilityEvaluator, ContentSafetyEvaluator, IndirectAttackEvaluator, FluencyEvaluator

from azure.ai.evaluation import AIAgentConverter

from azure.ai.evaluation import evaluate
from azure.ai.evaluation import GroundednessEvaluator, AzureOpenAIModelConfiguration


load_dotenv()

# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
# Azure AI Foundry project endpoint, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
project_endpoint = os.environ["AZURE_AI_PROJECT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

print(f"Using Azure AI Project endpoint: {project_endpoint}")
print(f"Using Model Deployment Name: {os.environ['MODEL_DEPLOYMENT_NAME']}")


# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=AzureCliCredential(),  # Use Azure CLI Credential for authentication
)

# Create an agent with the toolset 
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
    name="my-agent",  # Name of the agent
    instructions="You are a helpful agent",  # Instructions for the agent
    #toolset=toolset
)
print(f"Created agent, ID: {agent.id}")

# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Add a message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",  # Role of the message sender
    content="What is the weather in Seattle today?",  # Message content
)
print(f"Created message, ID: {message['id']}")

# Create and process an agent run
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages:
    print(f"Role: {message.role}, Content: {message.content}")


# Initialize the converter for Azure AI agents.
converter = AIAgentConverter(project_client)

# Specify the thread and run ID.
thread_id = thread.id
run_id = run.id

converted_data = converter.convert(thread_id, run_id)

print("Converted Data: ")
print(json.dumps(converted_data, indent=2))

######################


model_config = {
    "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME"),
    "api_key": os.getenv("AZURE_API_KEY"),
    "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
    "api_version": os.getenv("AZURE_API_VERSION"),
}

reasoning_model_config = {
    "azure_deployment": "o3-mini",
    "api_key": os.getenv("AZURE_API_KEY"),
    "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
    "api_version": os.getenv("AZURE_API_VERSION"),
}

# Evaluators with reasoning model support
quality_evaluators = {evaluator.__name__: evaluator(model_config=reasoning_model_config, is_reasoning_model=True) for evaluator in [IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator]}

# Other evaluators do not support reasoning models 
quality_evaluators.update({ evaluator.__name__: evaluator(model_config=model_config) for evaluator in [CoherenceEvaluator, FluencyEvaluator, RelevanceEvaluator]})

## Using Azure AI Foundry (non-Hub) project endpoint, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
azure_ai_project = os.environ.get("AZURE_AI_PROJECT")

safety_evaluators = {evaluator.__name__: evaluator(azure_ai_project=azure_ai_project, credential=AzureCliCredential()) for evaluator in [ContentSafetyEvaluator, IndirectAttackEvaluator, CodeVulnerabilityEvaluator]}

# Reference the quality and safety evaluator list above.
quality_and_safety_evaluators = {**quality_evaluators, **safety_evaluators}

for name, evaluator in quality_and_safety_evaluators.items():
    result = evaluator(**converted_data)
    print(name)
    print(json.dumps(result, indent=4)) 


#######
