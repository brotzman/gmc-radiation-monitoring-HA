# Changelog

## 8.3.2

- Added visible, dynamically updated explanations for Summary, Analysis and Expert view.
- Added a report-format guide for PDF, reproducible ZIP and CSV downloads.
- Increased mobile touch targets for primary controls and report actions.
- Improved the narrow-phone header title and contained the horizontally scrollable language chooser without causing page-level overflow.
- Fixed the page-1 report overlap by separating the chart and assessment into protected layout regions.
- Limited active-period charts to the actual report generation time and added a data-through timestamp.
- Fixed the single-day comparison chart so it no longer renders a misleading multi-year x-axis.
- Added usability and report-layout regression tests.

## 8.3.1

- Promoted the validated Stable R2 device-stability display corrections to a patch release.
- Updated add-on metadata, runtime version reporting, release notes and all eight bundled manuals to 8.3.1.
- Kept the database schema, analysis schema and metrology algorithm version unchanged for full 8.3.0 compatibility.

## 8.3.0

- Clarified the shared device-stability card for every connected counter: the 24-hour valid/expected sample count, total stored samples, configured interval, largest observed interval and maximum deviation are now shown separately.
- Corrected the rolling 24-hour query to an exact half-open window, preventing a regular 120-second series from briefly showing 721 instead of 720 samples.
- Displayed the per-device quality weight as a percentage.

- Added device-specific dead-time and reliable-range configuration.
- Added saturation/count-loss assessment and suppression of misleading dose conversion outside the reliable range.
- Added separated uncertainty budgets and cautiously qualified derived dose estimates.
- Added reproducible scientific export manifests with SHA-256 checksums.

## 8.2.2

- Added a directly accessible language switcher to the dashboard header for Auto, German, English, Spanish, French, Croatian, Italian, Dutch and Polish.
- Made the Auto choice follow the browser or system language even when a fixed app language is configured.
- Localized the GMCMap world-map link and removed remaining English runtime fallbacks from non-English dashboards.
- Improved the header hierarchy, focus states and compact horizontal language navigation on small screens.
- Added release-blocking tests for language switching, automatic locale resolution, translated resource links and fallback detection.
- Updated runtime, package, release-note and all integrated manual version references to 8.2.2.

## 8.2.1

- Completed localization of the statistical significance and historical-rarity explanations in all eight supported dashboard languages.
- Removed the English fallback text visible in non-English Intelligent radiation analysis cards.
- Extended the static translation audit to include dynamic analysis dictionaries that use `{"key": ...}` message templates.
- Added cross-language rendering tests so newly introduced analysis reasons cannot silently fall back to English.
- Updated runtime, package, release-note and all integrated manual version references to 8.2.1.

## 8.2.0

- Rebuilt the primary PDF export as a professional five-page beta/gamma radiation report with executive summary, recommendations, statistical analysis, anomaly events and technical traceability.
- Added explicit, unit-correct chart labels for CPM count rate, accepted sample counts, local date/time, local hour and heat-map CPM color scales.
- Clarified throughout the report that Geiger-Mueller data represent a combined beta/gamma detector response, do not separate radiation types or identify radionuclides, and that µSv/h is derived rather than independently measured.
- Added weekday/hour and calendar heat maps, Poisson distribution context, daily minimum/median/maximum comparison and selected measurement tables.
- Integrated data quality, baseline deviation and drift, recent-change significance, two-sided p-value, historical rarity and persistent level-shift results into the PDF.
- Optimized the History explorer with quick ranges, explicit local-time filters, coverage and distribution summaries, a smoothed trend, event markers and responsive mobile chart handling.
- Replaced the separate restore and complete-delete configuration switches with one protected `history_management_enabled` switch while retaining internal migration compatibility.
- Renamed the protected maintenance workspace to History management and clarified enabled/locked states.
- Retained the Home Assistant sidebar title **Radiation Monitoring** and promoted the complete feature set to version 8.2.0.

## 8.0.14

- Removed the mandatory GHCR image reference so Home Assistant builds the app from the included Dockerfile.
- Fixed installation failures reporting `ghcr.io/...:8.0.13: denied` when the container package was absent or private.
- Replaced automatic registry publication with non-publishing multi-architecture source-build validation for `amd64` and `aarch64`.
- Updated app, runtime, release-note and all eight integrated manual version references to 8.0.14.
- Kept measurements, storage, MQTT Discovery entities, serial communication, Ingress routes, dashboard behavior and user configuration compatible.

## 8.0.12

- Changed the Home Assistant Ingress sidebar icon from `mdi:chart-line` to `mdi:radioactive` for clearer identification.
- Updated the add-on, runtime, release-note and all eight integrated manual version references to 8.0.12.
- Added a release regression check for the sidebar icon and retained all 8.0.11 quality gates.
- Kept measurements, storage, MQTT entities, serial communication, routes, dashboard behavior and user configuration compatible.

## 8.0.11

- Split the HTTP request handler and localized exception mapping out of `report_web.py` into `report_web_http.py` while preserving the existing public imports and routes.
- Enabled the complete configured Ruff ruleset and resolved the existing non-translation lint backlog; intentional typographic symbols remain explicitly allowed.
- Added a release-blocking mypy check for the typed version, device-profile, web-security, cache, upload and serial core.
- Added combined branch coverage collection with a mandatory 70 percent project floor.
- Expanded responsive UI verification to Chromium, Firefox and WebKit across desktop, tablet, phone and narrow-phone viewports in English, German, French and Polish.
- Added a simulated hardware matrix for GMC-300/320, GMC-500, GMC-600 and generic RFC1201-compatible version, counter-width, corruption and identity paths.
- Updated all eight integrated manuals and current release references to version 8.0.11.
- Kept measurements, database schema, MQTT entities, serial protocol behavior, dashboard output and configuration compatible.

