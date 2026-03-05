#!/usr/bin/env python3
"""Generates zensical.toml with auto-discovered changelog nav from the template."""

import tomllib
from pathlib import Path

import tomli_w

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
BASE_CONFIG = ROOT / "zensical.toml.template"
BUILD_CONFIG = ROOT / "zensical.toml"

# Top-level pages in desired display order (paths relative to docs/)
STATIC_NAV = [
    "index.md",
    "maintenance.md",
    "loadsync.md",
    "contact.md",
]


def discover_changelogs() -> list[str]:
    """Return changelog paths relative to docs/, index.md first then sorted by name."""
    d = DOCS / "changelogs" / "loadsync"
    if not d.exists():
        return []
    files = sorted(d.glob("*.md"), key=lambda p: (p.stem != "index", p.stem))
    return [str(f.relative_to(DOCS)) for f in files]


def main() -> None:
    with BASE_CONFIG.open("rb") as f:
        config = tomllib.load(f)

    changelogs = discover_changelogs()

    nav: list = list(STATIC_NAV)
    if changelogs:
        nav.append({"Changelog": list(changelogs)})

    config["project"]["nav"] = nav

    BUILD_CONFIG.write_text(tomli_w.dumps(config))


if __name__ == "__main__":
    main()
