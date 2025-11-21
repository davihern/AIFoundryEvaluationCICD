"""Configuration management for Azure AI Evaluation."""
import os
from typing import Dict, Optional


class EvaluationConfig:
    """Manages configuration for Azure AI evaluation tasks."""

    def __init__(
        self,
        azure_deployment: Optional[str] = None,
        api_key: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        api_version: Optional[str] = None,
        azure_ai_project: Optional[str] = None,
    ):
        """Initialize evaluation configuration.

        Args:
            azure_deployment: Azure deployment name
            api_key: Azure API key
            azure_endpoint: Azure endpoint URL
            api_version: Azure API version
            azure_ai_project: Azure AI project URL
        """
        self.azure_deployment = azure_deployment or os.getenv("AZURE_DEPLOYMENT_NAME")
        self.api_key = api_key or os.getenv("AZURE_API_KEY")
        self.azure_endpoint = azure_endpoint or os.getenv("AZURE_ENDPOINT")
        self.api_version = api_version or os.getenv("AZURE_API_VERSION")
        self.azure_ai_project = azure_ai_project or os.getenv("AZURE_AI_PROJECT")

    def get_model_config(self) -> Dict[str, Optional[str]]:
        """Get model configuration dictionary.

        Returns:
            Dictionary containing model configuration parameters
        """
        return {
            "azure_deployment": self.azure_deployment,
            "api_key": self.api_key,
            "azure_endpoint": self.azure_endpoint,
            "api_version": self.api_version,
        }

    def is_valid(self) -> bool:
        """Check if configuration has all required fields.

        Returns:
            True if all required fields are present, False otherwise
        """
        return all([
            self.azure_deployment,
            self.api_key,
            self.azure_endpoint,
            self.api_version,
        ])

    def validate(self) -> None:
        """Validate configuration and raise exception if invalid.

        Raises:
            ValueError: If any required configuration field is missing
        """
        missing_fields = []
        if not self.azure_deployment:
            missing_fields.append("azure_deployment")
        if not self.api_key:
            missing_fields.append("api_key")
        if not self.azure_endpoint:
            missing_fields.append("azure_endpoint")
        if not self.api_version:
            missing_fields.append("api_version")

        if missing_fields:
            raise ValueError(
                f"Missing required configuration fields: {', '.join(missing_fields)}"
            )

    def __repr__(self) -> str:
        """Return string representation of configuration.

        Returns:
            String representation with masked API key
        """
        masked_key = f"{self.api_key[:4]}...{self.api_key[-4:]}" if self.api_key and len(self.api_key) > 8 else "****"
        return (
            f"EvaluationConfig("
            f"azure_deployment={self.azure_deployment!r}, "
            f"api_key={masked_key!r}, "
            f"azure_endpoint={self.azure_endpoint!r}, "
            f"api_version={self.api_version!r}, "
            f"azure_ai_project={self.azure_ai_project!r})"
        )