## 8.0.10

- Added headless Chromium tests that capture desktop and phone screenshots and verify responsive layout without horizontal overflow.
- Added fixed per-test and suite-level timeouts for all serial-related tests so stalled PTY or scheduler paths fail deterministically.
- Added automatic release checks for all eight packaged manuals, their embedded version text, filenames and current package version references.
- Updated all eight illustrated manuals and dashboard labels to version 8.0.10.
- Moved manual, report-target, multipart-upload and query helpers into `report_web_support.py` while preserving the existing `gmc_bridge.report_web` imports, routes and rendered UI.
- Kept measurements, database schema, MQTT entities, serial communication, dashboard behavior and configuration compatible.

## 8.0.9

- Raised the add-on, runtime and release metadata from 8.0.8 to 8.0.9.
- Updated all eight integrated illustrated user manuals and their dashboard labels to version 8.0.9.
- Kept the multilingual Ingress-safe manual route, dashboard layout, measurements, storage, MQTT entities and device communication unchanged.
- Updated release and packaging regression expectations for the 8.0.9 package.

## 8.0.8

- Integrated illustrated user manuals for all supported dashboard languages into the Ingress dashboard.
- Added automatic language selection for German, English, Spanish, French, Italian, Dutch, Polish and Croatian manuals.
- Kept the compact manual button next to the GMCMap world-map link and the original German route for backwards compatibility.
- Added an Ingress-safe same-origin PDF route that opens in a separate browser tab.
- Kept the two header links side by side on wide screens and stacked them on narrow screens.
- Removed unused vertical flex space from the View selector on phones.
- Preserved the upper status overview, View selector, measurements and all existing configuration.

## 8.0.7

- Moved the page-wide View selector directly below the GMCMap world-map link.
- Kept the full live-status overview at the top while making only the navigation bar sticky.
- Promoted History to a standalone main section and kept event notes beside the history explorer.
- Collapsed Workflow groups by default and persisted their open/closed state in the browser.
- Replaced the two global expand/collapse buttons with one state-aware control.
- Standardized the Reports heading and clarified quality-filtered versus original raw-data CSV exports.
- Increased responsive spacing and prevented crowded or overlapping cards and controls.

## 8.0.6

- released the refined detail-level selector with Summary, Analysis and Expert view on one desktop line
- retained responsive wrapping for narrower screens
- kept the upper status overview, global GMCMap link and all measurement behavior unchanged
- updated add-on metadata, runtime version reporting, release notes and regression expectations

## 8.0.5

- removed the redundant Configuration preflight dashboard card while retaining candidate validation and the JSON validation endpoint
- removed the duplicate detailed-analysis recommendation card while preserving the summary conclusion and action guidance
- kept the upper status overview and global GMCMap link unchanged
- kept Summary, Analysis and Expert view on one line at desktop widths
- updated add-on metadata, runtime version reporting, release notes and regression expectations

## 8.0.4

- retained the global GMCMap world-map link in the dashboard header
- carried the 8.0.3 dashboard consolidation forward without changing measurements, storage, MQTT entities or device communication
- updated add-on metadata, runtime version reporting, release notes and regression expectations

## 8.0.3

- improved spacing in the local-background status tile while preserving the upper live-status overview unchanged
- removed visible automatic device-refresh messages while retaining silent periodic refresh
- consolidated scheduled report files under Reports and added confirmed, CSRF-protected deletion
- consolidated managed SQLite backups under History maintenance and removed duplicate backup and maintenance summaries
- removed the redundant guided-status panel while retaining the global GMCMap world-map link
- reduced self-test duplication by showing it as collapsed additional diagnostics and excluding checks already present in the upper status overview
- corrected the History navigation target and renamed “Analysis depth” to “Detail level”
- added dashboard regression tests for the consolidated interface

## 8.0.2

- removed generated Python bytecode and pytest caches from the distributed source package
- consolidated superseded per-version release notes into this changelog
- added `.gitignore` and `.dockerignore` safeguards for generated and development-only files
- added packaging regression tests for clean release archives

## 8.0.1

- calculate a cumulative session ACPM from every accepted CPM reading
- transmit the ACPM value through the official GMCMap upload parameter
- show the last uploaded CPM and ACPM in each GMCMap device panel
- publish ACPM and its accepted-sample count as Home Assistant diagnostics
- add ACPM explanations in all eight supported interface languages

## 8.0.0

- added optional Home Assistant notification rules with cooldowns
- added scheduled daily/weekly ZIP reports and monthly JSON summaries
- added managed backup creation, comparison, download, deletion and retention pruning
- added event annotations with confirmation, dismissal, history markers and report export
- added freely selected period comparisons and a date-range history explorer
- added a guided readiness checklist and integrated system self-test
- added configuration preflight validation and versioned JSON workflow APIs
- migrated the database to schema 8 for event annotations
- kept notifications and scheduled reports disabled by default

## 7.1.4

- completed a full runtime translation-key audit across all eight dashboard languages
- translated the estimated signal probability sentence and nested semantic template values
- changed the German normal-state label to “Unauffällig” for clarity
- added regression checks that prevent untranslated runtime templates from reaching the dashboard

## 7.1.3

- increased spacing before the recommendation block
- combined cosmic-pressure learning requirements into one card
- removed the redundant statistical-indication label card

## 7.1.2

- Completed migration of all dashboard analyses to the shared typed presentation tree.
- Added structured analysis sections, messages, repeated entities and expert tables to the common model.
- Moved analysis-specific HTML rendering into `web_analysis_views.py` and reduced `report_web.py` to orchestration plus compatibility wrappers.
- Kept translation, report JSON and dashboard rendering on one semantic result contract.
- Preserved measurement calculations, serial communication, configuration, database schema, MQTT identifiers, Ingress routes and AppArmor.

