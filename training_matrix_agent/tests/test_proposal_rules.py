from datetime import date, datetime

from training_matrix_agent.models.schemas import AttendanceRecord, AttendanceStatus, ExtractionResult, MatrixRow
from training_matrix_agent.services.proposal_service import ProposalService


def test_not_attended_is_skipped():
    extraction = ExtractionResult(
        source_file="x.pdf",
        course_name="Forklift",
        training_date=date(2026, 4, 1),
        extracted_at=datetime.utcnow(),
        attendees=[AttendanceRecord("Jane Doe", "jane doe", AttendanceStatus.NOT_ATTENDED)],
    )
    rows = [MatrixRow("1", "Jane Doe", None)]

    preview = ProposalService().build_preview(extraction, rows)

    assert not preview.updates
    assert preview.skipped_not_attended == ["Jane Doe"]


def test_newer_date_is_protected():
    extraction = ExtractionResult(
        source_file="x.pdf",
        course_name="Forklift",
        training_date=date(2026, 4, 1),
        extracted_at=datetime.utcnow(),
        attendees=[AttendanceRecord("John Smith", "john smith", AttendanceStatus.ATTENDED)],
    )
    rows = [MatrixRow("2", "John Smith", date(2026, 5, 1))]

    preview = ProposalService().build_preview(extraction, rows)

    assert not preview.updates
    assert preview.skipped_newer_date == ["John Smith"]


def test_unknown_staff_flagged():
    extraction = ExtractionResult(
        source_file="x.pdf",
        course_name="Forklift",
        training_date=date(2026, 4, 1),
        extracted_at=datetime.utcnow(),
        attendees=[AttendanceRecord("Mystery Person", "mystery person", AttendanceStatus.ATTENDED)],
    )
    rows = [MatrixRow("2", "John Smith", None)]

    preview = ProposalService().build_preview(extraction, rows)

    assert not preview.updates
    assert len(preview.unresolved_names) == 1
