# GMC Radiation Monitor 10.0.6

Version 10.0.6 restores the intended always-available mobile dashboard navigation without reintroducing horizontal scrolling. It does not change database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, scientific algorithms or serial protocols.

## Persistent mobile navigation

- Keeps the dashboard navigation tile sticky at the top of the Home Assistant Ingress scroll view.
- Displays the eight section links in a four-column, two-row grid on 320-800 px views.
- Wraps long translated labels inside each link instead of extending the page width.
- Keeps the expand/collapse action below the section-link grid.
- Limits tile height at extreme text enlargement and permits vertical, never horizontal, internal scrolling.
- Uses the actual sticky-tile height when jumping to a section so headings remain visible.

## Regression protection

- Updates the compact mobile fixture and populated full-application Chromium test.
- Scrolls the dashboard and verifies that the tile remains sticky at the top of the scroll viewport.
- Checks computed grid columns, viewport boundaries and the absence of horizontal page or navigation scrolling.
- Covers all eight interface languages, 320-800 px widths and 100%/200% text size.

## Quality command

Run from the repository root:

```bash
python3 quality/run_quality_checks.py
```

Use `--skip-browser` when Chromium/Playwright are unavailable.
