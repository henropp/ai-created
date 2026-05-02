# Training Matrix Approval Agent

A starter implementation for an approval-gated training matrix updater that:

1. Detects new attendance PDFs in OneDrive/SharePoint input folders.
2. Extracts course/session details and attendee statuses from fixed-layout attendance sheets.
3. Compares extracted results against an Excel training matrix.
4. Produces a proposed update package for human approval.
5. Applies updates to Excel only after approval.
6. Writes audit logs and moves files to `Processed` or `Needs Review`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
```

## High-level architecture

- `connectors/` – file system / OneDrive / SharePoint adapters (starter filesystem adapter included).
- `services/` – orchestration services for extraction, matching, proposal building, approval, and update.
- `core/` – stateless business logic.
- `models/` – shared data models.
- `tests/` – starter tests for all business rules.

See `docs/implementation_plan.md` for rollout phases and `docs/test_cases.md` for detailed scenarios.
