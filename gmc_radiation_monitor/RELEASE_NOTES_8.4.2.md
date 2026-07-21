# GMC Radiation Monitor 8.4.2

Version 8.4.2 is a clarity, safety and public-release hardening update for the scientific detector workflow.

## Dashboard

- Removed the large measurement-quality tile from the detector profile card.
- The detector profile is now tiered: compact profile/status in Summary, detector load and dead-time monitor in Analysis, and tube details plus scientific statistics in Expert view.
- Retained the quality index only in Expert statistics and added a clear explanation that it is not a certified accuracy statement.
- Corrected the German title to **Detektorprofil**.

## Calibration semantics

- Automatic model handling is now described as an **automatically recognized device profile**, not physical tube verification.
- Predefined values are labelled as application working values.
- A calibration is only labelled documented when both a reference and calibration uncertainty are present; factory-calibrated wording is reserved for an explicit factory/manufacturer certificate source.

## Device identity and defaults

- Dual-tube settings can optionally include the physical counter serial number. The app verifies it at connection time and disables that device configuration on a mismatch rather than applying calibration values to the wrong counter.
- Duplicate device names cannot be used for a dual-tube override.
- Removed installation-specific orientation serial numbers and six-position calibration values from shipped defaults. Existing user options remain in Home Assistant and continue to be read.

## Localization

- Updated all eight bundled languages for profile recognition, application working values, documented calibration, stable serial verification and the measurement-quality explanation.

## Configuration and reporting

- A GMC-500+ is configured once as one complete dual-tube device. Existing 8.4.0/8.4.1 split entries are merged losslessly during startup, while a GMC-320 remains in the single-tube list without advanced dual-tube fields.
- Removed the duplicate standalone device-comparison dashboard card; comparison analytics remain available in the dedicated analysis and report workflows.
- The standard professional report remains a five-page report. The optional scientific report adds a sixth metrology page with detector, dead-time correction and quality documentation.

The report axis remains labelled **Count rate [CPM]**. Dose interpretation continues to describe the counters' combined beta/gamma response rather than falsely separating radiation components. History deletion and maintenance remain protected by the `history_management_enabled` option.
