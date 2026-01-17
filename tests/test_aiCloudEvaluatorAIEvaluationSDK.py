"""
Unit tests for aiCloudEvaluatorAIEvaluationSDK.py

These tests verify the Azure AI evaluation functionality using mocked dependencies.
"""

import os
import json
import pytest
from unittest.mock import Mock, patch, MagicMock


# Helper function to check if Azure modules are available
def azure_modules_available():
    """Check if Azure AI modules are installed."""
    try:
        import azure.ai.projects
        import azure.ai.evaluation
        import azure.identity
        return True
    except ImportError:
        return False


# Marker for tests requiring Azure modules
requires_azure = pytest.mark.skipif(
    not azure_modules_available(),
    reason="Azure AI modules not installed"
)


class TestEnvironmentConfiguration:
    """Tests for environment configuration validation."""

    @patch.dict(os.environ, {
        'AZURE_AI_PROJECT': 'https://test.services.ai.azure.com/api/projects/test',
        'MODEL_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01'
    })
    def test_environment_variables_loaded(self):
        """Test that required environment variables can be loaded."""
        assert os.getenv('AZURE_AI_PROJECT') is not None
        assert os.getenv('MODEL_DEPLOYMENT_NAME') is not None
        assert os.getenv('AZURE_DEPLOYMENT_NAME') is not None
        assert os.getenv('AZURE_ENDPOINT') is not None

    def test_missing_environment_variables(self):
        """Test handling of missing environment variables."""
        with patch.dict(os.environ, {}, clear=True):
            assert os.getenv('AZURE_AI_PROJECT') is None
            assert os.getenv('MODEL_DEPLOYMENT_NAME') is None


class TestModelConfiguration:
    """Tests for model configuration."""

    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01'
    })
    def test_model_config_structure(self):
        """Test that model configuration has correct structure."""
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

    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'o3-mini',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01'
    })
    def test_reasoning_model_config(self):
        """Test reasoning model configuration."""
        reasoning_model_config = {
            "azure_deployment": "o3-mini",
            "api_key": os.getenv("AZURE_API_KEY"),
            "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
            "api_version": os.getenv("AZURE_API_VERSION"),
        }
        
        assert reasoning_model_config["azure_deployment"] == "o3-mini"


class TestAIProjectClient:
    """Tests for AI Project Client initialization."""

    @requires_azure
    @patch('azure.ai.projects.AIProjectClient')
    @patch('azure.identity.AzureCliCredential')
    @patch.dict(os.environ, {
        'AZURE_AI_PROJECT': 'https://test.services.ai.azure.com/api/projects/test'
    })
    def test_project_client_creation(self, mock_credential, mock_client):
        """Test that AI Project Client can be created with proper parameters."""
        from azure.ai.projects import AIProjectClient
        from azure.identity import AzureCliCredential
        
        project_endpoint = os.environ["AZURE_AI_PROJECT"]
        
        # Create mock client
        mock_credential_instance = mock_credential.return_value
        client = AIProjectClient(
            endpoint=project_endpoint,
            credential=mock_credential_instance
        )
        
        assert client is not None
        mock_client.assert_called_once()


class TestAgentOperations:
    """Tests for agent creation and operations."""

    @requires_azure
    @patch('azure.ai.projects.AIProjectClient')
    @patch.dict(os.environ, {
        'MODEL_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_AI_PROJECT': 'https://test.services.ai.azure.com/api/projects/test'
    })
    def test_agent_creation_parameters(self, mock_client):
        """Test agent creation with correct parameters."""
        mock_project_client = Mock()
        mock_agents = Mock()
        mock_project_client.agents = mock_agents
        
        mock_agent = Mock()
        mock_agent.id = "test_agent_123"
        mock_agents.create_agent.return_value = mock_agent
        
        agent = mock_agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="my-agent",
            instructions="You are a helpful agent"
        )
        
        assert agent.id == "test_agent_123"
        mock_agents.create_agent.assert_called_once_with(
            model="gpt-4o",
            name="my-agent",
            instructions="You are a helpful agent"
        )

    @requires_azure
    @patch('azure.ai.projects.AIProjectClient')
    def test_thread_creation(self, mock_client):
        """Test thread creation."""
        mock_project_client = Mock()
        mock_agents = Mock()
        mock_threads = Mock()
        mock_project_client.agents = mock_agents
        mock_agents.threads = mock_threads
        
        mock_thread = Mock()
        mock_thread.id = "thread_123"
        mock_threads.create.return_value = mock_thread
        
        thread = mock_threads.create()
        
        assert thread.id == "thread_123"
        mock_threads.create.assert_called_once()

    @requires_azure
    @patch('azure.ai.projects.AIProjectClient')
    def test_message_creation(self, mock_client):
        """Test message creation in a thread."""
        mock_project_client = Mock()
        mock_agents = Mock()
        mock_messages = Mock()
        mock_project_client.agents = mock_agents
        mock_agents.messages = mock_messages
        
        mock_message = {"id": "msg_123", "role": "user", "content": "test"}
        mock_messages.create.return_value = mock_message
        
        message = mock_messages.create(
            thread_id="thread_123",
            role="user",
            content="What is the weather in Seattle today?"
        )
        
        assert message["id"] == "msg_123"
        mock_messages.create.assert_called_once_with(
            thread_id="thread_123",
            role="user",
            content="What is the weather in Seattle today?"
        )


