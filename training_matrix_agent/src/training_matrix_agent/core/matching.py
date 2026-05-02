from __future__ import annotations

import difflib
import re
from typing import Iterable


def normalize_name(name: str) -> str:
    clean = re.sub(r"[^a-zA-Z\s]", " ", name).lower()
    return " ".join(clean.split())


def best_name_match(raw_name: str, matrix_names: Iterable[str], threshold: float = 0.88) -> tuple[str | None, float]:
    normalized_raw = normalize_name(raw_name)
    best_name = None
    best_score = 0.0
    for candidate in matrix_names:
        score = difflib.SequenceMatcher(None, normalized_raw, normalize_name(candidate)).ratio()
        if score > best_score:
            best_score = score
            best_name = candidate

    if best_score >= threshold:
        return best_name, best_score
    return None, best_score
