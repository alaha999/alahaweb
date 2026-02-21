"""
site_builder/pages/index_page.py
=================================
Builds the main index.html from the config dict.

Content sections rendered here:
    Hero (name, role, bio, photo, hero-links)
    Physics image strip
    Research cards
    Publications list
    Teaching list
    Contact (emails, social pills, office address)
"""

from __future__ import annotations

from ..styles import SHARED_CSS, HTML_HEAD, MODAL_HTML, SHARED_JS
from ..nav    import nav_html, footer_html
from ..utils  import esc, pill, auto_link, pub_badge, section_header, hr_divider

# ─────────────────────────────────────────────────────────────────────────────
# Page-local CSS  (index-only layout classes that don't belong in the shared sheet)
# ─────────────────────────────────────────────────────────────────────────────

_INDEX_CSS = """\
<style>
/* ── Hero layout ── */
.hero-wrap {
  max-width:var(--max); margin:0 auto; padding:50px 18px 38px;
  display:grid; grid-template-columns:1fr 190px;
  gap:40px; align-items:start; animation:fade-up .5s ease both;
}
.hero-eyebrow {
  font-family:var(--mono); font-size:.72rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent-mid);
  margin-bottom:12px; display:flex; align-items:center; gap:10px;
}
.hero-eyebrow::before { content:''; display:block; width:24px; height:1px; background:var(--accent-mid); }
.hero-name {
  font-family:var(--serif); font-size:2.6rem; font-weight:400;
  line-height:1.15; color:var(--text); margin-bottom:6px; letter-spacing:-.01em;
}
.hero-role { font-size:.97rem; font-weight:300; color:var(--text-muted); margin-bottom:20px; }
.hero-role strong { font-weight:500; color:var(--text); }
.hero-bio { font-size:.95rem; color:var(--text-muted); line-height:1.8; max-width:540px; }
.hero-bio a { color:var(--accent); text-decoration:none; border-bottom:1px solid transparent; transition:border-color .15s; }
.hero-bio a:hover { border-color:var(--accent); }
.hero-links { display:flex; flex-wrap:wrap; gap:7px; margin-top:22px; }

/* ── Profile photo ── */
.photo-frame {
  width:190px; height:190px; border-radius:10px;
  overflow:hidden; background:var(--bg2); border:1px solid var(--border);
  cursor:pointer; transition:box-shadow .2s;
}
.photo-frame:hover { box-shadow:var(--shadow-lg); }
.photo-frame img { width:100%; height:100%; object-fit:cover; display:block; }
.photo-placeholder {
  width:100%; height:100%; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:10px; color:var(--text-dim);
}
.photo-placeholder svg { width:34px; height:34px; opacity:.45; }
.photo-placeholder span {
  font-family:var(--mono); font-size:.62rem; letter-spacing:.06em;
  text-transform:uppercase; text-align:center; line-height:1.5;
  opacity:.55; padding:0 14px;
}
.photo-caption {
  margin-top:10px; font-family:var(--mono); font-size:.63rem;
  color:var(--text-dim); text-align:center; letter-spacing:.04em;
}

/* ── Physics image strip ── */
.physics-strip { max-width:var(--max); margin:0 auto; padding:0 18px 36px; }
.physics-grid  { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; }
.gallery-thumb {
  border-radius:6px; overflow:hidden; background:var(--bg2);
  border:1px solid var(--border); aspect-ratio:4/3;
  cursor:pointer; position:relative; transition:box-shadow .2s, transform .2s;
}
.gallery-thumb:hover { box-shadow:var(--shadow-lg); transform:translateY(-2px); }
.gallery-thumb img   { width:100%; height:100%; object-fit:cover; display:block; }
.thumb-overlay {
  position:absolute; inset:0;
  background:linear-gradient(transparent 50%, rgba(0,0,0,.55));
  opacity:0; transition:opacity .2s;
  display:flex; align-items:flex-end; padding:8px;
}
.gallery-thumb:hover .thumb-overlay { opacity:1; }
.thumb-caption-preview {
  font-family:var(--mono); font-size:.58rem;
  color:rgba(255,255,255,.9); letter-spacing:.03em; line-height:1.4;
}
.gallery-note {
  font-family:var(--mono); font-size:.63rem; color:var(--text-dim);
  text-align:center; margin-top:8px; letter-spacing:.03em;
}

/* ── Research cards ── */
.research-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.rc {
  background:var(--surface); border:1px solid var(--border);
  border-radius:8px; padding:20px 22px; transition:border-color .2s, box-shadow .2s;
}
.rc:hover {
  border-color:var(--accent-mid);
  box-shadow:0 4px 20px color-mix(in srgb, var(--accent) 8%, transparent);
}
.rc-tag {
  font-family:var(--mono); font-size:.63rem; letter-spacing:.08em;
  text-transform:uppercase; color:var(--accent-mid);
  margin-bottom:9px; display:flex; align-items:center; gap:6px;
}
.rc-tag::before { content:''; display:block; width:6px; height:6px; border-radius:50%; background:var(--accent-mid); flex-shrink:0; }
.rc-title { font-size:.9rem; font-weight:500; color:var(--text); margin-bottom:8px; line-height:1.4; }
.rc-body  { font-size:.85rem; color:var(--text-muted); line-height:1.7; }

/* ── Publications ── */
.pub-list { display:flex; flex-direction:column; }
.pub-item {
  padding:18px 0; border-bottom:1px solid var(--border);
  display:grid; grid-template-columns:44px 1fr; gap:16px; align-items:start;
}
.pub-item:first-child { padding-top:0; }
.pub-year { font-family:var(--mono); font-size:.7rem; color:var(--text-dim); letter-spacing:.05em; padding-top:3px; }
.pub-title { font-size:.9rem; font-weight:500; color:var(--text); line-height:1.45; margin-bottom:4px; }
.pub-title a { color:inherit; text-decoration:none; border-bottom:1px solid var(--border2); transition:border-color .15s, color .15s; }
.pub-title a:hover { color:var(--accent); border-color:var(--accent); }
.pub-journal { font-size:.8rem; color:var(--text-muted); font-style:italic; }
.pub-badge {
  display:inline-block; font-family:var(--mono); font-size:.6rem;
  letter-spacing:.05em; padding:2px 7px; border-radius:3px;
  background:var(--accent-light); color:var(--accent);
  border:1px solid color-mix(in srgb, var(--accent) 18%, transparent);
  margin-left:8px; vertical-align:middle; font-style:normal;
}
.pub-more { margin-top:16px; font-family:var(--mono); font-size:.7rem; }
.pub-more a { color:var(--text-dim); text-decoration:none; display:inline-flex; align-items:center; gap:4px; }
.pub-more a:hover { color:var(--accent); }

/* ── Teaching ── */
.teaching-list { display:flex; flex-direction:column; }
.ti {
  padding:13px 0; border-bottom:1px solid var(--border);
  display:grid; grid-template-columns:1fr auto; gap:14px; align-items:baseline;
}
.ti:first-child { padding-top:0; }
.ti-course { font-size:.9rem; font-weight:500; color:var(--text); }
.ti-note   { font-weight:300; color:var(--text-muted); }
.ti-role   { font-size:.82rem; color:var(--text-muted); margin-top:2px; }
.ti-role a { color:var(--accent); text-decoration:none; }
.ti-term   { font-family:var(--mono); font-size:.68rem; color:var(--text-dim); letter-spacing:.04em; white-space:nowrap; }

/* ── Contact ── */
.contact-grid { display:grid; grid-template-columns:1fr 1fr; gap:28px; align-items:start; }
.contact-block h3 {
  font-family:var(--mono); font-size:.67rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--text-dim); margin-bottom:12px;
}
.email-list   { display:flex; flex-direction:column; gap:7px; margin-bottom:20px; }
.email-link {
  display:inline-flex; align-items:center; gap:8px;
  font-family:var(--mono); font-size:.8rem; color:var(--text);
  text-decoration:none; padding:9px 13px;
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius); transition:border-color .15s, background .15s;
}
.email-link:hover { border-color:var(--accent); background:var(--accent-light); color:var(--accent); }
.email-link svg  { width:13px; height:13px; color:var(--text-dim); flex-shrink:0; }
.email-link:hover svg { color:var(--accent); }
.social-row   { display:flex; flex-wrap:wrap; gap:7px; }
.address-block { font-size:.87rem; color:var(--text-muted); line-height:1.85; }
.address-block strong { color:var(--text); font-weight:500; }

/* ── Responsive overrides ── */
@media (max-width:760px) {
  .hero-wrap { grid-template-columns:1fr; padding:30px 14px 24px; }
  .hero-photo { order:-1; display:flex; flex-direction:column; align-items:flex-start; }
  .photo-frame { width:100px; height:100px; }
  .hero-name  { font-size:2rem; }
  .research-grid { grid-template-columns:1fr; }
  .contact-grid  { grid-template-columns:1fr; }
  .physics-grid  { grid-template-columns:repeat(2,1fr); }
  .ti { grid-template-columns:1fr; gap:2px; }
  .pub-item { grid-template-columns:36px 1fr; }
}
</style>"""


