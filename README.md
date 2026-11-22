# App store

Self-hosted apps for CasaOS, Runtipi and [Docker Apps](https://github.com/rosenkolev/home-assistant-docker-integration)
(Home Assistant). One store, three formats; app versions follow the apps' releases automatically.

| App | Description |
| - | - |
| [Bluetooth to Speaker](https://github.com/rosenkolev/bluetooth-to-speaker) | Turn your server into a Bluetooth speaker, with DLNA playback and Home Assistant controls |

## Add the store

| Platform | Where | URL |
| - | - | - |
| **Docker Apps** (Home Assistant) | **Settings > Devices & services > Docker Apps > Add app store repository**, format CasaOS | `https://github.com/rosenkolev/app-store` |
| **CasaOS** | **App Store > More apps > Add source** | `https://github.com/rosenkolev/app-store/releases/download/casaos/casaos-store.zip` |
| **Runtipi** | **Settings > App stores > Add a store** | `https://github.com/rosenkolev/app-store` |

## Home Assistant OS

Home Assistant OS cannot run these as Docker containers. Bluetooth to Speaker is also a
Home Assistant add-on: add `https://github.com/rosenkolev/bluetooth-to-speaker` in
**Settings > Add-ons > Add-on store > ⋮ > Repositories**.

## Layout

```text
apps.json                    the apps and the repositories they are released from
casaos/<app>/                CasaOS: docker-compose.yml with x-casaos, icon.png
apps/<app>/                  Runtipi: config.json, docker-compose.json, metadata/
scripts/update.py            moves apps to their latest release
scripts/validate.py          checks every app
```

CasaOS reads a zip with `Apps/<app>/` at the top. The **Publish** workflow builds it from
`casaos/` (the folder names `Apps` and `apps` would clash on Windows and macOS) and attaches it
to the `casaos` release.

## Updates

The **Publish** workflow runs daily: when an app has a new release, it sets the new image tag in
both formats, raises the Runtipi version, commits, and rebuilds the CasaOS archive. Platforms then
offer the update.

## Add an app

1. Add it to `apps.json`.
2. Add `casaos/<app>/` and `apps/<app>/` (see the existing app).
3. Run `python scripts/validate.py`.
