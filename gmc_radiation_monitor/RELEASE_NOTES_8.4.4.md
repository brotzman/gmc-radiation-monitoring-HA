# GMC Radiation Monitor 8.4.4

Version 8.4.4 improves the detector-profile presentation.

- The CPM-to-dose conversion factor is no longer repeated in the general device-information grid.
- Each physical tube now shows its own conversion factor inside the detector profile.
- An uncalibrated SI-3BG explicitly shows that no conversion factor is configured.
- Dual-tube devices with a calibrated primary tube and an uncalibrated secondary tube are labelled as partially calibrated instead of wholly uncalibrated.
- All supported UI languages include the new partial-calibration status.
- Measurement, database and migration behaviour are unchanged.

## Compatibility carried forward from 8.4.3

The legacy split GMC-500+ option migration continues to use one structured JSON request to the Home Assistant Supervisor. This prevents the former `jq: syntax error` with quoted calibration references and Unicode units such as `µSv/h`. No database schema or measurement algorithm changed.