## 7.0.0

- Consolidated dashboard and report presentation around shared typed analysis models.
- Split dashboard CSS, JavaScript, reusable web components and historical rendering into dedicated modules.
- Split the translation catalogue into one validated module per supported language.
- Added explanation codes, localized "why" guidance and structured optional-device issue contracts.
- Added presentation summaries to live analysis and machine-readable report JSON.
- Centralized historical periods and fixed incremental retention pruning for historical backfills.
- Preserved configuration, database schema, Ingress routes, AppArmor and measurement behavior.

## 6.9.2

- Reassemble complete `0xAA`-terminated optional-command frames from serial bursts that contain leading stale bytes.
- Retry malformed optional replies after a clean serial synchronization and reject incomplete frames.
- Prevent invalid orientation data from being published or stored while leaving CPM acquisition independent.
- Keep AppArmor, configuration, database schema and CPM filtering unchanged.

## 6.9.1

- Verify every RFC1801 `GETCPM` result of 1000 CPM or more with an immediate fresh protocol read before it reaches the high-CPM confirmation gate.
- Recover a normal second read directly instead of carrying a dirty-line candidate into the next measurement cycles.
- Reject unstable three-read serial sequences such as the observed `5375`, `4095`, `5631`, `3583` and `1048575` patterns before publication or history storage.
- Tighten the similarity requirement for the three independent high-CPM confirmations from a factor of 4.0 to 1.25.
- Add regression tests for real stable high CPM values and `0xff`-fragment corruption.

## 6.9.0

- Adds a three-level analysis presentation using neutral symbols: ◉ Summary, ▤ Analysis and ∑ Expert view.
- Persists the selected analysis depth in the browser and applies it consistently to intelligent analysis, adaptive background, cosmic indication, fleet comparison and the detailed device analysis.
- Keeps the summary focused on conclusions and primary values, moves supporting interpretation into Analysis, and reserves full distributions, confidence metrics and diagnostics for Expert view.
- Adds Historical development inside the adaptive background card with 7-, 30-, 90- and 365-day comparisons.
- Adds a compact server-rendered chart of 7-day-smoothed daily CPM medians.
- Adds optional 30-day temperature and air-pressure trends plus statistically detected baseline jumps when sufficient daily data exists.
- Uses robust daily medians and limits chart payload size so the additional history view remains resistant to isolated noise and inexpensive to render.
- Keeps measurement calculations, CPM peak filtering, automatic serial detection and AppArmor permissions unchanged.

## 6.8.4

- Breaks adaptive-background profile values onto a new line after the localized weekday/time phrase for clearer scanning.
- Groups the live status strip and dashboard navigation into one sticky floating toolbar on desktop.
- Keeps section jumps visible below the combined floating toolbar by calculating its live height.
- Falls back to a non-sticky stacked layout on narrower screens to preserve usable content space.

## 6.8.3

- Replaces the internal `enable_restore` option key in disabled-restore notices with the localized add-on configuration label.
- Uses the exact translated field name shown under History and backup, such as “Wiederherstellung erlauben” in German.
- Applies the same localized label to server-side restore-disabled responses and keeps restore security behavior unchanged.

## 6.8.2

- Applies the conservative 1,000 CPM plausibility threshold from the first sample, before a learned device baseline exists.
- Continues to require three consecutive, similarly sized high readings before publishing or storing a high event.
- Rechecks raw and accepted history on every app start and removes isolated unconfirmed peaks such as 6,339 CPM even after an earlier cleanup run.
- Adds the matching GMC-320 or GMC-500+ color badge before the selected device analysis heading.
- Adds a stable `analysis` anchor so the Analysis navigation control reliably opens and scrolls to the section.
- Removes the browser-only recent-report and saved-report-preset panels and their unused controls.
- Reflows the six live-status items into a readable responsive grid without clipped headings or ellipses.
- Keeps automatic serial discovery, AppArmor permissions and confirmed high-event handling unchanged.

## 6.8.1

- Removes the duplicate device-count and stored-sample chips from the page header.
- Moves the stored-sample total into the live status strip beside the database state.
- Restores dashboard JavaScript under the strict Content Security Policy with a per-response script nonce.
- Makes jump navigation and expand/collapse controls resilient and persists their resulting state.
- Corrects adaptive-background and cosmic-influence grid selectors for collapsible card markup.
- Reflows custom date/week report forms so fields and buttons no longer overlap.
- Shows a neutral deletion-disabled notice in the maintenance section when complete deletion is disabled.

## 6.8.0

- Adds a sticky live-status strip for device connectivity, the latest accepted value, last successful storage, discarded CPM peaks and database health.
- Remembers card open/closed state, pinned cards, selected device, active dashboard section and custom report fields in the browser.
- Adds dashboard jump navigation plus Expand all and Collapse all actions.
- Adds consistent GMC-320 and GMC-500+ visual accents and shows device-health, CPM-gate, serial-recovery, clock and history-write warnings directly in each device card.
- Adds clearer scanning, loading and insufficient-data states instead of ambiguous empty cards.
- Adds browser-side recent reports and reusable custom report presets.
- Adds a read-only SQLite restore preview with integrity, schema, device, row-count, file-size and data-period information before restore.
- Adds a destructive-action preview with affected row counts, data period, current database size and the last backup requested in the current browser.
- Adds compact help popovers, consistent device symbols and browser-side backup recency guidance.
- Improves long serial-number wrapping, card controls, report lists and action layouts on mobile screens.
- Keeps AppArmor, automatic serial discovery, measurement logic and configured startup staggering unchanged.

## 6.7.4

