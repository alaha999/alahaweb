"""
site_builder — modular static site generator for Arnab Laha's personal website.

Package layout
--------------
site_builder/
    __init__.py        ← this file; exposes the public build API
    utils.py           ← HTML helpers: escaping, links, pills, modals
    styles.py          ← static blobs: CSS, shared JS, nav control HTML, modal HTML
    nav.py             ← nav_html() and footer_html() (structure, not content)
    pages/
        __init__.py
        index_page.py  ← build_index(cfg) → str
        gallery_page.py← build_gallery(cfg) → str
        somefun_page.py← build_somefun(cfg) → str

Entry point
-----------
Call build_all(cfg, output_dir) from build_site.py.
"""

from .pages.index_page   import build_index
from .pages.gallery_page import build_gallery
from .pages.somefun_page import build_somefun

__all__ = ["build_index", "build_gallery", "build_somefun"]


def build_all(cfg: dict, output_dir) -> list[str]:
    """
    Build all HTML pages from *cfg* and write them to *output_dir*.

    Returns a list of written file paths (as strings).
    """
    from pathlib import Path

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.html":   build_index(cfg),
        "gallery.html": build_gallery(cfg),
        "somefun.html": build_somefun(cfg),
    }

    written = []
    for filename, content in pages.items():
        path = out / filename
        path.write_text(content, encoding="utf-8")
        written.append(str(path))

    return written
