# Implementation Plan

## Phase 1: Ingestion and Extraction
- Trigger on new files in configured OneDrive/SharePoint folder.
- Validate filename and PDF readability.
- Extract fixed-layout fields:
  - Course name
  - Training date
  - Attendee rows (typed names)
  - Attendance status and signature/notes indicator
- Write `extraction.json` beside working file.

## Phase 2: Matrix Reconciliation
- Load Excel matrix (`Matrix` sheet starter assumption).
- Match names with normalization + fuzzy scoring.
- Apply business rules:
  - Skip `Not Attended`
  - Never downgrade newer matrix dates
  - Do not auto-create missing staff
  - Flag ambiguous/low-confidence matches
- Build approval preview payload.

## Phase 3: Approval Gate
- Present proposed updates, skips, and unresolved matches.
- Require explicit `Approve` action to continue.
- If rejected or unresolved names exist, move document to `Needs Review`.

## Phase 4: Update and Audit
- Apply approved updates to Excel matrix.
- Save workbook version and retain backup copy.
- Write append-only audit entries for:
  - Proposed updates
  - Approval or rejection
  - Completed updates
- Move source PDF to `Processed` once complete.

## Phase 5: Hardening
- Add OCR confidence checks for handwritten notes.
- Add idempotency key to prevent duplicate processing.
- Add retries and dead-letter queue for transient connector issues.