- Accepted Firefox sandboxed-ingress `Origin: null` submissions only from the fixed Home Assistant Supervisor ingress proxy address.
- Kept Host validation, explicit cross-site rejection and one-time action-bound CSRF tokens unchanged.
- Fixed restore uploads being rejected before their multipart body was consumed, which could produce a follow-up malformed-request log entry.

## 6.7.3

- Accepts destructive Home Assistant ingress POST requests from the documented Supervisor ingress proxy address even when `X-Ingress-Path` is absent.
- Keeps explicit cross-site rejection, action-bound one-time CSRF tokens and exact destructive-action confirmation text.
- Closes rejected or otherwise unsuccessful POST connections so unread request-body bytes cannot be parsed as a second HTTP request.
- Suppresses harmless idle keep-alive timeout messages while retaining unexpected HTTP server errors.
- Adds regression coverage for the observed 403 and `csrf_token=...` 400/501 sequence.
- Leaves AppArmor permissions unchanged.

## 6.7.2

- Accepts destructive form submissions through Home Assistant ingress when the request comes from the Supervisor ingress proxy and carries its `X-Ingress-Path` header, while still requiring action-bound one-time CSRF tokens.
- Keeps strict Origin/Host matching outside trusted Home Assistant ingress and continues to reject cross-site requests.
- Suppresses expected HTTP client disconnect tracebacks such as `ConnectionResetError`, `BrokenPipeError` and request timeouts without hiding unexpected server exceptions.
- Adds regression tests for ingress host rewriting and benign client disconnects.
- Leaves AppArmor permissions unchanged.

## 6.7.1

- Fixes bridge startup by importing the secure logging configurator in the bridge service module.
- Adds a regression test that executes bridge logging setup so missing logging dependencies fail before packaging.
- Keeps the 6.7.0 security hardening, automatic serial discovery and AppArmor profile unchanged.

## 6.7.0

- Adds action-bound, short-lived, one-time CSRF tokens and proxy-aware same-origin checks for history purge and database restore actions.
- Replaces the unbounded report HTTP server with a bounded worker pool, request queue and per-socket timeout.
- Adds restrictive process umasks and owner-only permissions for SQLite databases, sidecars, backups, lock files and generated private artifacts.
- Redacts MQTT credentials, Home Assistant tokens and GMCMap identifiers from application logs.
- Centralizes grouped add-on option parsing in Python and removes duplicated shell normalization paths.
- URL-encodes Home Assistant entity identifiers before API requests.
- Streams report output, including ZIP archives, to temporary files instead of constructing complete downloads in memory.
- Adds a small revision-aware cache for expensive live-analysis snapshots and clears it after destructive history operations.
- Splits web security, bounded serving, file security, secure logging, runtime options and cache responsibilities into focused modules.
- Adds automated compile, lint, security, dependency, test and repository vulnerability checks in CI.
- Leaves the AppArmor profile unchanged.

## 6.6.3

- Removes the in-dashboard Simple/Advanced and language selectors; both remain configurable under the Interface group.
- Removes the duplicate location and timezone chips from the dashboard header.
- Shows the configured report timezone inside the Home Assistant location card.
- Keeps the connected-device and stored-measurement status chips unchanged.

## 6.6.2

- Orders the fleet stability cards for display with GMC-320 first and GMC-500+ second.
- Leaves device discovery, identity mapping, measurements and comparison calculations unchanged.

## 6.6.1

- Removes manual serial port and baud-rate fields from the add-on configuration.
- Makes automatic GMC port and baud-rate discovery mandatory.
- Removes the obsolete automatic/manual detection switch and manual runtime branch.
- Keeps per-device startup delays with a minimum 15-second stagger.

## 6.6.0

- Audited existing automation before adding duplicates.
- Added automatic device-health detection for prolonged zero readings, stuck CPM sequences and severe dual-tube imbalance.
- Added automatic one-time SQLite backup before schema migrations.
- Existing reconnect, port/baud rediscovery, retention cleanup, diagnostics and configuration migration remain active.

## 6.5.2

- Centralized version and user-agent metadata to remove repeated hard-coded values.
- Removed an unused duplicate image and obsolete standalone historical release-note files.
- Performed packaging cleanup with no intended functional change.

## 6.5.1

- Adds a per-device adaptive CPM plausibility gate based on the median of recent accepted normal readings.
- Holds back isolated, numerically valid but implausibly large CPM jumps below the fixed 10,000 CPM threshold.
- Requires exactly three consecutive, similarly sized suspicious values before publishing or storing the high sequence.
- Buffers unconfirmed candidates only in memory and discards them from raw and normal history when confirmation fails.
- Backfills all three samples into raw and accepted history when a high sequence is genuinely confirmed.
- Performs a one-time cleanup of legacy isolated spikes, including the previously stored one-off peak, from raw history, accepted history and matching operational events.
- Removes the no-longer-used Supervisor-management API permission and dead add-on-options client; the narrower Home Assistant Core API permission remains for optional HA data features.
- Removes the obsolete high-CPM threshold and confirmation input fields from the visible add-on configuration; the safe 10,000 CPM / three-confirmation policy is now internal.
- Seeds the adaptive baseline from recent stored normal measurements after restart and exposes gate details in diagnostics.

## 6.5.0

- Detects compatible GMC counters, stable Linux serial paths and baud rates automatically at startup.
- Matches detected counters to configured profiles by serial identity first and model family second.
- Removes the separate serial-device assignment page and all save/restart routes from the Ingress dashboard.
- Rescans every 15 seconds for newly attached GMC counters and restarts only the bridge child when the device topology changes.
- Ignores known Zigbee, Z-Wave, Thread and other unsuitable serial adapters during automatic probing.
- Keeps a configuration-only manual emergency override through `system.automatic_serial_detection: false` plus per-device port and baud-rate fields.
- Enforces at least 15 seconds between consecutive serial-device initializations while preserving larger configured startup offsets.

