from __future__ import annotations

from pathlib import Path
import json

from attendance_parser import apply_attendance_rules
from approval import approved, write_preview
from audit_logger import append_audit_rows
from file_router import move_file
from matcher import load_aliases, load_mapping, match_staff_name, match_training_title
from matrix_reader import get_staff_names, load_workbook
from matrix_updater import apply_updates
from pdf_extractor import extract_attendance_data


def process_once(base_dir: Path, matrix_path: Path):
    settings = json.loads((base_dir / 'config' / 'settings.yaml').read_text())
    paths = settings['paths']
    incoming = base_dir / paths['incoming']
    awaiting = base_dir / paths['awaiting_approval']
    processed = base_dir / paths['processed']
    review = base_dir / paths['needs_review']
    failed = base_dir / paths['failed']

    mapping_df = load_mapping(base_dir / settings["files"]["training_mapping"])
    aliases_df = load_aliases(base_dir / settings["files"]["staff_aliases"])

    for pdf in incoming.glob('*.pdf'):
        try:
            extracted = apply_attendance_rules(extract_attendance_data(pdf))
            train_map = match_training_title(extracted['training_title'], mapping_df)
            if not train_map:
                move_file(pdf, review)
                continue
            wb = load_workbook(str(matrix_path))
            ws = wb[train_map['Matrix Sheet']]
            staff_names = get_staff_names(ws)
            preview = {
                'source_file': pdf.name,
                'training_title': extracted['training_title'],
                'training_date': extracted['training_date'],
                'target_matrix_sheet': train_map['Matrix Sheet'],
                'target_training_row': train_map['Matrix Training Row'],
                'staff_to_update': [],
                'staff_skipped': [],
                'requires_review': False,
            }
            for att in extracted['attendees']:
                if att['attendance_status'] == 'not_attended':
                    preview['staff_skipped'].append({'name': att['name'], 'reason': 'Not Attended'})
                    continue
                if att['attendance_status'] == 'unclear':
                    preview['staff_skipped'].append({'name': att['name'], 'reason': 'Unclear signature'})
                    preview['requires_review'] = True
                    continue
                matched, conf = match_staff_name(att['name'], staff_names, aliases_df, settings['matching']['fuzzy_threshold'])
                if not matched:
                    preview['staff_skipped'].append({'name': att['name'], 'reason': 'No staff match'})
                    preview['requires_review'] = True
                    continue
                preview['staff_to_update'].append({
                    'pdf_name': att['name'], 'matched_staff_name': matched, 'match_confidence': conf,
                    'current_value': '', 'proposed_value': extracted['training_date'], 'evidence_file': str(pdf)
                })
            stem = pdf.stem
            write_preview(preview, awaiting, stem)
            state = approved(awaiting, stem, settings['approval'])
            if state == 'pending':
                continue
            if state == 'rejected' or preview['requires_review']:
                move_file(pdf, review)
                continue
            outcomes = apply_updates(ws, preview['staff_to_update'], training_column=2, evidence_column=3)
            wb.save(matrix_path)
            audit_rows = []
            for upd, action, prev, note in outcomes:
                audit_rows.append({
                    'Source PDF': pdf.name, 'Training Title': extracted['training_title'],
                    'Training Date': extracted['training_date'], 'Staff Name': upd['matched_staff_name'],
                    'Action': action, 'Previous Value': prev or '', 'New Value': upd['proposed_value'],
                    'Evidence Path': upd['evidence_file'], 'Status': 'ok' if action == 'updated' else 'skipped', 'Notes': note,
                })
            append_audit_rows(str(base_dir / paths['audit_log']), audit_rows)
            move_file(pdf, processed)
        except Exception:
            move_file(pdf, failed)


if __name__ == '__main__':
    process_once(Path('.'), Path('./data/training_matrix.xlsx'))
