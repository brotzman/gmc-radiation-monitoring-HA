from __future__ import annotations

import contextlib
import hashlib
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .file_security import secure_file
from .history import HistoryStore

_SAFE_BACKUP_NAME = re.compile(r"^gmc-managed-[0-9]{8}T[0-9]{6}Z(?:-[a-z0-9_-]+)?\.sqlite3$")


@dataclass(frozen=True, slots=True)
class ManagedBackup:
    name: str
    path: Path
    created_utc: int
    size_bytes: int
    sha256: str
    summary: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "created_utc": self.created_utc,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "summary": self.summary,
        }


class ManagedBackupManager:
    def __init__(self, store: HistoryStore, directory: str | Path | None = None) -> None:
        self.store = store
        self.directory = Path(directory or store.path.parent / "managed_backups")
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._description_cache: dict[Path, tuple[int, int, ManagedBackup]] = {}
        with contextlib.suppress(OSError):
            os.chmod(self.directory, 0o700)

    def create(self, *, label: str = "manual") -> ManagedBackup:
        safe_label = re.sub(r"[^a-z0-9_-]+", "-", label.strip().lower()).strip("-")[:24] or "manual"
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        path = self.directory / f"gmc-managed-{stamp}-{safe_label}.sqlite3"
        suffix = 1
        while path.exists():
            path = self.directory / f"gmc-managed-{stamp}-{safe_label}-{suffix}.sqlite3"
            suffix += 1
        self.store.backup_to_path(path)
        secure_file(path)
        return self._describe(path)

    def list(self) -> list[ManagedBackup]:
        backups: list[ManagedBackup] = []
        current_paths = set(self.directory.glob("gmc-managed-*.sqlite3"))
        for cached_path in set(self._description_cache) - current_paths:
            self._description_cache.pop(cached_path, None)
        for path in sorted(current_paths, reverse=True):
            try:
                backups.append(self._describe(path))
            except (OSError, ValueError):
                continue
        return backups

    def resolve(self, name: str) -> Path:
        candidate = str(name or "").strip()
        if not _SAFE_BACKUP_NAME.match(candidate):
            raise ValueError("Invalid managed backup name")
        path = self.directory / candidate
        resolved = path.resolve()
        if resolved.parent != self.directory.resolve() or not resolved.is_file():
            raise FileNotFoundError(candidate)
        return resolved

    def delete(self, name: str) -> None:
        path = self.resolve(name)
        path.unlink()
        self._description_cache.pop(path, None)

    def prune(self, keep: int) -> list[str]:
        keep_count = max(1, min(50, int(keep)))
        backups = self.list()
        removed: list[str] = []
        for backup in backups[keep_count:]:
            backup.path.unlink(missing_ok=True)
            self._description_cache.pop(backup.path, None)
            removed.append(backup.name)
        return removed

    def compare(self, first_name: str, second_name: str) -> dict[str, Any]:
        first = self._describe(self.resolve(first_name))
        second = self._describe(self.resolve(second_name))
        first_summary = first.summary
        second_summary = second.summary
        return {
            "first": first.as_dict(),
            "second": second.as_dict(),
            "measurement_difference": int(second_summary.get("measurements", 0)) - int(first_summary.get("measurements", 0)),
            "raw_measurement_difference": int(second_summary.get("raw_measurements", 0)) - int(first_summary.get("raw_measurements", 0)),
            "schema_equal": first_summary.get("schema_version") == second_summary.get("schema_version"),
            "device_count_difference": len(second_summary.get("device_serials", [])) - len(first_summary.get("device_serials", [])),
        }

    def _describe(self, path: Path) -> ManagedBackup:
        stat = path.stat()
        cached = self._description_cache.get(path)
        if cached and cached[0] == int(stat.st_mtime_ns) and cached[1] == int(stat.st_size):
            return cached[2]
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        summary = self.store.inspect_backup_path(path)
        description = ManagedBackup(
            name=path.name,
            path=path,
            created_utc=int(stat.st_mtime),
            size_bytes=int(stat.st_size),
            sha256=digest.hexdigest(),
            summary=summary,
        )
        self._description_cache[path] = (int(stat.st_mtime_ns), int(stat.st_size), description)
        return description