## 6.4.3

- Hides unsuitable and unrelated serial ports from the device-connection page.
- Removes the expandable **Other serial devices** list.

## 6.4.2

- Fixes measurement-history writes by converting ISO-8601 timestamps to UTC epoch seconds before SQLite insertion.
- Stores live measurement and orientation-event timestamps as epoch seconds at the source.
- Fixes the serial-device save confirmation redirect so it no longer requests `/serial-devices/serial-devices`.

## 6.4.1
- Added vertical spacing between the collapsed assessment-explanation panel and the status cards below it.
- Retained the 6.4.0 counting-statistics and relative-comparison UI cleanup.

## 6.4.0
- Added an in-app **Serial device connections** page with device-model-first labels, connection status and technical paths as secondary information.
- Added safe rescanning and cautious GMC protocol probing for suitable unassigned USB serial ports.
- Known Zigbee and radio adapters are separated from the normal GMC choices and cannot be assigned.
- Port assignments are saved through the authenticated Supervisor API while preserving the rest of the add-on configuration, followed by an automatic restart.
- Kept Home Assistant's raw `device(subsystem=tty)` selector as an advanced fallback and clarified its configuration label.

## 6.3.0
- Added per-window Poisson counting uncertainty from observed impulses and effective counting duration.
- Added a separate raw-data archive before high-value confirmation and analysis filtering, plus raw CSV export.
- Added long-term relative device-response learning with orientation/co-location qualification and no absolute-calibration claim.
- Added persistent statistical level-shift detection.
- Clarified Fano/Poisson overdispersion interpretation and updated the barometric scientific wording.
- Upgraded SQLite history schema to version 7.

## 6.2.2
- Added a concise scientific explanation of the relationship between air pressure and cosmically generated secondary radiation to the statistical cosmic-influence note.
- Added translations for all supported dashboard languages.

## 6.2.1
- Fixed Home Assistant weather-entity resolution for pressure-based cosmic analysis, including fallback discovery for installations that expose `weather.forecast_home_2`.
- Simplified and cleaned up the cosmic-influence panel layout, removed the dedicated air-pressure-source card and aligned the learning color with the existing blue learning state.
- Improved external temperature fallback handling for devices without an internal temperature sensor.

# 6.2.0

- Added a barometric background model using Home Assistant weather pressure.
- Preconfigured `weather.forecast_home` and `weather.forecast_balkon` with the displayed provider `Meteorologisk institutt (Met.no)`.
- Plausibility-checks two pressure sources, rejects stale or disagreeing values and stores accepted pressure with each measurement.
- Learns a robust site-specific CPM–pressure coefficient from quality-filtered hourly values.
- Added the localized **Cosmic influence – statistical indication** dashboard section with confidence, pressure effect and remaining deviation.
- The statistical hint never suppresses radiation alerts and does not claim physical separation of cosmic and terrestrial radiation.
- Upgraded the SQLite history schema to version 6 while keeping older backups importable.

# 6.1.5

- Translate the detected `device_time` capability in the dashboard device-capabilities list.
- German UI now displays `Gerätezeit`; all other supported UI languages receive equivalent labels.

# 6.1.4

- Classifies the longest measurement gap against each device's configured measurement interval.
- Shows `Warning` from 1.5 times the interval and `Critical` from 2.5 times the interval directly after the gap value.
- Keeps normal gaps unlabelled and provides localized threshold details in the status tooltip.

# 6.1.3

- Removed bullets from stability and device-health metrics.
- Kept every metric on one complete line.
- Made both stability cards equally wide.

# 6.1.2

- Improved spacing in the adaptive background profile.
- Removed two technical quality-filter notes from the dashboard.
- Reworked stability metadata into separate readable lines.
- Normalized compact device/firmware labels with a space before `Re`.

# 6.1.1

- Added a shared robust quality-filtering pipeline for live statistics, adaptive baselines and device comparison.
- Added one-to-one pairing, outlier rejection, minimum pair counts and comparison confidence.
- Added device baselines, a quality-weighted measurement-site baseline and reduced-confidence single-device fallback.
- Intelligent analysis now distinguishes device-specific deviations from shared site changes.

# 6.1.0

- Removed firmware monitoring, reference-version configuration, manufacturer links, status comparisons and related UI.
- Kept detected firmware revision as a passive device diagnostic only.
- Legacy firmware-monitoring option keys are ignored during upgrades.

## 6.0.2

- Completed the translation audit and localized the in-app title, intelligence explanations and firmware diagnostics.
- Kept the sidebar panel title language-neutral for stable Home Assistant Ingress behavior.

# Changelog

## 6.0.0

- Added explainable intelligent radiation analysis with confidence and probability estimate.
- Expanded the two-device comparison with current difference and one-hour means.
- Added per-device firmware monitoring against editable reference versions and manufacturer information links.

## 5.2.3
- Adds CSS-rendered color status indicators to fleet stability cards so they remain visible under Home Assistant Ingress and on mobile browsers.

- Improves the fleet stability cards by placing the status on its own line above availability and health details for better desktop and mobile readability.

## 5.2.1

- Added fleet intelligence, stability scoring, device comparison, shared event detection and position-change logging.

## 5.1.1

- Fixed the missing orientation-calculation import that could terminate both device worker threads after the first gyro sample.
- Hardened GETSERIAL framing against both leading and trailing `0xff` bytes.
- Reconnect identity checks now prefer the already-known serial number inside a contaminated response.

## 5.1.0

- Added compact color-coded orientation states to connected GMC device cards.
- Kept only position, roll, pitch and inclination in the main device view.
- Moved raw axes, calibrated axes, acceleration magnitude and calibration profile to MQTT diagnostic entities.
- Added MQTT diagnostic values for calibrated orientation angles and detected device position.

