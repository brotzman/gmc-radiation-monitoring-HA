# GMC Radiation Monitor 8.4.3

Version 8.4.3 is a compatibility patch for the 8.4.2 device-option migration.

## Fixed

- Existing split GMC-500+ settings are now persisted with a structured JSON request to the Home Assistant Supervisor API.
- JSON arrays are no longer passed to `bashio::addon.option`, avoiding the `jq: syntax error, unexpected IDENT` startup error.
- Calibration references containing quotes, plus signs, percent signs or Unicode units such as `µSv/h` remain valid.
- If persistence is unavailable, the app continues with its existing lossless runtime migration and emits one clear warning instead of jq errors.

No database schema or measurement algorithm changed in this patch.
