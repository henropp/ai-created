# training-matrix-approval-agent

Compliance-sensitive automation that reads attendance PDFs, prepares a human approval preview, and only updates the Excel training matrix after explicit approval.

## Safety guarantees
- Never updates matrix without approval flag file.
- Never updates people marked `Not Attended`.
- Never creates staff automatically.
- Never overwrites newer matrix dates.
- Never deletes training records.
- Logs all proposals/outcomes and preserves source PDF evidence.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage (local folder mode)
1. Put attendance PDF into `data/incoming/`.
2. Add extraction sidecar JSON (`same_name.json`) using extraction schema.
3. Run:
```bash
python src/main.py
```
4. Review preview files in `data/awaiting_approval/`.
5. To approve, place `approved.txt` in `data/awaiting_approval/` and rerun.
6. To reject, place `rejected.txt` and rerun.

## TODO
- OneDrive connector.
- SharePoint connector.
- OCR/AI extraction for scanned/handwritten PDFs.
