# GMC Radiation Monitor 9.4.0

Version 9.4.0 consolidates the navigation introduced in 9.3.0. It keeps all existing GMC measurements, cards, diagrams, calculations and reports, while making the detail level truly global and relocating long-term interpretation cards to the Long-term view. The database schema remains version 8.

## Global view level in the sidebar

- Moves Summary, Analysis and Expert view into a dedicated **View** category in the persistent sidebar.
- Applies the selected detail level across Overview, Analysis, Long-term, History, Workflows, Calibration, Reports and History management.
- Stores the selection in the current browser and no longer changes it automatically when an internal section link is opened.
- Keeps a concise, dynamically updated explanation of the selected level directly in the sidebar.
- Retains the existing tier semantics: Summary hides supporting tools, Analysis adds practical detail, and Expert view exposes statistical values, confidence intervals and diagnostics.

## Long-term interpretation structure

- Moves **Intelligent radiation analysis**, **Adaptive background profile** and **Cosmic influence - statistical indication** from Overview into the Long-term view.
- Groups the three cards in a dedicated long-term interpretation context without duplicating calculations or stored data.
- Keeps the live device cards and fleet summary on Overview for a clearer daily-monitoring page.
- Updates direct hash routing so links to the moved cards open the Long-term view.

## Visual harmonisation

- Replaces the yellow-orange sidebar highlight with the dashboard's established blue primary accent.
- Harmonises brand icon, active navigation item, group labels, view-level controls and utility button with existing dashboard buttons, selected device cards and focus styling.
- Adds compact sidebar-specific typography, spacing and wrapping for all three view-level choices.
- Preserves light/dark colour-scheme support, keyboard focus, reduced motion and mobile safe-area behaviour.

## Localisation and documentation

- Adds complete wording for the global view-level description and long-term interpretation context in all eight interface languages.
- Updates all eight user manuals to version 9.4.0 and documents the global sidebar view selector, the revised Overview, and the relocated long-term interpretation cards.

## Compatibility

- Database schema remains version 8.
- Serial acquisition, device detection, safety thresholds, MQTT entity identities, GMCMap handling, reports, calibration profiles and stored history remain compatible with existing 9.x installations.

## Preserved scientific and operational baseline

The release continues to include measurement freshness, report presets, copy-safe support-diagnostics and database schema 8 from the established 9.x architecture.
