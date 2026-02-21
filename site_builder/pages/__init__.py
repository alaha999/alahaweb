"""
site_builder/pages
==================
One module per generated HTML page.

    index_page.py   → build_index(cfg)   → str
    gallery_page.py → build_gallery(cfg) → str
    somefun_page.py → build_somefun(cfg) → str

Each builder is a pure function: cfg dict in, HTML string out.
"""
