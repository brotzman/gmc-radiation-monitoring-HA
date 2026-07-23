from __future__ import annotations

import html
import statistics
from datetime import UTC, datetime
from typing import Any

from .calibration_presets import PRESETS
from .device_profiles import normalize_device_version_display
from .history import HistoryStore
from .translations import Translator


def render_device_comparison(*, devices: list[dict[str, Any]], t: Translator) -> str:
    """Render a compact comparison for currently connected counters."""
    comparable = [item for item in devices if item.get("cpm") is not None]
    if len(comparable) < 2:
        return ""
    values = [float(item.get("cpm") or 0.0) for item in comparable]
    mean = statistics.fmean(values) if values else 0.0
    deviation = ((max(values) - min(values)) / mean * 100.0) if mean > 0 else 0.0
    status = "OK" if deviation <= 10.0 else t("Check difference")
    status_class = "ok" if deviation <= 10.0 else "warning"
    rows: list[str] = []
    for item in comparable:
        label = str(
            item.get("configured_name")
            or normalize_device_version_display(str(item.get("device_model") or "GMC"))
        )
        serial = str(item.get("serial") or "")
        rows.append(
            '<div class="device-comparison-row"><div><strong>'
            + html.escape(label)
            + "</strong><small>"
            + html.escape(serial)
            + "</small></div><span>"
            + html.escape(f"{float(item.get('cpm') or 0):.1f} CPM")
            + "</span></div>"
        )
    return (
        '<section class="advanced-only device-comparison-section" id="device-comparison">'
        '<div class="history-section-heading"><div><h2>'
        + html.escape(t("Device comparison"))
        + "</h2><p>"
        + html.escape(t("Compare the latest accepted count rate of all connected GMC devices."))
        + f'</p></div><span class="comparison-status {status_class}">{html.escape(status)}</span></div>'
        + '<div class="device-comparison-card">'
        + "".join(rows)
        + '<div class="device-comparison-summary"><strong>'
        + html.escape(t("Maximum deviation"))
        + f"</strong><span>{deviation:.1f} %</span></div></div></section>"
    )


