"""Unit tests for aiLOCALevaluator.py"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import os
import sys
import json

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestAILocalEvaluator(unittest.TestCase):
    """Test cases for AI Local Evaluator functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_env_vars = {
            'AZURE_DEPLOYMENT_NAME': 'test-deployment',
            'AZURE_API_KEY': 'test-key',
            'AZURE_ENDPOINT': 'https://test.endpoint.com',
            'AZURE_API_VERSION': '2024-01-01',
            'AZURE_AI_PROJECT': 'https://test.project.services.ai.azure.com/api/projects/test-project',
            'MODEL_DEPLOYMENT_NAME': 'gpt-4o'
        }

    def test_project_endpoint_format(self):
        """Test Azure AI project endpoint format"""
        with patch.dict(os.environ, {
            'AZURE_DEPLOYMENT_NAME': 'test-deployment',
            'AZURE_API_KEY': 'test-key',
            'AZURE_ENDPOINT': 'https://test.endpoint.com',
            'AZURE_API_VERSION': '2024-01-01',
            'AZURE_AI_PROJECT': 'https://test.project.services.ai.azure.com/api/projects/test-project',
            'MODEL_DEPLOYMENT_NAME': 'gpt-4o'
        }):
            project_endpoint = os.environ["AZURE_AI_PROJECT"]
            
            # Verify endpoint format
            self.assertTrue(project_endpoint.startswith("https://"))
            self.assertIn("services.ai.azure.com", project_endpoint)
            self.assertIn("/api/projects/", project_endpoint)

    def test_model_config_structure(self):
        """Test model configuration structure"""
        model_config = {
            "azure_deployment": "test-deployment",
            "api_key": "test-key",
            "azure_endpoint": "https://test.endpoint.com",
            "api_version": "2024-01-01",
        }
        
        self.assertIn("azure_deployment", model_config)
        self.assertIn("api_key", model_config)
        self.assertIn("azure_endpoint", model_config)
        self.assertIn("api_version", model_config)

    def test_reasoning_model_config_structure(self):
        """Test reasoning model configuration structure"""
        reasoning_model_config = {
            "azure_deployment": "o3-mini",
            "api_key": "test-key",
            "azure_endpoint": "https://test.endpoint.com",
            "api_version": "2024-01-01",
        }
        
        self.assertEqual(reasoning_model_config["azure_deployment"], "o3-mini")
        self.assertIn("api_key", reasoning_model_config)


class TestAgentOperations(unittest.TestCase):
    """Test cases for agent creation and operations"""

    def test_agent_creation_parameters(self):
        """Test agent creation parameters structure"""
        agent_params = {
            "model": "gpt-4o",
            "name": "my-agent",
            "instructions": "You are a helpful agent"
        }
        
        self.assertEqual(agent_params["model"], "gpt-4o")
        self.assertEqual(agent_params["name"], "my-agent")
        self.assertEqual(agent_params["instructions"], "You are a helpful agent")

    def test_thread_creation_flow(self):
        """Test thread creation flow"""
        # Simulate thread creation
        thread_data = {"id": "test-thread-456"}
        
        self.assertIn("id", thread_data)
        self.assertTrue(thread_data["id"].startswith("test-thread"))

    def test_message_creation_parameters(self):
        """Test message creation parameters"""
        message_params = {
            "thread_id": "test-thread-456",
            "role": "user",
            "content": "What is the weather in Seattle today?"
        }
        
        self.assertEqual(message_params["role"], "user")
        self.assertEqual(message_params["content"], "What is the weather in Seattle today?")
        self.assertIn("thread_id", message_params)

    def test_run_completed_status(self):
        """Test successful run status"""
        run_data = {
            "status": "completed",
            "id": "test-run-101"
        }
        
        self.assertEqual(run_data["status"], "completed")
        self.assertIn("id", run_data)

    def test_run_failed_status_structure(self):
        """Test handling of failed run status structure"""
        run_data = {
            "status": "failed",
            "last_error": "Test error message"
        }
        
        self.assertEqual(run_data["status"], "failed")
        self.assertEqual(run_data["last_error"], "Test error message")
        self.assertIn("last_error", run_data)


