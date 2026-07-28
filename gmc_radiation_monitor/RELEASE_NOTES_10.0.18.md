# GMC Radiation Monitor 10.0.18

Version 10.0.18 replaces the separate floating desktop and mobile navigation with a single compact section dropdown in the application header. The selector is positioned directly below the connection-status badge and contains grouped, symbol-prefixed destinations for all main dashboard areas.

The selected entry follows the visible section while scrolling, and choosing an entry jumps directly to that section without filling the browser history. The global expand/collapse action remains available as a small content utility control rather than part of the navigation. Obsolete floating-menu markup, mobile-sheet behavior, scroll-direction state and CSS were removed.

Database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, scientific algorithms, serial protocols and existing app options remain compatible.
