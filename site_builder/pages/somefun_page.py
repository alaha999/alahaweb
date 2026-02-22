"""
site_builder/pages/somefun_page.py
====================================
Builds somefun.html — the personal/hobbies page.
Zero external dependencies — pure stdlib only.

Content is fully driven by cfg["somefun"]["sections"], a list of section dicts.

Each section requires:
    title     : heading text shown in the collapsible toggle bar
    type      : "blog-box" | "blog-text"
    collapsed : bool — starts collapsed if true (default: false)
    num       : optional display label e.g. "01" (auto-assigned if omitted)

Type-specific fields
--------------------
blog-box  (external link card — for photo blogs, galleries, etc.):
    blog_name   : display name of the blog / gallery
    blog_url    : URL to link to
    description : short description shown in the card

blog-text  (GitHub-rendered Markdown post card):
    description : short intro paragraph shown on the site
    github_url  : full URL to the .md file on GitHub
                  e.g. https://github.com/you/repo/blob/main/blogs/my-post.md
                  GitHub renders it beautifully when the user clicks through.
"""

from __future__ import annotations

import textwrap

from ..styles import SHARED_CSS, HTML_HEAD, MODAL_HTML, SHARED_JS
from ..nav    import nav_html, footer_html
from ..utils  import esc


# ─────────────────────────────────────────────────────────────────────────────
# Page-local CSS
# ─────────────────────────────────────────────────────────────────────────────

_SOMEFUN_CSS = """\
<style>
.page { max-width:var(--max); margin:0 auto; padding:44px 18px 60px; animation:fade-up .5s ease both; }

/* ── Page header ── */
.page-eyebrow {
  font-family:var(--mono); font-size:.7rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent-mid);
  margin-bottom:10px; display:flex; align-items:center; gap:10px;
}
.page-eyebrow::before { content:''; display:block; width:24px; height:1px; background:var(--accent-mid); }
.page-title { font-family:var(--serif); font-size:2.2rem; font-weight:400; color:var(--text); letter-spacing:-.01em; margin-bottom:12px; }
.page-intro { font-size:.97rem; color:var(--text-muted); max-width:560px; line-height:1.8; margin-bottom:44px; }

/* ── Sub-section heading ── */
.sh { display:flex; align-items:baseline; gap:14px; margin-bottom:20px; margin-top:40px; }
.sh:first-of-type { margin-top:0; }
.sh-num   { font-family:var(--mono); font-size:.65rem; letter-spacing:.14em; text-transform:uppercase; color:var(--text-dim); }
.sh-title { font-family:var(--serif); font-size:1.4rem; font-weight:400; color:var(--text); }
.sh-line  { flex:1; height:1px; background:var(--border); }

/* ── Shared card base (used by both blog-box and blog-text) ── */
.pbc {
  background:var(--surface); border:1px solid var(--border);
  border-radius:10px; padding:22px 24px;
  display:flex; align-items:flex-start; gap:20px;
}
.pbc-icon {
  width:48px; height:48px; border-radius:8px;
  background:var(--accent-light);
  border:1px solid color-mix(in srgb, var(--accent) 20%, transparent);
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.pbc-icon svg { width:22px; height:22px; color:var(--accent-mid); }
.pbc-body h3  { font-family:var(--serif); font-size:1.1rem; font-weight:400; color:var(--text); margin-bottom:6px; }
.pbc-body p   { font-size:.88rem; color:var(--text-muted); line-height:1.7; margin-bottom:12px; }
.pbc-link {
  font-family:var(--mono); font-size:.7rem; letter-spacing:.04em;
  color:var(--accent); text-decoration:none;
  display:inline-flex; align-items:center; gap:6px;
  border-bottom:1px solid transparent; transition:border-color .15s;
}
.pbc-link:hover { border-color:var(--accent); }

/* ── Collapsible sections ── */
.collapsible { margin-top:40px; }
.collapsible:first-of-type { margin-top:0; }

.collapsible-header {
  display:flex; align-items:baseline; gap:14px;
  cursor:pointer; user-select:none; margin-bottom:0;
}
.collapsible-header:hover .sh-title { color:var(--accent-mid); }

.collapsible-toggle {
  font-family:var(--mono); font-size:.65rem; color:var(--text-dim);
  margin-left:auto; transition:transform .25s ease; flex-shrink:0; line-height:1;
}
.collapsible-toggle::after { content:'▾'; display:block; }
.collapsible.is-collapsed .collapsible-toggle { transform:rotate(-90deg); }

.collapsible-body {
  overflow:hidden; max-height:9999px;
  transition:max-height .4s ease, opacity .25s ease, padding-top .25s ease;
  opacity:1; padding-top:20px;
}
.collapsible.is-collapsed .collapsible-body { max-height:0; opacity:0; padding-top:0; }

/* ── Collapse-all toolbar ── */
.sections-toolbar {
  display:flex; justify-content:flex-end; margin-bottom:18px;
}
.btn-collapse-all {
  font-family:var(--mono); font-size:.68rem; letter-spacing:.06em;
  color:var(--text-dim); background:none;
  border:1px solid var(--border); border-radius:6px;
  padding:5px 12px; cursor:pointer;
  display:inline-flex; align-items:center; gap:6px;
  transition:color .15s, border-color .15s;
}
.btn-collapse-all:hover { color:var(--accent-mid); border-color:var(--accent-mid); }
.btn-collapse-all svg { width:11px; height:11px; flex-shrink:0; }

/* ── Responsive ── */
@media (max-width:760px) {
  .nav-links     { display:none; }
  .nav-hamburger { display:flex; }
}
</style>"""


