# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Documentation website for Upstream Data hardware products (loadcenters, mining containers, LoadSync). Built with **Zensical** (a Python static site generator similar to MkDocs Material), deployed to GitHub Pages.

**Live site:** https://docs.upstreamdata.com/

## Build & Development Commands

```bash
# Install dependencies (requires Python >=3.13)
pip install zensical

# Build the site (outputs to site/)
zensical build --clean

# Full dependency install via Poetry
poetry install
```

There are no test or lint commands — this is a content-only documentation site.

## Deployment

Automatic via GitHub Actions on push to `main` or `master`. The workflow (`.github/workflows/docs.yml`) installs zensical, runs `zensical build --clean`, and deploys the `site/` directory to GitHub Pages.

## Architecture

- **`docs/`** — Markdown source files and assets (images, CSS, logos)
- **`docs/guides/`** — All guide content: `initial-setup.md`, `maintenance.md`, `loadsync.md`, `contact.md`
- **`docs/stylesheets/`** — Custom CSS overrides (e.g., `images.css`)
- **`zensical.toml`** — Site configuration: navigation, theme, markdown extensions, metadata
- **`site/`** — Generated output (gitignored, do not edit)

Navigation is defined in `zensical.toml` under `nav`. There are only 4 top-level pages.

## Content Patterns

- **Redirect pages:** `docs/index.md` and `docs/guides/index.md` use `template: redirect` to redirect visitors to subsections.
- **Tabbed content:** Used for alternate setup paths (e.g., Starlink vs LTE). Uses `pymdownx.tabbed` with `=== "Tab Name"` syntax.
- **Admonitions:** `!!! tip`, `!!! warning`, `!!! danger` for callouts. Collapsible with `??? details` / `???+ details` (open by default).
- **Image styling:** Images use the `.fix-png` CSS class via `{ .fix-png }` attribute syntax for consistent sizing.
- **Markdown extensions:** The full list is in `zensical.toml` — includes superfences, tabbed, emoji (custom SVG via zensical), tasklist, caret/tilde/mark for text decoration, captions, snippets, and more.