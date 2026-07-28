#!/usr/bin/env python3
"""Render the real application with realistic data and test it in Chromium."""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
import tempfile
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

VIEWPORT_WIDTHS = (320, 360, 390, 430, 520, 620, 768, 800)
LANGUAGES = ("en", "de", "fr", "es", "it", "nl", "pl", "hr")


def _seed_store(store: Any) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    devices = (
        (
            "SERIAL-EXTREM-LANG-00000000000000000001",
            "GMC-500+ Wohnzimmer und Langzeit-Messstation mit ausführlicher Bezeichnung",
            "/dev/serial/by-id/usb-GQ_Electronics_GMC-500Plus_außergewöhnlich-lange-gerätekennung-0001",
            48,
        ),
        (
            "SERIAL-BETA-0002",
            "GMC-600+ Außenmesspunkt",
            "/dev/ttyUSB1",
            74,
        ),
    )
    for serial, name, port, baseline in devices:
        store.upsert_device_registry(
            serial,
            {
                "device_model": name,
                "device_profile": "gmc_500" if "500" in name else "gmc_600",
                "device_profile_name": name,
                "port": port,
                "runtime_online": True,
                "runtime_status": "online",
                "runtime_status_reason": "measurement_active_with_a_very_long_machine_readable_status_identifier",
                "runtime_status_updated_utc": now.isoformat().replace("+00:00", "Z"),
                "scan_interval_seconds": 300,
                "configured_name": name,
                "configured_baudrate": 115200,
                "configured_scan_interval_seconds": 300,
                "configured_cpm_per_usvh": 154.0,
                "hardware_model": name,
                "firmware_version": "GMC-500+Re 2.42",
                "last_seen_utc": now.isoformat().replace("+00:00", "Z"),
            },
        )
        # Seven days at five-minute cadence provides populated live, history,
        # daily and comparison views without creating an oversized test fixture.
        start = now - timedelta(days=7)
        for index in range(7 * 24 * 12):
            timestamp = int((start + timedelta(minutes=5 * index)).timestamp())
            daily_wave = 6.0 * math.sin(index / 47.0)
            cpm = max(1, round(baseline + daily_wave + (index % 9) / 3))
            if index in {730, 731, 732} and serial.endswith("0002"):
                cpm += 120
            sample = {
                "cpm": cpm,
                "temperature_c": 19.0 + 4.0 * math.sin(index / 150.0),
                "voltage_v": 3.15 - (index % 250) / 10000.0,
                "pressure_hpa": 1008.0 + 7.0 * math.sin(index / 210.0),
                "raw_cpm": float(cpm),
                "corrected_cpm": float(cpm) * 1.002,
                "detector_type": "M4011",
                "dual_tube_mode": "single",
                "active_tube": "primary",
                "dead_time_model": "nonparalyzable",
                "dead_time_us": 190.0,
                "dead_time_loss_percent": 0.2,
                "detector_load_percent": 0.15,
                "correction_factor": 1.002,
                "calibration_status": "working_values",
                "calibration_source": "predefined",
                "measurement_quality_index": 92,
                "dose_quality": "high",
                "derived_dose_usvh": cpm / 154.0,
            }
            store.insert_measurement(
                sample,
                device_serial=serial,
                timestamp_utc=timestamp,
                expected_interval_seconds=300,
            )
        store.insert_operational_event(
            {
                "timestamp_utc": int((now - timedelta(hours=3)).timestamp()),
                "event_type": "serial_reconnect",
                "severity": "warning",
                "cpm": baseline,
                "details": {
                    "reason": "simulated exceptionally long reconnect diagnostic message for responsive testing"
                },
            },
            device_serial=serial,
        )
    store.set_metadata(
        {
            "serial": devices[0][0],
            "device_model": devices[0][1],
            "device_profile": "gmc_500",
            "device_profile_name": devices[0][1],
        }
    )
    start = int((now - timedelta(hours=8)).timestamp())
    store.add_event_annotation(
        device_serial=devices[0][0],
        start_timestamp_utc=start,
        end_timestamp_utc=start + 3600,
        category="environment",
        status="confirmed",
        note="Sehr lange bestätigte Umgebungsnotiz, die auf schmalen Displays vollständig umbrechen muss.",
    )


