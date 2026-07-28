#!/usr/bin/env python3
"""Browser regression check for horizontal overflow in Home Assistant views."""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

VIEWPORT_WIDTHS = (320, 360, 390, 430, 520, 620, 768, 800)

FIXTURE_BODY = r'''
<div class="page-scroll"><main>
<header class="report-header">
  <div class="header-topline">
    <div class="header-intro"><h1>GMC Radiation Monitor responsive regression</h1><p>Sehr lange mobile Überschrift und Beschreibung für die Überprüfung der Darstellung.</p></div>
    <div class="header-tools"><div class="analysis-select-group"><label class="analysis-select-label"><span class="visually-hidden">Ansicht</span><span class="analysis-select-control"><span class="analysis-select-icon" aria-hidden="true">▤</span><select id="analysis-level-select" aria-label="Ansicht"><option>◉ Zusammenfassung</option><option selected>▤ Analyse</option><option>∑ Experte</option></select></span></label><small class="header-select-description">Detaillierte Interpretation und die wichtigsten unterstützenden Werte</small></div><form class="language-select-form"><label class="language-select-label"><span class="visually-hidden">Sprache</span><span class="language-select-control"><span class="language-select-icon" aria-hidden="true">🌐</span><select id="language-select" aria-label="Sprache"><option>Automatisch</option><option selected>Deutsch</option><option>English</option></select></span></label></form><a class="header-status-badge warning"><span class="header-status-symbol">🟡</span><span class="header-status-text">1/2 verbunden</span></a><button class="header-tool-button reload-button" id="reload-dashboard" aria-label="Seite aktualisieren" title="Seite aktualisieren"><span class="header-tool-icon">↻</span><span class="header-tool-label visually-hidden">Aktualisieren</span></button></div>
  </div>
</header>
<nav class="dashboard-controls" id="dashboard-controls">
  <div class="desktop-dashboard-navigation"><div class="jump-links"><a>Geräte</a><a>Intelligenz</a><a>Analyse</a><a>Langzeit</a><a>Verlauf</a></div><details class="navigation-menu"><summary>Mehr</summary></details></div>
  <div class="mobile-dashboard-navigation"><details class="navigation-menu sections-navigation-menu"><summary>☰ Bereiche</summary><div class="mobile-navigation-sheet"><strong>Übersicht</strong><a>Geräte</a><a>Intelligenz</a><strong>Auswertung</strong><a>Analyse</a><a>Langzeit</a><a>Verlauf</a></div></details><span class="current-section-label">Analyse</span><button class="back-to-top-button">⌃</button></div>
</nav>
<section><div class="device-card"><div class="device-card-header"><div class="device-card-title"><div class="device-card-icon">GMC-500+</div><div class="device-card-title-copy"><h3>GMC-500+ - Wohnzimmer und Messstation</h3><small>USB-/dev/serial/by-id/außergewöhnlich-lange-serielle-gerätekennung</small></div></div><div class="device-status-stack"><span class="device-status waiting">Verbindung wird hergestellt und Messdaten werden validiert</span><span class="device-freshness freshness-warning">Letzter Messwert ist älter als erwartet und wird erneut geprüft</span></div></div><div class="live-refresh-status" data-state="warning">Die Live-Aktualisierung ist vorübergehend verzögert: außergewöhnlichLangeFehlerkennungOhneTrennzeichen012345678901234567890123456789.</div><div class="device-alert warning"><strong>Statusmeldung</strong><small>Diese Meldung muss vollständig innerhalb des Kartenrandes bleiben und darf nicht horizontal abgeschnitten werden.</small></div></div></section>
<section><div class="status-summary"><div class="status-item yellow"><strong>Datenbankstatus</strong><span class="status-value">Wiederherstellung erforderlich</span><small>Sehr lange ergänzende Statusmeldung.</small></div><div class="status-item blue"><strong>Gerätestatus</strong><span class="status-value">Verbindung wird hergestellt</span></div></div></section>
<section><div class="table-wrap"><table><thead><tr><th>Messzeitpunkt</th><th>Status und Interpretation</th><th>Technischer Wert</th></tr></thead><tbody><tr><td data-label="Messzeitpunkt">26.07.2026 21:45:00</td><td data-label="Status und Interpretation">Außergewöhnlich lange Statusbeschreibung, die auf Mobilgeräten zweizeilig oder mehrzeilig erscheinen soll.</td><td data-label="Technischer Wert">UngewöhnlichLangerTechnischerWertOhneLeerzeichen012345678901234567890123456789</td></tr></tbody></table></div></section>
<section><div class="table-scroll long-term-table-wrap"><table class="long-term-table"><thead><tr><th>Monat</th><th>Mittelwert CPM</th><th>Abgeleitete Dosis</th></tr></thead><tbody><tr><td data-label="Monat">2026-07</td><td data-label="Mittelwert CPM">123,45</td><td data-label="Abgeleitete Dosis (µSv)">12,345</td></tr></tbody></table></div></section>
<section><div class="calendar-scroll"><div class="calendar-grid" id="calendar"></div></div></section>
<section><div class="calibration-wizard"><div class="step">Schritt 1 mit langem Text</div><span class="arrow">→</span><div class="step">Schritt 2 mit langem Text</div><span class="arrow">→</span><div class="step">Schritt 3 mit langem Text</div></div></section>
</main></div>
<script>for(let i=0;i<366;i++){const s=document.createElement('span');s.className='calendar-cell level-'+(i%5);document.getElementById('calendar').appendChild(s)}</script>
'''


