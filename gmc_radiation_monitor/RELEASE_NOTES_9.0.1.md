# GMC Radiation Monitor 9.0.1

Version 9.0.1 is a focused report-preview hotfix for the 9.0 architecture.

## Fixed

- Fixed the report-preview API failure `TypeError: _one() takes 2 positional arguments but 3 were given`.
- Made the preview period optional and defaulted it safely to `daily` when the browser has not supplied the field yet.
- Added HTTP regression coverage for preview requests with and without an explicit period.
- Kept database schema 8, measurement acquisition, time-weighted statistics, calibration, reports and device handling unchanged.
