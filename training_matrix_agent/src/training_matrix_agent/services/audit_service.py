from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from training_matrix_agent.models.schemas import AuditEvent


class AuditService:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event_type: str, details: dict) -> None:
        event = AuditEvent(event_type=event_type, timestamp=datetime.utcnow(), details=details)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), default=str) + "\n")
