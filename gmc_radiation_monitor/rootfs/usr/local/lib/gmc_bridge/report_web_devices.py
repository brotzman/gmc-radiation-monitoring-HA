from __future__ import annotations

import contextlib
import html
from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote_plus
from .analysis_presentation import AnalysisPresentationConfig, baseline_state, build_absolute_safety_result, build_adaptive_background_result, build_background_profile_entity, build_combined_interpretation_result, build_cosmic_influence_result, build_detailed_analysis_result, build_fleet_intelligence_result, build_local_background_result, build_radiation_intelligence_result, build_recommendation_result, effective_safety_thresholds, fleet_stability_display_key, safety_state
from .calibration_web import render_calibration_panel
from .device_profiles import normalize_device_version_display
from .device_card_display import format_live_dose as _format_live_dose, measurement_freshness, render_connection_details, render_device_card_header, render_live_measurement
from .fleet_analytics import build_fleet_snapshot
from .historical_presentation import trend_symbol
from .intelligence import build_radiation_intelligence
from .number_format import format_number, localize_numeric_text
from .orientation import calculate_orientation, orientation_status
from .report_web_support import _encode_report_target
from .report_statistics import build_statistics
from .reports import expected_samples, resolve_period
from .translations import Translator, resolve_language
from .utils import slugify
from .web_analysis_views import render_absolute_safety, render_adaptive_background, render_assessment_legend, render_background_profile_entity, render_combined_interpretation, render_cosmic_influence, render_device_analysis, render_fleet_intelligence, render_local_background, render_radiation_intelligence, render_recommendation
from .web_components import render_collapsible_card