def _render_pages(package_root: Path) -> tuple[dict[str, str], str]:
    library = package_root / "gmc_radiation_monitor/rootfs/usr/local/lib"
    sys.path.insert(0, str(library))
    from gmc_bridge.history import HistoryStore
    from gmc_bridge.report_web import ReportApplication

    with tempfile.TemporaryDirectory(prefix="gmc-e2e-") as directory:
        store = HistoryStore(Path(directory) / "history.sqlite3", retention_days=3650)
        _seed_store(store)
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=300,
            read_gyro=True,
            cpm_per_usvh=154.0,
            ui_mode="advanced",
            ui_language="de",
            history_management_enabled=True,
            started_at_utc=int(time.time()) - 7200,
            options_path=Path(directory) / "options.json",
        )
        pages = {
            language: app.render_index(
                mode_override="advanced",
                language_override=language,
                accept_language=language,
            ).decode("utf-8")
            for language in LANGUAGES
        }
        # Verify the application APIs are also backed by the populated store.
        live = app.live_devices_payload(language_override="de", accept_language="de")
        if len(live.get("devices", [])) != 2:
            raise AssertionError(f"Expected two live devices, got {len(live.get('devices', []))}")
        status = app.status()
        if int(status.get("measurements") or 0) < 4000:
            raise AssertionError("The full-app fixture did not populate enough measurements")
    css = (library / "gmc_bridge/static/dashboard.css").read_text(encoding="utf-8")
    javascript = (library / "gmc_bridge/static/dashboard.js").read_text(encoding="utf-8")
    return pages, css, javascript


def _inspect(page: Any, width: int, zoom: int) -> dict[str, Any]:
    page.set_viewport_size({"width": width, "height": 1100})
    if zoom == 2:
        page.add_style_tag(content="html{font-size:200%!important}")
    page.wait_for_timeout(20)
    return page.evaluate(
        """async () => {
          const viewport = window.innerWidth;
          const root = document.documentElement;
          const body = document.body;
          const offenders = [];
          for (const node of document.querySelectorAll('body *')) {
            const style = getComputedStyle(node);
            if (style.position === 'fixed' || style.position === 'absolute') continue;
            const box = node.getBoundingClientRect();
            if (box.width > 0 && (box.left < -1 || box.right > viewport + 1)) {
              offenders.push({tag:node.tagName, cls:String(node.className || '').slice(0,100), left:box.left, right:box.right, text:(node.textContent || '').trim().slice(0,100)});
              if (offenders.length >= 12) break;
            }
          }
          const horizontalScrollers = [];
          for (const node of document.querySelectorAll('main,section,article,nav,header,.device-card,.table-wrap,.table-scroll,.calendar-scroll')) {
            if (node.scrollWidth > node.clientWidth + 1) {
              horizontalScrollers.push({tag:node.tagName, cls:String(node.className || '').slice(0,100), client:node.clientWidth, scroll:node.scrollWidth});
              if (horizontalScrollers.length >= 12) break;
            }
          }
          const scroller = document.querySelector('.page-scroll');
          const languageSelect = document.querySelector('#language-select');
          const sectionSelect = document.querySelector('#section-select');
          const sectionFloatingNavigation = document.querySelector('#section-floating-navigation');
          const statusColumn = document.querySelector('.header-status-column');
          const statusBadge = document.querySelector('#header-status-badge');
          const analysisSelect = document.querySelector('#analysis-level-select');
          const reloadButton = document.querySelector('#reload-dashboard');
          const headerTools = document.querySelector('.header-tools');
          const statusColumnBox = statusColumn ? statusColumn.getBoundingClientRect() : null;
          const statusBadgeBox = statusBadge ? statusBadge.getBoundingClientRect() : null;
          const sectionSelectBox = sectionSelect ? sectionSelect.getBoundingClientRect() : null;
          const sectionSelectedInitial = sectionSelect ? sectionSelect.value : '';
          const sectionInitiallyFloating = Boolean(sectionFloatingNavigation?.classList.contains('is-floating'));
          if (scroller) {
            const scrollerBox = scroller.getBoundingClientRect();
            const slot = document.querySelector('#section-navigation-slot');
            const slotBoxBeforeScroll = slot ? slot.getBoundingClientRect() : null;
            const targetScroll = slotBoxBeforeScroll
              ? scroller.scrollTop + slotBoxBeforeScroll.top - scrollerBox.top + 96
              : Math.max(900, scroller.clientHeight);
            scroller.scrollTop = Math.min(targetScroll, Math.max(0, scroller.scrollHeight - scroller.clientHeight));
            await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
            await new Promise((resolve) => setTimeout(resolve, 25));
          }
          const sectionFloatingAfterScroll = Boolean(sectionFloatingNavigation?.classList.contains('is-floating'));
          const sectionFloatingPosition = sectionFloatingNavigation ? getComputedStyle(sectionFloatingNavigation).position : '';
          const statusPositionAfterScroll = statusBadge ? getComputedStyle(statusBadge).position : '';
          const analysisPositionAfterScroll = analysisSelect ? getComputedStyle(analysisSelect).position : '';
          const languagePositionAfterScroll = languageSelect ? getComputedStyle(languageSelect).position : '';
          const reloadPositionAfterScroll = reloadButton ? getComputedStyle(reloadButton).position : '';
          return {
            viewport,
            documentWidth: root.scrollWidth,
            bodyWidth: body.scrollWidth,
            offenders,
            horizontalScrollers,
            title: document.title,
            deviceCards: document.querySelectorAll('.device-card').length,
            tables: document.querySelectorAll('table').length,
            sectionSelectPresent: Boolean(sectionSelect),
            sectionSelected: sectionSelectedInitial,
            sectionInitiallyFloating,
            sectionFloatingAfterScroll,
            sectionFloatingPosition,
            statusPositionAfterScroll,
            analysisPositionAfterScroll,
            languagePositionAfterScroll,
            reloadPositionAfterScroll,
            sectionBelowStatus: Boolean(statusBadgeBox && sectionSelectBox && sectionSelectBox.top >= statusBadgeBox.bottom - 1),
            sectionWithinStatusColumn: Boolean(statusColumnBox && sectionSelectBox && sectionSelectBox.left >= statusColumnBox.left - 1 && sectionSelectBox.right <= statusColumnBox.right + 1),
            languageSelectPresent: Boolean(languageSelect),
            languageSelected: languageSelect ? languageSelect.value : '',
            reloadButtonPresent: Boolean(reloadButton),
            headerToolsWidth: headerTools ? headerTools.scrollWidth : 0,
            headerToolsClientWidth: headerTools ? headerTools.clientWidth : 0
          };
        }"""
    )


