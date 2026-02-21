"""
site_builder/pages/somefun_page.py
====================================
Builds somefun.html — the personal/hobbies page.

Content driven by cfg["somefun"]:
    intro        : opening paragraph
    photography  : {blog_name, blog_url, description}
    rides        : list of {place, description, badge}
    sports       : list of {icon, name, note}
    interests    : list of {icon, title, desc}
"""

from __future__ import annotations

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

/* ── Photography card ── */
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

/* ── Cycling rides ── */
.rides { display:flex; flex-direction:column; gap:9px; }
.ri {
  background:var(--surface); border:1px solid var(--border);
  border-radius:8px; padding:14px 16px;
  display:grid; grid-template-columns:1fr auto; gap:12px; align-items:center;
}
.ri-place { font-size:.9rem; font-weight:500; color:var(--text); }
.ri-desc  { font-size:.82rem; color:var(--text-muted); margin-top:2px; }
.ri-badge {
  font-family:var(--mono); font-size:.62rem; letter-spacing:.05em;
  padding:3px 9px; border-radius:100px;
  background:var(--bg2); border:1px solid var(--border2);
  color:var(--text-dim); white-space:nowrap;
}

/* ── Sports cards ── */
.sports-row { display:flex; gap:11px; flex-wrap:wrap; }
.sc {
  background:var(--surface); border:1px solid var(--border);
  border-radius:8px; padding:14px 18px; min-width:150px;
  transition:border-color .2s;
}
.sc:hover { border-color:var(--accent-mid); }
.sc-icon { font-size:1.7rem; margin-bottom:7px; }
.sc-name { font-size:.9rem; font-weight:500; color:var(--text); margin-bottom:3px; }
.sc-note { font-size:.8rem; color:var(--text-muted); }

/* ── Interests grid ── */
.interests-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:11px; }
.int-card {
  background:var(--surface); border:1px solid var(--border);
  border-radius:8px; padding:16px 18px; transition:border-color .2s;
}
.int-card:hover { border-color:var(--accent-mid); }
.int-icon  { font-size:1.5rem; margin-bottom:8px; }
.int-title { font-size:.9rem; font-weight:500; color:var(--text); margin-bottom:5px; }
.int-desc  { font-size:.84rem; color:var(--text-muted); line-height:1.65; }

/* ── Responsive ── */
@media (max-width:760px) {
  .nav-links     { display:none; }
  .nav-hamburger { display:flex; }
  .interests-grid { grid-template-columns:1fr 1fr; }
  .ri { grid-template-columns:1fr; gap:4px; }
}
@media (max-width:480px) { .interests-grid { grid-template-columns:1fr; } }
</style>"""


# ─────────────────────────────────────────────────────────────────────────────
# Fragment builders
# ─────────────────────────────────────────────────────────────────────────────

_CAMERA_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>'
    '<circle cx="12" cy="13" r="4"/></svg>'
)
_EXTERNAL_ICON = (
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>'
    '<polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
)


def _sub_heading(num: str, title: str) -> str:
    return (
        f'<div class="sh">'
        f'<span class="sh-num">{esc(num)}</span>'
        f'<h2 class="sh-title">{esc(title)}</h2>'
        f'<div class="sh-line"></div>'
        f'</div>'
    )


def _photography_block(photo_cfg: dict) -> str:
    name = esc(photo_cfg.get("blog_name", "Photography Blog"))
    url  = esc(photo_cfg.get("blog_url", "#"))
    desc = esc(photo_cfg.get("description", ""))
    return (
        '<div class="pbc">\n'
        f'  <div class="pbc-icon">{_CAMERA_SVG}</div>\n'
        '  <div class="pbc-body">\n'
        f'    <h3>{name}</h3>\n'
        f'    <p>{desc}</p>\n'
        f'    <a class="pbc-link" href="{url}" target="_blank">'
        f'{_EXTERNAL_ICON} Visit {name} →</a>\n'
        '  </div>\n'
        '</div>'
    )


def _rides_block(rides: list) -> str:
    items = []
    for r in rides:
        items.append(
            f'<div class="ri">\n'
            f'  <div>\n'
            f'    <div class="ri-place">{esc(r["place"])}</div>\n'
            f'    <div class="ri-desc">{esc(r["description"])}</div>\n'
            f'  </div>\n'
            f'  <span class="ri-badge">{esc(r.get("badge", ""))}</span>\n'
            f'</div>'
        )
    return '<div class="rides">\n' + "\n".join(items) + "\n</div>"


def _sports_block(sports: list) -> str:
    cards = []
    for s in sports:
        cards.append(
            f'<div class="sc">\n'
            f'  <div class="sc-icon">{s["icon"]}</div>\n'
            f'  <div class="sc-name">{esc(s["name"])}</div>\n'
            f'  <div class="sc-note">{esc(s["note"])}</div>\n'
            f'</div>'
        )
    return '<div class="sports-row">\n' + "\n".join(cards) + "\n</div>"


def _interests_block(interests: list) -> str:
    cards = []
    for it in interests:
        cards.append(
            f'<div class="int-card">\n'
            f'  <div class="int-icon">{it["icon"]}</div>\n'
            f'  <div class="int-title">{esc(it["title"])}</div>\n'
            f'  <p class="int-desc">{esc(it["desc"])}</p>\n'
            f'</div>'
        )
    return '<div class="interests-grid">\n' + "\n".join(cards) + "\n</div>"


# ─────────────────────────────────────────────────────────────────────────────
# Public builder
# ─────────────────────────────────────────────────────────────────────────────

def build_somefun(cfg: dict) -> str:
    """Return the complete somefun.html as a string."""
    site = cfg["site"]
    sf   = cfg.get("somefun", {})

    page_title = f"Some Fun — {esc(site['author'])}"
    intro      = esc(sf.get("intro", "Life beyond the lab.").strip())

    return "\n".join([
        HTML_HEAD.format(title=page_title, css=SHARED_CSS),
        _SOMEFUN_CSS,
        nav_html(cfg, "somefun"),
        "",
        '<div class="page">',
        '  <div class="page-eyebrow">Beyond the Lab</div>',
        f'  <h1 class="page-title">Some Fun</h1>',
        f'  <p class="page-intro">{intro}</p>',
        "",
        "  " + _sub_heading("01", "Photography"),
        "  " + _photography_block(sf.get("photography", {})),
        "",
        "  " + _sub_heading("02", "Fun With AI"),
        "  " + _photography_block(sf.get("funWithAI", {})),
        #"",
        #"  " + _sub_heading("03", "Sports"),
        #"  " + _sports_block(sf.get("sports", [])),
        #"",
        #"  " + _sub_heading("04", "Other Interests"),
        #"  " + _interests_block(sf.get("interests", [])),
        "</div>",
        "",
        footer_html(cfg),
        MODAL_HTML,
        SHARED_JS,
        "</body>\n</html>",
    ])
