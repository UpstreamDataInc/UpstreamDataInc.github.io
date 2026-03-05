#!/usr/bin/env bash
set -e
poetry run python scripts/gen_nav.py
poetry run zensical serve -a 0.0.0.0:8000
