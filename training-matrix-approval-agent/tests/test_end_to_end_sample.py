import json
from pathlib import Path
from openpyxl import Workbook
from main import process_once
from audit_logger import HEADERS


def test_approval_required_and_audit_created(tmp_path: Path):
    base = tmp_path
    for p in ['config', 'data/incoming', 'data/awaiting_approval', 'data/processed', 'data/needs_review', 'data/failed']:
        (base / p).mkdir(parents=True, exist_ok=True)
        (base / 'config' / 'settings.yaml').write_text('''{\n  "paths": {"incoming": "data/incoming", "awaiting_approval": "data/awaiting_approval", "processed": "data/processed", "needs_review": "data/needs_review", "failed": "data/failed", "audit_log": "data/audit_log.csv"},\n  "files": {"training_mapping": "config/training_mapping.csv", "staff_aliases": "config/staff_name_aliases.csv"},\n  "matching": {"fuzzy_threshold": 88},\n  "approval": {"approval_filename": "approved.txt", "rejection_filename": "rejected.txt"}\n}\n''')
    (base / 'config' / 'training_mapping.csv').write_text('PDF Training Name,Matrix Sheet,Matrix Training Row,Renewal Months,Requires Approval\nSession 5 - SCCIF,Management Training,Children Home Regulations - SCCIF Session 5,12,Yes\n')
    (base / 'config' / 'staff_name_aliases.csv').write_text('PDF Name,Matrix Staff Name,Notes\nJon Barney,John Barney,Known alias\n')

    wb = Workbook(); ws = wb.active; ws.title = 'Management Training'; ws.append(['Staff','Date','Evidence']); ws.append(['Azger Ali','','']); ws.append(['John Barney','',''])
    matrix = base / 'data' / 'training_matrix.xlsx'; wb.save(matrix)

    pdf = base / 'data' / 'incoming' / 'attendance.pdf'; pdf.write_text('fake')
    payload = {'source_file':'attendance.pdf','training_title':'Session 5 - SCCIF','training_date':'26/03/2026','training_time':'','instructor':'','location':'','attendees':[{'name':'Azger Ali','branch':'A','signature_detected':True,'attendance_status':'attended','notes':'','confidence':1.0},{'name':'Amie Jagne','branch':'A','signature_detected':True,'attendance_status':'attended','notes':'Not Attended','confidence':1.0},{'name':'Jon Barney','branch':'A','signature_detected':True,'attendance_status':'attended','notes':'','confidence':1.0}]}
    (base / 'data' / 'incoming' / 'attendance.json').write_text(json.dumps(payload), encoding='utf-8')

    process_once(base, matrix)
    assert (base / 'data' / 'incoming' / 'attendance.pdf').exists(), 'approval required before update'
    assert (base / 'data' / 'awaiting_approval' / 'attendance_approval_preview.json').exists()

    (base / 'data' / 'awaiting_approval' / 'approved.txt').write_text('approved')
    process_once(base, matrix)
    assert (base / 'data' / 'processed' / 'attendance.pdf').exists()
    log = (base / 'data' / 'audit_log.csv').read_text()
    assert all(h in log for h in HEADERS)
    assert 'Amie Jagne' not in log
