# vernglaser.com

Source for the academic website of **Vern L. Glaser**, Professor of Entrepreneurship and
Family Enterprise at the University of Alberta and Academic Director of the Alberta Business
Family Institute (ABFI).

Built with [Quarto](https://quarto.org). The site is rendered and deployed to GitHub Pages
automatically on every push to `main` (see `.github/workflows/publish.yml`) — no local build needed.

## Editing

- **Pages** are plain Markdown: `index.qmd`, `about.qmd`, `publications.qmd`, `teaching.qmd`, `cv.qmd`.
- **Site config + navigation:** `_quarto.yml`. **Theme/design:** `brand.scss`.
- **Preview locally** (optional): `quarto preview`. One-off build: `quarto render` (output goes to `_site/`, which is not committed).
- **Publish:** commit and push to `main`. GitHub Actions rebuilds and publishes in ~1 minute.

The CV PDF in `assets/` is generated from a separate RenderCV source and copied in when the CV is re-rendered.
