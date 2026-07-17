# Version 8.0.14

Version 8.0.14 is an installation reliability release for the official Home Assistant App repository layout.

## Fixed

- Removed the mandatory `image: ghcr.io/brotzman/gmc-radiation-monitor` setting from `config.yaml`.
- Home Assistant now builds the app directly from the included Dockerfile instead of requiring anonymous access to a pre-published GHCR package.
- This prevents installation failures with `error from registry: denied` when the package does not exist yet, is private or has not been made publicly readable.
- Replaced the registry-publishing workflow with a source-build verification workflow for `amd64` and `aarch64`.
- Added release checks that reject an accidental mandatory external image dependency.

## Compatibility

Measurements, serial communication, SQLite history, MQTT Discovery, Ingress routes, dashboard behavior, configuration options and stored data remain unchanged.

## Distribution note

The repository remains a standard Home Assistant App repository. A public multi-architecture registry image can be added again later, but only after the package has been published successfully and explicitly made public. The source-build distribution does not require GitHub Container Registry credentials.