class ReportDeviceViewMixin:
    """Device cards and analysis rendering for the report web application."""

    @staticmethod
    def _render_collapsible_card(
        *,
        card_id: str,
        title: str,
        body: str,
        attributes: str = "",
        open_by_default: bool = True,
        help_text: str = "",
        explanation_code: str | None = None,
        t: Translator | None = None,
        pin_label: str = "Pin card",
        help_label: str = "Show help",
    ) -> str:
        return render_collapsible_card(
            card_id=card_id,
            title=title,
            body=body,
            attributes=attributes,
            open_by_default=open_by_default,
            help_text=help_text,
            explanation_code=explanation_code,
            translator=t,
            pin_label=pin_label,
            help_label=help_label,
        )

    @staticmethod
    def _trend_symbol(value: float | None) -> str:
        return trend_symbol(value)

    @staticmethod
    def _background_profile_block(profile: dict[str, Any], *, title: str, t: Translator) -> str:
        """Compatibility wrapper for callers predating the shared model migration."""
        entity = build_background_profile_entity(
            profile, key=slugify(title) or "background-profile", title=title
        )
        return render_background_profile_entity(entity, t)

    @staticmethod
    def _fleet_stability_display_key(item: Any) -> tuple[int, str, str]:
        """Compatibility wrapper for the shared fleet-card ordering rule."""
        return fleet_stability_display_key(item)

    def _render_radiation_intelligence(
        self,
        *,
        analysis: dict[str, Any],
        selected_serial: str,
        snapshot: dict[str, Any],
        t,
        device_profile: dict[str, Any],
        site_profile: dict[str, Any],
    ) -> str:
        recent_move = any(
            str(event.get("serial")) == selected_serial
            and int(snapshot.get("generated_at_utc", 0)) - int(event.get("timestamp_utc", 0)) <= 1800
            for event in snapshot.get("orientation_events", [])
        )
        raw_result = build_radiation_intelligence(
            analysis,
            comparison=snapshot.get("comparison"),
            shared_event=snapshot.get("shared_event"),
            recent_orientation_change=recent_move,
            device_profile=device_profile,
            site_profile=site_profile,
        )
        collected = int(analysis.get("samples_24h") or analysis.get("samples_1h") or 0)
        needed = max(
            0,
            int(analysis.get("baseline_minimum_samples") or 6) - int(analysis.get("samples_7d") or 0),
        )
        result = build_radiation_intelligence_result(raw_result, collected=collected, needed=needed)
        return render_radiation_intelligence(result, t)

    def _render_adaptive_background(
        self, *, device_profile: dict[str, Any], site_profile: dict[str, Any], t
    ) -> str:
        result = build_adaptive_background_result(device_profile, site_profile)
        return render_adaptive_background(result, t)

    def _render_cosmic_influence(self, model: dict[str, Any], *, t) -> str:
        result = build_cosmic_influence_result(model)
        return render_cosmic_influence(result, t)

    def _render_fleet_intelligence(self, *, t, snapshot: dict[str, Any] | None = None) -> str:
        result = build_fleet_intelligence_result(snapshot or build_fleet_snapshot(self.store))
        return render_fleet_intelligence(result, t)

    def _render_devices_section(
        self,
        *,
        devices: list[dict[str, Any]],
        selected_serial: str,
        mode: str,
        language: str,
        t: Translator,
    ) -> str:
        capability_labels = {
            "cpm": "CPM",
            "temperature": t("Temperature"),
            "voltage": t("Voltage"),
            "gyro": t("Gyroscope"),
            "dual_tube": t("Dual-tube measurement"),
            "device_time": t("Device time"),
            "tube_low_cpm": t("Low-dose tube"),
            "tube_high_cpm": t("High-dose tube"),
        }

        def render_device_card(item: dict[str, Any]) -> str:
            serial_value = str(item.get("serial", "unknown"))
            selected = serial_value == selected_serial
            capabilities_map = item.get("capabilities_map") or {}
            if capabilities_map:
                enabled = [
                    capability_labels.get(name, name.replace("_", " "))
                    for name, supported in capabilities_map.items()
                    if supported
                ]
            else:
                enabled = [
                    capability_labels.get(name.strip(), name.strip().replace("_", " "))
                    for name in str(item.get("capabilities", "")).split(",")
                    if name.strip()
                ]
            capabilities_value = ", ".join(enabled) or t("Not detected yet")
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
            runtime_online = item.get("runtime_online")
            if isinstance(runtime_online, str):
                runtime_online = runtime_online.strip().lower() in {"1", "true", "yes", "on", "online"}
            if runtime_online is None:
                online = (
                    last_seen_epoch > 0
                    and int(datetime.now(UTC).timestamp()) - last_seen_epoch <= online_window
                )
            else:
                # The bridge owns the authoritative per-device connection state.
                # Analysis selection is a read-only view and must never affect it.
                online = bool(runtime_online)
            status_class = "online" if online else "offline"
            status_label = t("Online") if online else t("Offline")
            runtime_reason = str(item.get("runtime_status_reason") or "")

            def format_external_timestamp(value: object, fallback: str) -> str:
                if value in (None, ""):
                    return fallback
                try:
                    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
                    return parsed.astimezone(self.timezone).strftime("%d.%m.%Y %H:%M:%S %Z" if language == "de" else "%Y-%m-%d %H:%M:%S %Z")
                except (TypeError, ValueError):
                    return str(value)

            if latest_timestamp:
                last_update = (
                    datetime.fromtimestamp(latest_timestamp, UTC)
                    .astimezone(self.timezone)
                    .strftime("%d.%m.%Y %H:%M:%S %Z" if language == "de" else "%Y-%m-%d %H:%M:%S %Z")
                )
            else:
                last_update = t("Not detected yet")
            profile = t(str(item.get("device_profile_name", item.get("device_profile", "unknown"))))
            model_display = normalize_device_version_display(str(item.get("device_model", "GMC")))
            configured_name = str(item.get("configured_name") or "").strip()
            display_title = configured_name or model_display
            model_subtitle = model_display if model_display != display_title else ""
            measurement_age_seconds = max(0, int(datetime.now(UTC).timestamp()) - latest_timestamp) if latest_timestamp else None
            freshness = measurement_freshness(
                online=online,
                age_seconds=measurement_age_seconds,
                scan_interval_seconds=int(item.get("scan_interval_seconds") or self.scan_interval_seconds),
                runtime_reason=runtime_reason,
                t=t,
            )
            freshness_display = str(freshness["label"])
            normalized_model = model_display.casefold().replace(" ", "")
            if "320" in normalized_model:
                device_visual_class, device_icon = "device-320", "320"
            elif "500" in normalized_model:
                device_visual_class, device_icon = "device-500", "500+"
            else:
                device_visual_class, device_icon = "device-generic", "GMC"
            latest_cpm = item.get("cpm")
            latest_value = "—" if latest_cpm is None else f"{format_number(int(latest_cpm), language, grouping=True)} CPM"
            dose_value = item.get("derived_dose_usvh")
            dose_number, dose_unit = _format_live_dose(dose_value, language)
            quality_stars = str(item.get("measurement_quality_star_text") or "☆☆☆☆☆")
            detector_name = str(item.get("active_tube") or item.get("tube_model") or model_display)
            tube_values = ""
            if item.get("tube_low_cpm") is not None or item.get("tube_high_cpm") is not None:
                tube_values = (
                    f'<div class="device-field"><strong>{html.escape(t("Low-dose tube"))}</strong>'
                    f"<span>{html.escape(localize_numeric_text(item.get('tube_low_cpm', '—'), language, group_plain_integers=True))} CPM</span></div>"
                    f'<div class="device-field"><strong>{html.escape(t("High-dose tube"))}</strong>'
                    f"<span>{html.escape(localize_numeric_text(item.get('tube_high_cpm', '—'), language, group_plain_integers=True))} CPM</span></div>"
                )
            diagnostics_values: list[str] = []
            for label, key in (
                ("Hardware model", "hardware_model"),
                ("Firmware version", "firmware_version"),
            ):
                value = item.get(key)
                if value not in (None, "", "unknown"):
                    diagnostics_values.append(
                        f'<div class="device-field"><strong>{html.escape(t(label))}</strong>'
                        f"<span>{html.escape(str(value))}</span></div>"
                    )
            if item.get("voltage_v") is not None:
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Battery voltage"))}</strong>'
                    f"<span>{format_number(float(item['voltage_v']), language, decimals=2)} V</span></div>"
                )
            if item.get("device_time"):
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Device clock"))}</strong>'
                    f"<span>{html.escape(str(item['device_time']))}</span></div>"
                )
            if item.get("device_clock_offset_seconds") is not None:
                offset = int(item["device_clock_offset_seconds"])
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Device clock offset"))}</strong>'
                    f"<span>{format_number(offset, language, grouping=True, sign=True)} s</span></div>"
                )
            clock_status = str(item.get("device_clock_status", ""))
            clock_status_labels = {
                "ok": "Clock synchronized",
                "warning": "Clock offset exceeds warning threshold",
                "unavailable": "Device clock unavailable",
                "invalid": "Invalid device clock response",
            }
            if clock_status in clock_status_labels:
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Device clock status"))}</strong>'
                    f"<span>{html.escape(t(clock_status_labels[clock_status]))}</span></div>"
                )
            if item.get("heartbeat_enabled"):
                cps_value = item.get("heartbeat_cps", "—")
                rolling_value = item.get("heartbeat_cpm_60s", "—")
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Live radiation CPS"))}</strong>'
                    f"<span>{html.escape(localize_numeric_text(cps_value, language, group_plain_integers=True))} CPS</span></div>"
                )
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Heartbeat rolling 60 s CPM"))}</strong>'
                    f"<span>{html.escape(localize_numeric_text(rolling_value, language, group_plain_integers=True))} CPM</span></div>"
                )
            gyro_values = (item.get("gyro_x"), item.get("gyro_y"), item.get("gyro_z"))
            if all(value is not None for value in gyro_values):
                raw_x, raw_y, raw_z = (int(value) for value in gyro_values)
                orientation = calculate_orientation(serial_value, raw_x, raw_y, raw_z)
                if orientation is not None:
                    status_key, status_color = orientation_status(orientation)
                    diagnostics_values.extend(
                        [
                            f'<div class="orientation-state {status_color}">'
                            f'<div class="orientation-state-copy"><strong>{html.escape(t("Device position"))} · {html.escape(t(status_key))}</strong>'
                            f"<span>{html.escape(t(orientation.position_key))}</span>"
                            f"<small>{html.escape(t('Inclination'))}: {format_number(orientation.inclination_degrees, language, decimals=1)}°</small></div></div>",
                            f'<div class="device-field"><strong>{html.escape(t("Roll angle"))}</strong>'
                            f"<span>{format_number(orientation.roll_degrees, language, decimals=1, sign=True)}°</span></div>",
                            f'<div class="device-field"><strong>{html.escape(t("Pitch angle"))}</strong>'
                            f"<span>{format_number(orientation.pitch_degrees, language, decimals=1, sign=True)}°</span></div>",
                            f'<div class="device-field"><strong>{html.escape(t("Inclination"))}</strong>'
                            f"<span>{format_number(orientation.inclination_degrees, language, decimals=1)}°</span></div>",
                        ]
                    )
            device_diagnostics_values = "".join(diagnostics_values)

            calibration_html = render_calibration_panel(
                item=item,
                latest_cpm=latest_cpm,
                t=t,
            )
            gmcmap_html = ""
            if item.get("gmcmap_enabled"):
                raw_map_status = str(item.get("gmcmap_upload_status", "not_configured"))
                map_status_labels = {
                    "disabled": "Disabled",
                    "not_configured": "Not configured",
                    "waiting": "Waiting for first upload",
                    "uploading": "Uploading",
                    "success": "Upload successful",
                    "error": "Upload failed",
                }
                map_status_label = t(map_status_labels.get(raw_map_status, raw_map_status))
                map_status_class = {
                    "success": "online",
                    "uploading": "online",
                    "error": "error",
                    "not_configured": "offline",
                    "waiting": "waiting",
                }.get(raw_map_status, "offline")
                last_map_upload = format_external_timestamp(item.get("gmcmap_last_upload_utc"), t("Never"))
                counter_id_masked = item.get("gmcmap_counter_id_masked") or "—"
                map_error = ""
                if not item.get("gmcmap_configured"):
                    map_error = (
                        f'<div class="gmcmap-error">'
                        f"{html.escape(t('GMCMap is enabled, but this device has no counter ID mapping.'))}"
                        f"</div>"
                    )
                gmcmap_html = (
                    f'<div class="gmcmap-panel">'
                    f'<div class="gmcmap-header"><div><strong>{html.escape(t("Public GMCMap upload"))}</strong>'
                    f"<small>{html.escape(t('Measurements are sent to the public GMCMap service.'))}</small></div>"
                    f'<span class="device-status {map_status_class}">{html.escape(map_status_label)}</span></div>'
                    f'<div class="gmcmap-grid">'
                    f"<div><strong>{html.escape(t('Counter ID'))}</strong><span>{html.escape(str(counter_id_masked))}</span></div>"
                    f"<div><strong>{html.escape(t('Last upload'))}</strong><span>{html.escape(str(last_map_upload))}</span></div>"
                    f"<div><strong>{html.escape(t('Last uploaded CPM'))}</strong><span>{html.escape(localize_numeric_text(item.get('gmcmap_last_cpm') if item.get('gmcmap_last_cpm') is not None else '—', language, group_plain_integers=True))} CPM</span></div>"
                    f"<div><strong>{html.escape(t('Last uploaded ACPM'))}</strong><span>{html.escape(localize_numeric_text(item.get('gmcmap_last_average_cpm') if item.get('gmcmap_last_average_cpm') is not None else '—', language, group_plain_integers=True))} ACPM</span></div>"
                    f'</div><small class="gmcmap-acpm-help">{html.escape(t("ACPM is a time-weighted rolling average of accepted CPM readings from the last 60 minutes; long data gaps are not bridged."))}</small>'
                    f"{map_error}</div>"
                )
            alerts: list[str] = []
            health_status = str(item.get("device_health_status") or "ok")
            health_reason = str(item.get("device_health_reason") or "normal_variation")
            health_reason_labels = {
                "prolonged_zero_cpm": "Unusually long sequence of zero CPM values",
                "unchanged_cpm_sequence": "CPM has remained exactly unchanged for an unusually long time",
                "dual_tube_imbalance": "Dual-tube values are persistently implausible",
                "normal_variation": "Device values vary normally",
                "initializing": "Device health monitoring is still initializing",
            }
            if health_status != "ok":
                alerts.append(
                    f'<div class="device-alert warning"><strong>{html.escape(t("Device health warning"))}</strong>'
                    f"<span>{html.escape(t(health_reason_labels.get(health_reason, health_reason)))}</span></div>"
                )
            pending_confirmations = int(item.get("cpm_gate_pending_confirmations") or 0)
            required_confirmations = int(item.get("cpm_gate_required_confirmations") or 3)
            if pending_confirmations:
                alerts.append(
                    f'<div class="device-alert warning"><strong>{html.escape(t("Suspicious CPM value is being verified"))}</strong>'
                    f"<span>{format_number(pending_confirmations, language)}/{format_number(required_confirmations, language)} {html.escape(t('confirmations'))}</span></div>"
                )
            discarded_peaks = int(item.get("cpm_discarded_peak_samples") or 0)
            if discarded_peaks:
                alerts.append(
                    f'<div class="device-alert info"><strong>{html.escape(t("Discarded unconfirmed CPM peaks"))}</strong>'
                    f"<span>{format_number(discarded_peaks, language, grouping=True)} {html.escape(t('since the current bridge start'))}</span></div>"
                )
            serial_errors = int(item.get("serial_error_count") or 0)
            reconnects = int(item.get("serial_reconnect_count") or 0)
            if serial_errors or reconnects:
                alerts.append(
                    f'<div class="device-alert info"><strong>{html.escape(t("Serial connection recovered"))}</strong>'
                    f"<span>{format_number(serial_errors, language, grouping=True)} {html.escape(t('errors'))} · {format_number(reconnects, language, grouping=True)} {html.escape(t('reconnects'))}</span></div>"
                )
            history_errors = int(item.get("history_write_error_count") or 0)
            if history_errors:
                alerts.append(
                    f'<div class="device-alert error"><strong>{html.escape(t("History storage warning"))}</strong>'
                    f"<span>{format_number(history_errors, language, grouping=True)} {html.escape(t('write errors since app start'))}</span></div>"
                )
            if clock_status == "warning":
                alerts.append(
                    f'<div class="device-alert warning"><strong>{html.escape(t("Device clock warning"))}</strong>'
                    f"<span>{html.escape(t('The device clock differs from Home Assistant time.'))}</span></div>"
                )
            alert_html = (
                f'<div class="device-alerts">{"".join(alerts)}</div>'
                if alerts
                else f'<div class="device-ok"><span>✓</span>{html.escape(t("No active device warnings"))}</div>'
            )
            status_updated = format_external_timestamp(item.get("runtime_status_updated_utc"), t("Not available"))
            next_scan = t("Not available")
            if latest_timestamp and online:
                next_scan_epoch = latest_timestamp + int(item.get("scan_interval_seconds") or self.scan_interval_seconds)
                remaining = max(0, next_scan_epoch - int(datetime.now(UTC).timestamp()))
                next_scan = t("in {seconds} seconds", seconds=remaining)
            runtime_reason_label = runtime_reason.replace("_", " ") if runtime_reason else t("Not available")
            connection_details = render_connection_details(
                t=t, serial_value=serial_value, port=item.get("port", "—"),
                baudrate=item.get("baudrate", "—"), interval_seconds=item.get("scan_interval_seconds", "—"),
                last_response=last_update, next_scan=next_scan, status_updated=status_updated,
                runtime_reason=runtime_reason_label, reconnects=reconnects, serial_errors=serial_errors,
                profile=profile, capabilities=capabilities_value,
                stored_samples=int(item.get("stored_samples") or 0),
                health_summary=t("No active device warnings") if health_status == "ok" else t("Device health warning"),
                tube_values=tube_values, diagnostics_values=device_diagnostics_values,
            )
            action_label = t("Analysis shown") if selected else t("Show analysis")
            href = f"?mode={mode}&amp;lang={language}&amp;device={quote_plus(serial_value)}"
            selected_class = " selected" if selected else ""
            primary_class = " primary" if selected else ""
            return (
                f'<article class="device-card {device_visual_class}{selected_class}" data-device-serial="{html.escape(serial_value, quote=True)}" data-device-model="{html.escape(model_display, quote=True)}">'
                + render_device_card_header(
                    display_title=display_title, model_subtitle=model_subtitle, serial_value=serial_value,
                    device_icon=device_icon, status_class=status_class, status_label=status_label,
                    freshness_display=freshness_display, last_update=last_update,
                    freshness_state=str(freshness["state"]),
                    freshness_severity=str(freshness["severity"]),
                )
                + render_live_measurement(
                    t=t, dose_number=dose_number, dose_unit=dose_unit, quality_stars=quality_stars,
                    latest_value=latest_value, detector_name=detector_name,
                    cpm_per_usvh=item.get("cpm_per_usvh") or self.cpm_per_usvh,
                )
                + f"{alert_html}"
                + connection_details
                + f"{calibration_html}"
                + f"{gmcmap_html}"
                + f'<a class="button device-select{primary_class}" href="{href}">{html.escape(action_label)}</a>'
                + "</article>"
            )

        device_cards = "".join(render_device_card(item) for item in devices) or (
            f'<div class="empty-state scanning"><span class="empty-state-icon">⌁</span>'
            f"<strong>{html.escape(t('GMC devices are being detected automatically'))}</strong>"
            f"<span>{html.escape(t('No connected counter is available yet. The next serial scan runs automatically.'))}</span></div>"
        )
        connected_count = sum(1 for item in devices if self._device_is_connected(item))
        return self._render_collapsible_card(
            card_id="devices",
            title=t("Connected GMC devices"),
            body=(
                f'<div id="live-refresh-status" class="live-refresh-status" role="status" aria-live="polite" hidden></div>'
                + f'<div class="device-grid">{device_cards}</div>'
            ),
            attributes=(
                f'data-connected-count="{connected_count}" '
                f'data-selected-serial="{html.escape(selected_serial, quote=True)}"'
            ),
            help_text=t(
                "Shows live connection state, the latest accepted measurement and warnings for each automatically detected GMC counter."
            ),
            pin_label=t("Pin card"),
            help_label=t("Show help"),
        )

    def live_devices_payload(
        self, *, language_override: str | None = None, accept_language: str = "",
        device_override: str | None = None,
    ) -> dict[str, Any]:
        language = resolve_language(
            self.ui_language, accept_language=accept_language, override=language_override
        )
        t = Translator(language)
        devices = self._connected_devices(sorted(
            self.store.list_devices(),
            key=lambda item: (str(item.get("device_model", "")), str(item.get("serial", ""))),
        ))
        serials = {str(item.get("serial") or "") for item in devices}
        primary_serial = str(self.store.get_metadata().get("serial", ""))
        if primary_serial not in serials:
            primary_serial = next(iter(sorted(serials)), "")
        selected_serial = device_override if device_override in serials else primary_serial
        now_utc = int(datetime.now(UTC).timestamp())
        payload_devices: list[dict[str, Any]] = []
        for item in devices:
            serial = str(item.get("serial") or "")
            latest_timestamp = int(item.get("timestamp_utc") or item.get("last_timestamp_utc") or 0)
            runtime_online = item.get("runtime_online")
            if isinstance(runtime_online, str):
                runtime_online = runtime_online.strip().lower() in {"1", "true", "yes", "on", "online"}
            online_window = max(180, int(item.get("scan_interval_seconds") or self.scan_interval_seconds) * 3)
            online = bool(runtime_online) if runtime_online is not None else (
                latest_timestamp > 0 and now_utc - latest_timestamp <= online_window
            )
            age = max(0, now_utc - latest_timestamp) if latest_timestamp else None
            freshness = measurement_freshness(
                online=online,
                age_seconds=age,
                scan_interval_seconds=int(item.get("scan_interval_seconds") or self.scan_interval_seconds),
                runtime_reason=str(item.get("runtime_status_reason") or ""),
                t=t,
            )
            dose_number, dose_unit = _format_live_dose(item.get("derived_dose_usvh"), language)
            health_status = str(item.get("device_health_status") or "ok")
            health_summary = t("No active device warnings") if health_status == "ok" else t("Device health warning")
            latest_cpm = item.get("cpm")
            payload_devices.append({
                "serial": serial,
                "timestamp_utc": latest_timestamp,
                "status_class": "online" if online else "offline",
                "status_label": t("Online") if online else t("Offline"),
                "freshness_display": str(freshness["label"]),
                "freshness_state": str(freshness["state"]),
                "freshness_severity": str(freshness["severity"]),
                "dose_number": dose_number,
                "dose_unit": dose_unit,
                "quality_stars": str(item.get("measurement_quality_star_text") or "☆☆☆☆☆"),
                "latest_value": "—" if latest_cpm is None else f"{format_number(int(latest_cpm), language, grouping=True)} CPM",
                "health_summary": health_summary,
            })
        return {
            "generated_at_utc": now_utc,
            "selected_serial": selected_serial,
            "connected_count": len(devices),
            "devices": payload_devices,
        }

    def report_preview_payload(
        self, *, period_kind: str, date_value: str | None, week_value: str | None,
        device_serial: str | None = None, language: str = "en",
        month_value: str | None = None, start_value: str | None = None, end_value: str | None = None,
    ) -> dict[str, Any]:
        t = Translator(language)
        period = resolve_period(
            kind=period_kind, selection="specific", tz=self.timezone,
            date_value=date_value, week_value=week_value, month_value=month_value,
            start_value=start_value, end_value=end_value,
        )
        rows = self.store.query_range(
            int(period.start_utc.timestamp()), int(period.end_utc.timestamp()),
            device_serial=device_serial or None,
        )
        stats = build_statistics(
            rows, expected_count=expected_samples(period, self.scan_interval_seconds),
            start_utc=int(period.start_utc.timestamp()), end_utc=int(period.end_utc.timestamp()),
            scan_interval_seconds=self.scan_interval_seconds,
        )
        coverage = float(stats.get("time_coverage_percent") or 0.0)
        gap_seconds = float(stats.get("gap_seconds") or 0.0)
        warning = ""
        if not rows:
            warning = t("No accepted measurements are available for the selected period.")
        elif coverage < 75.0:
            warning = t("The selected period contains substantial data gaps; interpret averages cautiously.")
        return {
            "period_label": period.label,
            "start_local": period.start_local.isoformat(),
            "end_local": period.end_local.isoformat(),
            "samples": len(rows),
            "time_coverage_percent": coverage,
            "sample_coverage_percent": float(stats.get("sample_completeness_percent") or 0.0),
            "gap_seconds": gap_seconds,
            "warning": warning,
        }

    def render_devices_fragment(
        self,
        *,
        mode_override: str | None = None,
        language_override: str | None = None,
        device_override: str | None = None,
        report_device_override: str | None = None,
        accept_language: str = "",
    ) -> bytes:
        mode = mode_override if mode_override in {"simple", "advanced"} else self.ui_mode
        language = resolve_language(
            self.ui_language, accept_language=accept_language, override=language_override
        )
        t = Translator(language)
        all_sorted_devices = sorted(
            self.store.list_devices(),
            key=lambda item: (str(item.get("device_model", "")), str(item.get("serial", ""))),
        )
        devices = self._connected_devices(all_sorted_devices)
        card_devices = self._connected_devices(all_sorted_devices)
        device_serials = {str(item.get("serial")) for item in devices if item.get("serial")}
        primary_serial = str(self.store.get_metadata().get("serial", ""))
        if primary_serial not in device_serials:
            primary_serial = next(iter(sorted(device_serials)), "")
        selected_serial = device_override if device_override in device_serials else primary_serial
        _encode_report_target(selected_serial) if selected_serial else ""
        return self._render_devices_section(
            devices=card_devices,
            selected_serial=selected_serial,
            mode=mode,
            language=language,
            t=t,
        ).encode("utf-8")

    def _analysis_scan_interval(self, analysis: dict[str, Any]) -> int:
        return max(5, int(analysis.get("_scan_interval_seconds") or self.scan_interval_seconds))

    def _analysis_cpm_per_usvh(self, analysis: dict[str, Any]) -> float:
        value = float(analysis.get("_cpm_per_usvh") or self.cpm_per_usvh)
        return value if value > 0 else self.cpm_per_usvh

    def _device_report_settings(self, device_serial: str | None) -> tuple[int, float]:
        if device_serial:
            for item in self.store.list_devices():
                if str(item.get("serial")) == device_serial:
                    return (
                        max(5, int(item.get("scan_interval_seconds") or self.scan_interval_seconds)),
                        float(item.get("cpm_per_usvh") or self.cpm_per_usvh),
                    )
        return self.scan_interval_seconds, self.cpm_per_usvh

    def _presentation_config(self) -> AnalysisPresentationConfig:
        return AnalysisPresentationConfig(
            scan_interval_seconds=self.scan_interval_seconds,
            cpm_per_usvh=self.cpm_per_usvh,
            traffic_light_yellow_percent=self.traffic_light_yellow_percent,
            traffic_light_red_percent=self.traffic_light_red_percent,
            safety_profile=self.safety_profile,
            safety_threshold_basis=self.safety_threshold_basis,
            safety_warning_cpm=self.safety_warning_cpm,
            safety_danger_cpm=self.safety_danger_cpm,
            safety_warning_usvh=self.safety_warning_usvh,
            safety_danger_usvh=self.safety_danger_usvh,
        )

    def _render_analysis(
        self,
        analysis: dict[str, Any],
        *,
        advanced: bool = True,
        t: Translator | None = None,
        device_label: str = "",
        device_model: str = "",
    ) -> str:
        t = t or Translator("en")
        latest_local = None
        if analysis.get("available") and analysis.get("latest_timestamp_utc") is not None:
            latest_local = datetime.fromtimestamp(int(analysis["latest_timestamp_utc"]), UTC).astimezone(
                self.timezone
            )
        config = self._presentation_config()
        result = build_detailed_analysis_result(analysis, config=config, latest_local=latest_local)
        safety = build_absolute_safety_result(analysis, config=config)
        background = build_local_background_result(analysis, config=config)
        interpretation = build_combined_interpretation_result(analysis, config=config)
        return render_device_analysis(
            result,
            safety=safety,
            background=background,
            interpretation=interpretation,
            t=t,
            advanced=advanced,
            device_label=device_label,
            device_model=device_model,
        )

    def _effective_safety_thresholds(self, cpm_per_usvh: float | None = None) -> dict[str, Any]:
        return effective_safety_thresholds(self._presentation_config(), cpm_per_usvh=cpm_per_usvh)

    def _safety_state(self, analysis: dict[str, Any]) -> tuple[str, dict[str, Any], float, float]:
        return safety_state(analysis, config=self._presentation_config())

    def _render_safety_status(self, analysis: dict[str, Any], *, t: Translator | None = None) -> str:
        translator = t or Translator("en")
        return render_absolute_safety(
            build_absolute_safety_result(analysis, config=self._presentation_config()),
            translator,
        )

    def _baseline_state(self, analysis: dict[str, Any]) -> tuple[str, float | None, float]:
        return baseline_state(analysis, config=self._presentation_config())

    def _render_traffic_light(self, analysis: dict[str, Any], *, t: Translator | None = None) -> str:
        translator = t or Translator("en")
        return render_local_background(
            build_local_background_result(analysis, config=self._presentation_config()),
            translator,
        )

    def _render_combined_interpretation(
        self, analysis: dict[str, Any], *, t: Translator | None = None
    ) -> str:
        translator = t or Translator("en")
        return render_combined_interpretation(
            build_combined_interpretation_result(analysis, config=self._presentation_config()),
            translator,
        )

    def _render_recommendation(self, analysis: dict[str, Any], *, t: Translator | None = None) -> str:
        translator = t or Translator("en")
        return render_recommendation(
            build_recommendation_result(analysis, config=self._presentation_config()),
            translator,
        )

    def _render_assessment_legend(self, *, t: Translator | None = None) -> str:
        return render_assessment_legend(t or Translator("en"))

