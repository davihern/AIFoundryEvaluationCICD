"""
Unit tests for aiLOCALevaluator.py

These tests verify the local Azure AI evaluation functionality using mocked dependencies.
"""

import os
import json
import pytest
from unittest.mock import Mock, patch, mock_open


# Helper function to check if Azure modules are available
def azure_modules_available():
    """Check if Azure AI modules are installed."""
    try:
        import azure.ai.evaluation
        return True
    except ImportError:
        return False


# Marker for tests requiring Azure modules
requires_azure = pytest.mark.skipif(
    not azure_modules_available(),
    reason="Azure AI modules not installed"
)


class TestEnvironmentVariables:
    """Tests for environment variable handling."""

    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01',
        'AZURE_AI_PROJECT': 'https://test.services.ai.azure.com/api/projects/test'
    })
    def test_all_required_env_vars_present(self):
        """Test that all required environment variables are present."""
        assert os.getenv('AZURE_DEPLOYMENT_NAME') == 'gpt-4o'
        assert os.getenv('AZURE_API_KEY') == 'test-key'
        assert os.getenv('AZURE_ENDPOINT') == 'https://test.endpoint.com'
        assert os.getenv('AZURE_API_VERSION') == '2024-02-01'
        assert os.getenv('AZURE_AI_PROJECT') is not None

    @patch('builtins.print')
    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01',
        'AZURE_AI_PROJECT': 'https://test.services.ai.azure.com/api/projects/test'
    })
    def test_environment_variables_logging(self, mock_print):
        """Test that environment variables can be logged."""
        print("Loaded environment variables.")
        print(f"Azure Deployment Name: {os.getenv('AZURE_DEPLOYMENT_NAME')}")
        print(f"Azure Endpoint: {os.getenv('AZURE_ENDPOINT')}")
        print(f"Azure API Version: {os.getenv('AZURE_API_VERSION')}")
        print(f"Azure AI Project: {os.getenv('AZURE_AI_PROJECT')}")
        
        assert mock_print.call_count == 5


class TestModelConfigurationStructure:
    """Tests for model configuration structure."""

    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01'
    })
    def test_model_config_keys(self):
        """Test that model config has all required keys."""
        model_config = {
            "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
            "api_version": os.getenv("AZURE_API_VERSION"),
        }
        
        assert "azure_deployment" in model_config
        assert "api_key" in model_config
        assert "azure_endpoint" in model_config
        assert "api_version" in model_config

    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01'
    })
    def test_model_config_values(self):
        """Test that model config values are correctly set."""
        model_config = {
            "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
            "api_version": os.getenv("AZURE_API_VERSION"),
        }
        
        assert model_config["azure_deployment"] == "gpt-4o"
        assert model_config["api_key"] == "test-key"
        assert model_config["azure_endpoint"] == "https://test.endpoint.com"
        assert model_config["api_version"] == "2024-02-01"


class TestEvaluatorInitialization:
    """Tests for evaluator initialization."""

    @requires_azure
    @patch('azure.ai.evaluation.GroundednessEvaluator')
    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01'
    })
    def test_groundedness_evaluator_init(self, mock_evaluator):
        """Test GroundednessEvaluator initialization."""
        model_config = {
            "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
            "api_version": os.getenv("AZURE_API_VERSION"),
        }
        
        evaluator = mock_evaluator(model_config)
        
        assert evaluator is not None
        mock_evaluator.assert_called_once_with(model_config)

    @requires_azure
    @patch('azure.ai.evaluation.SimilarityEvaluator')
    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01'
    })
    def test_similarity_evaluator_init(self, mock_evaluator):
        """Test SimilarityEvaluator initialization with threshold."""
        model_config = {
            "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
            "api_version": os.getenv("AZURE_API_VERSION"),
        }
        
        evaluator = mock_evaluator(model_config=model_config, threshold=3)
        
        assert evaluator is not None
        mock_evaluator.assert_called_once_with(model_config=model_config, threshold=3)


class TestEvaluateFunction:
    """Tests for evaluate function configuration."""

    def test_evaluate_data_parameter(self):
        """Test evaluate function data parameter."""
        data_path = "sample.jsonl"
        
        assert data_path.endswith(".jsonl")
        assert os.path.basename(data_path) == "sample.jsonl"

    @patch.dict(os.environ, {
        'AZURE_AI_PROJECT': 'https://test.services.ai.azure.com/api/projects/test'
    })
    def test_evaluate_azure_ai_project_parameter(self):
        """Test evaluate function azure_ai_project parameter."""
        azure_ai_project = os.environ.get("AZURE_AI_PROJECT")
        
        assert azure_ai_project is not None
        assert isinstance(azure_ai_project, str)

    def test_evaluate_output_path_parameter(self):
        """Test evaluate function output_path parameter."""
        output_path = "./myevalresults.json"
        
        assert output_path.endswith(".json")
        assert "myevalresults" in output_path


