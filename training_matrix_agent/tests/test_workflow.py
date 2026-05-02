from pathlib import Path
from openpyxl import Workbook

from training_matrix_agent.services.audit_service import AuditService
from training_matrix_agent.services.workflow import TrainingMatrixApprovalWorkflow


def _build_matrix(path: Path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Matrix"
    ws.append(["staff_id", "full_name", "training_date"])
    ws.append(["1", "Jane Doe", None])
    wb.save(path)


def _build_attendance(tmp_path: Path):
    pdf = tmp_path / "attendance.pdf"
    pdf.write_text("placeholder", encoding="utf-8")
    txt = tmp_path / "attendance.txt"
    txt.write_text(
        "Course: Forklift\nDate: 2026-04-01\nAttendees:\nJane Doe | Attended\n",
        encoding="utf-8",
    )
    return pdf


def test_workflow_processed_when_approved(tmp_path: Path):
    matrix = tmp_path / "matrix.xlsx"
    _build_matrix(matrix)
    pdf = _build_attendance(tmp_path)

    audit = AuditService(tmp_path / "audit.log")
    workflow = TrainingMatrixApprovalWorkflow(audit)

    result = workflow.process(
        pdf_path=pdf,
        workbook_path=matrix,
        processed_dir=tmp_path / "Processed",
        needs_review_dir=tmp_path / "Needs Review",
        approved=True,
    )

    assert result["status"] == "processed"
    assert (tmp_path / "Processed" / "attendance.pdf").exists()
