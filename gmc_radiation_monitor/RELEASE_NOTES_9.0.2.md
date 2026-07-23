# GMC Radiation Monitor 9.0.2

Version 9.0.2 is a focused usability, diagnostics and regression-hardening release for the 9.0 architecture.

## Improved

- Shows measurement freshness independently from serial connection state, including current, delayed, stale, reconnecting and no-data states.
- Labels dose rate explicitly as an estimate derived from CPM and displays the active conversion factor when available.
- Adds collapsible per-device connection diagnostics with response age, next scan, reconnect and serial-error counters.
- Adds report presets for today, yesterday, the last 24 hours, the last 7 days, the current month and custom ranges.
- Validates report dates before download, preserves entered values in the browser and provides actionable preview error codes.
- Breaks chart lines across missing-data intervals, marks gaps visually and adds reset-view and SVG-download controls.
- Adds a copy-safe support-diagnostics endpoint that omits credentials, precise locations and full serial numbers.
- Reduces repeated connection notifications and reports recovery only after a real state transition.
- Improves mobile touch targets, safe-area spacing, narrow-view layouts, reduced-motion behaviour and translation validation.

## Compatibility

- Keeps database schema 8 and existing history fully compatible.
- Does not change serial acquisition, detector profiles, calibration, CPM acceptance, dose conversion, statistical calculations or report metrology.
