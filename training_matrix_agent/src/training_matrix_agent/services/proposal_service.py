from __future__ import annotations

from training_matrix_agent.core.matching import best_name_match
from training_matrix_agent.models.schemas import (
    ApprovalPreview,
    AttendanceStatus,
    ExtractionResult,
    MatrixRow,
    NameMatchIssue,
    ProposedUpdate,
)


class ProposalService:
    def build_preview(self, extraction: ExtractionResult, matrix_rows: list[MatrixRow]) -> ApprovalPreview:
        by_name = {row.full_name: row for row in matrix_rows}
        updates: list[ProposedUpdate] = []
        skipped_not_attended: list[str] = []
        skipped_newer_date: list[str] = []
        unresolved_names: list[NameMatchIssue] = []

        for attendee in extraction.attendees:
            if attendee.status == AttendanceStatus.NOT_ATTENDED:
                skipped_not_attended.append(attendee.raw_name)
                continue

            matched_name, confidence = best_name_match(attendee.raw_name, by_name.keys())
            if matched_name is None:
                unresolved_names.append(NameMatchIssue(attendee.raw_name, list(by_name.keys())[:3], confidence))
                continue

            row = by_name[matched_name]
            if row.training_date and row.training_date > extraction.training_date:
                skipped_newer_date.append(row.full_name)
                continue

            updates.append(
                ProposedUpdate(
                    staff_id=row.staff_id,
                    full_name=row.full_name,
                    current_date=row.training_date,
                    proposed_date=extraction.training_date,
                    reason=f"{extraction.course_name} attendance confirmed",
                )
            )

        return ApprovalPreview(
            extraction=extraction,
            updates=updates,
            skipped_not_attended=skipped_not_attended,
            skipped_newer_date=skipped_newer_date,
            unresolved_names=unresolved_names,
        )
