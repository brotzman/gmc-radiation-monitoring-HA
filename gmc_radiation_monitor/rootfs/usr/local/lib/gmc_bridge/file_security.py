from __future__ import annotations

import os
from pathlib import Path

PRIVATE_FILE_MODE = 0o600
PRIVATE_DIRECTORY_MODE = 0o700


def secure_file(path: str | Path) -> Path:
    """Apply owner-only permissions to an existing regular file."""
    target = Path(path)
    try:
        if target.is_file():
            os.chmod(target, PRIVATE_FILE_MODE)
    except FileNotFoundError:
        pass
    return target


def secure_sqlite_family(path: str | Path) -> None:
    """Secure a SQLite database and its transient sidecar files when present."""
    target = Path(path)
    for candidate in (
        target,
        Path(str(target) + "-wal"),
        Path(str(target) + "-shm"),
        target.with_suffix(target.suffix + ".lock"),
    ):
        secure_file(candidate)