def render_calibration_management(
    *,
    store: HistoryStore,
    timezone,
    devices: list[dict[str, Any]],
    selected_serial: str,
    t: Translator,
    csrf_token: str,
) -> str:
    """Render presets, custom profiles, wizard and calibration audit history."""
    preset_rows: list[str] = []
    for preset in PRESETS.values():
        secondary = ""
        if preset.high_dose_tube_model:
            secondary = (
                "<small>"
                + html.escape(preset.high_dose_tube_model)
                + " · "
                + html.escape(t("Not calibrated"))
                + "</small>"
            )
        preset_rows.append(
            '<div class="calibration-profile-row"><span class="profile-state">✓</span><div><strong>'
            + html.escape(preset.tube_model)
            + "</strong><small>"
            + html.escape(preset.display_name)
            + "</small>"
            + secondary
            + "</div><span>"
            + html.escape(f"{preset.cpm_per_usvh:g} CPM/µSv/h")
            + "</span></div>"
        )
    custom_rows: list[str] = []
    for item in store.list_custom_calibration_profiles():
        values = item.get("values") or {}
        custom_rows.append(
            '<div class="calibration-profile-row custom"><span class="profile-state">●</span><div><strong>'
            + html.escape(str(item.get("display_name") or item.get("profile_id") or ""))
            + "</strong><small>"
            + html.escape(str(item.get("detector_type") or ""))
            + "</small></div><span>"
            + html.escape(str(values.get("cpm_per_usvh") or "—"))
            + " CPM/µSv/h</span></div>"
        )
    if not custom_rows:
        custom_rows.append(
            '<div class="note">' + html.escape(t("No custom calibration profiles yet.")) + "</div>"
        )
    device_options = "".join(
        '<option value="'
        + html.escape(str(item.get("serial") or ""), quote=True)
        + '"'
        + (" selected" if str(item.get("serial") or "") == selected_serial else "")
        + ">"
        + html.escape(
            str(item.get("configured_name") or item.get("device_model") or item.get("serial") or "GMC")
        )
        + "</option>"
        for item in devices
        if str(item.get("serial") or "")
    )
    history_rows: list[str] = []
    for item in store.list_calibration_history(limit=20):
        when = (
            datetime.fromtimestamp(int(item.get("timestamp_utc") or 0), UTC)
            .astimezone(timezone)
            .strftime("%Y-%m-%d %H:%M %Z")
        )
        changed = ", ".join(str(value) for value in item.get("changed_fields") or []) or t(
            "Profile saved"
        )
        history_rows.append(
            '<div class="calibration-history-row"><div><strong>'
            + html.escape(str(item.get("profile_id") or ""))
            + "</strong><small>"
            + html.escape(when)
            + " · "
            + html.escape(str(item.get("source") or ""))
            + "</small></div><span>"
            + html.escape(changed)
            + "</span></div>"
        )
    if not history_rows:
        history_rows.append(
            '<div class="note">'
            + html.escape(t("No calibration changes have been recorded yet."))
            + "</div>"
        )
    return f'''<section class="advanced-only calibration-management" id="calibration-management">
<div class="history-section-heading"><div><h2>{html.escape(t("Calibration profiles"))}</h2><p>{html.escape(t("Review predefined detector profiles, create device-specific profiles and audit every change."))}</p></div></div>
<div class="calibration-manager-grid"><div class="calibration-manager-card"><h3>{html.escape(t("Predefined profiles"))}</h3>{''.join(preset_rows)}</div><div class="calibration-manager-card"><h3>{html.escape(t("Custom profiles"))}</h3>{''.join(custom_rows)}</div></div>
<details class="analysis-group" id="calibration-wizard"><summary><span class="summary-copy">{html.escape(t("Calibration assistant"))}<small>{html.escape(t("Create a transparent custom calibration profile in four steps."))}</small></span></summary><div class="group-body">
<div class="calibration-wizard-steps"><span><b>1</b>{html.escape(t("Select device"))}</span><i>→</i><span><b>2</b>{html.escape(t("Confirm tube"))}</span><i>→</i><span><b>3</b>{html.escape(t("Apply calibration"))}</span><i>→</i><span><b>4</b>{html.escape(t("Done"))}</span></div>
<form method="post" action="?action=save-calibration-profile" class="calibration-profile-form calibration-dossier-form"><input type="hidden" name="calibration_csrf_token" value="{html.escape(csrf_token, quote=True)}"><h4 class="wide">{html.escape(t("Detector and calibration model"))}</h4><label>{html.escape(t("Device"))}<select name="device_serial">{device_options}</select></label><label>{html.escape(t("Profile ID"))}<input name="profile_id" required pattern="[A-Za-z0-9_-]+" placeholder="my_m4011_profile"></label><label>{html.escape(t("Profile name"))}<input name="display_name" required></label><label>{html.escape(t("Tube model"))}<input name="detector_type" required></label><label>{html.escape(t("CPM per µSv/h"))}<input name="cpm_per_usvh" type="number" min="0.001" step="0.001" required></label><label>{html.escape(t("Dead time"))} [µs]<input name="dead_time_us" type="number" min="0" step="0.1"></label><label>{html.escape(t("Maximum reliable CPM"))}<input name="reliable_max_cpm" type="number" min="1" step="1"></label><label>{html.escape(t("Dead-time model"))}<select name="dead_time_model"><option value="nonparalyzable">Non-Paralyzable</option><option value="none">{html.escape(t("None"))}</option></select></label><label>{html.escape(t("Conversion-factor uncertainty"))} [%]<input name="conversion_factor_uncertainty_percent" type="number" min="0" max="1000" step="0.01"></label><label>{html.escape(t("Calibration uncertainty"))} [%]<input name="calibration_uncertainty_percent" type="number" min="0" max="1000" step="0.01"></label><h4 class="wide">{html.escape(t("Calibration dossier and traceability"))}</h4><label>{html.escape(t("Calibration type"))}<select name="calibration_type"><option value="factory_undocumented">{html.escape(t("Factory state, not further documented"))}</option><option value="user_reference">{html.escape(t("User calibration with known reference"))}</option><option value="device_comparison">{html.escape(t("Comparison with another instrument"))}</option><option value="reference_atmosphere">{html.escape(t("Reference radiation field"))}</option><option value="traceable_laboratory">{html.escape(t("Traceable laboratory calibration"))}</option></select></label><label>{html.escape(t("Source"))}<select name="source"><option value="user">{html.escape(t("User"))}</option><option value="manufacturer">{html.escape(t("Manufacturer"))}</option><option value="laboratory">{html.escape(t("Laboratory"))}</option><option value="comparison">{html.escape(t("Device comparison"))}</option><option value="import">{html.escape(t("Import"))}</option></select></label><label>{html.escape(t("Device model"))}<input name="device_model" maxlength="120"></label><label>{html.escape(t("Device serial number"))}<input name="device_serial_number" maxlength="120"></label><label>{html.escape(t("Firmware version"))}<input name="firmware_version" maxlength="120"></label><label>{html.escape(t("Reference instrument or source"))}<input name="reference_device" maxlength="240"></label><label>{html.escape(t("Laboratory"))}<input name="laboratory" maxlength="240"></label><label>{html.escape(t("Accreditation"))}<input name="accreditation" maxlength="240"></label><label>{html.escape(t("Certificate number"))}<input name="certificate_number" maxlength="160"></label><label>{html.escape(t("Calibration date"))}<input name="calibration_date" type="date"></label><label>{html.escape(t("Valid until"))}<input name="valid_until" type="date"></label><label>{html.escape(t("Operator"))}<input name="operator_name" maxlength="160"></label><label class="wide">{html.escape(t("Measurement geometry"))}<textarea name="measurement_geometry" maxlength="1000"></textarea></label><label class="wide">{html.escape(t("Environmental conditions"))}<textarea name="environment_conditions" maxlength="1000"></textarea></label><label class="wide">{html.escape(t("Certificate SHA-256"))}<input name="certificate_sha256" pattern="[A-Fa-f0-9]{64}" maxlength="64" inputmode="text"></label><label class="wide">{html.escape(t("Comment"))}<textarea name="comment" maxlength="2000"></textarea></label><button class="primary wide" type="submit">+ {html.escape(t("New calibration"))}</button></form></div></details>
<details class="analysis-group" id="calibration-history"><summary><span class="summary-copy">{html.escape(t("Calibration history"))}<small>{html.escape(t("Date, changed values, source and comment"))}</small></span></summary><div class="group-body"><div class="calibration-history-list">{''.join(history_rows)}</div><div class="actions"><a class="button" href="./api/v1/calibration-history">{html.escape(t("Open calibration history JSON"))}</a><a class="button" href="./api/v1/calibration-profiles">{html.escape(t("Open calibration profiles JSON"))}</a></div></div></details>
</section>'''
