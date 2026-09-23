"""Post-render cleanup for every rendered page.

1. Removes Quarto's title-block <header>s. Each page brings its own h1 banner, and the
   auto title block (hidden with CSS) left a second h1 and a duplicate id in the DOM.
   An empty title-block partial does not work: Quarto then hoists the page's first h1.
2. Replaces the navbar/footer Bootstrap Icons (<i class="bi bi-…">) with inline SVGs of the
   same glyphs. With no icon-font glyph on the page, the 176 KB bootstrap-icons font is never
   downloaded. Paths were extracted from Quarto's bootstrap-icons.woff (300-unit em); add an
   entry to ICONS before using a new `icon:` in _quarto.yml, or that icon falls back to the font.
3. Inserts a skip-to-content link as the first element of <body>. Quarto's
   include-before-body lands inside <main>, after the navbar, which defeats the purpose.
"""
import os, re, glob

SKIP = '<a class="skip-link" href="#quarto-document-content">Skip to main content</a>'
TITLE_BLOCK = re.compile(r'<header id="title-block-header"[^>]*>.*?</header>\s*', re.S)
BODY = re.compile(r'(<body[^>]*>)')
ICON = re.compile(r'<i class="bi bi-([a-z0-9-]+)" role="img" aria-label="([^"]*)">\s*</i>')
ICONS = {
    "linkedin": "M0 21Q0 13 6.5 6.5Q13 0 22 0H278Q287 0 293.5 6.5Q300 13 300 21V279Q300 287 293.5 293.5Q287 300 278 300H22Q13 300 6.5 293.5Q0 287 0 279ZM93 251V116H48V251ZM70 97Q82 97 89.0 90.5Q96 84 95.5 74.0Q95 64 88.5 57.0Q82 50 70.5 50.0Q59 50 52.0 57.0Q45 64 45.0 74.0Q45 84 52.0 90.5Q59 97 70 97ZM162 251V175Q162 168 164 164Q166 158 172.0 153.0Q178 148 187 148Q199 148 204.5 156.0Q210 164 210 179V251H255V173Q255 143 240.5 127.5Q226 112 203 112Q187 112 176 120Q168 125 162 135V116H117Q118 124 117 188V251Z",
    "envelope-fill": "M1 67Q4 54 14.0 45.5Q24 37 37 37H263Q276 37 286.0 45.5Q296 54 299 67L150 158ZM0 88V221L109 155ZM127 166 4 241Q8 251 17.5 257.0Q27 263 37 263H263Q273 263 282.5 257.0Q292 251 296 241L173 166L150 180ZM191 155 300 221V88Z"
}

def svg_icon(m):
    name, label = m.group(1), m.group(2)
    if name not in ICONS:
        return m.group(0)
    return ('<svg class="bi-svg" viewBox="0 0 300 300" width="1em" height="1em" fill="currentColor" '
            f'role="img" aria-label="{label}"><path d="{ICONS[name]}"/></svg>')

files = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES", "").split()
if not files:
    files = glob.glob(os.path.join(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"), "*.html"))

for path in files:
    if not path.endswith(".html") or not os.path.exists(path):
        continue
    html = open(path, encoding="utf-8").read()
    out = TITLE_BLOCK.sub("", html)
    out = ICON.sub(svg_icon, out)
    if SKIP not in out:
        out = BODY.sub(r"\1\n" + SKIP, out, count=1)
    if out != html:
        open(path, "w", encoding="utf-8").write(out)
