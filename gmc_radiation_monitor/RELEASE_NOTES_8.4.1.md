# GMC Radiation Monitor 8.4.1

Version 8.4.1 is a focused usability and configuration correction for the scientific detector workflow.

## Detector Profile card

- Renamed the connected-device card from **Detector and calibration** to **Detector Profile**.
- Removed repeated **Current CPM** and **Calibration** rows from the card because those values already appear in the main device summary.
- Added an explicit responsive label/value grid to the live dead-time monitor and Expert statistics. Raw CPM, corrected CPM, dead-time loss, correction factor, detector and measurement quality no longer run into their values.

## Single- and dual-tube configuration

- The normal `devices` form now contains only common and only/primary-tube values. A GMC-320 therefore no longer shows **Tube operating mode (advanced)** or second-tube fields.
- Added one dedicated `dual_tube_devices` configuration group for the GMC-500+ and other supported dual-tube models.
- The GMC-500+ advanced mode and SI-3BG values appear exactly once in that group and are merged into the matching device by name at runtime.
- Legacy inline second-tube fields remain readable by the application for imported configuration data, while the dedicated group takes precedence.

## Localization

- Reviewed all eight Supervisor configuration translations after moving the dual-tube controls.
- Added localized group, device-name, operating-mode, switch-point and SI-3BG field descriptions.
- Corrected the German card title to **Detektor Profil** and retained consistent scientific terminology for raw CPM, corrected CPM, dead time and correction factor.

## Existing report and history capabilities

The established five-page professional report remains unchanged, including the **Count rate [CPM]** axis and the careful description of the detector's combined beta/gamma response. Protected history maintenance continues to use the single `history_management_enabled` switch.