def _fixture(css_path: Path) -> str:
    css = css_path.read_text(encoding="utf-8")
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>{css}</style></head><body>{FIXTURE_BODY}</body></html>'''


def run(css_path: Path, *, chromium_path: str | None = None) -> list[dict[str, object]]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Playwright is required: python -m pip install playwright") from exc

    executable = chromium_path or shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not executable:
        raise SystemExit("Chromium was not found. Set CHROMIUM_PATH or pass --chromium.")

    failures: list[dict[str, object]] = []
    fixture = _fixture(css_path)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=executable, headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        for zoom in (1, 2):
            for width in VIEWPORT_WIDTHS:
                page.set_viewport_size({"width": width, "height": 1000})
                page.set_content(fixture, wait_until="load")
                if zoom == 2:
                    page.add_style_tag(content="html{font-size:200%!important}")
                result = page.evaluate(
                    """async () => {
                      const viewport = window.innerWidth;
                      const pageScroll = document.querySelector('.page-scroll');
                      const selectors = ['main','header','section','.dashboard-controls','.mobile-dashboard-navigation','.header-topline','.header-tools','.analysis-select-group','.analysis-select-label','.language-select-form','.language-select-label','.header-status-badge','.device-card','.table-wrap','.long-term-table-wrap','.calendar-scroll','.calibration-wizard'];
                      const outside = [];
                      for (const selector of selectors) {
                        for (const node of document.querySelectorAll(selector)) {
                          const box = node.getBoundingClientRect();
                          if (box.left < -0.51 || box.right > viewport + 0.51) outside.push({selector,left:box.left,right:box.right});
                        }
                      }
                      const status = document.querySelector('.device-status');
                      const tableCell = document.querySelector('.table-wrap td');
                      const dashboard = document.querySelector('.dashboard-controls');
                      const mobileNavigation = document.querySelector('.mobile-dashboard-navigation');
                      const dashboardStyle = getComputedStyle(dashboard);
                      const mobileNavigationStyle = getComputedStyle(mobileNavigation);
                      pageScroll.scrollTop = Math.min(dashboard.offsetTop + dashboard.offsetHeight + 240, Math.max(0, pageScroll.scrollHeight - pageScroll.clientHeight));
                      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
                      const dashboardBox = dashboard.getBoundingClientRect();
                      const pageBox = pageScroll.getBoundingClientRect();
                      const pagePaddingTop = parseFloat(getComputedStyle(pageScroll).paddingTop) || 0;
                      return {
                        viewport,
                        documentWidth: document.documentElement.scrollWidth,
                        bodyWidth: document.body.scrollWidth,
                        pageClientWidth: pageScroll.clientWidth,
                        pageScrollWidth: pageScroll.scrollWidth,
                        outside,
                        statusWhiteSpace: getComputedStyle(status).whiteSpace,
                        tableCellDisplay: getComputedStyle(tableCell).display,
                        tableCellColumns: getComputedStyle(tableCell).gridTemplateColumns,
                        dashboardPosition: dashboardStyle.position,
                        dashboardDisplay: dashboardStyle.display,
                        dashboardOverflowX: dashboardStyle.overflowX,
                        dashboardTop: dashboardBox.top,
                        pageTop: pageBox.top,
                        pagePaddingTop,
                        dashboardLeft: dashboardBox.left,
                        dashboardRight: dashboardBox.right,
                        mobileNavigationColumns: mobileNavigationStyle.gridTemplateColumns.split(' ').filter(Boolean).length
                      };
                    }"""
                )
                ok = (
                    result["documentWidth"] <= width
                    and result["bodyWidth"] <= width
                    and result["pageScrollWidth"] <= result["pageClientWidth"]
                    and not result["outside"]
                    and result["statusWhiteSpace"] == "normal"
                    and result["tableCellDisplay"] == "grid"
                    and result["dashboardPosition"] == "sticky"
                    and result["dashboardDisplay"] == "block"
                    and result["dashboardOverflowX"] in {"visible", "clip", "hidden"}
                    and 5 <= result["dashboardTop"] - (result["pageTop"] + result["pagePaddingTop"]) <= 16
                    and result["dashboardLeft"] >= -1
                    and result["dashboardRight"] <= width + 1
                    and result["mobileNavigationColumns"] == 3
                )
                if not ok:
                    failures.append({"width": width, "zoom": zoom, **result})
        browser.close()
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--css", type=Path, required=True)
    parser.add_argument("--chromium")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    failures = run(args.css, chromium_path=args.chromium)
    if args.json:
        print(json.dumps({"ok": not failures, "failures": failures}, ensure_ascii=False, indent=2))
    elif failures:
        print(f"Mobile layout regression failed in {len(failures)} viewport/zoom combinations")
        for failure in failures[:8]:
            print(failure)
    else:
        print(f"Mobile layout regression passed for {len(VIEWPORT_WIDTHS)} widths at 100% and 200% text size")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
