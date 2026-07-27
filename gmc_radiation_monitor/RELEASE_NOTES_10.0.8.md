# GMC Radiation Monitor 10.0.8

Version 10.0.8 introduces compact application-header controls. The previous row of language links is replaced by an accessible dropdown that preserves the current dashboard mode and selected GMC device. A localized refresh button beside it reloads the complete dashboard on demand.

The controls remain compact on desktop, reflow below the title on mobile and stack at very narrow widths without horizontal scrolling. The sticky/floating section navigation remains unchanged. Two UI regression tests cover the rendered controls and JavaScript behavior, bringing the repeatable unit/integration suite to 23 tests.

Database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, scientific algorithms and serial protocols are unchanged.
