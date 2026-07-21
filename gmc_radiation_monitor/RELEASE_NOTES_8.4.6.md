# GMC Radiation Monitor 8.4.6

Version 8.4.6 redesigns the **Connected GMC devices** card and adds a configurable main-value size.

- Reworked each device card around a clear identity → connection → measurement hierarchy.
- Shows configured device name, detected model/version and a subdued physical device ID without duplicating technical metadata.
- Splits the live dose reading into a dominant numeric value and a smaller unit.
- Formats dose values automatically according to magnitude and the selected interface language.
- Adds compact CPM, active-detector and measurement-quality context directly below the main value.
- Shows the age of the latest accepted measurement beside the connection badge.
- Adds **Main measurement font size** with Small, Medium, Large and Custom choices; Custom accepts 20–64 px.
- Makes the display choice available both in Home Assistant add-on options and as a browser-local dashboard control.
- Improves narrow-screen wrapping, touch targets and spacing while preserving full Expert diagnostics.

Compatibility note: the existing startup migration continues to persist options through one structured JSON request to the Home Assistant Supervisor API, preserving arrays, Unicode units and quoted calibration references without shell interpolation.
The migration avoids the former `jq: syntax error` failure mode and continues to preserve values such as `µSv/h`. No database schema or measurement algorithm changed.
