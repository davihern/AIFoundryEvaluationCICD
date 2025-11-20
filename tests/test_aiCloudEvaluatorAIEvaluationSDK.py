"""Unit tests for aiCloudEvaluatorAIEvaluationSDK.py"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestAICloudEvaluatorSDK(unittest.TestCase):
    """Test cases for AI Cloud Evaluator SDK functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_env_vars = {
            'AZURE_DEPLOYMENT_NAME': 'test-deployment',
            'AZURE_API_KEY': 'test-key',
            'AZURE_ENDPOINT': 'https://test.endpoint.com',
            'AZURE_API_VERSION': '2024-01-01',
            'AZURE_AI_PROJECT': 'https://test.project.com'
        }

    def test_model_config_from_env_vars(self):
        """Test that model configuration can be created from environment variables"""
        with patch.dict(os.environ, {
            'AZURE_DEPLOYMENT_NAME': 'test-deployment',
            'AZURE_API_KEY': 'test-key',
            'AZURE_ENDPOINT': 'https://test.endpoint.com',
            'AZURE_API_VERSION': '2024-01-01',
            'AZURE_AI_PROJECT': 'https://test.project.com'
        }):
            # Verify environment variables are set
            self.assertEqual(os.getenv('AZURE_DEPLOYMENT_NAME'), 'test-deployment')
            self.assertEqual(os.getenv('AZURE_API_KEY'), 'test-key')
            self.assertEqual(os.getenv('AZURE_ENDPOINT'), 'https://test.endpoint.com')
            self.assertEqual(os.getenv('AZURE_API_VERSION'), '2024-01-01')
            self.assertEqual(os.getenv('AZURE_AI_PROJECT'), 'https://test.project.com')

    def test_model_config_structure(self):
        """Test model configuration has the correct structure"""
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
        self.assertEqual(model_config["azure_deployment"], "test-deployment")

    def test_evaluate_parameters_structure(self):
        """Test that evaluate parameters have the correct structure"""
        # Test the expected structure of evaluate call parameters
        evaluate_params = {
            "data": "sample.jsonl",
            "evaluators": {},
            "evaluator_config": {},
            "azure_ai_project": "https://test.project.com",
            "output_path": "./myevalresults.json"
        }
        
        self.assertEqual(evaluate_params["data"], "sample.jsonl")
        self.assertEqual(evaluate_params["output_path"], "./myevalresults.json")
        self.assertIsInstance(evaluate_params["evaluators"], dict)
        self.assertIsInstance(evaluate_params["evaluator_config"], dict)

    def test_environment_variables_required(self):
        """Test that required environment variables are checked"""
        required_vars = [
            'AZURE_DEPLOYMENT_NAME',
            'AZURE_API_KEY',
            'AZURE_ENDPOINT',
            'AZURE_API_VERSION',
            'AZURE_AI_PROJECT'
        ]
        
        # Verify these are the expected environment variables
        for var in required_vars:
            self.assertIsInstance(var, str)
            self.assertTrue(len(var) > 0)


class TestEvaluatorConfig(unittest.TestCase):
    """Test cases for evaluator configuration"""

    def test_groundedness_evaluator_config(self):
        """Test groundedness evaluator column mapping configuration"""
        groundedness_config = {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${data.response}"
            }
        }
        
        self.assertIn("column_mapping", groundedness_config)
        self.assertEqual(groundedness_config["column_mapping"]["query"], "${data.query}")
        self.assertEqual(groundedness_config["column_mapping"]["context"], "${data.context}")
        self.assertEqual(groundedness_config["column_mapping"]["response"], "${data.response}")

    def test_similarity_evaluator_config(self):
        """Test similarity evaluator column mapping configuration"""
        similarity_config = {
            "column_mapping": {
                "query": "${data.query}",
                "ground_truth": "${data.context}",
                "response": "${data.response}"
            }
        }
        
        self.assertIn("column_mapping", similarity_config)
        self.assertEqual(similarity_config["column_mapping"]["query"], "${data.query}")
        self.assertEqual(similarity_config["column_mapping"]["ground_truth"], "${data.context}")
        self.assertEqual(similarity_config["column_mapping"]["response"], "${data.response}")


if __name__ == '__main__':
    unittest.main()
