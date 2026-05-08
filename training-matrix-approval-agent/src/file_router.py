from __future__ import annotations

import shutil
from pathlib import Path


def move_file(src: Path, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    target = destination_dir / src.name
    shutil.move(str(src), str(target))
    return target