# ─────────────────────────────────────────────────────────────────────────────
# Collapsible JS
# ─────────────────────────────────────────────────────────────────────────────

_COLLAPSIBLE_JS = """\
<script>
(function () {
  /* ── per-section toggle ── */
  document.querySelectorAll('.collapsible-header').forEach(function (header) {
    header.addEventListener('click', function () {
      header.closest('.collapsible').classList.toggle('is-collapsed');
      _syncCollapseBtn();
    });
  });

  /* ── collapse-all / expand-all ── */
  var btn = document.getElementById('btn-collapse-all');
  if (btn) {
    btn.addEventListener('click', function () {
      var sections   = document.querySelectorAll('.collapsible');
      var allCollapsed = Array.from(sections).every(function (s) {
        return s.classList.contains('is-collapsed');
      });
      sections.forEach(function (s) {
        if (allCollapsed) s.classList.remove('is-collapsed');
        else              s.classList.add('is-collapsed');
      });
      _syncCollapseBtn();
    });
  }

  function _syncCollapseBtn() {
    var btn = document.getElementById('btn-collapse-all');
    if (!btn) return;
    var sections     = document.querySelectorAll('.collapsible');
    var allCollapsed = Array.from(sections).every(function (s) {
      return s.classList.contains('is-collapsed');
    });
    btn.querySelector('.btn-label').textContent = allCollapsed ? 'Expand All' : 'Collapse All';
    /* flip the chevron SVG */
    var icon = btn.querySelector('svg');
    if (icon) icon.style.transform = allCollapsed ? 'rotate(-90deg)' : '';
  }

  _syncCollapseBtn();
})();
</script>"""


# ─────────────────────────────────────────────────────────────────────────────
# SVG icons
# ─────────────────────────────────────────────────────────────────────────────

_CAMERA_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>'
    '<circle cx="12" cy="13" r="4"/></svg>'
)

_DOC_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
    '<polyline points="14 2 14 8 20 8"/>'
    '<line x1="16" y1="13" x2="8" y2="13"/>'
    '<line x1="16" y1="17" x2="8" y2="17"/>'
    '<polyline points="10 9 9 9 8 9"/></svg>'
)

_EXTERNAL_ICON = (
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>'
    '<polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
)


# ─────────────────────────────────────────────────────────────────────────────
# Content renderers
# ─────────────────────────────────────────────────────────────────────────────

def _render_blog_box(section: dict) -> str:
    """External link card — for photo blogs, galleries, or any external URL."""
    name = esc(section.get("blog_name", "Blog"))
    url  = esc(section.get("blog_url", "#"))
    desc = esc(section.get("description", ""))
    return (
        '<div class="pbc">\n'
        f'  <div class="pbc-icon">{_CAMERA_SVG}</div>\n'
        '  <div class="pbc-body">\n'
        f'    <h3>{name}</h3>\n'
        f'    <p>{desc}</p>\n'
        f'    <a class="pbc-link" href="{url}" target="_blank" rel="noopener">'
        f'{_EXTERNAL_ICON} Visit {name} →</a>\n'
        '  </div>\n'
        '</div>'
    )


