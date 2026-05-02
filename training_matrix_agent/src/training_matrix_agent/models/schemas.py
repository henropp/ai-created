from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum


class AttendanceStatus(str, Enum):
    ATTENDED = "Attended"
    NOT_ATTENDED = "Not Attended"
    UNCERTAIN = "Uncertain"


@dataclass
class AttendanceRecord:
    raw_name: str
    normalized_name: str
    status: AttendanceStatus
    signature_present: bool = False
    note: str | None = None


@dataclass
class ExtractionResult:
    source_file: str
    course_name: str
    training_date: date
    extracted_at: datetime
    attendees: list[AttendanceRecord] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class MatrixRow:
    staff_id: str
    full_name: str
    training_date: date | None


@dataclass
class ProposedUpdate:
    staff_id: str
    full_name: str
    current_date: date | None
    proposed_date: date
    reason: str


@dataclass
class NameMatchIssue:
    raw_name: str
    candidates: list[str]
    confidence: float


@dataclass
class ApprovalPreview:
    extraction: ExtractionResult
    updates: list[ProposedUpdate]
    skipped_not_attended: list[str]
    skipped_newer_date: list[str]
    unresolved_names: list[NameMatchIssue]


@dataclass
class AuditEvent:
    event_type: str
    timestamp: datetime
    details: dict
