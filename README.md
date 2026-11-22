# App store

Self-hosted apps for CasaOS and [Docker Apps](https://github.com/rosenkolev/home-assistant-docker-integration)
(Home Assistant). App versions follow the apps' releases automatically.

| App | Description |
| - | - |
| [Bluetooth to Speaker](https://github.com/rosenkolev/bluetooth-to-speaker) | Turn your server into a Bluetooth speaker, with DLNA playback and Home Assistant controls |

## Add the store

| Platform | Where | URL |
| - | - | - |
| **Docker Apps** (Home Assistant) | **Settings > Devices & services > Docker Apps > Add app store repository**, format CasaOS | `https://github.com/rosenkolev/app-store` |
| **CasaOS** | **App Store > More apps > Add source** | `https://github.com/rosenkolev/app-store/archive/refs/heads/main.zip` |

## Home Assistant OS

Home Assistant OS cannot run these as Docker containers. Bluetooth to Speaker is also a
Home Assistant add-on: add `https://github.com/rosenkolev/bluetooth-to-speaker` in
**Settings > Add-ons > Add-on store > ⋮ > Repositories**.

## Layout

```text
apps.json                    the apps and the repositories they are released from
Apps/<app>/                  docker-compose.yml with x-casaos, icon.png
.github/workflows/store.yml  checks every app; daily, moves apps to their latest release
```

## Updates

The **Store** workflow runs daily: when an app has a new release, it sets the new image tag
and commits. CasaOS and Docker Apps then offer the update.

## Add an app

1. Add it to `apps.json`.
2. Add `Apps/<app>/docker-compose.yml` with `x-casaos` and an `icon.png` (see the existing app).
3. Open a pull request: the **Store** workflow checks it.
