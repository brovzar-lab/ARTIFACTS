#!/usr/bin/env python3
"""Rebuild index.html from manifest.json. Standard library only.

Usage:  python3 build.py
The manifest is the single source of truth. This script regenerates the
static hub page so it works both locally (file://) and on GitHub Pages.
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

# --- Category filter buttons ------------------------------------------------
filters = [
    '<button class="cat-card active" data-filter="all" style="--accent:#8b93a7">'
    '<span class="cat-emoji">🗃️</span><span class="cat-label">All</span>'
    f'<span class="cat-count">{len(artifacts)}</span></button>'
]
for c in categories:
    filters.append(
        f'<button class="cat-card" data-filter="{c["id"]}" style="--accent:{c["color"]}">'
        f'<span class="cat-emoji">{c["emoji"]}</span>'
        f'<span class="cat-label">{html.escape(c["label"])}</span>'
        f'<span class="cat-count">{counts[c["id"]]}</span></button>'
    )

# --- Artifact cards (newest first) ------------------------------------------
cards = []
for a in sorted(artifacts, key=lambda x: x.get("date", ""), reverse=True):
    c = cat_by_id.get(a["category"], {"label": a["category"], "emoji": "", "color": "#8b93a7"})
    cards.append(
        f'<a class="artifact" href="{html.escape(a["file"])}" '
        f'data-category="{html.escape(a["category"])}" style="--accent:{c["color"]}">'
        f'<div class="artifact-head">'
        f'<span class="pill">{c["emoji"]} {html.escape(c["label"])}</span>'
        f'<span class="date">{html.escape(a.get("date", ""))}</span></div>'
        f'<div class="artifact-title">{html.escape(a["title"])}</div>'
        f'<div class="artifact-desc">{html.escape(a.get("description", ""))}</div>'
        f'</a>'
    )

built = datetime.date.today().isoformat()

CSS = """
  :root{
    --bg:#0b0d12; --card:#151923; --card-hover:#1a1f2b; --line:#242b38;
    --text:#eef1f6; --muted:#98a2b5;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;
    background:radial-gradient(1200px 600px at 50% -12%, #1a2030 0%, var(--bg) 55%);
    color:var(--text); line-height:1.55; -webkit-font-smoothing:antialiased;
    padding:52px 20px 80px; min-height:100vh;
  }
  .wrap{max-width:960px;margin:0 auto}
  header{margin-bottom:30px}
  .eyebrow{display:inline-block;font-size:12px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--muted);margin-bottom:14px;font-weight:600}
  h1{font-size:clamp(30px,5vw,44px);letter-spacing:-.02em;font-weight:750;line-height:1.05}
  .subtitle{color:var(--muted);font-size:16px;margin-top:10px;max-width:60ch}
  .cats{display:flex;flex-wrap:wrap;gap:10px;margin:30px 0 34px}
  .cat-card{cursor:pointer;display:flex;align-items:center;gap:9px;
    background:var(--card);border:1px solid var(--line);border-radius:12px;
    padding:11px 15px;color:var(--text);font-size:14px;font-weight:600;
    transition:border-color .15s ease,background .15s ease,transform .1s ease}
  .cat-card:hover{background:var(--card-hover);border-color:color-mix(in srgb,var(--accent) 55%,var(--line))}
  .cat-card.active{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 14%,var(--card))}
  .cat-emoji{font-size:16px}
  .cat-count{font-size:12px;color:var(--muted);background:rgba(255,255,255,.06);
    padding:1px 8px;border-radius:999px;min-width:22px;text-align:center}
  .cat-card.active .cat-count{color:var(--accent)}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
  .artifact{display:block;text-decoration:none;color:inherit;background:var(--card);
    border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:14px;
    padding:20px 22px;transition:transform .15s ease,background .15s ease,border-color .15s ease}
  .artifact:hover{background:var(--card-hover);transform:translateY(-2px);
    border-color:color-mix(in srgb,var(--accent) 45%,var(--line));border-left-color:var(--accent)}
  .artifact-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:11px}
  .pill{font-size:11px;font-weight:650;letter-spacing:.02em;padding:3px 10px;border-radius:999px;
    color:var(--accent);background:color-mix(in srgb,var(--accent) 15%,transparent)}
  .date{font-size:12px;color:var(--muted)}
  .artifact-title{font-size:17px;font-weight:650;letter-spacing:-.01em;line-height:1.3;margin-bottom:7px}
  .artifact-desc{font-size:14px;color:var(--muted)}
  .empty{display:none;grid-column:1/-1;text-align:center;color:var(--muted);
    padding:48px 0;font-size:15px}
  footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);
    color:var(--muted);font-size:12.5px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
  footer a{color:var(--muted)}
"""

JS = """
  const cards=document.querySelectorAll('.artifact');
  const buttons=document.querySelectorAll('.cat-card');
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
    <header>
      <span class="eyebrow">Atlas · Artifacts</span>
      <h1>{html.escape(site["title"])}</h1>
      <p class="subtitle">{html.escape(site["subtitle"])}</p>
    </header>

    <nav class="cats">
      {"".join(filters)}
    </nav>

    <main class="grid">
      {"".join(cards)}
      <div class="empty" id="empty">No artifacts in this category yet.</div>
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
