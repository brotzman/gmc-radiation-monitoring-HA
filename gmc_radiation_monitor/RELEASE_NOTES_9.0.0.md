# GMC Radiation Monitor 9.0.0

Version 9.0.0 is a scientific, operational and architectural major release. It corrects the treatment of overlapping rolling CPM windows, introduces time-based coverage and time-weighted period statistics, modernises live updates and report creation, strengthens calibration traceability and separates dashboard assets and analytical interfaces into maintainable modules.

## Scientific and metrological changes

- Treats fast CPM polls as overlapping rolling one-minute windows and uses only conservatively independent windows for Poisson counting uncertainty, significance and level-shift calculations.
- Adds gap-aware time-weighted CPM means, temporal coverage, covered duration and uncovered duration for reports, history exploration and dose-rate summaries.
- Keeps descriptive distribution statistics sample based while clearly separating them from time-weighted period estimates.
- Defines GMCMap ACPM as a time-weighted rolling 60-minute value that does not bridge long gaps and no longer depends on process uptime.
- Adds a complete calibration dossier with instrument identity, firmware, calibration type, laboratory, accreditation, certificate, dates, geometry, environmental conditions, operator and certificate SHA-256.

## Reliability and performance

- Replaces repeated full-history baseline scans with a seeded rolling in-memory baseline cache.
- Adds rate-limited diagnostic counters for recoverable bridge, heartbeat and baseline failures.
- Keeps bridge health, device connectivity and measurement freshness independently observable.

## Dashboard and reports

- Replaces full device-card HTML refreshes with a small JSON live-data endpoint, DOM field updates, retry backoff and a visible interruption status.
- Adds a unified custom-report form with remembered settings and a live preview of selected period, sample count, temporal coverage and data gaps.
- Improves help-popover semantics, Escape handling, focus restoration, reduced-motion support, forced-colour behaviour and narrow-screen layouts.
- Preserves the floating dashboard navigation as a compact sticky control on mobile devices.
- Constrains date, ISO-week, month and date-time inputs to their report cards on narrow screens.

## Architecture and localisation

- Moves dashboard CSS and JavaScript out of Python string literals into versioned static assets.
- Adds dedicated time-series, report-statistics, baseline-cache, runtime-diagnostics and stable interface modules.
- Extends translation validation to detect likely untranslated user-facing strings while allowing technical notation.
- Updates all eight bundled manuals to version 9.0.0 and documents the changed statistical interpretation.

Database schema 8 remains compatible. Existing history is retained without conversion.
