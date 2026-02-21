"""
site_builder/pages/gallery_page.py
====================================
Builds gallery.html — a filterable, lightbox-enabled photo gallery.

Content driven entirely by cfg["gallery"]:
    description : page subtitle text
    categories  : list of tag strings used as filter buttons
    photos      : list of {src, caption, tag} dicts

Add more photos by appending entries to cfg["gallery"]["photos"] in config.yaml.
"""

from __future__ import annotations

from ..styles import SHARED_CSS, HTML_HEAD, MODAL_HTML, SHARED_JS
from ..nav    import nav_html, footer_html
from ..utils  import esc


# ─────────────────────────────────────────────────────────────────────────────
# Page-local CSS
# ─────────────────────────────────────────────────────────────────────────────

_GALLERY_CSS = """\
<style>
/* ── Page header ── */
.page-header {
  max-width:var(--max); margin:0 auto; padding:44px 18px 0;
  animation:fade-up .5s ease both;
}
.page-eyebrow {
  font-family:var(--mono); font-size:.7rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent-mid);
  margin-bottom:10px; display:flex; align-items:center; gap:10px;
}
.page-eyebrow::before { content:''; display:block; width:24px; height:1px; background:var(--accent-mid); }
.page-title { font-family:var(--serif); font-size:2.2rem; font-weight:400; color:var(--text); letter-spacing:-.01em; margin-bottom:10px; }
.page-desc  { font-size:.95rem; color:var(--text-muted); max-width:540px; line-height:1.75; margin-bottom:28px; }

/* ── Filter bar ── */
.filter-bar {
  max-width:var(--max); margin:0 auto; padding:0 18px 20px;
  display:flex; gap:6px; flex-wrap:wrap;
}
.filter-btn {
  font-family:var(--mono); font-size:.68rem; letter-spacing:.06em;
  text-transform:uppercase; padding:5px 14px; border-radius:100px;
  border:1px solid var(--border2); background:var(--surface);
  color:var(--text-muted); cursor:pointer; transition:all .15s;
}
.filter-btn:hover, .filter-btn.active {
  border-color:var(--accent); color:var(--accent); background:var(--accent-light);
}

/* ── Gallery grid ── */
.gallery-grid {
  max-width:var(--max); margin:0 auto; padding:0 18px 52px;
  display:grid; grid-template-columns:repeat(3,1fr); gap:12px;
}
.gcard {
  border-radius:8px; overflow:hidden;
  background:var(--surface); border:1px solid var(--border);
  cursor:pointer; position:relative;
  transition:box-shadow .2s, transform .2s;
  animation:fade-up .4s ease both;
}
.gcard:hover { box-shadow:var(--shadow-lg); transform:translateY(-3px); }
.gcard-img   { aspect-ratio:4/3; overflow:hidden; background:var(--bg2); }
.gcard-img img { width:100%; height:100%; object-fit:cover; display:block; transition:transform .3s; }
.gcard:hover .gcard-img img { transform:scale(1.04); }
.gcard-body  { padding:11px 14px 13px; }
.gcard-caption { font-size:.85rem; color:var(--text); line-height:1.5; margin-bottom:3px; }
.gcard-tag {
  font-family:var(--mono); font-size:.62rem;
  letter-spacing:.06em; text-transform:uppercase; color:var(--text-dim);
}
.gcard-overlay {
  position:absolute; inset:0;
  display:flex; align-items:center; justify-content:center;
  background:rgba(0,0,0,.3); opacity:0; transition:opacity .2s;
}
.gcard:hover .gcard-overlay { opacity:1; }
.gcard-overlay svg { color:white; width:28px; height:28px; }

/* ── Placeholder card ── */
.gcard-placeholder {
  border:2px dashed var(--border2); background:transparent;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  min-height:180px; color:var(--text-dim); gap:10px; cursor:default;
}
.gcard-placeholder:hover { transform:none; box-shadow:none; }
.gcard-placeholder svg  { width:28px; height:28px; opacity:.4; }
.gcard-placeholder span {
  font-family:var(--mono); font-size:.65rem; letter-spacing:.06em;
  text-transform:uppercase; text-align:center; opacity:.5; padding:0 20px;
}

/* ── Responsive ── */
@media (max-width:760px) {
  .nav-links     { display:none; }
  .nav-hamburger { display:flex; }
  .gallery-grid  { grid-template-columns:repeat(2,1fr); }
  .lb-nav        { display:none; }
}
@media (max-width:480px) { .gallery-grid { grid-template-columns:1fr; } }
</style>"""


