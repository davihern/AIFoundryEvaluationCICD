# Unit Tests for AIFoundryEvaluationCICD

This directory contains comprehensive unit tests for the AI Foundry Evaluation CICD project.

## Test Structure

- `test_aiCloudEvaluatorAIEvaluationSDK.py` - Tests for the Azure AI Evaluation SDK implementation
- `test_aiLOCALevaluator.py` - Tests for the local evaluation implementation

## Running Tests

### Prerequisites

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_aiCloudEvaluatorAIEvaluationSDK.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov/` directory.

## Test Categories

### Unit Tests
Tests that verify individual components and functions with mocked dependencies.

### Skipped Tests
Some tests are automatically skipped when Azure AI modules are not installed in the test environment. These tests will run in CI/CD environments where the full dependencies are installed.

## Test Configuration

The test configuration is defined in `pytest.ini`:
- Test files must start with `test_`
- Test classes must start with `Test`
- Test functions must start with `test_`

## CI/CD Integration

Tests can be integrated into GitHub Actions workflows by adding a test step:

```yaml
- name: Install test dependencies
  run: pip install -r requirements-test.txt

- name: Run tests
  run: pytest tests/ -v
```

## Writing New Tests

When adding new tests:
1. Follow the existing test structure
2. Use descriptive test names that explain what is being tested
3. Mock external dependencies (Azure services, API calls)
4. Use `@requires_azure` decorator for tests that need Azure modules
5. Keep tests isolated and independent

## Test Coverage

Current test coverage includes:
- Environment configuration validation
- Model configuration structure
- Azure AI Project Client initialization
- Agent operations (creation, messaging, threading)
- Data conversion and formatting
- Evaluator configuration and initialization
- Column mapping for evaluators
- File format validation
- Output handling

## Troubleshooting

### Azure Module Import Errors
If you see `ModuleNotFoundError: No module named 'azure'`, install the main dependencies:
```bash
pip install -r requirements.txt
```

### Test Discovery Issues
Make sure you're running pytest from the repository root directory.
