# GMC Radiation Monitor 8.4.8

Version 8.4.8 is a focused health-monitoring and expert-interface maintenance release. No database schema or measurement algorithm changed; detector factors and stored measurements also remain unchanged.

- Replaces the unconditional plain-text `/health` response with a real JSON health assessment.
- Returns HTTP 200 for healthy and warning states, and HTTP 503 only for critical errors.
- Checks report/measurement service uptime, SQLite integrity, schema version, configuration validity, device connectivity, measurement freshness and available storage.
- Applies startup and reconnect grace periods so transient device states remain warnings instead of causing immediate watchdog restarts.
- Uses one shared configuration validator for runtime option loading, the dashboard editor, self-tests, health checks and migrated options.
- Distinguishes validation warnings from errors and returns structured issue codes, paths and messages.
- Replaces the nested detector **Expert view** disclosure with an always-visible **Measurement details** block when the app-wide Expert level is selected.
- Removes the redundant plus/minus control and duplicate “Expert view” heading from that block.
- Keeps raw CPM, corrected CPM, dead-time loss, correction factor and measurement quality aligned in the full-width responsive layout.
- Adds localized “Measurement details” wording for all eight supported interface languages.
- Adds release-specific regression tests for health JSON, HTTP 503 critical states, shared validation and the non-collapsible expert measurement block.
- Retains the structured JSON request migration from 8.4.3, which avoided the former `jq: syntax error` and safely preserves strings such as `µSv/h`.

Compatibility note: warnings remain operational (`healthy: true`, `ok: true`, `status: "warning"`). Only checks with `status: "error"` make the watchdog endpoint return HTTP 503. Existing 8.4.7 browser display settings and configuration remain compatible.
