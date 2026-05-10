from datetime import datetime
from openpyxl import Workbook
from matrix_updater import apply_updates


def test_newer_existing_date_not_overwritten():
    wb = Workbook()
    ws = wb.active
    ws.append(['Staff', 'Training Date', 'Evidence'])
    ws.append(['Azger Ali', datetime(2026, 4, 1), 'old.pdf'])
    outcomes = apply_updates(ws, [{
        'matched_staff_name': 'Azger Ali', 'proposed_value': '2026-03-26', 'evidence_file': 'new.pdf'
    }], training_column=2, evidence_column=3)
    assert outcomes[0][1] == 'skipped'
