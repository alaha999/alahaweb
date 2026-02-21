"""
site_builder/utils.py
=====================
Pure HTML-generation helpers that are independent of any particular page.

All functions return strings.  No I/O, no global state.
"""

from __future__ import annotations


# ─────────────────────────────────────────────────────────────────────────────
# Basic escaping
# ─────────────────────────────────────────────────────────────────────────────

def esc(value) -> str:
    """HTML-escape a plain-text value (str-cast first)."""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


# ─────────────────────────────────────────────────────────────────────────────
# Link / modal helpers
# ─────────────────────────────────────────────────────────────────────────────

def modal_link(url: str, label: str, title: str, css_class: str = "pill") -> str:
    """
    An <a> that opens *url* inside the in-page modal popup.

    onclick calls the global JS function openLink(url, title).
    """
    safe_url   = esc(url)
    safe_title = esc(title)
    safe_label = esc(label)
    return (
        f'<a class="{css_class}" href="#" '
        f'onclick="openLink(\'{safe_url}\',\'{safe_title}\');return false;">'
        f'{safe_label}</a>'
    )


def external_link(url: str, label: str, css_class: str = "pill") -> str:
    """A plain <a> that opens *url* in a new browser tab."""
    return f'<a class="{css_class}" href="{esc(url)}" target="_blank">{esc(label)}</a>'


def auto_link(
    url: str,
    label: str,
    title: str = "",
    modal: bool = False,
    css_class: str = "pill",
) -> str:
    """
    Choose modal or external link based on the *modal* flag.

    *title* is only used for the modal popup header.
    """
    if not url:
        return ""
    if modal:
        return modal_link(url, label, title or label, css_class)
    return external_link(url, label, css_class)


# ─────────────────────────────────────────────────────────────────────────────
# Pill badges
# ─────────────────────────────────────────────────────────────────────────────

# Map of icon keys → SVG path content (stroke-based, 24×24 viewBox)
ICON_PATHS: dict[str, str] = {
    "pdf": (
        '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
    ),
    "search": (
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    ),
    "github": (
        '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61'
        "c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0"
        " 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09"
        ' 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61'
        ' 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>'
    ),
    "external": (
        '<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>'
        '<polyline points="15 3 21 3 21 9"/>'
        '<line x1="10" y1="14" x2="21" y2="3"/>'
    ),
}


def icon_svg(key: str) -> str:
    """Return an inline <svg> element for the named icon, or empty string."""
    paths = ICON_PATHS.get(key, "")
    if not paths:
        return ""
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        f'{paths}</svg>'
    )


def pill(
    url: str,
    label: str,
    title: str = "",
    modal: bool = False,
    primary: bool = False,
    icon_key: str = "",
) -> str:
    """
    Render a pill-shaped badge link.

    Parameters
    ----------
    url      : destination URL
    label    : visible text
    title    : modal popup header (only relevant when modal=True)
    modal    : open in in-page modal instead of new tab
    primary  : apply 'pill primary' styling (filled accent colour)
    icon_key : optional icon name from ICON_PATHS
    """
    css = "pill primary" if primary else "pill"
    svg = icon_svg(icon_key)
    inner = f"{svg}{esc(label)}" if svg else esc(label)

    if modal:
        safe_url   = esc(url)
        safe_title = esc(title or label)
        return (
            f'<a class="{css}" href="#" '
            f'onclick="openLink(\'{safe_url}\',\'{safe_title}\');return false;">'
            f'{inner}</a>'
        )
    return f'<a class="{css}" href="{esc(url)}" target="_blank">{inner}</a>'


# ─────────────────────────────────────────────────────────────────────────────
# Small structural helpers
# ─────────────────────────────────────────────────────────────────────────────

def section_header(num: str, title: str) -> str:
    """Render the numbered section header row (num | title | rule line)."""
    return (
        '<div class="section-header">'
        f'<span class="section-num">{esc(num)}</span>'
        f'<h2 class="section-title">{esc(title)}</h2>'
        '<div class="section-line"></div>'
        "</div>"
    )


def hr_divider() -> str:
    return '<hr class="section-divider">'


def pub_badge(text: str) -> str:
    """Render an inline publication badge span."""
    return f'<span class="pub-badge">{esc(text)}</span>' if text else ""
