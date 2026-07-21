# GMC Radiation Monitor 8.3.3

## Detector calibration in the main dashboard

Each connected-device card now contains a responsive **Detector and calibration** section. The summary level shows the tube model, conversion factor and calibration status. The analysis level adds dead time, correction state, reliable CPM limit, dual-tube mode, switch threshold and the currently selected tube profile. The expert level shows the full per-tube uncertainty and reference data.

Calibration values are labelled as documented, working values or incomplete. A configured conversion factor is no longer confused with its percentage uncertainty.

## GMC-500+ dual-tube support

The GMC-500+ can now use two independent calibration profiles:

- low-dose tube profile, normally M4011;
- high-dose tube profile, normally SI-3BG.

Three modes are available:

- `single`: backwards-compatible primary CPM calibration;
- `separate`: use the device's low- and high-dose tube CPM channels and select one profile without double-counting;
- `curve`: apply a piecewise calibration to the primary CPM channel at a configurable switch point.

Existing single-profile GMC-500+ settings are automatically used as the low-dose profile when the new nested profile is empty. A missing high-dose conversion factor is shown as an incomplete calibration; the app suppresses a derived dose value instead of applying the M4011 factor to SI-3BG data.

## Reports and compatibility

Analysis JSON and integrated-dose processing preserve the selected dual-tube profile, gaps, invalid intervals and profile switches. Existing databases and single-tube configurations remain compatible. The user interface remains responsive on narrow mobile displays.

## Retained reporting and history features

The professional **five-page** report layout remains unchanged. Radiation charts continue to use the explicit **Count rate [CPM]** axis and document the detector's **combined beta/gamma response**. Protected database maintenance continues to use the single `history_management_enabled` switch.