def run(package_root: Path, *, chromium_path: str | None = None) -> list[dict[str, Any]]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Playwright is required: python -m pip install playwright") from exc
    executable = chromium_path or shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not executable:
        raise SystemExit("Chromium was not found. Set CHROMIUM_PATH or pass --chromium.")

    pages, css, javascript = _render_pages(package_root)
    failures: list[dict[str, Any]] = []
    checks: list[tuple[str, int, int]] = []
    for zoom in (1, 2):
        checks.extend(("de", width, zoom) for width in VIEWPORT_WIDTHS)
        checks.extend((language, 320, zoom) for language in LANGUAGES if language != "de")
        checks.extend((language, 390, zoom) for language in LANGUAGES if language != "de")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=executable, headless=True, args=["--no-sandbox"])
        browser_page = browser.new_page()
        styled_pages = {}
        for language, document in pages.items():
            styled = re.sub(
                r'<link rel="stylesheet" href="\./assets/dashboard\.css\?v=[^"]+">',
                lambda _match: f"<style>{css}</style>",
                document,
                count=1,
            )
            styled = re.sub(
                r'<script src="\./assets/dashboard\.js\?v=[^"]+" defer></script>',
                lambda _match: f"<script>{javascript}</script>",
                styled,
                count=1,
            )
            styled_pages[language] = styled
        for language, width, zoom in checks:
            browser_page.set_content(styled_pages[language], wait_until="domcontentloaded")
            result = _inspect(browser_page, width, zoom)
            ok = (
                result["documentWidth"] <= width + 1
                and result["bodyWidth"] <= width + 1
                and not result["offenders"]
                and not result["horizontalScrollers"]
                and result["deviceCards"] >= 2
                and result["tables"] >= 1
                and result["sectionSelectPresent"]
                and result["sectionSelected"] == "devices"
                and not result["sectionInitiallyFloating"]
                and result["sectionFloatingAfterScroll"]
                and result["sectionFloatingPosition"] == "fixed"
                and result["statusPositionAfterScroll"] != "fixed"
                and result["analysisPositionAfterScroll"] != "fixed"
                and result["languagePositionAfterScroll"] != "fixed"
                and result["reloadPositionAfterScroll"] != "fixed"
                and result["sectionBelowStatus"]
                and result["sectionWithinStatusColumn"]
                and result["languageSelectPresent"]
                and result["languageSelected"] == language
                and result["reloadButtonPresent"]
                and result["headerToolsWidth"] <= result["headerToolsClientWidth"] + 1
            )
            if not ok:
                failures.append({"language": language, "width": width, "zoom": zoom, **result})
        browser.close()
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--chromium")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    failures = run(args.package_root.resolve(), chromium_path=args.chromium)
    if args.json:
        print(json.dumps({"ok": not failures, "failures": failures}, ensure_ascii=False, indent=2))
    elif failures:
        print(f"Full application E2E failed in {len(failures)} combinations")
        for failure in failures[:6]:
            print(json.dumps(failure, ensure_ascii=False))
    else:
        print("Full application E2E passed with populated SQLite history in all languages and responsive viewports")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
