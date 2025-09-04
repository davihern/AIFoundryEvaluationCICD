import os
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

import json, os
from azure.ai.evaluation import IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator 
from azure.ai.evaluation import RelevanceEvaluator, CoherenceEvaluator, CodeVulnerabilityEvaluator, ContentSafetyEvaluator, IndirectAttackEvaluator, FluencyEvaluator,SimilarityEvaluator

from azure.ai.evaluation import AIAgentConverter

from azure.ai.evaluation import evaluate
from azure.ai.evaluation import GroundednessEvaluator, AzureOpenAIModelConfiguration

load_dotenv()

print("Loaded environment variables.")
print(f"Azure Deployment Name: {os.getenv('AZURE_DEPLOYMENT_NAME')}")
print(f"Azure Endpoint: {os.getenv('AZURE_ENDPOINT')}")
print(f"Azure API Version: {os.getenv('AZURE_API_VERSION')}")



model_config = {
    "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME"),
    "api_key": os.getenv("AZURE_API_KEY"),
    "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
    "api_version": os.getenv("AZURE_API_VERSION"),
}

azure_ai_project = os.environ.get("AZURE_AI_PROJECT")

#Upload results to AI Foundry
groundedness_eval = GroundednessEvaluator(model_config)
similarity = SimilarityEvaluator(model_config=model_config, threshold=3)

result = evaluate(
    data="sample.jsonl", # Provide your data here:
    evaluators={
        "groundedness": groundedness_eval,
        "similarity": similarity
    },
    # Column mapping:
    evaluator_config={
        "groundedness": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${data.response}"
            },
        "similarity": {
            "column_mapping": {
                "query": "${data.query}",
                "ground_truth": "${data.context}",
                "response": "${data.response}"
            }
        }
        }
    },
    # Optionally, provide your Azure AI Foundry project information to track your evaluation results in your project portal.
    azure_ai_project = azure_ai_project,
    # Optionally, provide an output path to dump a JSON file of metric summary, row-level data, and the metric and Azure AI project URL.
    output_path="./myevalresults.json"
)