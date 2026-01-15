"""Unit tests for EvaluationConfig class."""
import os
import pytest
from evaluation_config import EvaluationConfig


class TestEvaluationConfigInitialization:
    """Tests for EvaluationConfig initialization."""

    def test_init_with_all_parameters(self):
        """Test initialization with all parameters provided."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key-123456789",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
            azure_ai_project="https://test.project.com",
        )

        assert config.azure_deployment == "test-deployment"
        assert config.api_key == "test-key-123456789"
        assert config.azure_endpoint == "https://test.endpoint.com"
        assert config.api_version == "2024-01-01"
        assert config.azure_ai_project == "https://test.project.com"

    def test_init_with_no_parameters(self):
        """Test initialization with no parameters falls back to environment variables."""
        # Clear any existing env vars
        env_vars = [
            "AZURE_DEPLOYMENT_NAME",
            "AZURE_API_KEY",
            "AZURE_ENDPOINT",
            "AZURE_API_VERSION",
            "AZURE_AI_PROJECT",
        ]
        original_values = {key: os.getenv(key) for key in env_vars}

        try:
            # Clear all env vars
            for key in env_vars:
                if key in os.environ:
                    del os.environ[key]

            config = EvaluationConfig()

            assert config.azure_deployment is None
            assert config.api_key is None
            assert config.azure_endpoint is None
            assert config.api_version is None
            assert config.azure_ai_project is None
        finally:
            # Restore original values
            for key, value in original_values.items():
                if value is not None:
                    os.environ[key] = value

    def test_init_from_environment_variables(self):
        """Test initialization from environment variables."""
        env_vars = {
            "AZURE_DEPLOYMENT_NAME": "env-deployment",
            "AZURE_API_KEY": "env-key-987654321",
            "AZURE_ENDPOINT": "https://env.endpoint.com",
            "AZURE_API_VERSION": "2024-02-01",
            "AZURE_AI_PROJECT": "https://env.project.com",
        }

        # Store original values
        original_values = {key: os.getenv(key) for key in env_vars.keys()}

        try:
            # Set env vars
            for key, value in env_vars.items():
                os.environ[key] = value

            config = EvaluationConfig()

            assert config.azure_deployment == "env-deployment"
            assert config.api_key == "env-key-987654321"
            assert config.azure_endpoint == "https://env.endpoint.com"
            assert config.api_version == "2024-02-01"
            assert config.azure_ai_project == "https://env.project.com"
        finally:
            # Restore original values
            for key, value in original_values.items():
                if value is not None:
                    os.environ[key] = value
                elif key in os.environ:
                    del os.environ[key]

    def test_init_parameters_override_environment(self):
        """Test that explicit parameters override environment variables."""
        # Set env var
        original_value = os.getenv("AZURE_DEPLOYMENT_NAME")
        os.environ["AZURE_DEPLOYMENT_NAME"] = "env-deployment"

        try:
            config = EvaluationConfig(azure_deployment="param-deployment")
            assert config.azure_deployment == "param-deployment"
        finally:
            if original_value is not None:
                os.environ["AZURE_DEPLOYMENT_NAME"] = original_value
            elif "AZURE_DEPLOYMENT_NAME" in os.environ:
                del os.environ["AZURE_DEPLOYMENT_NAME"]


class TestEvaluationConfigGetModelConfig:
    """Tests for get_model_config method."""

    def test_get_model_config_returns_correct_structure(self):
        """Test that get_model_config returns correct dictionary structure."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        model_config = config.get_model_config()

        assert isinstance(model_config, dict)
        assert "azure_deployment" in model_config
        assert "api_key" in model_config
        assert "azure_endpoint" in model_config
        assert "api_version" in model_config

    def test_get_model_config_contains_correct_values(self):
        """Test that get_model_config contains correct values."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        model_config = config.get_model_config()

        assert model_config["azure_deployment"] == "test-deployment"
        assert model_config["api_key"] == "test-key"
        assert model_config["azure_endpoint"] == "https://test.endpoint.com"
        assert model_config["api_version"] == "2024-01-01"

    def test_get_model_config_excludes_azure_ai_project(self):
        """Test that get_model_config excludes azure_ai_project field."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
            azure_ai_project="https://test.project.com",
        )

        model_config = config.get_model_config()

        assert "azure_ai_project" not in model_config


