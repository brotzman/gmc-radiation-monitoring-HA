# GMC Radiation Monitor 10.0.4

Version 10.0.4 is a focused runtime hotfix. It does not change database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, scientific algorithms, responsive layout or serial protocols.

## Fixed device startup failure

- Restores the missing standard-library `time` import in `history_models.py`.
- Prevents the GMC worker thread from terminating when the automatic runtime probe stores detected device capabilities without an explicit timestamp.
- Restores normal continuation from automatic serial discovery through capability persistence and measurement acquisition.

## Regression protection

- Adds an integration test for `HistoryStore.set_device_capabilities()` using the same default-timestamp path that failed in production.
- Adds an undefined-global inspection for source-defined functions in the modules extracted during the 10.0.2 and 10.0.3 maintenance work.
- Raises the repeatable unit/integration test count from 17 to 19.

## Quality command

Run from the repository root:

```bash
python3 quality/run_quality_checks.py
```

Use `--skip-browser` when Chromium/Playwright are unavailable.
