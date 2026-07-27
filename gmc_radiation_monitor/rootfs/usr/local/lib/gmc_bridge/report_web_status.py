from __future__ import annotations

import contextlib
import time
from datetime import UTC, datetime
from typing import Any
from .adaptive_background import build_adaptive_background, build_site_adaptive_background
from .barometric_background import build_barometric_cosmic_hint
from .fleet_analytics import build_fleet_snapshot
from .reports import build_live_analysis


class ReportStatusMixin:
    """Status, caching and Home Assistant context for the report web application."""

    def _device_is_connected(self, item: dict[str, Any]) -> bool:
        """Return the bridge-owned live state, with a legacy freshness fallback."""
        runtime_online = item.get("runtime_online")
        if isinstance(runtime_online, str):
            runtime_online = runtime_online.strip().lower() in {"1", "true", "yes", "on", "online"}
        if runtime_online is not None:
            return bool(runtime_online)
        if not item.get("runtime_status") and not item.get("runtime_status_updated_utc"):
            # Legacy/history-only databases have no live-state field. The bridge
            # resets every known device to explicit offline at startup, so this
            # compatibility path is only used before that first runtime write.
            return True
        latest_timestamp = int(item.get("timestamp_utc") or item.get("last_timestamp_utc") or 0)
        last_seen_text = str(item.get("last_seen_utc", ""))
        last_seen_epoch = latest_timestamp
        if last_seen_text:
            with contextlib.suppress(ValueError):
                last_seen_epoch = max(
                    last_seen_epoch,
                    int(datetime.fromisoformat(last_seen_text.replace("Z", "+00:00")).timestamp()),
                )
        online_window = max(180, int(item.get("scan_interval_seconds") or self.scan_interval_seconds) * 3)
        return last_seen_epoch > 0 and int(datetime.now(UTC).timestamp()) - last_seen_epoch <= online_window

    def _connected_devices(self, devices: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Hide historical/offline counters from the live analysis views."""
        return [item for item in devices if self._device_is_connected(item)]

    def _data_revision(self) -> tuple[int, int | None, int]:
        count = self.store.count(all_devices=True)
        _first, last = self.store.bounds()
        # A minute bucket lets cached environmental context refresh even when no
        # new radiation sample has arrived.
        return count, last, int(time.time() // 60)

    def _live_analysis_cached(
        self, *, device_serial: str, scan_interval_seconds: int, cpm_per_usvh: float
    ) -> dict[str, Any]:
        key = (
            "live-analysis",
            self._data_revision()[:2],
            device_serial,
            scan_interval_seconds,
            self.traffic_light_yellow_percent,
            self.traffic_light_red_percent,
        )
        def build() -> dict[str, Any]:
            result = build_live_analysis(
                self.store,
                scan_interval_seconds=scan_interval_seconds,
                traffic_light_yellow_percent=self.traffic_light_yellow_percent,
                traffic_light_red_percent=self.traffic_light_red_percent,
                device_serial=device_serial,
            )
            result["_scan_interval_seconds"] = scan_interval_seconds
            result["_cpm_per_usvh"] = cpm_per_usvh
            return result
        return self.analysis_cache.get_or_build(key, build)

    def _fleet_context_cached(self, *, selected_serial: str, devices: list[dict[str, Any]]) -> dict[str, Any]:
        revision = self._data_revision()
        device_signature = tuple(
            sorted(
                (
                    str(item.get("serial") or ""),
                    int(float(item.get("scan_interval_seconds") or self.scan_interval_seconds)),
                )
                for item in devices
                if item.get("serial")
            )
        )
        key = ("fleet-context", revision, selected_serial, device_signature)
        def build() -> dict[str, Any]:
            fleet_snapshot = build_fleet_snapshot(self.store)
            selected_rows = self.store.query_all(device_serial=selected_serial) if selected_serial else []
            device_profile = (
                build_adaptive_background(selected_rows, timezone_name=self.timezone_name)
                if selected_serial
                else {"available": False}
            )
            rows_by_serial = {
                str(item.get("serial")): self.store.query_all(device_serial=str(item.get("serial")))
                for item in devices
                if item.get("serial")
            }
            tolerance = max(
                [
                    int(float(item.get("scan_interval_seconds") or self.scan_interval_seconds))
                    for item in devices
                ]
                or [self.scan_interval_seconds]
            )
            site_profile = build_site_adaptive_background(
                rows_by_serial,
                timezone_name=self.timezone_name,
                device_weights=fleet_snapshot.get("device_weights", {}),
                tolerance_seconds=tolerance,
            )
            pressure_snapshot = (
                self.pressure_client.get_pressure().as_dict()
                if self.pressure_client is not None
                else {"available": False, "error": "Pressure client is not configured"}
            )
            barometric_hint = build_barometric_cosmic_hint(
                rows_by_serial,
                timezone_name=self.timezone_name,
                device_weights=fleet_snapshot.get("device_weights", {}),
                tolerance_seconds=tolerance,
                pressure_snapshot=pressure_snapshot,
                enabled=self.cosmic_hint_enabled,
            )
            return {
                "fleet_snapshot": fleet_snapshot,
                "device_profile": device_profile,
                "site_profile": site_profile,
                "barometric_hint": barometric_hint,
            }
        return self.analysis_cache.get_or_build(key, build)

    def status(self) -> dict[str, Any]:
        count = self.store.count(all_devices=True)
        first, last = self.store.bounds()
        metadata = self.store.get_metadata()
        database = self.store.database_stats()
        capabilities = self.store.get_device_capabilities()
        devices = self.store.list_devices()
        ingest = self.store.get_ingest_diagnostics()
        home_location = (
            self.home_assistant_client.get_location().as_dict()
            if self.home_assistant_client is not None
            else {"available": False, "error": "Home Assistant API client is not configured"}
        )
        return {
            "status": "ok",
            "measurements": count,
            "first_timestamp_utc": first,
            "last_timestamp_utc": last,
            "timezone": self.timezone_name,
            "scan_interval_seconds": self.scan_interval_seconds,
            "history_retention_days": self.store.retention_days,
            "cpm_per_usvh": self.cpm_per_usvh,
            "traffic_light_yellow_percent": self.traffic_light_yellow_percent,
            "traffic_light_red_percent": self.traffic_light_red_percent,
            "safety_profile": self.safety_profile,
            "safety_threshold_basis": self.safety_threshold_basis,
            "safety_warning_cpm": self.safety_warning_cpm,
            "safety_danger_cpm": self.safety_danger_cpm,
            "safety_warning_usvh": self.safety_warning_usvh,
            "safety_danger_usvh": self.safety_danger_usvh,
            "restore_enabled": self.restore_enabled,
            "device_model": metadata.get("device_model", "Not detected yet"),
            "serial": metadata.get("serial", "Not detected yet"),
            "device_profile": metadata.get(
                "device_profile_name", metadata.get("device_profile", "Not detected yet")
            ),
            "capabilities": capabilities,
            "database": database,
            "ingest_diagnostics": ingest,
            "devices": devices,
            "home_assistant_location": home_location,
        }

