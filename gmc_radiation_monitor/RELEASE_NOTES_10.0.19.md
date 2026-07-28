# GMC Radiation Monitor 10.0.19

Version 10.0.19 refines the header and section navigation. The view selector, language selector, connection-status badge and refresh button remain grouped at the top right beside the application title. The section selector is placed directly below the connection-status badge.

Only the section selector becomes floating after its original header position scrolls beyond the top of the dashboard. Its original slot remains reserved to avoid layout jumps, its horizontal position is kept inside the viewport, and it returns to the header when scrolling back. The remaining header controls never become floating. Browser regression checks now exercise this behavior in every supported language, at responsive widths and at 100% and 200% text size.

The duplicated symbol in the analysis selector was removed. Database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, scientific algorithms, serial protocols and existing app options remain compatible.