## 5.0.0

- Added automatic hard serial recovery, stable-path re-resolution and a no-measurement watchdog.
- Identity changes now require three independent confirmed reads before the worker stops.
- Recovery remains isolated to the affected device.

## 4.7.15

- Harden GETSERIAL against stale `0xff` prefix bytes and truncated exact-length reads.
- Retry serial identity reads after stream recovery instead of falsely reporting a device swap.

## 4.7.14

- Unified pill-shaped button styling across the complete report interface.
- Responsive Analyse/Sprache controls and touch-friendly action buttons.
- Rebuilt reports to follow the device currently displayed in Analysis.
- Removed the report-target dropdown and combined-report fallback.
- Optimized Downloads with an explicit active-device context.

## 4.7.12

- Analysis-linked reports and responsive download controls.

## 4.7.9

## 4.7.11

- Fixed the complete-history deletion form under Home Assistant Ingress.
- The destructive POST now stays on the Ingress root via `?action=purge-all-history`.
- The success-page return link now points to the Ingress dashboard instead of a non-existent parent path.

- Complete history deletion now clears Home Assistant long-term and short-term statistics through `recorder/clear_statistics` in addition to normal Recorder state history.
- The delete result reports how many statistic IDs were removed.

## 4.7.9

- Moved the report-device selector from the page header into Downloads.
- Added explicit GMC-320, GMC-500+ and combined-report choices.
- Bound the selected target to every quick, custom and advanced download.

## 4.7.6

- Renumbered the complete-history deletion release to 4.7.6.
- Added a pre-deletion preview with measurement count, time range, affected devices, events, diagnostics and Home Assistant Recorder entity patterns.
- Added a detailed post-deletion status page confirming Recorder purge, internal table cleanup, SQLite vacuum and readiness for new measurements.

## 4.7.4

- Removed the per-device connection on/off controls from GMC Radiation Monitoring.
- Removed the device-control API, persistent control state and worker pause branches.
- Device cards and analysis now follow only the actual live serial connection state.
- Kept the multi-device report selection, serial scheduler and all protocol hardening unchanged.

## 4.7.3

- Added an individual on/off connection switch to every device card in GMC Radiation Monitoring.
- Disabling one counter closes only its serial port, marks its MQTT measurements unavailable, and pauses its GMCMap uploader.
- A manually disabled counter remains visible so it can be re-enabled without restarting the add-on.
- Re-enabling uses the shared serial scheduler and performs a clean identity check before measurements resume.
- Device connection choices persist across report page reloads and add-on restarts.

# 4.7.0

- Added a shared serial scheduler that serializes command windows across multiple GMC counters.
- Added a configurable quiet gap between command bursts on the shared USB controller.
- Added explicit INIT, READ, SYNC and RECONNECT communication states.
- Protocol framing and timeout failures now resynchronize and retry once before reconnecting.
- Added optional bounded per-device TX/RX hexadecimal and ASCII frame diagnostics.
- Preserved GMCMap staggering, connected-device live filtering and Home Assistant temperature fallback.

# 4.6.12

- Added configurable Home Assistant temperature fallback for GMC devices without an internal temperature sensor.
- Added friendly-name discovery for `Raumklima (Arbeitszimmer)` when the configured entity ID differs.
- Added Celsius/Fahrenheit normalization and stale-state protection.
- Stored fallback temperature alongside accepted CPM samples for correlation without claiming GMC temperature capability.

# 4.6.11

- Show only counters that are currently connected in the live "Connected GMC devices" section and analysis selector.
- Automatically switch the analysis to the remaining connected counter when one device is unplugged.
- Refresh the complete live page when the connected-device set changes so counts, cards and analysis remain consistent.
- Reset persisted runtime connection states at bridge startup to prevent stale devices from appearing online after an unclean restart.
- Preserve all historical measurements and exports; only the live UI is filtered.

# 4.6.10

- Reject partial `0xff` RFC1801 counter frames such as `ff ff 00 00`.
- Flush pending serial bytes before CPM and dual-tube counter requests.
- Retry corrupt counter frames after serial resynchronisation.
- Parse compact firmware text such as `GMC-500+Re 1.14` correctly.

# 4.6.9

- Replaced the free-text serial-port field with Home Assistant's dynamic `device(subsystem=tty)` selector.
- The device dropdown lists currently detected serial USB/UART devices and validates that the selected path exists.
- Kept both preconfigured GMC-320 and GMC-500+ profiles fully editable while requiring a separate selected port for each device.
- Preserved all serial resynchronization, staggered polling and GMCMap timing fixes from 4.6.8.

# 4.6.8

- Preconfigured new installations with editable stable profiles for one GMC-320 and one GMC-500+.
- Applied the recommended 60/75-second CPM intervals, 0/15-second startup staggering, 300-second auxiliary polling, conservative command delays and disabled heartbeat/gyro defaults.
- Kept serial device paths and GMCMap identifiers blank because they are host/account-specific; startup now reports exactly which profile still needs a port.
- Kept GMCMap uploads and privacy confirmation opt-in while retaining the recommended 300-second interval and 10-second HTTP timeout.

# 4.6.7

- Consolidated all serial-stability fixes from 4.6.3 through 4.6.6 into one installable release.
- Includes serial resynchronization for contaminated `GETVER`, `GETVOLT`, counter and terminator-framed replies.
- Permanently rejects all-`0xFF` CPM and dual-tube responses and retries them without publishing false measurements.
- Includes deterministic GMCMap upload staggering, a shared connection gap and a safety margin below the 300-second server deadline.
- Includes per-device serial startup staggering and reduced-rate auxiliary polling for stable parallel GMC-320 and GMC-500+ operation.
- Added an install-ready two-device stability example under `examples/gmc-320-gmc-500plus-stable.yaml`.

