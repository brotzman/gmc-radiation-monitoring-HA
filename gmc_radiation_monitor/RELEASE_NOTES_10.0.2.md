# GMC Radiation Monitor 10.0.2

Version 10.0.2 is a maintenance and stability release. It does not change database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, statistical algorithms or serial protocols.

## Responsive layout consolidation

- Replaces layered mobile follow-up patches with one documented responsive-layout contract.
- Navigation, dashboard actions and language selection wrap into one or two columns instead of scrolling horizontally.
- Status messages, device states, diagnostics and long unbroken technical values remain inside their cards.
- Analysis and long-term tables become labelled card rows on small screens.
- Calendar, calibration and workflow graphics scale or stack within the viewport.
- Retains responsive behaviour down to 320 px and at 200% text size without masking layout faults with a page-level sideways scroller.

## Web-module maintenance

- Moves status, cache and Home Assistant context handling into `report_web_status.py`.
- Moves device cards, live payloads and analysis rendering into `report_web_devices.py`.
- Reduces the central `report_web.py` module while preserving the existing `ReportApplication` interface and request handling.

## Translation maintenance

- Adds one canonical language registry shared by catalogue assembly and validation.
- Moves placeholder, missing-key and untranslated-fallback checks into a dedicated validation module.
- Stores the 10.0.1 wording additions once in `release_1001.json` instead of copying the same release block into eight language modules.
- Confirms identical key counts and valid placeholders in German, English, Spanish, French, Croatian, Italian, Dutch and Polish.

## Automated quality checks

- Adds `quality/run_quality_checks.py` for Python compilation, module-boundary, CSS-contract and translation checks.
- Adds a Chromium/Playwright regression test for 320, 360, 390, 430, 520, 620, 768 and 800 px at normal and 200% text size.
- The quality tools are maintenance assets and are not copied into the add-on runtime image.

## Compatibility

- Database schema remains version 8.
- Existing history, calibration profiles, device identities, reports and Home Assistant entities remain compatible.
- All long-term evidence rules and field-test diagnostics introduced in 10.0.1 remain unchanged.
