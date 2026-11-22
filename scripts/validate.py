"""Check every app of the store. Exits 1 with a list of problems."""

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
problems: list[str] = []


def need(ok: bool, message: str) -> None:
    if not ok:
        problems.append(message)


apps = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
ids = {a["id"] for a in apps}
need(ids == {p.name for p in (ROOT / "Apps").iterdir() if p.is_dir()}, "apps.json and Apps/ list different apps")

for app in apps:
    app_id = app["id"]
    folder = ROOT / "Apps" / app_id
    compose = yaml.safe_load((folder / "docker-compose.yml").read_text(encoding="utf-8"))
    meta = compose.get("x-casaos") or {}
    for key in ("id", "architectures", "main", "title", "tagline", "description", "icon", "port_map", "category"):
        need(key in meta, f"{app_id}: x-casaos.{key} missing")
    services = compose.get("services") or {}
    need(meta.get("main") in services, f"{app_id}: x-casaos.main is not a service")
    need((folder / "icon.png").is_file(), f"{app_id}: icon.png missing")
    images = [s.get("image", "") for s in services.values()]
    need(any(i.startswith(app["image"] + ":") for i in images), f"{app_id}: no service uses {app['image']}")
    need(not any(i.endswith((":latest", ":edge")) for i in images), f"{app_id}: images must use a release tag")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"{len(apps)} app(s) OK")
