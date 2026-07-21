# GMC Radiation Monitor 8.3.2

## Usability and report-layout patch

Version 8.3.2 improves the dashboard guidance and corrects several presentation problems in the professional PDF report. Database, analysis-schema and metrology-algorithm compatibility with 8.3.x is retained.

## Dashboard usability

- The selected information level now shows its explanation directly instead of hiding it only in a tooltip.
- The explanation updates immediately when Summary, Analysis or Expert view is selected and remains accessible to screen readers.
- Report downloads now include a visible format guide explaining when to use the PDF, reproducible ZIP package or CSV export.
- Touch targets for view controls and actions are enlarged on small displays.
- The app title wraps cleanly on narrow phones, while the language chooser remains independently scrollable without widening the whole page.

## PDF report corrections

- The page-1 assessment is placed in a dedicated panel with a protected gap below the chart, preventing overlap with the chart x-axis label.
- Reports for a day or week still in progress stop the visible time axis at the generation time instead of displaying future hours as a large empty area.
- The report shows an explicit data-through timestamp beside the primary chart.
- A one-day daily comparison uses a centered single-date axis instead of Matplotlib's misleading multi-year auto-range.
- Layout constants and regression tests protect the chart-to-assessment spacing.

## Scientific scope

The report remains an interpretation of combined beta/gamma count-rate measurements. CPM is the primary measurement, and derived µSv/h values are not independent or official dosimetry.

## Retained professional report and history controls

- The established five-page professional report remains available, with **Count rate [CPM]** as its primary charted quantity and explicit wording that a Geiger-Müller tube provides a **combined beta/gamma response**.
- Protected history maintenance continues to use the single `history_management_enabled` control.
