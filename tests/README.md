# Unit Tests for AIFoundryEvaluationCICD

This directory contains comprehensive unit tests for the Azure AI Foundry evaluation scripts.

## Test Structure

### test_aiCloudEvaluatorAIEvaluationSDK.py
Tests for `aiCloudEvaluatorAIEvaluationSDK.py` covering:
- Model configuration structure and environment variable handling
- Evaluate function parameters and structure
- Groundedness and Similarity evaluator configurations
- Column mapping for evaluators

### test_aiLOCALevaluator.py
Tests for `aiLOCALevaluator.py` covering:
- AI Project Client initialization and configuration
- Agent creation, thread management, and message handling
- Run creation and processing (both completed and failed states)
- AI Agent Converter functionality
- Quality evaluators (IntentResolution, TaskAdherence, ToolCallAccuracy, Coherence, Fluency, Relevance)
- Safety evaluators (ContentSafety, IndirectAttack, CodeVulnerability)
- Reasoning model configuration
- Evaluation execution and result structure

## Running Tests

### Run all tests
```bash
python -m pytest tests/ -v
```

### Run tests with coverage
```bash
python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html
```

### Run a specific test file
```bash
python -m pytest tests/test_aiCloudEvaluatorAIEvaluationSDK.py -v
```

### Run a specific test
```bash
python -m pytest tests/test_aiLOCALevaluator.py::TestAILocalEvaluator::test_model_config_structure -v
```

## Test Dependencies

Install test dependencies using:
```bash
pip install -r requirements-test.txt
```

Or install individually:
```bash
pip install pytest pytest-cov pytest-mock
```

## Test Coverage

The tests achieve comprehensive coverage of:
- Configuration handling
- Data structure validation
- Parameter validation
- Environment variable management
- Error handling patterns
- JSON serialization

## Design Philosophy

These tests follow best practices:
1. **No external dependencies**: Tests don't require Azure credentials or actual Azure services
2. **Fast execution**: All tests run in under 1 second
3. **Isolated**: Each test is independent and can run in any order
4. **Clear naming**: Test names describe what is being tested
5. **Structured**: Tests are organized into logical test classes
6. **Maintainable**: Tests focus on verifying structure and behavior, not implementation details

## CI/CD Integration

These tests can be integrated into GitHub Actions workflows to ensure code quality:

```yaml
- name: Install test dependencies
  run: pip install -r requirements-test.txt

- name: Run tests
  run: python -m pytest tests/ -v --cov=. --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```