def _render_blog_text(section: dict) -> str:
    """Card with a short description and a link to the .md file on GitHub,
    where it will be rendered natively by GitHub's Markdown viewer."""
    title      = esc(section.get("title", "Read more"))
    desc       = esc(section.get("description", ""))
    github_url = esc(section.get("github_url", "#"))
    return (
        '<div class="pbc">\n'
        f'  <div class="pbc-icon">{_DOC_SVG}</div>\n'
        '  <div class="pbc-body">\n'
        f'    <h3>{title}</h3>\n'
        f'    <p>{desc}</p>\n'
        f'    <a class="pbc-link" href="{github_url}" target="_blank" rel="noopener">'
        f'{_EXTERNAL_ICON} Read on GitHub →</a>\n'
        '  </div>\n'
        '</div>'
    )


_RENDERERS = {
    "blog-box":  _render_blog_box,
    "blog-text": _render_blog_text,
}


# ─────────────────────────────────────────────────────────────────────────────
# Collapsible section wrapper
# ─────────────────────────────────────────────────────────────────────────────

def _collapsible_section(num: str, title: str, body_html: str, collapsed: bool) -> str:
    state = " is-collapsed" if collapsed else ""
    return textwrap.dedent(f"""\
        <div class="collapsible{state}">
          <div class="collapsible-header sh">
            <span class="sh-num">{esc(num)}</span>
            <h2 class="sh-title">{esc(title)}</h2>
            <div class="sh-line"></div>
            <span class="collapsible-toggle"></span>
          </div>
          <div class="collapsible-body">
            {body_html}
          </div>
        </div>""")


# ─────────────────────────────────────────────────────────────────────────────
# Public builder
# ─────────────────────────────────────────────────────────────────────────────

def build_somefun(cfg: dict) -> str:
    """Return the complete somefun.html as a string."""
    site     = cfg["site"]
    sf       = cfg.get("somefun", {})
    sections = sf.get("sections", [])

    page_title = f"Some Fun — {esc(site['author'])}"
    intro      = esc(sf.get("intro", "Life beyond the lab.").strip())

    section_parts = []
    for idx, sec in enumerate(sections):
        sec_type  = sec.get("type", "blog-text")
        title     = sec.get("title", sec_type)
        num       = sec.get("num", f"{idx + 1:02d}")
        collapsed = sec.get("collapsed", False)

        renderer = _RENDERERS.get(sec_type)
        if renderer is None:
            section_parts.append(
                f'<!-- unknown section type "{esc(sec_type)}" — '
                f'use "blog-box" or "blog-text" -->'
            )
            continue

        body_html = renderer(sec)
        section_parts.append(_collapsible_section(num, title, body_html, collapsed))

    sections_html = "\n\n  ".join(section_parts)

    # Collapse-all toolbar SVG (chevrons-up icon, inline)
    _chevrons_svg = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"'
        ' style="transition:transform .25s ease">'
        '<polyline points="17 11 12 6 7 11"/>'
        '<polyline points="17 18 12 13 7 18"/></svg>'
    )
    toolbar_html = (
        '<div class="sections-toolbar">'
        f'<button id="btn-collapse-all" class="btn-collapse-all">'
        f'{_chevrons_svg}'
        f'<span class="btn-label">Collapse All</span>'
        f'</button></div>'
    )

    return "\n".join([
        HTML_HEAD.format(title=page_title, css=SHARED_CSS),
        _SOMEFUN_CSS,
        nav_html(cfg, "somefun"),
        "",
        '<div class="page">',
        '  <div class="page-eyebrow">Beyond the Lab</div>',
        '  <h1 class="page-title">Some Fun</h1>',
        f'  <p class="page-intro">{intro}</p>',
        "",
        f"  {toolbar_html}",
        f"  {sections_html}",
        "</div>",
        "",
        footer_html(cfg),
        MODAL_HTML,
        SHARED_JS,
        _COLLAPSIBLE_JS,
        "</body>\n</html>",
    ])
