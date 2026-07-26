# GMC Radiation Monitor 9.1.1

Version 9.1.1 is a visual-consistency maintenance release for the long-term overview.

## Interface adjustment

- Reduces the main value size in long-term cards to the same visual scale as the established metric cards elsewhere in the dashboard.
- Uses a slightly smaller type scale for multi-line readiness messages such as “Not yet meaningful”.
- Increases line height for wrapped values so long German and translated messages remain readable.
- Preserves responsive one-, two- and multi-column layouts without changing card spacing or touch targets.

## Compatibility

- No database migration is required.
- Long-term calculations, alarms, derived dose, stored measurements, detector profiles, MQTT entities and Home Assistant configuration are unchanged.
- All eight user manuals remain content-compatible and carry the current 9.1.1 release label.

## Retained safeguards

- Retains independent measurement freshness states, report presets, copy-safe support-diagnostics and database schema 8.
