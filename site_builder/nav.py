"""
site_builder/nav.py
===================
Generates the shared <nav> bar and <footer> that appear on every page.

Both functions receive the full config dict so they can pull site-level
values (author name, repo URL, copyright year) without needing extra
arguments.

The *active* parameter identifies which page is currently being rendered
so the correct nav link receives the CSS 'active' class:
    "index"   → highlights Research / Publications / Teaching / Contact anchors
    "gallery" → highlights the Gallery link
    "somefun" → highlights the Some Fun link
"""

from .styles import NAV_CONTROLS
from .utils  import esc


# ─────────────────────────────────────────────────────────────────────────────
# Nav link definitions
# (href, display-label, page-key that should mark it active)
# ─────────────────────────────────────────────────────────────────────────────

_NAV_ITEMS = [
    ("index.html#research",     "Research",     "index"),
    ("index.html#publications", "Publications", "index"),
    ("index.html#teaching",     "Teaching",     "index"),
    ("index.html#contact",      "Contact",      "index"),
    ("gallery.html",            "Gallery",      "gallery"),
    ("somefun.html",            "Some Fun",     "somefun"),
]


def nav_html(cfg: dict, active: str = "index") -> str:
    """
    Return the full <nav> + mobile drawer HTML for a page.

    Parameters
    ----------
    cfg    : full site configuration dict
    active : one of "index", "gallery", "somefun"
    """
    author = esc(cfg["site"]["author"])

    # ── desktop nav links ────────────────────────────────────────────────────
    links_html = ""
    for href, label, page_key in _NAV_ITEMS:
        is_active = active == page_key
        cls = ' class="active"' if is_active else ""
        links_html += f'    <li><a href="{href}"{cls}>{label}</a></li>\n'

    # ── mobile drawer links ──────────────────────────────────────────────────
    drawer_html = ""
    for href, label, _ in _NAV_ITEMS:
        # anchor links inside index should close the drawer
        onclick = ' onclick="closeDrawer()"' if "#" in href else ""
        drawer_html += f'  <a href="{href}"{onclick}>{label}</a>\n'

    return f"""\
<nav>
  <a class="nav-name" href="index.html">{author}</a>
  <ul class="nav-links">
{links_html}  </ul>
{NAV_CONTROLS}
</nav>

<div class="nav-drawer" id="navDrawer">
{drawer_html}</div>"""


# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

def footer_html(cfg: dict) -> str:
    """Return the shared <footer> element."""
    year   = esc(cfg["site"].get("copyright_year", "2024"))
    author = esc(cfg["site"]["author"])
    repo   = cfg["site"].get("github_repo", "#")

    return f"""\
<footer>
  <div class="footer-inner">
    <span class="footer-copy">© {year} {author} & Claude AI · All rights reserved</span>
    <div class="footer-links">
      <a href="index.html">Home</a>
      <a href="gallery.html">Gallery</a>
      <a href="somefun.html">Some Fun</a>
      <a href="{esc(repo)}" target="_blank">Source</a>
    </div>
  </div>
</footer>"""
