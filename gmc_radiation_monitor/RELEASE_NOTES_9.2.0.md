# GMC Radiation Monitor 9.2.0

Version 9.2.0 consolidates long-term analysis around understandable results, conservative evidence requirements and practical endurance diagnostics. It does not change database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds or serial protocols.

## Simplified long-term presentation

- Adds a plain-language assessment before statistical method details.
- Keeps the real 24-hour, 7-day, 30-day, 90-day and 365-day windows in one visible overview.
- Moves effective sample size, bootstrap intervals, EWMA, CUSUM, dispersion and environmental correlations into collapsed expert groups.
- Uses coherent metric-card typography and responsive wrapping down to 320 px and at 200% text size.
- Explains unavailable results instead of showing unexplained placeholders.

## Protection against statistical overinterpretation

- Adds evidence levels: not evaluable, exploratory, preliminary, supported and well supported.
- Uses explicit minimum duration, coverage and effective-sample requirements.
- Requires at least 90% coverage for the 24-hour window.
- Requires at least 30 sufficiently complete daily values for long-term trend interpretation.
- Shows practical monthly trend magnitude alongside test statistics.
- Delays annual dose projection until a sufficiently complete 90-day window exists.
- Requires at least 100 paired hourly values for each environmental association.
- Applies Benjamini-Hochberg false-discovery-rate correction across tested environmental lags.
- Continues to label correlations, process-control signals and structural changes as statistical context rather than proof of a source or cause.
- Keeps configured absolute warning and danger thresholds independent of all statistical models.

## Long-term field-test diagnostics

- Adds operational counters for service uptime, serial errors, reconnects and database write errors.
- Adds longest-gap, gap-count and estimated missing-duration diagnostics.
- Includes GMCMap success and error counters.
- Adds a downloadable JSON field-test protocol with a repeatable endurance-test checklist.
- Clearly states that operational diagnostics do not certify calibration or measurement accuracy.

## Documentation and localisation

- Updates all eight user manuals to 35-page version 9.2.0 editions.
- Adds fully localised chapters for evidence levels, dose wording, environmental interpretation and field testing.
- Adds all new interface text in German, English, Spanish, French, Croatian, Italian, Dutch and Polish.

## Compatibility

- Database schema remains version 8.
- Existing history, calibration profiles, device identities, reports and Home Assistant entities remain compatible.
- Coordinate formatting introduced in 9.1.2 remains unchanged, including degree symbols and cardinal directions.

## Retained platform capabilities

- Retains independent measurement freshness states.
- Retains report presets and validated custom ranges.
- Retains copy-safe support-diagnostics with secret redaction.
- Retains database schema 8 and existing history compatibility.
