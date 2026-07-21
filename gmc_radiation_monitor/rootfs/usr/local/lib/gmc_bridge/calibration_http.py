from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .calibration_presets import PRESETS
from .history import HistoryStore
from .utils import slugify

Translate = Callable[[str], str]


def calibration_profiles_payload(store: HistoryStore) -> dict[str, Any]:
    return {
        "predefined": {
            key: {
                "profile_id": preset.profile_id,
                "display_name": preset.display_name,
                "dual_tube_mode": preset.dual_tube_mode,
                "tube_model": preset.tube_model,
                "cpm_per_usvh": preset.cpm_per_usvh,
                "dead_time_us": preset.dead_time_us,
                "reliable_max_cpm": preset.reliable_max_cpm,
                "dead_time_model": preset.dead_time_model,
                "high_dose_tube_model": preset.high_dose_tube_model,
                "high_dose_dead_time_us": preset.high_dose_dead_time_us,
                "calibration_source": preset.calibration_source,
            }
            for key, preset in PRESETS.items()
        },
        "custom": store.list_custom_calibration_profiles(),
    }


def calibration_history_payload(
    store: HistoryStore, *, device_serial: str | None
) -> dict[str, Any]:
    return {
        "history": store.list_calibration_history(device_serial=device_serial, limit=1000)
    }


def persist_calibration_profile(
    store: HistoryStore, data: dict[str, list[str]], *, translate: Translate
) -> None:
    profile_id = slugify((data.get("profile_id") or [""])[0]).replace("-", "_")
    display_name = (data.get("display_name") or [""])[0].strip()
    detector_type = (data.get("detector_type") or [""])[0].strip()
    device_serial = (data.get("device_serial") or [""])[0].strip() or None
    source = (data.get("source") or ["user"])[0].strip() or "user"
    comment = (data.get("comment") or [""])[0].strip()
    cpm_per_usvh = float((data.get("cpm_per_usvh") or ["0"])[0])
    dead_time_text = (data.get("dead_time_us") or [""])[0].strip()
    reliable_text = (data.get("reliable_max_cpm") or [""])[0].strip()
    dead_time_model = (data.get("dead_time_model") or ["none"])[0].strip()
    if not profile_id or not display_name or not detector_type or cpm_per_usvh <= 0:
        raise ValueError(
            translate("Profile ID, profile name, tube model and conversion factor are required")
        )
    if dead_time_model not in {"none", "nonparalyzable"}:
        raise ValueError(translate("Unsupported dead-time model"))
    values = {
        "tube_model": detector_type,
        "cpm_per_usvh": cpm_per_usvh,
        "dead_time_us": float(dead_time_text) if dead_time_text else None,
        "reliable_max_cpm": int(float(reliable_text)) if reliable_text else None,
        "dead_time_model": dead_time_model,
        "calibration_reference": comment,
        "calibration_status": "customized",
        "calibration_source": source,
    }
    store.save_custom_calibration_profile(
        profile_id=profile_id,
        display_name=display_name,
        detector_type=detector_type,
        values=values,
        source=source,
        comment=comment,
    )
    store.record_calibration_change(
        device_serial=device_serial,
        profile_id=profile_id,
        detector_type=detector_type,
        values=values,
        changed_fields=[key for key, value in values.items() if value not in (None, "")],
        source=source,
        comment=comment,
    )
    if not device_serial:
        return
    store.assign_custom_calibration_profile(
        device_serial=device_serial, profile_id=profile_id, values=values
    )
    store.upsert_device_registry(
        device_serial,
        {
            "detector_profile": profile_id,
            "tube_model": detector_type,
            "detector_type": detector_type,
            "cpm_per_usvh": cpm_per_usvh,
            "dead_time_us": values["dead_time_us"],
            "reliable_max_cpm": values["reliable_max_cpm"],
            "dead_time_model": dead_time_model,
            "calibration_status": "customized",
            "calibration_source": source,
            "calibration_reference": comment,
        },
    )
