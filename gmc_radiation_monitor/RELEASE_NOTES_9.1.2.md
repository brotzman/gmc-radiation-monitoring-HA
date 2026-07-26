# GMC Radiation Monitor 9.1.2

Version 9.1.2 is a small display and metadata maintenance release.

## Changes

- Home Assistant coordinates now include angular units and cardinal directions.
- Coordinates are displayed as, for example, `51,60176° N, 7,45410° E`.
- Negative latitudes and longitudes are rendered with `S` and `W` respectively.
- The underlying Home Assistant location data, privacy behavior, calculations and database schema are unchanged.
- All user manuals retain their existing content and carry the current 9.1.2 release label.

## Retained safeguards

- Retains independent measurement freshness states, report presets, copy-safe support-diagnostics and database schema 8.
