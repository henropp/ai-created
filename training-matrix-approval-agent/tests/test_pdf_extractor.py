from pathlib import Path
import json
from pdf_extractor import extract_attendance_data


def test_sidecar_json_extraction(tmp_path: Path):
    pdf = tmp_path / 'sample.pdf'
    pdf.write_text('fake')
    payload = {'source_file': 'sample.pdf', 'training_title': 'Session 5 - SCCIF', 'training_date': '2026-03-26', 'training_time': '10:00', 'instructor': 'A', 'location': 'B', 'attendees': []}
    (tmp_path / 'sample.json').write_text(json.dumps(payload), encoding='utf-8')
    assert extract_attendance_data(pdf)['training_title'] == 'Session 5 - SCCIF'
