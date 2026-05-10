from __future__ import annotations

from datetime import datetime


def normalize_training_date(value: str) -> str:
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
        try:
            return datetime.strptime(value, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    raise ValueError(f'Unsupported date format: {value}')


def apply_attendance_rules(extracted: dict) -> dict:
    extracted['training_date'] = normalize_training_date(extracted['training_date'])
    for attendee in extracted.get('attendees', []):
        note = (attendee.get('notes') or '').strip().lower()
        has_signature = bool(attendee.get('signature_detected'))
        if 'not attended' in note:
            attendee['attendance_status'] = 'not_attended'
        elif has_signature:
            attendee['attendance_status'] = 'attended'
        else:
            attendee['attendance_status'] = 'unclear'
    return extracted
