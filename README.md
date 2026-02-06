# AIFoundryEvaluationCICD
Sample repo to have a GH Action trigger an evaluation in Azure AI Foundry.

## Repository contents
- `aiCloudEvaluatorAIEvaluationSDK.py`: runs Azure AI Evaluation SDK against `sample.jsonl`, using environment variables such as `AZURE_DEPLOYMENT_NAME`, `AZURE_ENDPOINT`, `AZURE_API_VERSION`, `AZURE_AI_PROJECT`, and `AZURE_API_KEY`. Produces `myevalresults.json` and can upload results to an AI Foundry project.
- `aiLOCALevaluator.py`: demonstrates creating an Azure AI agent via `AIProjectClient`, converting a run to evaluation data, and scoring it with quality and safety evaluators. Requires Azure CLI login plus `AZURE_AI_PROJECT`, `AZURE_DEPLOYMENT_NAME`, `AZURE_ENDPOINT`, `AZURE_API_VERSION`, and `MODEL_DEPLOYMENT_NAME`.
- `aiCloudEvaluator.py`: placeholder for a cloud-based evaluator entry point.
- `datafile.json`: example evaluation dataset definition listing queries, contexts, and expected answers for multiple evaluators.
- `sample.jsonl`: small JSONL dataset of user queries, responses, and context snippets used by the cloud evaluator sample.
- `myevalresults.json`: sample output produced by the evaluation run in `aiCloudEvaluatorAIEvaluationSDK.py`.
- `requirements.txt`: Python dependencies for the Azure AI agents/evaluation samples.

## Running the samples
1) Install dependencies: `pip install -r requirements.txt`.
2) Set the required Azure environment variables (see above).
3) Cloud evaluation example: `python aiCloudEvaluatorAIEvaluationSDK.py` to score `sample.jsonl` and write `myevalresults.json`.
4) Local agent evaluation example: authenticate with `az login` and run `python aiLOCALevaluator.py` to create an agent, collect a run, and evaluate it.
