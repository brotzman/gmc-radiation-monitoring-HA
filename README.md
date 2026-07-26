# GMC Radiation Monitor - Home Assistant App Repository

This repository contains the **GMC Radiation Monitor** Home Assistant App for local GQ GMC counter monitoring.
It is installed as a Home Assistant App/add-on repository; it is not a `custom_components` integration.
Measurements are published to Home Assistant through MQTT Discovery, while the local ingress dashboard provides live status, analysis, history, reports and maintenance tools.

Add this repository to Home Assistant, then install **GMC Radiation Monitor** from the App Store.

Current release: **10.0.0**, with evidence-led long-term analysis, conservative interpretation thresholds and exportable endurance diagnostics.


## Development test suite

From the repository root, run:

```bash
python3 -m pytest
```

The root test configuration resolves the add-on package path and keeps legacy path-based tests anchored to the add-on directory, so test results do not depend on execution order.
