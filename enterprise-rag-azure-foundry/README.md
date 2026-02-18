
# Enterprise RAG on Azure AI Foundry

Reference implementation book: Real World RAG on Microsoft AI Foundry.

## Architecture
Blob Storage -> AI Search Indexer (RAG) -> Chunked/Vector Index -> Secure Chat API -> Azure OpenAI

## Quick Deploy

1. Deploy infra: `az deployment group create --resource-group <rg> --template-file infra/main.bicep --parameters infra/parameters.json`
2. Deploy API: `cd api && func azure functionapp publish <functionAppName>`
3. Upload docs to Blob container 'knowledge'
4. Test: POST /api/chat {"question": "What is the refund policy?"}

## Requirements
- Azure Subscription
- Azure CLI
- Azure Functions Core Tools
- Python 3.11
