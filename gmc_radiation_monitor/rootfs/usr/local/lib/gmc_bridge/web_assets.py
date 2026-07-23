from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol


class TranslatorLike(Protocol):
    def __call__(self, text: str, **values: object) -> str: ...


_ASSET_DIR = Path(__file__).with_name("static")
DASHBOARD_CSS = (_ASSET_DIR / "dashboard.css").read_text(encoding="utf-8")
DASHBOARD_JS = (_ASSET_DIR / "dashboard.js").read_text(encoding="utf-8")


def dashboard_bootstrap_payload(
    *, selected_serial: str, language: str, translator: TranslatorLike
) -> dict[str, object]:
    t = translator
    return {
        "analysisDevice": selected_serial,
        "language": language,
        "liveRefreshInterrupted": t("Live update interrupted; retrying automatically."),
        "uiText": {
            "previewing": t("Inspecting backup…"),
            "previewFailed": t("Backup preview failed"),
            "noFile": t("Select a SQLite backup file first."),
            "measurements": t("Measurements"),
            "rawMeasurements": t("Raw-data archive"),
            "annotations": t("Annotations"),
            "devices": t("Devices"),
            "dataPeriod": t("Data period"),
            "schema": t("Schema"),
            "fileSize": t("File size"),
            "integrity": t("Integrity"),
            "noData": t("No data"),
            "backupReady": t("Backup is compatible and ready to restore."),
            "expandAll": t("Expand all"),
            "collapseAll": t("Collapse all"),
            "reportEndBeforeStart": t("The end date must not be before the start date."),
            "completeRequiredFields": t("Complete the required period fields."),
            "reportPreviewFailed": t("The report preview could not be created."),
            "errorCode": t("Error code"),
            "preparingDownload": t("Preparing…"),
            "reportInputsPreserved": t("The selected settings are saved in this browser."),
            "diagnosticsCopied": t("Support diagnostics copied."),
            "copyFailed": t("Copy failed"),
        },
    }


def render_dashboard_bootstrap(
    *, selected_serial: str, language: str, translator: TranslatorLike
) -> str:
    payload = dashboard_bootstrap_payload(
        selected_serial=selected_serial, language=language, translator=translator
    )
    return "window.GMC_BOOTSTRAP=" + json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).replace("</", "<\\/") + ";"


def render_dashboard_script(
    *, selected_serial: str, language: str, translator: TranslatorLike
) -> str:
    """Compatibility helper used by tests and non-HTML integrations."""
    return render_dashboard_bootstrap(
        selected_serial=selected_serial, language=language, translator=translator
    ) + "\n" + DASHBOARD_JS


def read_dashboard_asset(name: str) -> bytes:
    if name not in {"dashboard.css", "dashboard.js"}:
        raise FileNotFoundError(name)
    return (_ASSET_DIR / name).read_bytes()
