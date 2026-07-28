# GMC Radiation Monitor 10.0.17

Version 10.0.17 is a maintenance and archive-cleanup release. It removes obsolete dashboard styles, JavaScript handlers, rendering variables and empty wrappers that remained after the large status panel and segmented view selector were replaced by compact header controls.

The responsive fixture now tests the current analysis dropdown, language selector, connection badge and reload button. A dedicated cleanup regression prevents retired components from returning, and the quality runner reports its discovered test count dynamically. Duplicate 10.0.15 documentation was consolidated and generated caches are excluded from the final archive.

Database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, scientific algorithms, serial protocols and existing app options remain compatible.
