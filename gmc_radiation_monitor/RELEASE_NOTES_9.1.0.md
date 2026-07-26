# GMC Radiation Monitor 9.1.0

Version 9.1.0 adds a dedicated, detector-aware long-term analysis without duplicating the existing live analysis, adaptive background or fleet comparison functions.

## Long-term analysis

- Adds real 24-hour, 7-day, 30-day, 90-day and 365-day windows with explicit duration and data-coverage checks.
- Shows “not yet meaningful” instead of a number until the requested period and minimum coverage are available.
- Adds robust local background statistics, daily and monthly development, a calendar heat map and a rolling seven-day median.
- Adds cumulative derived dose and a clearly labelled annual projection only when a sufficiently complete 30-day basis exists.
- Adds effective sample size, moving-block bootstrap confidence intervals, Mann–Kendall trend testing and Sen slope.
- Adds contextual EWMA, CUSUM and hourly overdispersion diagnostics that do not replace the existing radiation-safety thresholds.
- Groups connected periods above the robust local background into persistent relative elevation episodes.
- Adds lagged exploratory Spearman associations with temperature and air pressure at 0, 3, 6, 12 and 24 hours.
- Keeps the established seven-day live baseline analysis as a separate “recent baseline context” rather than duplicating it.

## Data and compatibility

- Adds an indexed SQL aggregation path for long histories instead of loading every raw sample into memory.
- Increases the default retention for new installations to 730 days so annual analysis can become available; existing user options are preserved.
- Keeps database schema 8, measurement rows, device registry, MQTT entities, calibration profiles and existing reports compatible.
- Long-term calculations do not interpolate missing values and never alter safety alarms.

## Interface and localisation

- Adds a dedicated dashboard jump target and clear Summary, Analysis and Expert tiers.
- Adds responsive cards, internally scrollable tables and a calendar heat map designed for 320 px phones through desktop widths.
- Adds complete long-term-analysis wording in English, German, French, Spanish, Italian, Dutch, Polish and Croatian.
- Updates all eight user manuals and documents the scientific limitations of derived dose, control charts, trend tests and environmental correlations.

## Quality assurance

- Adds unit, integration, localisation and browser layout coverage for long-term calculations and presentation.
- Retains the existing measurement freshness, report presets, copy-safe support-diagnostics and database schema 8 safeguards.