# ─────────────────────────────────────────────────────────────────────────────
# Section builders  (each returns a self-contained HTML fragment string)
# ─────────────────────────────────────────────────────────────────────────────

def _hero_links(links_cfg: list) -> str:
    icon_map = {
        "pdf":    '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/>',
        "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
        "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    }
    parts = []
    for lk in links_cfg:
        svg_paths = icon_map.get(lk.get("icon", ""), "")
        svg = (
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{svg_paths}</svg>'
            if svg_paths else ""
        )
        inner = f"{svg}{esc(lk['label'])}"
        css   = "pill primary" if lk.get("primary") else "pill"
        url   = lk["url"]
        if lk.get("modal"):
            safe_url   = esc(url)
            safe_title = esc(lk["label"])
            parts.append(
                f'<a class="{css}" href="#" '
                f'onclick="openLink(\'{safe_url}\',\'{safe_title}\');return false;">'
                f'{inner}</a>'
            )
        else:
            parts.append(f'<a class="{css}" href="{esc(url)}" target="_blank">{inner}</a>')
    return "\n".join(parts)


def _physics_strip(images: list) -> str:
    thumbs = []
    for img in images:
        thumbs.append(
            f'<div class="gallery-thumb" '
            f'data-src="{esc(img["src"])}" data-caption="{esc(img["caption"])}">\n'
            f'  <img src="{esc(img["src"])}" alt="{esc(img.get("preview",""))}" '
            f'loading="lazy" onerror="this.parentElement.style.display=\'none\'">\n'
            f'  <div class="thumb-overlay">'
            f'<span class="thumb-caption-preview">{esc(img.get("preview",""))}</span>'
            f'</div>\n</div>'
        )
    return (
        '<div class="physics-strip">\n'
        '  <div class="physics-grid" id="physicsGallery">\n'
        + "\n".join(f"    {t}" for t in thumbs)
        + "\n  </div>\n"
        '  <p class="gallery-note">Click any image to enlarge</p>\n'
        "</div>"
    )


def _research_section(research_cfg: list) -> str:
    cards = []
    for rc in research_cfg:
        cards.append(
            f'<div class="rc" data-searchable="{esc(rc.get("keywords",""))}">\n'
            f'  <div class="rc-tag">{esc(rc["tag"])}</div>\n'
            f'  <div class="rc-title">{esc(rc["title"])}</div>\n'
            f'  <p class="rc-body">{rc["body"].strip()}</p>\n'
            f'</div>'
        )
    return (
        '<section id="research">\n'
        + section_header("01", "Research") + "\n"
        + '  <div class="research-grid">\n'
        + "\n".join(f"    {c}" for c in cards)
        + "\n  </div>\n</section>"
    )


def _publications_section(pubs_cfg: list, inspire_url: str, author_name: str) -> str:
    items = []
    for pub in pubs_cfg:
        badge = pub_badge(pub.get("badge", ""))
        if pub.get("url"):
            if pub.get("modal"):
                safe_url   = esc(pub["url"])
                safe_title = esc(pub["title"][:60])
                title_inner = (
                    f'<a href="#" onclick="openLink(\'{safe_url}\',\'{safe_title}\');return false;">'
                    f'{esc(pub["title"])}</a>{badge}'
                )
            else:
                title_inner = (
                    f'<a href="{esc(pub["url"])}" target="_blank">'
                    f'{esc(pub["title"])}</a>{badge}'
                )
        else:
            title_inner = esc(pub["title"]) + badge

        items.append(
            f'<div class="pub-item" data-searchable="{esc(pub.get("keywords",""))}">\n'
            f'  <span class="pub-year">{esc(pub["year"])}</span>\n'
            f'  <div>\n'
            f'    <div class="pub-title">{title_inner}</div>\n'
            f'    <div class="pub-journal">{esc(pub["journal"])}</div>\n'
            f'  </div>\n'
            f'</div>'
        )

    safe_inspire = esc(inspire_url)
    safe_author  = esc(author_name)
    inspire_link = (
        f'<a href="#" onclick="openLink(\'{safe_inspire}\',\'iNSPIRE HEP — {safe_author}\');return false;">'
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>'
        '<polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>'
        '</svg> Full publication list on iNSPIRE HEP</a>'
    )

    return (
        '<section id="publications">\n'
        + section_header("02", "Publications") + "\n"
        + '  <div class="pub-list">\n'
        + "\n".join(f"    {it}" for it in items)
        + "\n  </div>\n"
        + f'  <p class="pub-more">{inspire_link}</p>\n'
        + "</section>"
    )


def _teaching_section(teaching_cfg: list) -> str:
    items = []
    for ti in teaching_cfg:
        code = f' <span class="ti-note">({esc(ti["code"])})</span>' if ti.get("code") else ""
        if ti.get("link_url") and ti.get("link_label"):
            link = auto_link(
                url    = ti["link_url"],
                label  = ti["link_label"],
                title  = ti["link_label"],
                modal  = bool(ti.get("link_modal")),
                css_class = "",
            )
            role_suffix = f" · {link}"
        else:
            role_suffix = ""

        items.append(
            f'<div class="ti" data-searchable="{esc(ti.get("keywords",""))}">\n'
            f'  <div>\n'
            f'    <div class="ti-course">{esc(ti["course"])}{code}</div>\n'
            f'    <div class="ti-role">{esc(ti["role"])}{role_suffix}</div>\n'
            f'  </div>\n'
            f'  <span class="ti-term">{esc(ti["term"])}</span>\n'
            f'</div>'
        )

    return (
        '<section id="teaching">\n'
        + section_header("03", "Teaching & Outreach") + "\n"
        + '  <div class="teaching-list">\n'
        + "\n".join(f"    {it}" for it in items)
        + "\n  </div>\n</section>"
    )


def _contact_section(contact_cfg: dict) -> str:
    # email rows
    email_svg = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6'
        'c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
    )
    emails_html = "\n".join(
        f'<a class="email-link" href="mailto:{esc(em)}">{email_svg}{esc(em)}</a>'
        for em in contact_cfg.get("emails", [])
    )

    # social pills
    social_html = "\n".join(
        auto_link(
            url       = s["url"],
            label     = s["label"],
            title     = s["label"],
            modal     = bool(s.get("modal")),
            css_class = "pill",
        )
        for s in contact_cfg.get("social", [])
    )

    # office address
    addr = contact_cfg.get("office", {})
    address_html = (
        f'<strong>{esc(addr.get("room",""))}</strong><br>\n'
        f'{esc(addr.get("building",""))}<br>\n'
        f'{esc(addr.get("institution",""))}<br>\n'
        f'{esc(addr.get("street",""))}<br>\n'
        f'{esc(addr.get("city",""))}'
    )

    return (
        '<section id="contact">\n'
        + section_header("04", "Contact") + "\n"
        + '  <div class="contact-grid">\n'
        + '    <div class="contact-block">\n'
        + '      <h3>Email</h3>\n'
        + f'      <div class="email-list">{emails_html}</div>\n'
        + '      <h3 style="margin-bottom:12px;">Academic Profiles</h3>\n'
        + f'      <div class="social-row">{social_html}</div>\n'
        + '    </div>\n'
        + '    <div class="contact-block">\n'
        + '      <h3>Office</h3>\n'
        + f'      <div class="address-block">{address_html}</div>\n'
        + '    </div>\n'
        + '  </div>\n</section>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Page-level search JavaScript  (index-specific: scans sections, syncs active nav)
# ─────────────────────────────────────────────────────────────────────────────

_INDEX_JS = """\
<script>
// ── Physics gallery lightbox wiring ──
document.querySelectorAll('#physicsGallery .gallery-thumb').forEach((el, i) => {
  el.onclick = () => {
    const thumbs = Array.from(document.querySelectorAll('#physicsGallery .gallery-thumb'));
    lbImages = thumbs.map(t => ({ src: t.dataset.src, caption: t.dataset.caption }));
    lbIdx = i;
    showLightbox();
  };
});

// ── In-page search ──
const searchInput   = document.getElementById('navSearch');
const searchResults = document.getElementById('searchResults');

function buildSearchIndex() {
  const items = [];
  document.querySelectorAll('[data-searchable]').forEach(el => {
    const titleEl = el.querySelector('.rc-title, .pub-title, .ti-course, .section-title');
    const title   = titleEl?.textContent?.trim();
    if (!title) return;
    items.push({
      el,
      title:   title.substring(0, 80),
      text:    (el.getAttribute('data-searchable') + ' ' + el.textContent).toLowerCase(),
      section: el.closest('section')?.id || 'page',
    });
  });
  return items;
}

let searchIndex = null;

searchInput.addEventListener('input', () => {
  const q = searchInput.value.trim().toLowerCase();
  if (!q) { searchResults.style.display = 'none'; return; }
  if (!searchIndex) searchIndex = buildSearchIndex();

  const esc_re = q.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
  const re     = new RegExp('(' + esc_re + ')', 'gi');
  const hits   = searchIndex.filter(i => i.text.includes(q) || i.title.toLowerCase().includes(q)).slice(0, 8);

  searchResults.innerHTML = hits.length
    ? hits.map((h, i) =>
        `<div class="sr-item" data-idx="${i}">
           <div class="sr-title">${h.title.replace(re, '<mark>$1</mark>')}</div>
           <div class="sr-section">${h.section}</div>
         </div>`
      ).join('')
    : '<div class="sr-empty">No results found</div>';

  searchResults.querySelectorAll('.sr-item').forEach((el, i) => {
    if (i < hits.length) el.onclick = () => {
      searchResults.style.display = 'none';
      searchInput.value = '';
      hits[i].el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      hits[i].el.classList.add('search-highlight');
      setTimeout(() => hits[i].el.classList.remove('search-highlight'), 2500);
    };
  });
  searchResults.style.display = 'block';
});

document.addEventListener('click', e => {
  if (!e.target.closest('.nav-search-wrap') && !e.target.closest('#searchResults'))
    searchResults.style.display = 'none';
});

// ── Active nav highlight on scroll ──
const sections = document.querySelectorAll('section[id]');
const navLinks  = document.querySelectorAll('.nav-links a');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => { if (window.scrollY >= s.offsetTop - 90) current = s.id; });
  navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + current));
}, { passive: true });
</script>"""


# ─────────────────────────────────────────────────────────────────────────────
# Public builder
# ─────────────────────────────────────────────────────────────────────────────

def build_index(cfg: dict) -> str:
    """Return the complete index.html as a string."""
    p    = cfg["person"]
    site = cfg["site"]

    # Bio text — substitute {advisor_url} and {advisor_name} placeholders
    bio = p.get("bio", "").format(
        advisor_url  = p.get("advisor_url", "#"),
        advisor_name = esc(p.get("advisor_name", "")),
    )

    # Photo block — shows placeholder until user drops in an actual image
    photo_src     = p.get("photo", "images/photo.jpg")
    photo_caption = p.get("photo_caption", "")
    photo_html = (
        f'<div class="photo-frame" onclick="openLightbox(\'{esc(photo_src)}\',\'{esc(p["name"])}\')">\n'
        f'  <!-- To add your photo replace this block with:\n'
        f'       <img src="{esc(photo_src)}" alt="{esc(p["name"])}"> -->\n'
        f'  <div class="photo-placeholder">\n'
        f'       <img src="{esc(photo_src)}" alt="{esc(p["name"])}">\n'
        f'  </div>\n'
        f'</div>\n'
        f'<p class="photo-caption">{esc(photo_caption)}</p>'
    )

    hero_links = _hero_links(cfg.get("links", []))

    return "\n".join([
        HTML_HEAD.format(title=esc(site["title"]), css=SHARED_CSS),
        _INDEX_CSS,
        nav_html(cfg, "index"),
        "",
        "<!-- HERO -->",
        '<div class="hero-wrap" id="home">',
        '  <div class="hero-text">',
        f'    <div class="hero-eyebrow">{esc(p["field"])}</div>',
        f'    <h1 class="hero-name">{esc(p["name"])}</h1>',
        f'    <p class="hero-role"><strong>{esc(p["title"])}</strong>'
        f' · {esc(p["institution"])} &nbsp;·&nbsp; {esc(p["group"])}</p>',
        f'    <p class="hero-bio" data-searchable="about intro bio">{bio}</p>',
        f'    <div class="hero-links">{hero_links}</div>',
        '  </div>',
        '  <div class="hero-photo">',
        photo_html,
        '  </div>',
        '</div>',
        "",
        "<!-- PHYSICS STRIP -->",
        _physics_strip(cfg.get("physics_images", [])),
        "",
        hr_divider(),
        _research_section(cfg.get("research", [])),
        "",
        hr_divider(),
        _publications_section(
            cfg.get("publications", []),
            cfg.get("inspire_url", "#"),
            p["name"],
        ),
        "",
        hr_divider(),
        _teaching_section(cfg.get("teaching", [])),
        "",
        hr_divider(),
        _contact_section(cfg.get("contact", {})),
        "",
        footer_html(cfg),
        MODAL_HTML,
        SHARED_JS,
        _INDEX_JS,
        "</body>\n</html>",
    ])