# 4.6.6

- Added per-device `serial_startup_delay`; when omitted, serial workers start 15 seconds apart.
- Added per-device `auxiliary_read_interval` (default 300 seconds) for temperature, voltage, dual-tube, device-time and gyro commands.
- Kept CPM sampling on the normal `scan_interval` and retained the last valid optional values between auxiliary polls.
- Preserved the independent GMCMap upload staggering and 300-second deadline safety margin.

# 4.6.5

- Reject all-`0xFF` CPM and dual-tube counter replies as serial protocol corruption instead of allowing them to reach the high-CPM confirmation gate.
- Read binary counter replies until idle and use the final complete response width, preventing stale prefix bytes from becoming part of the CPM value.
- Resynchronise and retry malformed counter replies once; persistent corruption now causes a controlled reconnect instead of a false measurement or World Map upload.

# 4.6.4

- Prevent an RFC1801 `GETVOLT` response containing stale binary bytes such as `0xff` from terminating a device worker with `UnicodeDecodeError`.
- Read the complete voltage response until idle, extract a valid ASCII voltage from a contaminated buffer, and retry once after serial resynchronization.
- Preserve the 4.6.3 per-device GMCMap phase staggering and shared connection spacing.

# 4.6.3

- Resynchronize `GETVER` after stale heartbeat/binary bytes and accept a valid GMC ASCII version inside a contaminated response.
- Retry malformed terminator-framed optional commands, including `GETGYRO`, after clearing the serial stream.
- Treat heartbeat cleanup interrupted by normal service shutdown as a clean stop instead of a measurement error.
- Stagger multi-device GMCMap uploads, serialize HTTP connections with a 10-second gap, and keep the effective cadence below the 300-second server deadline.

# 4.6.2

- Aktualisiert den Bereich „Verbundene GMC-Geräte“ alle 20 Sekunden über einen kleinen HTML-Fragment-Endpunkt, ohne die gewählte Geräteanalyse, die URL oder die Scrollposition zu verändern.
- Pausiert die automatische Geräteanzeige im Hintergrund und aktualisiert sie beim Zurückkehren in den Tab beziehungsweise in die Home-Assistant-App sofort.

- Kept the learned local baseline separate for every device and reload it from SQLite whenever the analysis selection changes.
- Split baseline learning from missing recent measurement coverage: an already learned baseline is no longer shown as newly learning after a device switch.
- Added localized status text for an available baseline that is waiting for enough current samples.

# 4.6.1

- Keeps every configured counter online independently while another device’s detail analysis is displayed.
- Persists an explicit per-device runtime connection state from each serial worker instead of deriving availability only from the latest accepted history row.
- A successfully read but temporarily gated high-CPM sample now refreshes the device’s online state without being stored as an accepted measurement.
- Serial failures, reconnect requests, identity changes and service shutdowns update only the affected device’s runtime state.
- Renames the device action to “Show analysis” / “Analysis shown” to make clear that it is a read-only view switch and does not pause another counter.

# 4.6.0

- Reorganized the Home Assistant configuration into a dedicated `devices` list plus shared `gmcmap`, `history`, `analysis`, `safety`, `interface` and `system` sections.
- Removed visible global duplicates of serial, measurement and conversion settings; every physical GMC now owns those values independently.
- Moved the GMCMap upload interval and timeout into the shared GMCMap section while keeping the counter ID per device.
- Added nested configuration translations for all eight supported languages.
- Kept 4.5.x flat options and partial device entries readable as a runtime compatibility fallback; legacy values take precedence until the obsolete keys are removed.

# 4.5.5

- Fixed structured multi-device startup on Home Assistant by preserving `devices` as a JSON array instead of letting Bashio expand the array into individual objects.
- Added explicit validation of the Supervisor options document before starting the bridge.
- Restored simultaneous mixed-model configurations such as a GMC-320 at 19200 baud and a GMC-500+ at 115200 baud.
- Kept legacy `port` and `ports` configurations unchanged.

# 4.5.4

- Reduced the visible GMCMap device details to only the masked counter ID and the last successful upload time.
- Removed the visible last-attempt and next-upload fields while keeping all internal diagnostics and MQTT entities unchanged.
- Preserved the existing responsive two-column desktop and one-column mobile layout.

# 4.5.3

- Simplified the GMCMap device panel in the report dashboard.
- Removed upload counters, consecutive-error count, HTTP status, historical upload-error details and the last server response from the visible report interface.
- Kept the underlying GMCMap diagnostics and MQTT entities unchanged for technical troubleshooting and automation.
- Retained the compact mobile layout with counter ID, last attempt, last successful upload and next upload.

# 4.5.2

- Added a 30-second GMCMap startup grace period so the first reading is not uploaded while networking is still settling.
- Replaced broad response keyword matching with explicit GMCMap rejection detection, avoiding false failures caused by incidental words in HTML.
- Preserved the last upload error and its timestamp after later successful uploads.
- Added separate total and consecutive error counters, last-attempt time, HTTP status and compact server-response diagnostics per device.
- Added the extended GMCMap diagnostics to the responsive report dashboard and Home Assistant MQTT Discovery in all eight UI languages.
- Continued to redact GMCMap account and counter identifiers from errors and server-response diagnostics.

# 4.5.1

- Added a visually consistent external link to the Geiger Counter World Map below GMC Radiation Monitoring.
- The link opens `https://www.gmcmap.com/index.php` in a new browser tab with safe external-link attributes.
- Added responsive hover, focus and mobile styling matching the Home Assistant location panel.

# 4.5.0

