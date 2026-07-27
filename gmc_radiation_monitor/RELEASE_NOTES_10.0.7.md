# GMC Radiation Monitor 10.0.7

Version 10.0.7 fixes concurrent atomic writes of the acquisition bridge heartbeat. It does not change database schema 8, stored measurements, MQTT entity identities, detector profiles, alarm thresholds, dose conversion, scientific algorithms, serial protocols or the mobile navigation layout.

## Heartbeat write correction

- Serializes periodic liveness writes and immediate supervisor-state writes.
- Uses a unique temporary file for each operation instead of one shared PID-only path.
- Creates temporary files with restrictive mode-0600 permissions in the same `/data` directory as the final heartbeat.
- Flushes and synchronizes the JSON content before atomically replacing the final file.
- Removes residual temporary files after successful or failed operations.
- Prevents transient `No such file or directory` warnings caused by one thread moving another thread's temporary source.

## Regression protection

- Verifies that sequential writes receive different temporary paths.
- Executes 24 simultaneous heartbeat updates and validates the final JSON record.
- Confirms that no temporary files remain and no write error is recorded.
- Raises the repeatable suite to 21 unit and integration tests.

## Quality command

Run from the repository root:

```bash
python3 quality/run_quality_checks.py
```

Use `--skip-browser` when Chromium/Playwright are unavailable.
