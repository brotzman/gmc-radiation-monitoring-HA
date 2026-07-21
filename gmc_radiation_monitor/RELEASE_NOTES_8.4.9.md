# GMC Radiation Monitor 8.4.9

Version 8.4.9 is a small watchdog and service-observability maintenance release. It adds an independent bridge heartbeat and makes the health timing limits configurable. Database schema 8, detector calibration, dose conversion and measurement algorithms are unchanged.

- Adds an atomic bridge heartbeat file written by the automatic acquisition supervisor in `/data/gmc_bridge_heartbeat.json`.
- Records bridge state, update time, supervisor and child PIDs, configured and assigned device counts, and the last child exit status.
- Keeps the heartbeat current while the bridge is discovering devices, running, reconfiguring or restarting.
- Adds a dedicated `bridge_heartbeat` check to `/health`, separate from device connectivity and measurement freshness.
- Detects a crashed or stopped acquisition service even when the report server still answers normally.
- Distinguishes a live bridge with disconnected counters from a stale bridge process.
- Adds configurable startup, bridge-heartbeat and measurement-freshness thresholds under **System**.
- Validates threshold ranges and ordering and warns when limits are shorter than the heartbeat or device scan cadence.
- Exposes the effective health thresholds in the structured `/health` configuration check.
- Preserves HTTP 200 for healthy and warning states and HTTP 503 only for critical errors.
- Adds localized configuration labels and descriptions in all eight supported languages.
- Adds regression tests for atomic heartbeat writing, fresh and stale bridge states, threshold validation and runtime environment export.

Default timing values:

- Bridge heartbeat interval: 15 seconds
- Startup grace period: 900 seconds
- Bridge warning/error: 45 / 120 seconds
- Measurement warning/error: 600 / 1200 seconds

Existing 8.4.8 installations remain compatible. Missing new options use these conservative defaults automatically.

Compatibility safeguard retained from 8.4.3: the options migration still uses one structured JSON request instead of embedding arrays in shell-generated jq expressions. This prevents the former `jq: syntax error` and preserves Unicode strings such as `µSv/h`. No database schema or measurement algorithm changed.
