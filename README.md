Appendix A
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

Appendix B
| File                             | Format   | Use Case           |
| -------------------------------- | -------- | ------------------ |
| README.md                        | Markdown | Quick overview     |
| project-charter.docx             | Word     | Executive approval |
| index-design-worksheet.xlsx      | Excel    | Schema planning    |
| security-review-checklist.md     | Markdown | Security sign‑off  |
| deployment-checklist.md          | Markdown | Go‑live readiness  |
| evaluation-template.jsonl        | JSONL    | QA testing         |
| stakeholder-matrix.xlsx          | Excel    | Change management  |
| prompt-library.md                | Markdown | Prompt engineering |
| content-classification-policy.md | Markdown | Governance         |

1. Download ZIP → Extract
2. Print checklists (Markdown → PDF)
3. Fill Excel worksheets
4. Copy JSONL for evals
5. Customize Word templates

