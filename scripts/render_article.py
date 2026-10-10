#!/usr/bin/env python3
"""Optional editorial build; not needed to run the application or experiments."""
from html import escape
from pathlib import Path
import re

import markdown

ROOT = Path(__file__).resolve().parents[1]
raw = (ROOT / "article/devto.md").read_text()
_, front, body = raw.split("---", 2)
title = re.search(r'^title: "(.+)"$', front, re.M)[1]
rendered = markdown.markdown(body, extensions=["fenced_code", "tables"])
css = """
:root{color-scheme:light;--ink:#282723;--muted:#6d685f;--paper:#faf8f2;--accent:#aa432a}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink)}
.masthead{max-width:1120px;margin:auto;padding:28px 32px 18px;display:flex;justify-content:space-between;font:700 11px/1.5 system-ui;letter-spacing:2px;border-bottom:1px solid #ccc3b6}
header{max-width:900px;margin:56px auto 44px;padding:0 28px}.eyebrow{font:700 12px system-ui;letter-spacing:2px;color:var(--accent)}
h1{font:500 clamp(36px,5.2vw,64px)/1.08 Georgia,serif;letter-spacing:-1.6px;margin:20px 0 24px;max-width:870px}
.dek{font:20px/1.55 system-ui;color:var(--muted);max-width:720px}.meta{margin-top:22px;font:12px system-ui;color:var(--muted)}
.cover{display:block;width:100%;height:auto;margin:30px 0 0;border:1px solid #d7cebf}
main{max-width:780px;margin:auto;padding:0 28px 88px;font:20px/1.75 Georgia,serif}p{margin:0 0 25px}
main>p:first-child{font-size:25px;line-height:1.55}h2{font:650 29px/1.2 system-ui;margin:56px 0 22px;letter-spacing:-.7px}h3{font:650 22px system-ui}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px;overflow-wrap:anywhere}
strong{font-weight:700}li{margin:10px 0}ul,ol{padding-left:25px}code{font:14px/1.6 ui-monospace,monospace;background:#ece7dc;border-radius:3px;padding:2px 5px;overflow-wrap:anywhere}
pre{background:#292a27;color:#f5f0e5;border-radius:8px;padding:24px;margin:28px 0;overflow-x:auto;max-width:100%}pre code{padding:0;background:none;color:inherit;white-space:pre;overflow-wrap:normal}
table{font:14px/1.5 system-ui;border-collapse:collapse;width:100%;margin:30px 0}th{text-align:left;background:#eae4d8}td,th{padding:12px 10px;border-bottom:1px solid #d7cebf;vertical-align:top}
blockquote{border-left:3px solid var(--accent);margin:30px 0;padding:5px 22px;color:var(--muted)}
footer{border-top:1px solid #d7cebf;padding:28px;text-align:center;font:12px system-ui;color:var(--muted)}
@media(max-width:600px){.masthead{padding:20px}.masthead span:last-child{display:none}header{margin-top:32px;padding:0 20px}.dek{font-size:17px}main{padding:0 20px 55px;font-size:18px}h2{font-size:25px}pre{padding:16px}table{display:block;overflow:auto;font-size:12px}h1{letter-spacing:-1px}}
"""
html = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><style>{css}</style>
<div class="masthead"><span>FIELD NOTES / SOFTWARE PRACTICE</span><span>LOCAL EDITORIAL PREVIEW · UNPUBLISHED</span></div>
<header><div class="eyebrow">A PRACTICAL TUTORIAL</div><h1>{escape(title)}</h1>
<p class="dek">Build a small app, challenge its promises, and keep the evidence another developer needs to reproduce the result.</p>
<div class="meta">Python + SQLite · No model account required · Original teaching example</div>
<img class="cover" src="cover.svg" alt="Give your agent something to prove: claim, experiment, decision"></header>
<main>{rendered}</main><footer>Independent teaching project · The article remains a draft.</footer></html>'''
(ROOT / "article/preview.html").write_text(html)
try:
    import cairosvg
    cairosvg.svg2png(url=str(ROOT / "article/cover.svg"), write_to=str(ROOT / "article/cover.png"))
except ImportError:
    print("HTML rendered. Optional cover.png conversion requires CairoSVG.")
print("Rendered article/preview.html")
