# Contributing

1. Create a focused branch from `main`.
2. Keep repository metadata at the Git root and app files inside `gmc_radiation_monitor/`.
3. Run the test and quality commands from the app directory.
4. Update tests, documentation and the changelog for user-visible changes.
5. Open a pull request and describe compatibility and migration impact.

## Local quality checks

```bash
cd gmc_radiation_monitor
python -m compileall -q rootfs/usr/local/bin rootfs/usr/local/lib/gmc_bridge
ruff check rootfs/usr/local/bin rootfs/usr/local/lib/gmc_bridge tests
mypy
pytest -q
```

Browser tests additionally require Playwright browsers. Hardware-facing changes should include simulated serial coverage and, where possible, a smoke test with a supported physical counter.
