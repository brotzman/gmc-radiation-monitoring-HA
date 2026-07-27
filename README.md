# GMC Radiation Monitor - Home Assistant App Repository

This repository contains the **GMC Radiation Monitor** Home Assistant App for local GQ GMC counter monitoring.
It is installed as a Home Assistant App/add-on repository; it is not a `custom_components` integration.
Measurements are published to Home Assistant through MQTT Discovery, while the local ingress dashboard provides live status, analysis, history, reports and maintenance tools.

Add this repository to Home Assistant, then install **GMC Radiation Monitor** from the App Store.

Current release: **10.0.2**, a maintenance release focused on responsive-layout reliability, clearer module boundaries and centrally validated translations.


## Release quality checks

From the repository root, run:

```bash
python3 quality/run_quality_checks.py
```

The checks compile the runtime package, validate all translation catalogues, confirm the split web-module architecture and test the mobile layout in Chromium at 320-800 px and 100%/200% text size. Playwright and Chromium are required for the browser check; use `--skip-browser` for the static checks only.