class TestEvaluationConfigIsValid:
    """Tests for is_valid method."""

    def test_is_valid_with_all_required_fields(self):
        """Test is_valid returns True when all required fields are present."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        assert config.is_valid() is True

    def test_is_valid_missing_azure_deployment(self):
        """Test is_valid returns False when azure_deployment is missing."""
        config = EvaluationConfig(
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        assert config.is_valid() is False

    def test_is_valid_missing_api_key(self):
        """Test is_valid returns False when api_key is missing."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        assert config.is_valid() is False

    def test_is_valid_missing_azure_endpoint(self):
        """Test is_valid returns False when azure_endpoint is missing."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            api_version="2024-01-01",
        )

        assert config.is_valid() is False

    def test_is_valid_missing_api_version(self):
        """Test is_valid returns False when api_version is missing."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
        )

        assert config.is_valid() is False

    def test_is_valid_missing_all_fields(self):
        """Test is_valid returns False when all fields are missing."""
        config = EvaluationConfig()

        assert config.is_valid() is False

    def test_is_valid_does_not_require_azure_ai_project(self):
        """Test is_valid returns True even without azure_ai_project."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        assert config.is_valid() is True
        assert config.azure_ai_project is None


class TestEvaluationConfigValidate:
    """Tests for validate method."""

    def test_validate_with_all_required_fields(self):
        """Test validate does not raise exception with all required fields."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        # Should not raise an exception
        config.validate()

    def test_validate_missing_azure_deployment(self):
        """Test validate raises ValueError when azure_deployment is missing."""
        config = EvaluationConfig(
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        assert "azure_deployment" in str(exc_info.value)

    def test_validate_missing_api_key(self):
        """Test validate raises ValueError when api_key is missing."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        assert "api_key" in str(exc_info.value)

    def test_validate_missing_azure_endpoint(self):
        """Test validate raises ValueError when azure_endpoint is missing."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            api_version="2024-01-01",
        )

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        assert "azure_endpoint" in str(exc_info.value)

    def test_validate_missing_api_version(self):
        """Test validate raises ValueError when api_version is missing."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key",
            azure_endpoint="https://test.endpoint.com",
        )

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        assert "api_version" in str(exc_info.value)

    def test_validate_missing_multiple_fields(self):
        """Test validate error message includes all missing fields."""
        config = EvaluationConfig(
            azure_endpoint="https://test.endpoint.com",
        )

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        error_message = str(exc_info.value)
        assert "azure_deployment" in error_message
        assert "api_key" in error_message
        assert "api_version" in error_message

    def test_validate_missing_all_fields(self):
        """Test validate error message when all fields are missing."""
        config = EvaluationConfig()

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        error_message = str(exc_info.value)
        assert "azure_deployment" in error_message
        assert "api_key" in error_message
        assert "azure_endpoint" in error_message
        assert "api_version" in error_message


class TestEvaluationConfigRepr:
    """Tests for __repr__ method."""

    def test_repr_masks_api_key(self):
        """Test that __repr__ masks the API key."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key-123456789",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        repr_str = repr(config)

        assert "test-key-123456789" not in repr_str
        assert "test..." in repr_str or "****" in repr_str

    def test_repr_short_api_key(self):
        """Test that __repr__ handles short API keys."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="short",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
        )

        repr_str = repr(config)

        assert "short" not in repr_str
        assert "****" in repr_str

    def test_repr_includes_all_fields(self):
        """Test that __repr__ includes all configuration fields."""
        config = EvaluationConfig(
            azure_deployment="test-deployment",
            api_key="test-key-123456789",
            azure_endpoint="https://test.endpoint.com",
            api_version="2024-01-01",
            azure_ai_project="https://test.project.com",
        )

        repr_str = repr(config)

        assert "azure_deployment='test-deployment'" in repr_str
        assert "azure_endpoint='https://test.endpoint.com'" in repr_str
        assert "api_version='2024-01-01'" in repr_str
        assert "azure_ai_project='https://test.project.com'" in repr_str

    def test_repr_with_none_values(self):
        """Test that __repr__ handles None values correctly."""
        config = EvaluationConfig()

        repr_str = repr(config)

        assert "None" in repr_str
        assert "EvaluationConfig(" in repr_str
