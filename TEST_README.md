# Unit Tests for Azure AI Evaluation

This document describes the unit test suite for the Azure AI Evaluation project.

## Overview

The test suite provides comprehensive coverage for the `EvaluationConfig` class, which manages configuration for Azure AI evaluation tasks.

## Test Structure

### Test File: `test_evaluation_config.py`

The test file is organized into multiple test classes, each focusing on a specific aspect of the `EvaluationConfig` class:

1. **TestEvaluationConfigInitialization** - Tests for object initialization
2. **TestEvaluationConfigGetModelConfig** - Tests for model configuration retrieval
3. **TestEvaluationConfigIsValid** - Tests for configuration validation checks
4. **TestEvaluationConfigValidate** - Tests for validation with exceptions
5. **TestEvaluationConfigRepr** - Tests for string representation

## Running Tests

### Install Dependencies

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Run All Tests

Run all tests with verbose output:

```bash
pytest test_evaluation_config.py -v
```

### Run Specific Test Class

Run tests from a specific class:

```bash
pytest test_evaluation_config.py::TestEvaluationConfigInitialization -v
```

### Run Single Test

Run a single test method:

```bash
pytest test_evaluation_config.py::TestEvaluationConfigInitialization::test_init_with_all_parameters -v
```

### Run with Coverage

To run tests with coverage reporting:

```bash
pip install pytest-cov
pytest test_evaluation_config.py --cov=evaluation_config --cov-report=html
```

## Test Coverage

The test suite includes **25 comprehensive tests** covering:

### Initialization Tests (4 tests)
- ✅ Initialization with all parameters
- ✅ Initialization with no parameters (fallback to environment)
- ✅ Initialization from environment variables
- ✅ Parameter override behavior

### Model Configuration Tests (3 tests)
- ✅ Correct dictionary structure
- ✅ Correct values in model config
- ✅ Exclusion of non-model fields

### Validation Tests (14 tests)
- ✅ Valid configuration detection
- ✅ Missing field detection (individual and multiple)
- ✅ Exception-based validation
- ✅ Comprehensive error messages

### Representation Tests (4 tests)
- ✅ API key masking for security
- ✅ Handling of short API keys
- ✅ Complete field inclusion
- ✅ None value handling

## Class Under Test: EvaluationConfig

The `EvaluationConfig` class provides:

- **Configuration Management**: Centralized handling of Azure AI configuration
- **Environment Variable Support**: Automatic fallback to environment variables
- **Validation**: Multiple validation methods for configuration completeness
- **Security**: API key masking in string representations

### Key Methods

```python
# Initialize with explicit parameters
config = EvaluationConfig(
    azure_deployment="deployment-name",
    api_key="your-api-key",
    azure_endpoint="https://endpoint.com",
    api_version="2024-01-01"
)

# Get model configuration dictionary
model_config = config.get_model_config()

# Check if configuration is valid
if config.is_valid():
    # Proceed with evaluation
    pass

# Validate and raise exception if invalid
config.validate()
```

## Best Practices Demonstrated

The test suite demonstrates several testing best practices:

1. **Clear Test Names**: Tests are named to describe what they test and expected behavior
2. **Test Organization**: Tests are grouped into logical classes
3. **Isolation**: Each test is independent and doesn't affect others
4. **Environment Cleanup**: Tests properly save and restore environment variables
5. **Comprehensive Coverage**: Tests cover success cases, edge cases, and error conditions
6. **Assertions**: Clear, specific assertions that verify expected behavior

## Adding New Tests

When adding new functionality to `EvaluationConfig`:

1. Create a new test class if testing a new method
2. Follow the naming convention: `test_<method>_<scenario>`
3. Use descriptive docstrings
4. Ensure tests are isolated and don't depend on execution order
5. Clean up any environment modifications

Example:

```python
class TestEvaluationConfigNewMethod:
    """Tests for new_method."""

    def test_new_method_with_valid_input(self):
        """Test new_method with valid input returns expected result."""
        config = EvaluationConfig(...)
        result = config.new_method()
        assert result == expected_value
```

## Continuous Integration

These tests should be run as part of the CI/CD pipeline to ensure code quality. Add to your GitHub Actions workflow:

```yaml
- name: Run Unit Tests
  run: |
    pip install -r requirements.txt
    pytest test_evaluation_config.py -v
```

## Test Results

All 25 tests currently pass:

```
================================================== 25 passed in 0.05s ==================================================
```
