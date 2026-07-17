# Version 8.0.13

Version 8.0.13 is a repository and distribution maintenance release. It converts the package from a single app-directory archive into a GitHub-ready Home Assistant App repository while preserving the application runtime and user-visible behavior.

## Official Home Assistant repository layout

- places `repository.yaml` at the Git repository root
- stores the complete app in the unique `gmc_radiation_monitor/` folder
- keeps `config.yaml`, `Dockerfile`, `rootfs/`, translations, AppArmor policy, icons, documentation and changelog together inside the app folder
- adds the Home Assistant-standard `DOCS.md` alongside the app `README.md`
- ensures the repository root does not contain an app `config.yaml`, so Supervisor discovers exactly one app

## GitHub publishing and quality automation

- adds the official Home Assistant app linter workflow
- adds official Home Assistant multi-architecture builder actions for `aarch64` and `amd64`
- publishes the generic multi-architecture image as `ghcr.io/brotzman/gmc-radiation-monitor` on pushes to the canonical `main` branch
- retains the existing Ruff, mypy, Bandit, dependency, test, coverage, browser and repository-security checks
- adds Dependabot configuration, issue forms, a pull-request template, contribution guidance and a security policy

## Home Assistant integration model

GMC Radiation Monitor remains a Home Assistant App rather than a `custom_components` integration. Supervisor-managed UART access, Ingress, persistent app storage and AppArmor require the app container model. Home Assistant entities continue to be created through MQTT Discovery, and the Home Assistant API remains available to the app where needed.

No duplicate custom integration is included because it would not replace the required Supervisor permissions and would create a second, conflicting device/entity ownership path.

## Version consistency

- updates app and runtime versions to 8.0.13
- updates all eight integrated illustrated manuals, filenames, visible version labels and PDF metadata
- adds release regression tests for repository discovery, app metadata, image publishing and workflow placement

## Compatibility

No migration is required. Existing options, measurements, SQLite history, backups, reports, MQTT entity identifiers, serial-device behavior and Ingress URLs remain compatible. After pushing the repository to GitHub, add the repository URL to the Home Assistant App store and install or update the app normally.
