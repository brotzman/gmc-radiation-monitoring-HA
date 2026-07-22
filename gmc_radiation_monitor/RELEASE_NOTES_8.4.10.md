# GMC Radiation Monitor 8.4.10

Version 8.4.10 is a focused report-layout maintenance release. It fixes the overlap visible on the first page of analysis reports between the chart x-axis caption, the measurement-quality summary, and the assessment panel.

## Changes

- Raised and slightly shortened the main chart to reserve a reliable caption area.
- Added a dedicated vertical position for the measurement-quality summary.
- Reduced the assessment panel height without removing content.
- Added regression tests that enforce minimum spacing between all three report regions.
- Database schema 8, detector calibration, dose conversion, health monitoring, and measurement algorithms are unchanged.
