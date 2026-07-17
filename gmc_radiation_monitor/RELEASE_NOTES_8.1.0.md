# Version 8.1.0

Version 8.1.0 is a feature release that adds explicit statistical significance, confidence and historical rarity assessment while retaining the source-build installation reliability of 8.0.14.

## Fixed

- Removed the mandatory `image: ghcr.io/brotzman/gmc-radiation-monitor` setting from `config.yaml`.
- Home Assistant now builds the app directly from the included Dockerfile instead of requiring anonymous access to a pre-published GHCR package.
- This prevents installation failures with `error from registry: denied` when the package does not exist yet, is private or has not been made publicly readable.
- Replaced the registry-publishing workflow with a source-build verification workflow for `amd64` and `aarch64`.
- Added release checks that reject an accidental mandatory external image dependency.

## Compatibility

Measurements, serial communication, SQLite history, MQTT Discovery, Ingress routes, dashboard behavior, configuration options and stored data remain unchanged.

## Distribution note

The repository remains a standard Home Assistant App repository. A public multi-architecture registry image can be added again later, but only after the package has been published successfully and explicitly made public. The source-build distribution does not require GitHub Container Registry credentials.

## Statistical analysis enhancement

This build of 8.1.0 adds an explicit statistical assessment of recent changes:

- comparison of the latest quality-filtered one-hour count rate with earlier baseline history;
- Poisson rate-difference significance in sigma and as a two-sided probability;
- confidence reduced automatically when recent data quality is limited;
- empirical percentile and an approximate “once in N historical hours” rarity indicator;
- integration into the explainable intelligence result.

The result remains a statistical aid. It does not identify a physical cause and does not replace radiation-protection guidance or calibrated instrumentation. Existing traffic-light thresholds and alarms are unchanged.
