# GMC Radiation Monitor 10.0.3

Version 10.0.3 is a verification and maintainability release. It does not change database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, scientific algorithms or serial protocols.

## Measurement and integration tests

- Adds 17 standard-library unit and integration tests.
- Verifies nonparalyzable dead-time correction and saturation handling.
- Verifies gap-aware dose integration and dual-tube range selection.
- Verifies adaptive high-CPM confirmation and legacy-spike seed cleanup.
- Verifies database migrations, history round trips and ingest diagnostics.
- Verifies daylight-saving-aware report periods.
- Simulates optional serial-channel failures while preserving a valid CPM sample.
- Simulates retained MQTT state and channel-availability synchronization without a broker.

## Populated full-application browser test

- Builds a temporary schema-8 SQLite database with two connected devices, more than 4,000 measurements, events, annotations and deliberately long identifiers.
- Renders the real advanced `ReportApplication` rather than a component-only fixture.
- Checks all eight interface languages at 320 and 390 px with normal and 200% text size.
- Checks the complete German dashboard at 320, 360, 390, 430, 520, 620, 768 and 800 px at both text-size levels.
- Rejects document overflow, component overflow and nested horizontal scrollers.
- Corrects the custom-report download action, analysis-level controls, assessment cards, header resources and report-format/action grids uncovered by this test.

## Single translation source

- Stores the fully assembled runtime translations in `i18n/catalogs.json`.
- Removes the eight generated Python language modules and release-specific override files from the runtime source tree.
- Retains deterministic key, placeholder, empty-value and untranslated-fallback validation.

## Further module boundaries

- Moves report period resolution and timezone handling to `report_periods.py`.
- Moves `HistoryRow` and timestamp coercion to `history_models.py`.
- Moves live detector metrology enrichment to `service_metrology.py`.
- Preserves the previous imports exposed by `reports.py`, `history.py` and `service.py`.

## Quality command

Run from the repository root:

```bash
python3 quality/run_quality_checks.py
```

Use `--skip-browser` when Chromium/Playwright are unavailable.

## Compatibility

- Database schema remains version 8.
- Existing history, calibration profiles, device identities, reports and Home Assistant entities remain compatible.
- Measurement acquisition, safety thresholds and long-term evidence rules remain unchanged.
