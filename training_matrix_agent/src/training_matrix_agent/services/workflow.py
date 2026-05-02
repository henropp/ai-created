from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import shutil

from training_matrix_agent.services.audit_service import AuditService
from training_matrix_agent.services.extractor import FixedLayoutPdfExtractor
from training_matrix_agent.services.matrix_service import TrainingMatrixService
from training_matrix_agent.services.proposal_service import ProposalService


class TrainingMatrixApprovalWorkflow:
    def __init__(self, audit_service: AuditService):
        self.audit_service = audit_service
        self.extractor = FixedLayoutPdfExtractor()
        self.matrix_service = TrainingMatrixService()
        self.proposal_service = ProposalService()

    def process(
        self,
        pdf_path: Path,
        workbook_path: Path,
        processed_dir: Path,
        needs_review_dir: Path,
        approved: bool,
    ) -> dict:
        extraction = self.extractor.extract(pdf_path)
        rows = self.matrix_service.load_rows(workbook_path)
        preview = self.proposal_service.build_preview(extraction, rows)

        self.audit_service.log("proposed_update", asdict(preview))

        needs_review = len(preview.unresolved_names) > 0
        if not approved or needs_review:
            target = needs_review_dir / pdf_path.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(pdf_path, target)
            self.audit_service.log("needs_review", {"file": str(target), "approved": approved})
            return {"status": "needs_review", "preview": asdict(preview)}

        update_map = {u.staff_id: u.proposed_date for u in preview.updates}
        self.matrix_service.apply_updates(workbook_path, update_map)
        self.audit_service.log("completed_update", {"count": len(update_map), "file": str(workbook_path)})

        target = processed_dir / pdf_path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(pdf_path, target)
        return {"status": "processed", "preview": asdict(preview)}