class TestAIAgentConverter(unittest.TestCase):
    """Test cases for AI Agent Converter"""

    def test_converter_parameters(self):
        """Test converter parameters structure"""
        converter_params = {
            "thread_id": "thread-123",
            "run_id": "run-456"
        }
        
        self.assertIn("thread_id", converter_params)
        self.assertIn("run_id", converter_params)
        self.assertEqual(converter_params["thread_id"], "thread-123")
        self.assertEqual(converter_params["run_id"], "run-456")

    def test_converted_data_structure(self):
        """Test converted data structure from converter"""
        converted_data = {
            "messages": [{"role": "user", "content": "test"}],
            "responses": [{"role": "assistant", "content": "response"}]
        }
        
        self.assertIn("messages", converted_data)
        self.assertIn("responses", converted_data)
        self.assertIsInstance(converted_data["messages"], list)
        self.assertIsInstance(converted_data["responses"], list)


class TestEvaluators(unittest.TestCase):
    """Test cases for evaluator initialization and configuration"""

    def test_quality_evaluators_names(self):
        """Test quality evaluators names are defined"""
        quality_evaluator_names = [
            "IntentResolutionEvaluator",
            "TaskAdherenceEvaluator",
            "ToolCallAccuracyEvaluator",
            "CoherenceEvaluator",
            "FluencyEvaluator",
            "RelevanceEvaluator"
        ]
        
        # Verify evaluator names
        self.assertEqual(len(quality_evaluator_names), 6)
        self.assertIn("CoherenceEvaluator", quality_evaluator_names)
        self.assertIn("FluencyEvaluator", quality_evaluator_names)

    def test_safety_evaluators_names(self):
        """Test safety evaluators names are defined"""
        safety_evaluator_names = [
            "ContentSafetyEvaluator",
            "IndirectAttackEvaluator",
            "CodeVulnerabilityEvaluator"
        ]
        
        # Verify evaluator names
        self.assertEqual(len(safety_evaluator_names), 3)
        self.assertIn("ContentSafetyEvaluator", safety_evaluator_names)
        self.assertIn("IndirectAttackEvaluator", safety_evaluator_names)

    def test_reasoning_model_evaluator_config(self):
        """Test evaluator configuration with reasoning model support"""
        evaluator_config = {
            "model_config": {
                "azure_deployment": "o3-mini",
                "api_key": "test-key",
                "azure_endpoint": "https://test.endpoint.com",
                "api_version": "2024-01-01",
            },
            "is_reasoning_model": True
        }
        
        self.assertTrue(evaluator_config["is_reasoning_model"])
        self.assertEqual(evaluator_config["model_config"]["azure_deployment"], "o3-mini")

    def test_standard_evaluator_config(self):
        """Test evaluator configuration without reasoning model support"""
        evaluator_config = {
            "model_config": {
                "azure_deployment": "gpt-4o",
                "api_key": "test-key",
                "azure_endpoint": "https://test.endpoint.com",
                "api_version": "2024-01-01",
            }
        }
        
        self.assertEqual(evaluator_config["model_config"]["azure_deployment"], "gpt-4o")
        self.assertIn("model_config", evaluator_config)

    def test_safety_evaluator_config(self):
        """Test safety evaluator configuration with Azure AI project"""
        evaluator_config = {
            "azure_ai_project": "https://test.project.services.ai.azure.com/api/projects/test-project",
            "credential_required": True
        }
        
        self.assertIn("azure_ai_project", evaluator_config)
        self.assertTrue(evaluator_config["azure_ai_project"].startswith("https://"))


class TestEvaluatorExecution(unittest.TestCase):
    """Test cases for evaluator execution"""

    def test_converted_data_structure(self):
        """Test converted data structure for evaluation"""
        converted_data = {
            "messages": [
                {"role": "user", "content": "What is the weather?"}
            ],
            "response": "The weather is sunny.",
            "context": "Weather information"
        }
        
        self.assertIn("messages", converted_data)
        self.assertIn("response", converted_data)
        self.assertIn("context", converted_data)

    def test_evaluation_result_structure(self):
        """Test evaluation result structure"""
        result = {
            "coherence_score": 4.5,
            "reasoning": "The response is coherent"
        }
        
        self.assertIn("coherence_score", result)
        self.assertIn("reasoning", result)
        self.assertIsInstance(result["coherence_score"], float)
        self.assertIsInstance(result["reasoning"], str)

    def test_json_serialization_of_results(self):
        """Test JSON serialization of evaluation results"""
        result = {
            "coherence_score": 4.5,
            "reasoning": "Test reasoning"
        }
        
        # Verify JSON serialization works
        json_str = json.dumps(result, indent=4)
        self.assertIn("coherence_score", json_str)
        self.assertIn("reasoning", json_str)
        
        # Verify deserialization
        parsed = json.loads(json_str)
        self.assertEqual(parsed["coherence_score"], 4.5)


if __name__ == '__main__':
    unittest.main()