- Added structured per-device configuration with independent serial, timing, validation, clock, heartbeat and CPM-conversion settings.
- Added per-device GMCMap counter IDs, upload intervals and network timeouts while retaining the legacy serial-to-counter mapping.
- Preserved backward compatibility with the existing `port` and `ports` options and global defaults.
- Added configured device names to Home Assistant MQTT device identity and the shared dashboard.
- Device-specific analysis and exports now use the selected device's scan interval and CPM-to-dose conversion factor.
- Added localized nested configuration fields and diagnostics in all eight supported languages.

# 4.4.0

- Added optional public GMCMap uploads using the official AID/GID/CPM/ACPM/uSV request format.
- Added independent serial-to-counter-ID mappings for simultaneous multi-device uploads.
- Added non-blocking per-device upload workers, retry backoff, masked identifiers and upload diagnostics.
- Added per-device GMCMap status to the Ingress dashboard and MQTT Discovery.
- GMCMap remains disabled by default and requires explicit public-data confirmation.
- Added localized GMCMap configuration and runtime text in all eight supported languages.

# 4.3.0

- Added RFC1801 device-clock reading and configurable clock-offset diagnostics for supported GMC-500/600 firmware.
- Added optional 1 Hz heartbeat mode with live CPS and rolling 60-second CPM MQTT sensors.
- Corrected GMC-500/600 battery-voltage parsing to the documented five-byte ASCII response while retaining legacy GMC-300/320 decoding.
- Added separate hardware-model and firmware-version diagnostics to MQTT, device cards and report metadata.
- Extended all eight configuration and runtime translations for the new diagnostics.

# 4.2.6

- Mobile analysis cards now reflow into two columns on tablets and one column on phones.
- Page-wide horizontal scrolling is disabled; only dedicated tables and compact controls can scroll horizontally.

- Displays the connected-device section icon in the same icon tile used by analysis headers.
- Keeps each device icon and model name aligned on one horizontal title row.

# 4.2.3

- Redesigned the global report header with compact status chips, a unified control toolbar, and collapsible Home Assistant location details.
- Improved responsive layout for language, analysis-mode, and report-target controls on phones and tablets.
- Preserved all eight localized interfaces without introducing untranslated runtime labels.

# 4.2.0

- Shows the location configured in Home Assistant in the global report settings, including name, coordinates, elevation and country when available.
- Reads location data through the authenticated internal Home Assistant Core API only; no external geocoding service is used.
- Adds complete Croatian (`hr`) translations for the add-on configuration, Ingress dashboard, reports and MQTT Discovery names.
- Uses `homeassistant_api: true` instead of the unused Supervisor API permission.

# 4.1.6

- Completed runtime localization across the dashboard, restore and download flows, device profiles, PDF/PNG reports and MQTT Discovery names.
- Added translations for dynamically generated metric-card and report-format labels in all seven supported UI languages.
- Localized user-facing request and maintenance errors while keeping technical CSV/JSON field identifiers stable for automation compatibility.
- Replaced locale-dependent English weekday/month labels in time-series charts with language-neutral numeric dates.
- Added regression checks for translation-catalog completeness and rendered non-English pages.

# 4.1.5

- Enabled horizontal panning and scrolling in the Ingress dashboard on iPhone and other narrow touch devices.
- Completed localization of analysis cards, data-quality labels, notes, diagnostics, formulas and empty-state messages in all supported UI languages.
- Added regression coverage for mobile overflow behavior and German analysis translations.

# 4.1.4

- Updated package and runtime version metadata to 4.1.4.

- Moved device identity, serial port, profile, capabilities and per-device history statistics into the connected-device cards.
- Reduced the report header to global report and export settings.
- Added per-device analysis selection and report targeting for one device or all devices.
- Added connection state, latest measurement, last update and dual-tube values to device cards.
- Added complete translations for the new multi-device interface.

# 4.0.0

- Added parallel multi-device support using comma-separated stable serial paths.
- Added independent MQTT identities and histories for every GMC serial number.
- Added a shared dashboard overview with the latest value from each device.
- Preserved the legacy single `port` configuration as a fallback.

# Changelog

## 3.3.2

- Replaced the Home Assistant add-on icon with the supplied radiation-monitor icon.
- Shortened the German threshold-profile label to “GQ-Empfehlung” for cleaner card wrapping.
- Updated package and report-server version metadata.

## 3.3.1

- Added `logo1.png` above the README title with a blank alternative text.
- Restored the bold **GMC Radiation Monitor** heading directly below the logo.
- Updated package and report-server version metadata.

## 3.3.0

- Added a dedicated recommendation card that combines absolute thresholds, local anomaly status and trend.
- Improved analysis-page wording, status hierarchy and visual consistency.
- Reworked all supported UI translations for recommendation and assessment text.
- Grouped flat Home Assistant configuration options with translated functional prefixes.
- Rewrote the README as current product documentation and changed the header graphic to an absolute Markdown image URL.
- Updated the add-on store description and regression tests.

## 3.2.1

- Fixed operational event persistence by restoring `insert_operational_event` and `recent_operational_events` as methods of `HistoryStore`.
- Added a regression test for inserting and reading operational events.
- Replaced the README text heading with the bundled `logo1.png` graphic.

## 3.2.0

- Redesigned the analysis page to clearly separate absolute threshold assessment from local background anomaly detection.
- Added a combined interpretation that explains both assessments together.
- Added explicit legends and official-reference guidance.
- Added a 30-minute trend indicator to the local background card.
- Completed the new dashboard terminology in all supported UI languages.

## 3.1.0

- Added GQ, BfS reference, ICRP reference and fully custom threshold profiles.
- Rewrote all add-on configuration translations.
- Reworked README to document only the current feature set and operation.
- Preserved Ingress-safe streaming downloads and GMC-500+ dual-tube support.
