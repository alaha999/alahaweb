#!/usr/bin/env python3
"""
build_site.py
=============
Entry point for the Arnab Laha personal website generator.

Usage
-----
    python build_site.py                          # defaults below
    python build_site.py --output ./dist          # write to a different directory
    python build_site.py --config site_config/config.yaml --output .

What this script does
---------------------
1. Loads site content from a YAML config file (default: site_config/config.yaml).
2. Calls the site_builder package to generate all HTML pages.
3. Writes the output files to the specified output directory.

Anything you want to change about the *look* of the site lives in:
    site_builder/styles.py   <- CSS, shared JS, modal HTML
    site_builder/nav.py      <- nav bar and footer structure

Anything you want to change about the *content* of the site lives in:
    site_config/config.yaml  <- all text, links, publications, photos, etc.

Requirements
------------
    pip install pyyaml
"""

import argparse
import sys
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Dependency check
# ─────────────────────────────────────────────────────────────────────────────

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required.  Run: pip install pyyaml")
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Config loader
# ─────────────────────────────────────────────────────────────────────────────

def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}")
        sys.exit(1)
    with config_path.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not cfg:
        print(f"ERROR: Config file is empty: {config_path}")
        sys.exit(1)
    return cfg


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the personal website from a YAML config.",
    )
    parser.add_argument(
        "--config",
        default="site_config/config.yaml",
        metavar="PATH",
        help="Path to the YAML config file (default: site_config/config.yaml)",
    )
    parser.add_argument(
        "--output",
        default=".",
        metavar="DIR",
        help="Output directory for generated HTML files (default: current directory)",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    output_dir  = Path(args.output)

    print(f"  Config : {config_path.resolve()}")
    print(f"  Output : {output_dir.resolve()}")
    print()

    cfg = load_config(config_path)

    # Import here so error messages above always appear first
    from site_builder import build_all
    written = build_all(cfg, output_dir)

    for path in written:
        print(f"  ✓  {path}")

    print()
    print(f"✅  Built {len(written)} pages -> {output_dir.resolve()}")
    print("   Open index.html in your browser to preview.")


if __name__ == "__main__":
    main()