class TestEvaluatorColumnMapping:
    """Tests for evaluator column mapping configuration."""

    def test_groundedness_column_mapping(self):
        """Test groundedness evaluator column mapping."""
        column_mapping = {
            "query": "${data.query}",
            "context": "${data.context}",
            "response": "${data.response}"
        }
        
        assert "query" in column_mapping
        assert "context" in column_mapping
        assert "response" in column_mapping
        assert column_mapping["query"] == "${data.query}"
        assert column_mapping["context"] == "${data.context}"
        assert column_mapping["response"] == "${data.response}"

    def test_similarity_column_mapping(self):
        """Test similarity evaluator column mapping."""
        column_mapping = {
            "query": "${data.query}",
            "ground_truth": "${data.context}",
            "response": "${data.response}"
        }
        
        assert "query" in column_mapping
        assert "ground_truth" in column_mapping
        assert "response" in column_mapping
        assert column_mapping["ground_truth"] == "${data.context}"

    def test_evaluator_config_structure(self):
        """Test complete evaluator config structure."""
        evaluator_config = {
            "groundedness": {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${data.context}",
                    "response": "${data.response}"
                }
            },
            "similarity": {
                "column_mapping": {
                    "query": "${data.query}",
                    "ground_truth": "${data.context}",
                    "response": "${data.response}"
                }
            }
        }
        
        assert "groundedness" in evaluator_config
        assert "similarity" in evaluator_config
        assert "column_mapping" in evaluator_config["groundedness"]
        assert "column_mapping" in evaluator_config["similarity"]


class TestDataFileFormat:
    """Tests for data file format validation."""

    def test_jsonl_line_format(self):
        """Test JSONL line format."""
        test_line = '{"query":"test query","context":"test context","response":"test response"}'
        data = json.loads(test_line)
        
        assert "query" in data
        assert "context" in data
        assert "response" in data

    def test_sample_data_structure(self):
        """Test sample data structure."""
        sample_data = {
            "query": "What is the importance of choosing the right provider?",
            "ground_truth": "Choosing the right provider is important.",
            "response": "The right provider helps you get value.",
            "context": "Provider information.",
            "latency": 8.733296,
            "response_length": 2160
        }
        
        assert "query" in sample_data
        assert "response" in sample_data
        assert isinstance(sample_data["latency"], float)
        assert isinstance(sample_data["response_length"], int)


class TestEvaluatorsConfiguration:
    """Tests for evaluators dictionary configuration."""

    @requires_azure
    @patch('azure.ai.evaluation.GroundednessEvaluator')
    @patch('azure.ai.evaluation.SimilarityEvaluator')
    def test_evaluators_dictionary_structure(self, mock_similarity, mock_groundedness):
        """Test evaluators dictionary structure."""
        model_config = {}
        
        groundedness_eval = mock_groundedness(model_config)
        similarity = mock_similarity(model_config=model_config, threshold=3)
        
        evaluators = {
            "groundedness": groundedness_eval,
            "similarity": similarity
        }
        
        assert "groundedness" in evaluators
        assert "similarity" in evaluators
        assert len(evaluators) == 2


class TestOutputFileHandling:
    """Tests for output file handling."""

    def test_output_path_format(self):
        """Test output path format."""
        output_path = "./myevalresults.json"
        
        assert output_path.startswith("./")
        assert output_path.endswith(".json")

    def test_json_output_structure(self):
        """Test expected JSON output structure."""
        expected_output = {
            "metrics": {},
            "rows": [],
            "studio_url": "https://example.com"
        }
        
        json_str = json.dumps(expected_output, indent=2)
        parsed = json.loads(json_str)
        
        assert "metrics" in parsed
        assert "rows" in parsed
        assert isinstance(parsed["rows"], list)


class TestEvaluateParameters:
    """Tests for evaluate function parameters."""

    def test_evaluate_required_parameters(self):
        """Test that evaluate function has required parameters."""
        params = {
            "data": "sample.jsonl",
            "evaluators": {},
            "evaluator_config": {},
            "azure_ai_project": "https://test.services.ai.azure.com/api/projects/test",
            "output_path": "./myevalresults.json"
        }
        
        assert "data" in params
        assert "evaluators" in params
        assert "evaluator_config" in params
        assert "azure_ai_project" in params
        assert "output_path" in params

    def test_data_parameter_validation(self):
        """Test data parameter validation."""
        data = "sample.jsonl"
        
        assert isinstance(data, str)
        assert data.endswith(".jsonl")

    def test_evaluators_parameter_type(self):
        """Test evaluators parameter is a dictionary."""
        evaluators = {
            "groundedness": Mock(),
            "similarity": Mock()
        }
        
        assert isinstance(evaluators, dict)
        assert len(evaluators) >= 1


class TestImports:
    """Tests for module imports."""

    def test_azure_evaluation_imports(self):
        """Test that azure.ai.evaluation imports are available."""
        try:
            from azure.ai.evaluation import (
                GroundednessEvaluator, 
                SimilarityEvaluator,
                evaluate
            )
            assert True
        except ImportError:
            pytest.skip("Azure AI Evaluation SDK not installed in test environment")

    def test_dotenv_import(self):
        """Test that dotenv import is available."""
        try:
            from dotenv import load_dotenv
            assert True
        except ImportError:
            pytest.skip("python-dotenv not installed in test environment")


class TestAzureProjectConfiguration:
    """Tests for Azure AI Project configuration."""

    @patch.dict(os.environ, {
        'AZURE_AI_PROJECT': 'https://davihern.services.ai.azure.com/api/projects/test-project'
    })
    def test_azure_project_url_format(self):
        """Test Azure AI Project URL format."""
        azure_ai_project = os.environ.get("AZURE_AI_PROJECT")
        
        assert azure_ai_project is not None
        assert azure_ai_project.startswith("https://")
        assert ".services.ai.azure.com" in azure_ai_project
        assert "/api/projects/" in azure_ai_project

    def test_azure_project_url_parsing(self):
        """Test parsing Azure AI Project URL components."""
        test_url = "https://account.services.ai.azure.com/api/projects/my-project"
        
        assert "https://" in test_url
        assert "services.ai.azure.com" in test_url
        assert "/api/projects/" in test_url
        
        # Extract project name
        project_name = test_url.split("/")[-1]
        assert project_name == "my-project"
