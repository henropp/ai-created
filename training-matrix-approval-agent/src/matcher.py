from __future__ import annotations

import csv
from difflib import SequenceMatcher


def load_mapping(mapping_csv: str) -> list[dict]:
    with open(mapping_csv, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def load_aliases(alias_csv: str) -> list[dict]:
    with open(alias_csv, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def match_training_title(training_title: str, mapping_rows: list[dict]) -> dict | None:
    for row in mapping_rows:
        if row['PDF Training Name'] == training_title:
            return row
    return None


def match_staff_name(pdf_name: str, staff_names: list[str], aliases_rows: list[dict], threshold: int = 88) -> tuple[str | None, float]:
    for row in aliases_rows:
        if row['PDF Name'] == pdf_name:
            return str(row['Matrix Staff Name']), 1.0
    best_name = None
    best_conf = 0.0
    for candidate in staff_names:
        conf = SequenceMatcher(None, pdf_name.lower(), candidate.lower()).ratio()
        if conf > best_conf:
            best_name, best_conf = candidate, conf
    if best_conf * 100 < threshold:
        return None, best_conf
    return best_name, best_conf
