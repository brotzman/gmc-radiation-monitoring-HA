# GMC Radiation Monitor 8.4.0

## Scientific detector and calibration workspace

Version 8.4.0 makes the detector model, active calibration and limits of the current measurement visible instead of treating the CPM-to-dose conversion as an opaque device setting.

### Detector card and automatic model profiles

The Expert view now adds **Detector and calibration** directly to every connected-device card. It shows the physical tube or tubes, conversion factor, detector dead time, dead-time model, active channel, calibration state and live count rate.

The runtime identifies the connected device from its serial identity and applies a conservative predefined application profile for:

- GMC-300 family;
- GMC-320 Plus V4;
- GMC-500+;
- GMC-600/600+.

The GMC-320 Plus V4 remains a true single-tube profile. The GMC-500+ uses separate M4011 and SI-3BG channels. The M4011 working profile is never copied to the SI-3BG channel. SI-3BG CPM remains available, but its derived dose stays unavailable until a verified device-specific conversion factor is supplied.

Predefined values are transparent application working assumptions, not a traceable calibration certificate. The dashboard therefore labels them **Predefined profile**, not factory calibrated. A documented calibration can still be marked as factory calibrated, while custom values are shown as a user profile.

### Live measurement quality and detector loading

Every accepted measurement now stores and displays:

- raw CPM and non-paralyzable dead-time-corrected CPM;
- detector occupancy/load;
- estimated dead-time losses;
- correction factor and correction state;
- a five-star measurement-quality indicator and 0–100 quality index;
- live dose-quality classification;
- calibration and plausibility warnings.

The detector-load bar uses green, yellow and red states. Missing dead time, unknown tube model, implausible conversion values and incomplete calibration are reported explicitly.

### Dual-tube GMC-500+ view

When separate tube channels are available, the device card shows the M4011 and SI-3BG independently, including their current CPM, calibration, dead time and active/inactive state. The active detector is selected from the physical channel data and configured switch behavior rather than by applying one universal conversion factor.

### Device comparison

A new comparison card lists the latest accepted CPM for every connected GMC, calculates the maximum relative deviation and marks the agreement as acceptable or requiring review. The comparison is contextual only; different tube geometry, shielding and calibration can legitimately produce different responses.

### Calibration management, assistant and audit history

The dashboard now contains a calibration-management workspace with predefined profiles, custom profiles and a four-step assistant:

1. select the device;
2. confirm the tube;
3. enter and apply the calibration;
4. save the result.

Every saved change records the date, affected values, source and comment. Custom profiles can be assigned to a physical device and are reapplied after the serial identity is known. JSON endpoints expose profile and audit-history data for reproducible review.

### Raw, corrected and comparison modes

History charts and reports support three data modes:

- raw device counts;
- dead-time-corrected values;
- raw and corrected comparison.

The standard report includes a measurement-quality summary. An optional scientific PDF adds a sixth technical page with detector model, dead-time model, dead time, correction factor, estimated loss, quality index and raw-versus-corrected trace. The scientific ZIP bundle includes the corresponding reproducibility data.

### Storage and compatibility

The existing SQLite schema version remains 8 for backup compatibility. Version 8.4 columns and calibration tables are added idempotently to both new and existing schema-8 databases. Stored measurements now include detector type, dual-tube mode, active tube, dead-time values, losses, correction factor, calibration state/source, measurement-quality index, dose quality, and raw/corrected CPM.

Existing 8.3.x configurations remain valid. Legacy low-dose profile data are accepted as migration input, while single-tube devices ignore stale second-tube fields.

### Localization and safety

All new controls, warnings and workflow labels are included in German, English, French, Spanish, Italian, Dutch, Polish and Croatian. Derived dose remains a model-based estimate and does not turn the application into a certified radiation-protection instrument.

## Retained report and history contract

The standard professional report remains a **five-page** document; the scientific option appends a sixth metrology page. Its primary count-rate axis remains **Count rate [CPM]**, and the report continues to describe the instrument result as a **combined beta/gamma response** where applicable. Protected restore and complete-history deletion remain controlled by `history_management_enabled`.
