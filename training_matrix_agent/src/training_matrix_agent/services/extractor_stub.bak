from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from training_matrix_agent.core.matching import normalize_name
from training_matrix_agent.models.schemas import AttendanceRecord, AttendanceStatus, ExtractionResult


class FixedLayoutPdfExtractor:
    """Starter extractor.

    Replace stub parsing with OCR/PDF parser logic for your known layout.
    For now, it reads a companion text file with deterministic lines.
    """

    def extract(self, pdf_path: Path) -> ExtractionResult:
        txt_path = pdf_path.with_suffix(".txt")
        if not txt_path.exists():
            raise FileNotFoundError(f"Companion file missing for starter parser: {txt_path}")

        lines = txt_path.read_text(encoding="utf-8").splitlines()
        course_name = lines[0].split(":", 1)[1].strip()
        training_date = date.fromisoformat(lines[1].split(":", 1)[1].strip())

        attendees: list[AttendanceRecord] = []
        for line in lines[3:]:
            if not line.strip():
                continue
            name, status = [x.strip() for x in line.split("|", 1)]
            enum_status = AttendanceStatus(status)
            attendees.append(
                AttendanceRecord(
                    raw_name=name,
                    normalized_name=normalize_name(name),
                    status=enum_status,
                    signature_present=(enum_status == AttendanceStatus.ATTENDED),
                )
            )

        return ExtractionResult(
            source_file=str(pdf_path),
            course_name=course_name,
            training_date=training_date,
            extracted_at=datetime.utcnow(),
            attendees=attendees,
        )
