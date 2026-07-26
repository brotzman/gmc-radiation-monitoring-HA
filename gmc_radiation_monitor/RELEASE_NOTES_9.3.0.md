# GMC Radiation Monitor 9.3.0

Version 9.3.0 adopts the proven Radon Monitoring 5.3.1 navigation model while retaining the existing GMC dashboard design, cards, diagrams, measurements, calculations and reports. The database schema remains version 8.

## New application navigation

- Adds a persistent desktop sidebar with grouped destinations for monitoring, evaluation, documentation and administration.
- Adds an Ingress-safe mobile drawer with a dimmed page overlay, automatic closing after selection, outside-click handling and Escape-key support.
- Shows exactly one selected content view at a time without a full page reload.
- Persists the last selected view in browser storage and supports direct hash links to views and existing sections.
- Keeps Summary, Analysis and Expert detail-level controls available independently of the selected view.
- Preserves the existing expandable cards and the established GMC visual language.

## View structure

- **Overview:** live status, connected devices, radiation intelligence, adaptive background, environmental context and fleet summary.
- **Analysis:** detailed selected-device analysis.
- **Long-term:** detector-aware long-term assessment and field-test diagnostics.
- **History:** history explorer and exports.
- **Workflows:** notifications, annotations, comparisons and operational workflows.
- **Calibration profiles:** device and detector calibration management.
- **Reports:** report creation, downloads and generated reports.
- **History management:** backups, restore and protected history maintenance.

## Responsive and accessible behavior

- Uses a fixed sidebar on desktop and an overlay drawer below 860 px.
- Supports 320 px displays, 200% text zoom, safe-area insets and reduced-motion preferences.
- Adds a skip link, visible keyboard focus, `aria-current` state, accessible menu state and translated navigation labels.
- Keeps wide tables and heat maps internally scrollable instead of widening the page.

## Documentation and localisation

- Updates all eight interface catalogues with the new navigation labels.
- Updates all eight user manuals to 36-page version 9.3.0 editions with a dedicated navigation chapter.
- Keeps coordinate degree symbols and cardinal directions introduced in 9.1.2.

## Compatibility

- Database schema remains version 8.
- Measurement acquisition, device detection, serial protocols, safety thresholds, MQTT entity identities, long-term calculations, stored data and report contents are unchanged.
- Existing 9.x histories, calibration profiles and settings remain compatible.

## Retained platform capabilities

- Retains independent measurement freshness states.
- Retains report presets and validated custom ranges.
- Retains copy-safe support-diagnostics with secret redaction.
- Retains database schema 8 and existing history compatibility.
