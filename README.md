# AIFoundryEvaluationCICD
Small reference repo showing how to run Azure AI Foundry evaluations from CI.

## What’s here
- `aiCloudEvaluatorAIEvaluationSDK.py`: runs an evaluation with the Azure AI Evaluation SDK against `sample.jsonl`, mapping query/response/context columns and writing results to `myevalresults.json`. Expects Azure AI Foundry project details and model deployment info in environment variables.
- `aiLOCALevaluator.py`: spins up an agent in your Azure AI project (using Azure CLI auth), runs a sample thread, converts the interaction for evaluation, and executes quality/safety evaluators locally.
- `aiCloudEvaluator.py`: placeholder for alternate cloud evaluation flow.
- `sample.jsonl`: example dataset (query/ground truth/response/context).
- `myevalresults.json`: sample evaluation output.
- `requirements.txt`: pinned dependencies for the evaluation scripts.

## Running locally
1) Install Python 3.10+ and dependencies:
```bash
pip install -r requirements.txt
```
2) Set required environment variables (at minimum): `AZURE_DEPLOYMENT_NAME`, `AZURE_API_KEY`, `AZURE_ENDPOINT`, `AZURE_API_VERSION`, `AZURE_AI_PROJECT`, and for `aiLOCALevaluator.py`, `MODEL_DEPLOYMENT_NAME`. Sign in with `az login` for CLI-based auth.
3) Execute a script:
- Cloud evaluation: `python aiCloudEvaluatorAIEvaluationSDK.py` (writes `myevalresults.json`).
- Local agent evaluation: `python aiLOCALevaluator.py` (prints evaluator results).