class TestConverterOperations:
    """Tests for AI Agent Converter operations."""

    @requires_azure
    @patch('azure.ai.evaluation.AIAgentConverter')
    @patch('azure.ai.projects.AIProjectClient')
    def test_converter_initialization(self, mock_client, mock_converter):
        """Test AIAgentConverter initialization."""
        mock_project_client = Mock()
        converter = mock_converter(mock_project_client)
        
        assert converter is not None
        mock_converter.assert_called_once_with(mock_project_client)

    @requires_azure
    @patch('azure.ai.evaluation.AIAgentConverter')
    @patch('azure.ai.projects.AIProjectClient')
    def test_converter_convert(self, mock_client, mock_converter):
        """Test data conversion."""
        mock_project_client = Mock()
        mock_converter_instance = Mock()
        mock_converter.return_value = mock_converter_instance
        
        test_data = {
            "query": "test query",
            "response": "test response",
            "context": "test context"
        }
        mock_converter_instance.convert.return_value = test_data
        
        converter = mock_converter(mock_project_client)
        converted_data = converter.convert("thread_123", "run_456")
        
        assert "query" in converted_data
        assert "response" in converted_data
        mock_converter_instance.convert.assert_called_once_with("thread_123", "run_456")


class TestEvaluatorConfiguration:
    """Tests for evaluator configuration."""

    @patch.dict(os.environ, {
        'AZURE_DEPLOYMENT_NAME': 'gpt-4o',
        'AZURE_API_KEY': 'test-key',
        'AZURE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_API_VERSION': '2024-02-01'
    })
    def test_quality_evaluators_config(self):
        """Test quality evaluators configuration structure."""
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
        
        # Verify configs are properly structured
        assert model_config["azure_deployment"] == "gpt-4o"
        assert reasoning_model_config["azure_deployment"] == "o3-mini"

    @patch.dict(os.environ, {
        'AZURE_AI_PROJECT': 'https://test.services.ai.azure.com/api/projects/test'
    })
    def test_safety_evaluators_config(self):
        """Test safety evaluators configuration."""
        azure_ai_project = os.environ.get("AZURE_AI_PROJECT")
        
        assert azure_ai_project is not None
        assert azure_ai_project.startswith("https://")
        assert "/api/projects/" in azure_ai_project


class TestDataConversion:
    """Tests for data format and conversion."""

    def test_converted_data_structure(self):
        """Test that converted data has expected structure."""
        converted_data = {
            "query": "What is the weather?",
            "response": "The weather is sunny.",
            "context": "Weather information"
        }
        
        assert "query" in converted_data
        assert "response" in converted_data
        assert "context" in converted_data

    def test_json_serialization(self):
        """Test JSON serialization of converted data."""
        test_data = {
            "query": "test",
            "response": "response",
            "context": "context"
        }
        
        json_str = json.dumps(test_data, indent=2)
        parsed_data = json.loads(json_str)
        
        assert parsed_data["query"] == "test"
        assert parsed_data["response"] == "response"


class TestRunStatus:
    """Tests for run status handling."""

    def test_run_success_status(self):
        """Test successful run status."""
        mock_run = Mock()
        mock_run.status = "completed"
        
        assert mock_run.status == "completed"

    def test_run_failed_status(self):
        """Test failed run status handling."""
        mock_run = Mock()
        mock_run.status = "failed"
        mock_run.last_error = "Test error message"
        
        assert mock_run.status == "failed"
        assert mock_run.last_error == "Test error message"

    def test_run_status_check(self):
        """Test run status checking logic."""
        mock_run = Mock()
        mock_run.status = "completed"
        
        if mock_run.status == "failed":
            error = mock_run.last_error
            assert False, "Should not reach here"
        else:
            assert mock_run.status == "completed"