# ─────────────────────────────────────────────────────────────────────────────
# Photo card builder
# ─────────────────────────────────────────────────────────────────────────────

_EXPAND_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>'
)
_CAMERA_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">'
    '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>'
    '<circle cx="12" cy="13" r="4"/></svg>'
)


def _photo_card(photo: dict) -> str:
    src     = esc(photo["src"])
    caption = esc(photo["caption"])
    tag     = esc(photo.get("tag", ""))
    return (
        f'<div class="gcard" data-src="{src}" data-caption="{caption}" data-tag="{tag}">\n'
        f'  <div class="gcard-img">'
        f'<img src="{src}" alt="{caption[:40]}" loading="lazy" '
        f'onerror="this.parentElement.style.background=\'var(--bg2)\'"></div>\n'
        f'  <div class="gcard-body">\n'
        f'    <div class="gcard-caption">{caption}</div>\n'
        f'    <div class="gcard-tag">{tag}</div>\n'
        f'  </div>\n'
        f'  <div class="gcard-overlay">{_EXPAND_ICON}</div>\n'
        f'</div>'
    )


def _placeholder_card() -> str:
    return (
        '<div class="gcard gcard-placeholder">\n'
        f'  {_CAMERA_ICON}\n'
        '  <span>Add photos in config.yaml</span>\n'
        '</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Page-level JS  (filter + lightbox wiring)
# ─────────────────────────────────────────────────────────────────────────────

_GALLERY_JS = """\
<script>
// ── Filter ──
const galleryCards = Array.from(
  document.querySelectorAll('.gallery-grid .gcard:not(.gcard-placeholder)')
);

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.filter;
    galleryCards.forEach(c => {
      c.style.display = (f === 'all' || c.dataset.tag.toLowerCase().includes(f)) ? '' : 'none';
    });
  };
});

// ── Lightbox wiring ──
galleryCards.forEach((card, i) => {
  // Stagger entrance animation
  card.style.animationDelay = (i * 0.05) + 's';

  card.onclick = () => {
    const visible = galleryCards.filter(c => c.style.display !== 'none');
    lbImages = visible.map(c => ({ src: c.dataset.src, caption: c.dataset.caption }));
    lbIdx    = Math.max(0, visible.indexOf(card));
    showLightbox();
  };
});
</script>"""


# ─────────────────────────────────────────────────────────────────────────────
# Public builder
# ─────────────────────────────────────────────────────────────────────────────

def build_gallery(cfg: dict) -> str:
    """Return the complete gallery.html as a string."""
    site = cfg["site"]
    gal  = cfg.get("gallery", {})

    page_title = f"Gallery — {esc(site['author'])}"
    description = esc(gal.get("description", "Academic and field photos."))

    # Filter buttons
    categories = gal.get("categories", ["all"])
    filter_btns = '<button class="filter-btn active" data-filter="all">All</button>\n'
    for cat in categories:
        if cat != "all":
            filter_btns += f'<button class="filter-btn" data-filter="{esc(cat)}">{esc(cat.title())}</button>\n'

    # Photo cards + one placeholder at the end
    cards_html = "\n".join(_photo_card(p) for p in gal.get("photos", []))
    cards_html += "\n" + _placeholder_card()

    return "\n".join([
        HTML_HEAD.format(title=page_title, css=SHARED_CSS),
        _GALLERY_CSS,
        nav_html(cfg, "gallery"),
        "",
        '<div class="page-header">',
        '  <div class="page-eyebrow">Academic &amp; Field Photos</div>',
        '  <h1 class="page-title">Gallery</h1>',
        f'  <p class="page-desc">{description}</p>',
        '</div>',
        "",
        f'<div class="filter-bar">{filter_btns}</div>',
        "",
        f'<div class="gallery-grid" id="galleryGrid">{cards_html}</div>',
        "",
        footer_html(cfg),
        MODAL_HTML,
        SHARED_JS,
        _GALLERY_JS,
        "</body>\n</html>",
    ])
