# GMC Radiation Monitor 8.4.7

Version 8.4.7 is a focused maintenance release for configuration validation, diagnostics and interface consistency. It does not change the database schema or radiation-measurement algorithms.

- Treats `devices` and `dual_tube_devices` as equal, independent physical-device lists during configuration validation.
- Accepts a GMC-500+ only under `dual_tube_devices`; it no longer has to be duplicated under `devices`.
- Requires at least one device across both lists and checks device-name uniqueness across both lists.
- Includes the concrete configuration problems in the self-test JSON instead of returning only a warning count.
- Reports pure warnings as `healthy: true`, `ok: true`, `status: "warning"`; only error checks mark the app unhealthy.
- Marks browser-local main-value sizing visibly and adds **Reset to app default**.
- Rebuilds the detector **Expert view** as a full-width disclosure panel with its plus/minus control in the top-right header, matching the other expandable cards.
- Removes installation-specific temperature and weather entity IDs from public defaults; the optional pressure hint is disabled until configured.
- Corrects release ownership in README/DOCS and documents the large-module split as planned version-9 architecture work.

Compatibility note: the 8.4.3 startup migration remains unchanged and continues to persist options through one structured JSON request to the Home Assistant Supervisor API. Arrays, quoted calibration references and Unicode units such as `µSv/h` remain protected from the former `jq: syntax error` failure mode.
No database schema or measurement algorithm changed.
