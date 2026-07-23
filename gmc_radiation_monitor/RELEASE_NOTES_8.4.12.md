# GMC Radiation Monitor 8.4.12

Version 8.4.12 is a focused responsive-layout maintenance release. It restores the floating dashboard navigation on mobile devices and keeps temporal report fields inside their cards on narrow screens.

## Changes

- Restored sticky dashboard navigation below 800 px instead of changing it to static positioning.
- Added a WebKit sticky fallback and a safe-area-aware top offset for Home Assistant mobile ingress.
- Kept section links horizontally scrollable while the compact action remains accessible.
- Constrained date, ISO-week, month and date-time inputs with explicit minimum and maximum inline sizes.
- Added 16 px temporal form controls on phones to avoid browser zoom and improve touch usability.
- Added mobile browser regression checks for sticky behavior, horizontal overflow and report-field containment.
- Database schema 8, PDF generation, detector calibration, health monitoring and measurement algorithms are unchanged.
