"""Check every app of the store: the files each store format needs, and that the
CasaOS and Runtipi entries use the same image. Exits 1 with a list of problems."""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
problems: list[str] = []


def need(ok: bool, message: str) -> None:
    if not ok:
        problems.append(message)


def images(text: str) -> set[str]:
    return set(re.findall(r"ghcr\.io/[\w./-]+:[\w.\-]+|docker\.io/[\w./-]+:[\w.\-]+", text))


apps = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
ids = {a["id"] for a in apps}
need(ids == {p.name for p in (ROOT / "casaos").iterdir() if p.is_dir()}, "apps.json and casaos/ list different apps")
need(ids == {p.name for p in (ROOT / "apps").iterdir() if p.is_dir()}, "apps.json and apps/ list different apps")

for app in apps:
    app_id = app["id"]
    # CasaOS
    compose_path = ROOT / "casaos" / app_id / "docker-compose.yml"
    compose_text = compose_path.read_text(encoding="utf-8")
    compose = yaml.safe_load(compose_text)
    meta = compose.get("x-casaos") or {}
    for key in ("id", "architectures", "main", "title", "tagline", "description", "icon", "port_map", "category"):
        need(key in meta, f"casaos/{app_id}: x-casaos.{key} missing")
    need(meta.get("main") in (compose.get("services") or {}), f"casaos/{app_id}: x-casaos.main is not a service")
    need((ROOT / "casaos" / app_id / "icon.png").is_file(), f"casaos/{app_id}: icon.png missing")
    # Runtipi
    folder = ROOT / "apps" / app_id
    config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
    for key in ("name", "id", "available", "short_desc", "author", "port", "categories", "description",
                "tipi_version", "version", "source", "supported_architectures"):
        need(key in config, f"apps/{app_id}: config.json {key} missing")
    need(config.get("id") == app_id, f"apps/{app_id}: config.json id differs from the folder name")
    dynamic_text = (folder / "docker-compose.json").read_text(encoding="utf-8")
    dynamic = json.loads(dynamic_text)
    need(any(s.get("isMain") for s in dynamic.get("services", [])), f"apps/{app_id}: no main service")
    need((folder / "metadata" / "logo.jpg").is_file(), f"apps/{app_id}: metadata/logo.jpg missing")
    need((folder / "metadata" / "description.md").is_file(), f"apps/{app_id}: metadata/description.md missing")
    # Same release everywhere
    casaos_images, runtipi_images = images(compose_text), images(dynamic_text)
    need(casaos_images == runtipi_images, f"{app_id}: images differ: {casaos_images} vs {runtipi_images}")
    for image in casaos_images:
        need(image.rsplit(":", 1)[1] == config.get("version"), f"{app_id}: image tag differs from version {config.get('version')}")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"{len(apps)} app(s) OK")
