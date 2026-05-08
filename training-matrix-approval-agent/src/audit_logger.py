from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import csv

HEADERS = [
    'Processed Timestamp', 'Source PDF', 'Training Title', 'Training Date', 'Staff Name',
    'Action', 'Previous Value', 'New Value', 'Evidence Path', 'Status', 'Notes'
]


def append_audit_rows(path: str, rows: list[dict]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    write_headers = not file_path.exists()
    with file_path.open('a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if write_headers:
            writer.writeheader()
        ts = datetime.now(timezone.utc).isoformat()
        for row in rows:
            row.setdefault('Processed Timestamp', ts)
            writer.writerow(row)
