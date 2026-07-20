# Version 8.2.2

Version 8.2.2 is a dashboard-language, localization and usability patch release for **Radiation Monitoring**. It retains the professional reporting and History-management features introduced in 8.2.0.

## Direct language switching

The dashboard header now offers **Auto**, German, English, Spanish, French, Croatian, Italian, Dutch and Polish as directly accessible language choices. The selected language is applied immediately through an Ingress-safe query parameter. The current device and simple/advanced view are preserved when the language changes.

**Auto** follows the browser or operating-system language. It also overrides a fixed app-language setting for the current browser request, making it possible to return to automatic selection without reopening the Home Assistant configuration.

The switcher uses native language names, an explicit current-language state, keyboard-visible focus styling and compact horizontal scrolling on narrow screens.

## Complete runtime localization

The GMCMap resource link is now translated instead of exposing the hard-coded English label “Geiger Counter World Map”. A complete fallback audit also localizes newer workflow, diagnostic, history and maintenance messages that could still appear in English in Spanish, French, Croatian, Italian, Dutch or Polish.

Technical names and units such as GMCMap, Home Assistant, CPM, ACPM, USB, MQTT, SQLite, PDF and JSON remain unchanged intentionally. Catalogue validation checks matching keys, non-empty values and formatting placeholders; cross-language rendering tests additionally reject visible English fallback text.

## Header and mobile usability

The title, product-family subtitle, language switcher, Home Assistant location and resource links now form a clearer visual hierarchy. Resource links have localized accessible names, and language choices remain usable at 320-pixel phone width without causing page-wide horizontal overflow.

## Professional beta/gamma PDF reports

The primary PDF export is now a structured five-page report inspired by professional environmental-monitoring reports while remaining scientifically appropriate for Geiger-Mueller beta/gamma measurements:

1. executive summary with key values, period assessment and a practical recommendation;
2. count-rate time series, rolling mean, histogram, Poisson reference and daily range comparison;
3. weekday/hour and calendar heat maps;
4. data quality, local baseline, statistical significance, historical rarity, persistent level shifts and anomaly events;
5. device metadata, traceability, method limitations and selected measurements.

All graph axes and color scales explicitly identify the measured quantity and unit, including **Count rate [CPM]**, local date/time, sample count and daily/mean CPM heat-map scales. CPM remains the primary measurement. Any displayed µSv/h value is marked as derived from the configured conversion factor and is not presented as independent dosimetry.

The reports describe the detector's combined beta/gamma response. They do not claim to separate beta from gamma, identify radionuclides or replace calibrated radiation-protection instrumentation.

## History explorer

The History view now provides:

- quick ranges for 24 hours, 7 days, 30 days and 90 days;
- explicit local start and end filters;
- accepted-sample, coverage, mean, median, minimum and maximum summaries;
- a correctly labelled CPM chart with accepted measurements, smoothed trend, event markers and an optional rejected-raw-value layer;
- clearer event-note placement and responsive behavior on phones and tablets.

## One protected History management switch

The previous restore and complete-delete switches are replaced in the Home Assistant configuration by one option:

```yaml
history:
  history_management_enabled: false
```

When enabled, the protected History management workspace unlocks both backup restore and complete history deletion. The option should be enabled only for planned maintenance and disabled again afterwards. Restore validation, CSRF protection and explicit deletion confirmation remain unchanged.

Existing legacy option values are recognized internally during migration, but only the single new switch is shown in the configuration UI.

## Statistical analysis

The explicit Poisson rate-change significance, two-sided p-value, quality-adjusted confidence, empirical historical percentile and approximate rarity indicators introduced in the previous analysis build remain integrated into the report and dashboard. Safety thresholds and alarm semantics are unchanged.

## Compatibility

Serial communication, MQTT Discovery entities, SQLite measurement storage, accepted/raw measurement separation, Ingress routes and existing report download formats remain compatible.
