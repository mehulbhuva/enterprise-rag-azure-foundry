
# Security Review Checklist ✅

## Data Classification
- [ ] All content tagged with `access_groups`
- [ ] Classification policy documented
- [ ] Sample queries tested with different user roles

## Search Security
- [ ] Security filter syntax validated
- [ ] Edge cases tested (no groups, empty groups)
- [ ] Filter bypass attempts blocked

## Logging & Audit
- [ ] All queries logged (user + question + chunks)
- [ ] PII scrubbed from logs
- [ ] Retention policy (90 days ops, 7yr compliance)

## Content Safety
- [ ] Azure Content Safety on input + output
- [ ] Blocklist configured
- [ ] Safe refusal prompts tested

## Approvals
Security: ________________ Date: ______
Legal: __________________ Date: ______
Compliance: ______________ Date: ______
