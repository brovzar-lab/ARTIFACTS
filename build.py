#!/usr/bin/env python3
"""Rebuild index.html from manifest.json. Standard library only.

Usage:  python3 build.py
The manifest is the single source of truth. This script regenerates the
static hub page so it works both locally (file://) and on GitHub Pages.

Design language: "ATLAS-GLASS" (Superhuman-style) — periwinkle/violet
gradient, big tight white headings, dark navy pill controls, violet accent,
frosted-glass white cards.
"""
import json
import html
import datetime
import pathlib

ROOT = pathlib.Path(__file__).parent
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

site = manifest["site"]
categories = manifest["categories"]
artifacts = manifest["artifacts"]

cat_by_id = {c["id"]: c for c in categories}
counts = {c["id"]: 0 for c in categories}
for a in artifacts:
    counts[a["category"]] = counts.get(a["category"], 0) + 1

# --- Category filter pills --------------------------------------------------
filters = [
    '<button class="cat active" data-filter="all">'
    '<span class="cat-emoji">🗃️</span><span>All</span>'
    f'<span class="cat-count">{len(artifacts)}</span></button>'
]
for c in categories:
    filters.append(
        f'<button class="cat" data-filter="{c["id"]}">'
        f'<span class="cat-emoji">{c["emoji"]}</span>'
        f'<span>{html.escape(c["label"])}</span>'
        f'<span class="cat-count">{counts[c["id"]]}</span></button>'
    )

# --- Artifact cards (newest first) ------------------------------------------
cards = []
for a in sorted(artifacts, key=lambda x: x.get("date", ""), reverse=True):
    c = cat_by_id.get(a["category"], {"label": a["category"], "emoji": "", "color": "#6b5ce6"})
    cards.append(
        f'<a class="artifact" href="{html.escape(a["file"])}" '
        f'data-category="{html.escape(a["category"])}" style="--accent:{c["color"]}">'
        f'<div class="artifact-head">'
        f'<span class="pill">{c["emoji"]} {html.escape(c["label"])}</span>'
        f'<span class="date">{html.escape(a.get("date", ""))}</span></div>'
        f'<div class="artifact-title">{html.escape(a["title"])}</div>'
        f'<div class="artifact-desc">{html.escape(a.get("description", ""))}</div>'
        f'<span class="go">Open &rarr;</span>'
        f'</a>'
    )

built = datetime.date.today().isoformat()

CSS = """
  @import url("https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400..700&display=swap");
  :root{ --ink:#1b1b27; --accent:#6b5ce6;
    --font-sans:"Instrument Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,"Helvetica Neue",Arial,sans-serif; }
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    font-family:var(--font-sans);
    background:radial-gradient(1300px 820px at 50% -10%, #a9b7f0 0%, #b1ace9 44%, #c8b9e6 100%) fixed;
    color:var(--ink); min-height:100vh; -webkit-font-smoothing:antialiased;
    padding:66px 22px 92px;
  }
  .wrap{max-width:1000px;margin:0 auto}
  .hero{text-align:center;margin-bottom:14px}
  .eyebrow{display:inline-block;font-size:12px;letter-spacing:.2em;text-transform:uppercase;
    color:rgba(255,255,255,.82);font-weight:600;margin-bottom:18px}
  h1{font-size:clamp(46px,8.5vw,88px);line-height:1.0;letter-spacing:-.038em;font-weight:600;color:#fff}
  .subtitle{color:rgba(255,255,255,.85);font-size:17px;margin:18px auto 0;max-width:52ch;line-height:1.5}

  .cats{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:38px 0 42px}
  .cat{cursor:pointer;display:inline-flex;align-items:center;gap:9px;
    background:rgba(255,255,255,.58);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);
    border:1px solid rgba(255,255,255,.65);border-radius:999px;padding:10px 16px;
    color:#2a2a40;font-size:14px;font-weight:550;box-shadow:0 2px 12px rgba(40,40,90,.06);
    transition:background .16s ease,transform .12s ease,box-shadow .16s ease,color .16s ease}
  .cat:hover{background:rgba(255,255,255,.9);transform:translateY(-1px)}
  .cat.active{background:#1c1c28;border-color:#1c1c28;color:#fff;box-shadow:0 8px 22px rgba(28,28,44,.32)}
  .cat-emoji{font-size:15px}
  .cat-count{font-size:12px;font-weight:600;color:#6a6a82;background:rgba(0,0,0,.06);
    padding:1px 8px;border-radius:999px;min-width:22px;text-align:center}
  .cat.active .cat-count{color:#fff;background:rgba(255,255,255,.2)}

  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
  .artifact{position:relative;display:block;text-decoration:none;color:inherit;overflow:hidden;
    background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);
    border:1px solid rgba(255,255,255,.7);border-radius:22px;padding:24px 24px 20px;
    box-shadow:0 10px 30px rgba(40,40,90,.10);
    transition:transform .18s ease,box-shadow .18s ease,background .18s ease}
  .artifact::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent)}
  .artifact:hover{transform:translateY(-3px);background:rgba(255,255,255,.86);
    box-shadow:0 18px 44px rgba(40,40,90,.18)}
  .artifact-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:13px}
  .pill{font-size:11px;font-weight:650;letter-spacing:.02em;padding:4px 11px;border-radius:999px;
    color:var(--accent);background:color-mix(in srgb,var(--accent) 13%,#fff)}
  .date{font-size:12px;color:#7b7b92;font-variant-numeric:tabular-nums}
  .artifact-title{font-size:18px;font-weight:600;letter-spacing:-.015em;line-height:1.28;
    margin-bottom:8px;color:#1a1a28}
  .artifact-desc{font-size:14px;color:#5c5c74;line-height:1.5}
  .go{display:inline-block;margin-top:16px;font-size:13px;font-weight:600;color:var(--accent)}

  .empty{display:none;grid-column:1/-1;text-align:center;color:rgba(255,255,255,.85);
    padding:54px 0;font-size:15px}
  footer{margin-top:46px;padding-top:22px;border-top:1px solid rgba(255,255,255,.4);
    color:rgba(255,255,255,.78);font-size:12.5px;display:flex;justify-content:space-between;
    flex-wrap:wrap;gap:8px}
"""

JS = """
  const cards=document.querySelectorAll('.artifact');
  const buttons=document.querySelectorAll('.cat');
  const empty=document.getElementById('empty');
  function apply(f){
    let v=0;
    cards.forEach(c=>{const s=f==='all'||c.dataset.category===f;c.style.display=s?'':'none';if(s)v++;});
    empty.style.display=v===0?'':'none';
  }
  buttons.forEach(b=>b.addEventListener('click',()=>{
    buttons.forEach(x=>x.classList.remove('active'));
    b.classList.add('active');apply(b.dataset.filter);
  }));
"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(site["title"])}</title>
<style>{CSS}</style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <span class="eyebrow">Atlas · Artifacts</span>
      <h1>{html.escape(site["title"])}</h1>
      <p class="subtitle">{html.escape(site["subtitle"])}</p>
    </header>

    <nav class="cats">
      {"".join(filters)}
    </nav>

    <main class="grid">
      {"".join(cards)}
      <div class="empty" id="empty">Nothing here yet.</div>
    </main>

    <footer>
      <span>{len(artifacts)} artifact(s) · last built {built}</span>
      <span>brovzar-lab/ARTIFACTS</span>
    </footer>
  </div>
  <script>{JS}</script>
</body>
</html>
"""

(ROOT / "index.html").write_text(page, encoding="utf-8")
print(f"Built index.html — {len(artifacts)} artifact(s), {len(categories)} categories.")
