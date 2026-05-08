from __future__ import annotations

import json
from pathlib import Path


def write_preview(preview: dict, awaiting_dir: Path, stem: str) -> tuple[Path, Path]:
    awaiting_dir.mkdir(parents=True, exist_ok=True)
    json_path = awaiting_dir / f'{stem}_approval_preview.json'
    md_path = awaiting_dir / f'{stem}_approval_preview.md'
    json_path.write_text(json.dumps(preview, indent=2), encoding='utf-8')
    md_path.write_text(_to_markdown(preview), encoding='utf-8')
    return json_path, md_path


def approved(awaiting_dir: Path, stem: str, settings: dict) -> str:
    if (awaiting_dir / f'{stem}_{settings["approval_filename"]}').exists() or (awaiting_dir / settings['approval_filename']).exists():
        return 'approved'
    if (awaiting_dir / f'{stem}_{settings["rejection_filename"]}').exists() or (awaiting_dir / settings['rejection_filename']).exists():
        return 'rejected'
    return 'pending'


def _to_markdown(preview: dict) -> str:
    lines = [
        f"# Approval Preview: {preview['source_file']}",
        f"- Training: {preview['training_title']}",
        f"- Date: {preview['training_date']}",
        f"- Target Sheet: {preview.get('target_matrix_sheet', 'N/A')}",
        '',
        '## Staff to update',
    ]
    for item in preview['staff_to_update']:
        lines.append(f"- {item['pdf_name']} -> {item['matched_staff_name']} ({item['proposed_value']})")
    lines += ['', '## Staff skipped']
    for item in preview['staff_skipped']:
        lines.append(f"- {item['name']}: {item['reason']}")
    return '\n'.join(lines)
