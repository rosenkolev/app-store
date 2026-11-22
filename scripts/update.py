"""Move every app in apps.json to the latest release of its repository.

Updates the image tag in the CasaOS and Runtipi files and the Runtipi version
(tipi_version goes up by one). Prints the apps that changed. Needs GITHUB_TOKEN
for the GitHub API (any token; the workflow token works).
"""

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def latest_release(repository: str) -> str | None:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repository}/releases/latest",
        headers={"Accept": "application/vnd.github+json"},
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            tag = json.load(resp)["tag_name"]
    except urllib.error.HTTPError as err:
        if err.code == 404:  # no release yet
            return None
        raise
    return tag[1:] if tag.startswith("v") else tag


def set_image_tag(path: Path, image: str, version: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new = re.sub(rf"{re.escape(image)}:[\w.\-]+", f"{image}:{version}", text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> int:
    apps = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
    changed = []
    for app in apps:
        version = latest_release(app["repository"])
        if not version:
            print(f"{app['id']}: no release", file=sys.stderr)
            continue
        casaos = ROOT / "casaos" / app["id"] / "docker-compose.yml"
        runtipi = ROOT / "apps" / app["id"]
        updated = set_image_tag(casaos, app["image"], version)
        updated |= set_image_tag(runtipi / "docker-compose.json", app["image"], version)
        config_path = runtipi / "config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if config.get("version") != version:
            config["version"] = version
            config["tipi_version"] = int(config.get("tipi_version", 0)) + 1
            config["updated_at"] = int(time.time() * 1000)
            config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            updated = True
        if updated:
            changed.append(f"{app['id']} {version}")
    print("\n".join(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
