# GMC Radiation Monitor - Home Assistant App Repository

This repository contains the **GMC Radiation Monitor** Home Assistant App for local GQ GMC counter monitoring.
It is installed as a Home Assistant App/add-on repository; it is not a `custom_components` integration.
Measurements are published to Home Assistant through MQTT Discovery, while the local ingress dashboard provides live status, analysis, history, reports and maintenance tools.

Add this repository to Home Assistant, then install **GMC Radiation Monitor** from the App Store.

Current release: **10.0.6**, restoring a persistent sticky mobile navigation tile while preserving wrapped multi-row controls and preventing horizontal scrolling.


## Release quality checks

From the repository root, run:

```bash
python3 quality/run_quality_checks.py
```

The checks compile the runtime package, run 19 unit/integration tests, validate the canonical translation source, confirm the module-boundary contracts, run the compact responsive fixture and render the real application against a populated SQLite database in every interface language. Chromium is tested at 320-800 px and at 100%/200% text size. Playwright and Chromium are required for browser checks; use `--skip-browser` for compilation, translation and unit/integration checks only.
