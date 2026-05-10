from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def extract_attendance_data(pdf_path: Path) -> Dict[str, Any]:
    """Extract data from attendance PDF.

    First version supports manual sidecar JSON to simulate extraction.
    TODO: Integrate OCR/vision extraction for fixed-layout forms.
    """
    sidecar = pdf_path.with_suffix('.json')
    if sidecar.exists():
        return json.loads(sidecar.read_text(encoding='utf-8'))
    return ocr_placeholder(pdf_path)


def ocr_placeholder(pdf_path: Path) -> Dict[str, Any]:
    raise NotImplementedError(
        f"Could not extract text from {pdf_path.name}. "
        "TODO: implement OCR/vision extraction integration."
    )
