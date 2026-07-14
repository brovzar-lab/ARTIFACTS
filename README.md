# ARTIFACTS

A page for pages. Every HTML artifact Atlas builds for Billy gets dropped here,
sorted by area of life, and surfaced on one hub page.

- **Live hub:** https://brovzar-lab.github.io/ARTIFACTS/
- **Local hub:** open `index.html` in a browser

## How it works

1. `manifest.json` is the single source of truth. It lists every artifact:
   title, description, category, file path, and date.
2. Each artifact is a standalone HTML file inside its category folder
   (`business/`, `personal/`, `spiritual/`, `financial/`, `miscellaneous/`).
3. `build.py` reads the manifest and regenerates `index.html`, a static hub
   with clickable category filters. No servers, no dependencies.

## Adding an artifact (Atlas's routine)

1. Copy `templates/artifact.html` into the right category folder and rename it.
   It carries the shared **Atlas-glass** design system (frosted glass over a
   periwinkle sky) so every artifact stays homogeneous with the hub. Keep its
   `<style>` block verbatim; edit only the `<title>`, the `--accent` on `<body>`
   (use the category colour), and the content between the `CONTENT` markers.
2. Add an entry to `manifest.json`.
3. Rebuild the hub:
   ```
   cd "/Users/quantumcode/CODE/ARTIFACTS" && python3 build.py
   ```
4. Commit and push. GitHub Pages updates the live URL within about a minute.

## Notes

- The repo is **public**. Anything genuinely sensitive (real financial or
  personal detail) should be flagged and kept out of here.
- `index.html` is generated. Do not hand-edit it; edit `manifest.json` and
  rerun `build.py`.
- **Design system:** the hub and every artifact share one look — *Atlas-glass*
  (periwinkle sky gradient, Instrument Sans, frosted-glass white cards, pill
  chips, iris/violet accent). The canonical starting point is
  `templates/artifact.html`. Don't invent a per-page theme; start from the
  template so the collection reads as one system.
