from __future__ import annotations

from datetime import datetime


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            return datetime.strptime(str(value), fmt).date()
        except ValueError:
            continue
    return None


def apply_updates(ws, staff_updates: list[dict], training_column: int, evidence_column: int | None = None):
    outcomes = []
    for row in range(2, ws.max_row + 1):
        staff = ws.cell(row=row, column=1).value
        for upd in staff_updates:
            if staff != upd['matched_staff_name']:
                continue
            existing = ws.cell(row=row, column=training_column).value
            new_date = _parse_date(upd['proposed_value'])
            existing_date = _parse_date(existing)
            if existing_date and new_date and existing_date > new_date:
                outcomes.append((upd, 'skipped', existing, 'Existing newer date'))
                continue
            ws.cell(row=row, column=training_column).value = upd['proposed_value']
            if evidence_column:
                ws.cell(row=row, column=evidence_column).value = upd['evidence_file']
            outcomes.append((upd, 'updated', existing, ''))
    return outcomes
