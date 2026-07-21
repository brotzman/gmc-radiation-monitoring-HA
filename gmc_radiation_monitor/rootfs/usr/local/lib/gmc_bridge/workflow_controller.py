from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .analysis_presentation import build_detailed_analysis_result
from .config_validation import validate_options
from .health import assess_health
from .workflow import (
    compare_periods,
    default_comparison_ranges,
    downsample_history,
    run_self_test,
)


class WorkflowApplicationMixin:
    """Application-level workflow APIs kept separate from the report renderer.

    The concrete application supplies the history store, presentation settings,
    device helpers and runtime directories. Keeping these APIs here prevents the
    main HTML report orchestrator from growing with every workflow feature.
    """

    scheduled_report_directory: Path

    def list_scheduled_reports(self, *, limit: int = 50) -> list[dict[str, Any]]:
        allowed_suffixes = {".zip", ".json"}
        candidates: list[tuple[float, Path]] = []
        try:
            paths = list(self.scheduled_report_directory.iterdir())
        except OSError:
            paths = []
        for path in paths:
            try:
                stat = path.stat()
            except OSError:
                continue
            if not path.is_file() or path.suffix.lower() not in allowed_suffixes or not path.name.startswith("gmc-"):
                continue
            candidates.append((stat.st_mtime, path))
        items: list[dict[str, Any]] = []
        for _modified, path in sorted(candidates, key=lambda item: item[0], reverse=True):
            try:
                stat = path.stat()
            except OSError:
                continue
            items.append({"name": path.name, "size_bytes": int(stat.st_size), "created_utc": int(stat.st_mtime)})
            if len(items) >= max(1, min(200, int(limit))):
                break
        return items

    def resolve_scheduled_report(self, name: str) -> Path:
        candidate = str(name or "").strip()
        suffix = Path(candidate).suffix.lower()
        if not candidate.startswith("gmc-") or Path(candidate).name != candidate or suffix not in {".zip", ".json"}:
            raise ValueError("Invalid scheduled report name")
        path = (self.scheduled_report_directory / candidate).resolve()
        if path.parent != self.scheduled_report_directory.resolve() or not path.is_file():
            raise FileNotFoundError(candidate)
        return path

    def delete_scheduled_report(self, name: str) -> Path:
        """Delete one validated scheduled report file."""
        path = self.resolve_scheduled_report(name)
        path.unlink()
        return path

    def _known_device_serial(self, requested: str | None = None) -> str:
        devices = self._connected_devices(self.store.list_devices())
        serials = [str(item.get("serial") or "") for item in devices if str(item.get("serial") or "")]
        if requested and requested in serials:
            return requested
        primary = str(self.store.get_metadata().get("serial") or "")
        return primary if primary in serials else (serials[0] if serials else "")

    def api_analysis(self, device_serial: str | None = None) -> dict[str, Any]:
        serial = self._known_device_serial(device_serial)
        if not serial:
            return {"available": False, "device_serial": "", "analysis": {}}
        scan, factor = self._device_report_settings(serial)
        raw = self._live_analysis_cached(
            device_serial=serial,
            scan_interval_seconds=scan,
            cpm_per_usvh=factor,
        )
        latest_local = None
        if raw.get("latest_timestamp_utc") is not None:
            latest_local = datetime.fromtimestamp(int(raw["latest_timestamp_utc"]), UTC).astimezone(self.timezone)
        return {
            "available": bool(raw.get("available")),
            "device_serial": serial,
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "raw": raw,
            "presentation": build_detailed_analysis_result(
                raw,
                config=self._presentation_config(),
                latest_local=latest_local
            ).as_dict(),
        }

    def api_history(
        self,
        *,
        device_serial: str | None,
        start_utc: int | None = None,
        end_utc: int | None = None,
        include_raw: bool = False,
    ) -> dict[str, Any]:
        serial = self._known_device_serial(device_serial)
        end = int(time.time()) + 1 if end_utc is None else int(end_utc)
        start = end - 86400 if start_utc is None else int(start_utc)
        if end <= start:
            raise ValueError("History end must be greater than start")
        if end - start > 366 * 86400:
            raise ValueError("History API period is limited to 366 days")
        rows = self.store.query_range(start, end, device_serial=serial)
        payload: dict[str, Any] = {
            "device_serial": serial,
            "start_utc": start,
            "end_utc": end,
            "accepted": downsample_history(rows, maximum_points=2000),
            "annotations": self.store.list_event_annotations(
                start_utc=start, end_utc=end, device_serial=serial, limit=1000
            ),
        }
        if include_raw:
            payload["raw"] = self.store.query_raw_measurements(start, end, device_serial=serial)[:5000]
        return payload

    def api_comparison(
        self,
        *,
        device_serial: str | None,
        first_range: tuple[int, int] | None = None,
        second_range: tuple[int, int] | None = None,
    ) -> dict[str, Any]:
        serial = self._known_device_serial(device_serial)
        default_first, default_second = default_comparison_ranges(self.timezone)
        first = first_range or default_first
        second = second_range or default_second
        scan, _factor = self._device_report_settings(serial)
        return {
            "device_serial": serial,
            "comparison": compare_periods(
                self.store,
                device_serial=serial,
                first_start_utc=first[0],
                first_end_utc=first[1],
                second_start_utc=second[0],
                second_end_utc=second[1],
                scan_interval_seconds=scan,
            ).as_dict(),
        }

    def api_health(self) -> dict[str, Any]:
        devices = []
        for item in self.store.list_devices():
            normalized = dict(item)
            normalized["health_connected"] = self._device_is_connected(item)
            devices.append(normalized)
        assessment = assess_health(
            store=self.store,
            devices=devices,
            options_path=self.options_path,
            scan_interval_seconds=self.scan_interval_seconds,
            started_at_utc=self.started_at_utc,
            bridge_heartbeat_path=self.bridge_heartbeat_path,
        )
        return assessment.as_dict(generated_at_utc=datetime.now(UTC).isoformat())

    def api_self_test(self) -> dict[str, Any]:
        status = self.status()
        checks = run_self_test(
            store=self.store,
            timezone_name=self.timezone_name,
            devices=list(status.get("devices") or []),
            home_assistant_available=bool((status.get("home_assistant_location") or {}).get("available")),
            options_path=self.options_path,
            backup_directory=self.backup_manager.directory,
        )
        has_errors = any(item.status == "error" for item in checks)
        has_warnings = any(item.status == "warning" for item in checks)
        overall_status = "error" if has_errors else "warning" if has_warnings else "ok"
        return {
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "ok": not has_errors,
            "healthy": not has_errors,
            "status": overall_status,
            "checks": [item.as_dict() for item in checks],
        }

    def api_config_validation(self) -> dict[str, Any]:
        try:
            payload = json.loads(self.options_path.read_text(encoding="utf-8"))
            validation = validate_options(payload)
            source = str(self.options_path)
            return {"source": source, **validation.as_dict(), "problems": validation.messages()}
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return {
                "valid": False,
                "clean": False,
                "status": "error",
                "source": "unavailable",
                "problems": [str(exc)],
                "errors": [str(exc)],
                "warnings": [],
                "issues": [],
            }
