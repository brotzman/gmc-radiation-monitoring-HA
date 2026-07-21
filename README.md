# GMC Radiation Monitor - Home Assistant App Repository

This repository contains the **GMC Radiation Monitor** Home Assistant App for compatible GQ GMC Geiger counters.

The app reads counters through USB serial, publishes entities with MQTT Discovery, stores local history and provides an Ingress dashboard for analysis, reports, diagnostics, backup and export.

## Repository layout

```text
.
├── repository.yaml
├── .github/workflows/
└── gmc_radiation_monitor/
    ├── config.yaml
    ├── Dockerfile
    ├── DOCS.md
    ├── README.md
    ├── CHANGELOG.md
    ├── apparmor.txt
    ├── icon.png
    ├── logo.png
    ├── rootfs/
    └── translations/
```

This follows the official Home Assistant App repository model: repository metadata is stored at the Git root and each app lives in its own folder.

## Installation

This app requires a Home Assistant installation with the Supervisor app store, such as Home Assistant OS or a supported Supervised installation.

1. Push this repository to `https://github.com/brotzman/gmc-homeassistant` or keep that URL when using the prepared repository.
2. In Home Assistant, open **Settings > Apps > App store**.
3. Open **Repositories**, add `https://github.com/brotzman/gmc-homeassistant`, and reload the store.
4. Install **GMC Radiation Monitor**.
5. Connect the supported GMC counter over USB and configure the app.

[Open the repository dialog in Home Assistant](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fbrotzman%2Fgmc-homeassistant)

## Installation troubleshooting

Version 8.3.3 intentionally has no `image:` entry in the app configuration. If Home Assistant still tries to pull `ghcr.io/brotzman/gmc-radiation-monitor`, refresh the app repository metadata and verify that GitHub contains the 8.3.3 commit. Removing and re-adding the custom repository can clear stale metadata; existing app data should be backed up before uninstalling an installed instance.

## Home Assistant architecture

GMC Radiation Monitor is intentionally packaged as a **Home Assistant App** rather than a `custom_components` integration. It needs Supervisor-managed UART access, a dedicated container, Ingress, persistent app storage and an AppArmor profile. Home Assistant entities are provided through MQTT Discovery, while the app also uses the Home Assistant API where required.

A separate custom integration would duplicate the device and entity model and would not replace the Supervisor permissions needed for USB serial access.

## App documentation

- [App overview](gmc_radiation_monitor/README.md)
- [Full documentation](gmc_radiation_monitor/DOCS.md)
- [Changelog](gmc_radiation_monitor/CHANGELOG.md)
- [Release notes 8.3.3](gmc_radiation_monitor/RELEASE_NOTES_8.3.3.md)

## Development and publishing

Pull requests and pushes run the Home Assistant app linter, the project quality suite and non-publishing source builds for `aarch64` and `amd64`. Home Assistant installs the app by building the included Dockerfile locally; no GitHub Container Registry package or credentials are required.

## Safety notice

This software is intended for monitoring and home automation. It is not a calibrated radiation-protection instrument and does not replace official measurements, professional advice or emergency instructions.

## Version 8.3.3 highlights

- Detector and calibration details are visible directly in each main-dashboard device card.
- Summary, Analysis and Expert levels progressively expose tube model, conversion factor, dead time, reliable CPM limit, uncertainty and calibration reference.
- GMC-500+ supports independent M4011 and SI-3BG profiles through separate-channel or piecewise-curve modes.
- Missing high-dose calibration is reported as incomplete, and the M4011 factor is never silently applied to SI-3BG counts.
- Analysis JSON, integrated-dose processing and the eight bundled manuals are updated for version 8.3.3.
