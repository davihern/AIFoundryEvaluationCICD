# AIFoundryEvaluationCICD
Sample repo to have a GH Action to trigger an evaluation in AI Foundry

## Testing

This repository includes comprehensive unit tests for the evaluation scripts.

### Running Tests

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

Run all tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

### Test Structure

- `tests/test_aiCloudEvaluatorAIEvaluationSDK.py` - Tests for Azure AI Evaluation SDK
- `tests/test_aiLOCALevaluator.py` - Tests for local evaluation

See [tests/README.md](tests/README.md) for detailed testing documentation.

### CI/CD

Tests are automatically run on push and pull requests via GitHub Actions. See [.github/workflows/test.yml](.github/workflows/test.yml).
