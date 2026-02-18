
# Security Patterns

## RBAC with Azure AI Search

### Index Field
Add `access_groups` (Collection(Edm.String), filterable) to every chunk.

### Query Filter
```python
security_filter = f"access_groups/any(g: search.in(g, '{groups_str}', ','))"
```

### Token Validation
Use MSAL to validate Azure AD tokens and extract group memberships.

## Data Classification

| Level       | access_groups value      | Example content        |
|-------------|--------------------------|------------------------|
| Public      | ["all-employees"]        | Company handbook       |
| Internal    | ["all-employees"]        | Org charts             |
| Confidential| ["dept-finance"]         | Budget documents       |
| Restricted  | ["exec-team","legal"]    | M&A documents          |

## Never Do This
- Never filter sensitive content in prompts only
- Never log raw answers containing PII
- Never skip security filter for "testing"
