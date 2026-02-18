| File                    | Purpose                                           |
| ----------------------- | ------------------------------------------------- |
| README.md               | Quickstart + deploy instructions                  |
| infra/main.bicep        | Complete IaC: Storage, AI Search, Function App    |
| infra/parameters.json   | Fill in your resource names + keys                |
| infra/deploy.sh         | Mac/Linux one‑click deploy                        |
| infra/deploy.ps1        | Windows PowerShell deploy                         |
| api/function_app.py     | Full chat API: hybrid search, security, telemetry |
| api/requirements.txt    | Python dependencies                               |
| api/host.json           | Azure Functions config                            |
| api/local.settings.json | Local dev settings template                       |
| api/tests/test_chat.py  | Unit test stubs                                   |
| docs/prompts.md         | 5 ready-to-use prompt templates                   |
| docs/security.md        | RBAC patterns + data classification table         |
| evals/hr_eval.jsonl     | Sample evaluation dataset                         |
| evals/test_runner.py    | Eval runner script                                |
| .gitignore              | Standard Python/Azure ignores                     |
| LICENSE                 | MIT                                               |

🚀 First steps after download
Extract the ZIP

Edit infra/parameters.json with your Azure resource names + keys

Deploy: chmod +x infra/deploy.sh && ./infra/deploy.sh

Deploy API: cd api && func azure functionapp publish <your-fn-name>

Upload docs to Blob container knowledge

Test: POST /api/chat {"question": "What is the refund policy?"}
