I made this website with the help of Claude AI.

The website is controlled from a YAML config file. A python macro `build_site.py` builds
the website reading the config file and using modules defined in site_builder/. The structure is as I directed claude:

```
top-level-repo/
├── build_site.py                  ← driving python macro
├── site_config/
│   └── config.yaml                ← ALL your content lives here
└── site_builder/                  ← Python package, rarely touched
    ├── __init__.py                ← exposes build_all(), wires pages together
    ├── utils.py                   ← esc(), pill(), modal_link(), pub_badge()...
    ├── styles.py                  ← SHARED_CSS, NAV_CONTROLS, MODAL_HTML, SHARED_JS
    ├── nav.py                     ← nav_html(), footer_html()
    └── pages/
        ├── __init__.py
        ├── index_page.py          ← build_index(cfg)
        ├── gallery_page.py        ← build_gallery(cfg)
        └── somefun_page.py        ← build_somefun(cfg)
```

How to maintain:

```
- Add content    : site_config/config.yaml
- Add CSS changes: site_builder/styles.py
- Add a new nav link or footer item: site_builder/nav.py
- Add a new section to a page: the relevant pages/*.py
- Add a brand new page       : pages/newpage.py + register in __init__.py

```

P.S: I finetuned the python scripts to pick on the changes from yaml config. Some work still need to be done. Claude is not perfect or may be I can do
more prompt engineering. But, I need fine control over the config file. So, decided to work on it of my own. :)

PPS: It is impressive, No? ! I don't have that much of HTML knowledge honestly! Check out my old website (old/) with my html scripting. LOL! I am keeping it as sweet memories!

