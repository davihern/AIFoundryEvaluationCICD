"""Example usage of EvaluationConfig class with Azure AI evaluation.

This example demonstrates how to use the EvaluationConfig class
to manage configuration for Azure AI evaluation tasks.
"""
from evaluation_config import EvaluationConfig
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Example 1: Create configuration from environment variables
print("Example 1: Configuration from environment variables")
print("-" * 50)
config = EvaluationConfig()

if config.is_valid():
    print("✓ Configuration is valid")
    model_config = config.get_model_config()
    print(f"Model config ready with deployment: {model_config['azure_deployment']}")
else:
    print("✗ Configuration is incomplete")
    try:
        config.validate()
    except ValueError as e:
        print(f"Validation error: {e}")

print()

# Example 2: Create configuration with explicit parameters
print("Example 2: Configuration with explicit parameters")
print("-" * 50)
custom_config = EvaluationConfig(
    azure_deployment="my-custom-deployment",
    api_key="sk-test-key-1234567890",
    azure_endpoint="https://my-custom-endpoint.openai.azure.com",
    api_version="2024-02-01",
    azure_ai_project="https://my-project.services.ai.azure.com/api/projects/my-project"
)

print(f"✓ Custom configuration created: {custom_config.azure_deployment}")
print(f"✓ Is valid: {custom_config.is_valid()}")
print(f"✓ Configuration: {repr(custom_config)}")

print()

# Example 3: Use with Azure AI evaluation (conceptual)
print("Example 3: Integration with Azure AI evaluation")
print("-" * 50)
print("# This is how you would use EvaluationConfig with the existing evaluation scripts:")
print()
print("from azure.ai.evaluation import GroundednessEvaluator, SimilarityEvaluator")
print("from evaluation_config import EvaluationConfig")
print()
print("# Create configuration")
print("config = EvaluationConfig()")
print("config.validate()  # Ensure all required fields are present")
print()
print("# Get model configuration for evaluators")
print("model_config = config.get_model_config()")
print()
print("# Initialize evaluators with the configuration")
print("groundedness_eval = GroundednessEvaluator(model_config)")
print("similarity_eval = SimilarityEvaluator(model_config=model_config, threshold=3)")
print()
print("# Use azure_ai_project if available")
print("azure_ai_project = config.azure_ai_project")
print()
print("This provides a clean, testable way to manage Azure AI evaluation configuration!")
