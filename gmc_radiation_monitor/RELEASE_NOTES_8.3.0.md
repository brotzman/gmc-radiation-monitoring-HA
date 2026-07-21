# GMC Radiation Monitor 8.3.0

## Metrology and scientific reproducibility

- Device-specific dead time, dead-time model and maximum reliable count rate can be configured.
- Measurements above the reliable range are flagged as possible saturation/count loss and are not rendered as apparently precise µSv/h values.
- Non-paralyzable dead-time correction is only applied when an explicit dead time and model are configured.
- The analysis document contains a separated uncertainty budget for counting statistics, CPM/µSv/h conversion and calibration.
- A combined uncertainty is only reported when every required contribution is known.
- Dose-rate output is explicitly qualified as a **derived dose estimate** unless traceable calibration information is documented.
- Full-history ZIP exports now include `scientific_manifest.json` and `SHA256SUMS`, protecting the database, accepted CSV, raw CSV and metadata with SHA-256.
- Analysis schema version increased to 3; metrology algorithm version is `8.3-metrology-1`.

## New per-device options

- `dead_time_us`
- `reliable_max_cpm`
- `dead_time_model`: `none` or `nonparalyzable`
- `conversion_factor_uncertainty_percent`
- `calibration_uncertainty_percent`
- `calibration_reference`
- `tube_model`

Unknown values should remain unset. The application deliberately does not invent correction or calibration data.

## Existing report scope retained

The established five-page professional report structure remains available. Combined beta/gamma indication continues to be presented as a detector-dependent derived interpretation, not nuclide identification or a traceably calibrated radiation-protection measurement.
The report axis remains labelled “Count rate [CPM]”. The detector result remains a combined beta/gamma response. Existing controlled-history behavior via `history_management_enabled` is unchanged.


## Stable-package corrections

- Added complete localized configuration labels and descriptions for all new metrology fields in all supported languages.
- Updated the full-history export regression test for `scientific_manifest.json` and `SHA256SUMS`.
- Removed obsolete 8.2.2 release notes from the 8.3.0 package.
- Updated all bundled manual filenames and visible version references to 8.3.0.
