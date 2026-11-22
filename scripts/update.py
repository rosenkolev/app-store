"""Move every app in apps.json to the latest release of its repository.

Sets the image tag in Apps/<app>/docker-compose.yml. Prints the apps that changed.
Uses GITHUB_TOKEN for the GitHub API when set (the workflow token works).
"""

import json
import os
import re
import sys
import urllib.error
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


def main() -> int:
    apps = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
    changed = []
    for app in apps:
        version = latest_release(app["repository"])
        if not version:
            print(f"{app['id']}: no release", file=sys.stderr)
            continue
        path = ROOT / "Apps" / app["id"] / "docker-compose.yml"
        text = path.read_text(encoding="utf-8")
        new = re.sub(rf"{re.escape(app['image'])}:[\w.\-]+", f"{app['image']}:{version}", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed.append(f"{app['id']} {version}")
    print("\n".join(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
