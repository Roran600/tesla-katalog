# Agent notes

## Repository layout

- `zaloha-data/` is the original HTTrack mirror of teslakatalog.cz. Treat it as source archival material: do not rewrite mirrored HTML, paths, `hts-cache/`, or `hts-log.txt` unless the task explicitly targets the raw mirror.
- `zaloha-dataset-clean/` is the processed archival dataset, not Hugo content. Its `index.md` files are metadata, and scans/PDFs stay beside their corresponding component records.
- `stranka/` is the Hugo presentation site, using the Hextra Hugo module. It is a self-contained project: keep its build and font-generation inputs inside `stranka/`; do not make them depend on sibling directories. See `stranka/README.md`.
- `stranka/dizajn/` contains the color-scheme proposal, standalone mockup and its desktop/mobile screenshots. They are reference material, not Hugo content or build inputs; the mockup references the scan in `stranka/static/images/`.

## Dataset changes

- When changing component inventory, verify the category totals in `zaloha-dataset-clean/STRUCTURE.md` and the paths in `zaloha-dataset-clean/MANIFEST.tsv` remain accurate.
- `zaloha-dataset-clean/AUDIT_COMPARISON.md` documents the HTML-only mirror audit. Do not claim it verifies image or PDF bytes against the live site.
- The processed dataset contains 2,853 unique component types. The 58 IO-package records are separate package entries, not component types.

## Assets and verification

- PDFs are tracked through Git LFS (`.gitattributes`); do not replace them with ordinary Git blobs.
- The site can be built with `hugo` or previewed with `hugo server` from `stranka/`. Hugo and Go are required; resolving its Hextra module may require network access.
- `stranka/content/docs/` and `stranka/content/blog/` use Hextra's native documentation and blog layouts. Their sample pages are explicitly labelled; keep them labelled or remove them when real content replaces them. Documentation sidebar order comes from the content tree and `weight`; explicit `prev`/`next` links must be updated when pages move or samples are removed. Blog posts use dates and the blog index links to its RSS feed.
- `stranka/content/docs/_index.md` is the documentation root. Its `katalog/_index.md` section is the introduction and parent of the category pages; categories are placeholders until catalogue records are added. Keep their order and links consistent, and retain `sidebar.open: true` on the catalogue section so categories start expanded.
- The existing `stranka/layouts/_partials/sidebar.html` override adds the documentation root above the desktop sidebar tree and highlights it on `/docs/`; mobile navigation instead uses the main-menu label `Docs 📚`. Do not add a duplicate `/docs/` link to `menu.sidebar`. This override is based on Hextra 0.13.0 and must be compared with upstream when upgrading.
- Documentation pages and blog articles that offer Hextra's copy-page menu require `contextMenu: true` and a `markdown` output in their front matter. Preserve RSS in section outputs where used. The exported Markdown is source content and can contain Hugo shortcodes. Slovak UI strings are in `stranka/i18n/sk.yaml` and the Tesla palette and Hextra-specific overrides are in `stranka/assets/css/custom.css`.
- Header brand and main-menu labels, configurable footer texts, and docs and blog titles support explicit Unicode emoji and Hugo emoji shortcodes as safely escaped text. Some existing menu and sample-content titles deliberately contain emoji for testing; do not add others automatically. The Markdown export keeps the author's original shortcode. Emoji-related overrides in `stranka/layouts/` and `stranka/assets/json/search-data.json` are based on Hextra 0.13.0; compare them with upstream when upgrading the module.
- Run `python3 scripts/test_emoji.py` from `stranka/` when changing emoji rendering, relevant templates, navigation or search. It builds an isolated temporary copy and checks HTML escaping, titles, search, RSS, Markdown, subpath links and the desktop documentation root link; it creates temporary documentation fixtures and depends on the sample blog article and `Docs 📚` menu label. Update the test if those change. It does not replace browser and clipboard checks.
- When changing docs or blog, verify indexes and individual pages, sidebar/mobile menu, table of contents, pagination, search, and copy-page behavior as applicable. Check desktop and mobile in light and dark modes and preserve the home page, header, and footer. Build with a subpath base URL and check internal links and assets; use a separate destination rather than overwriting existing work in `stranka/public/`. See `stranka/README.md` for commands.
- The home page uses Hextra's `hextra-home` layout and the project shortcode `stranka/layouts/_shortcodes/tesla-home.html`. Its content, image, responsive breakpoints and light/dark styling are configured under `params.home` in `stranka/hugo.yaml`; CSS defaults and styling live in `stranka/assets/css/custom.css`. Keep these in sync when changing the home page.
- Home-page images must remain inside `stranka/static/`; image paths are relative to that directory and must work when the site is deployed under a URL subpath. Check desktop and mobile layouts and both color modes when changing the design. Test configurable defaults and explicit `false` values when changing the shortcode.
- The header uses the pre-generated `stranka/static/fonts/tesla-katalog-display.woff2`; normal Hugo builds do not regenerate the font and do not require Python or WOFF2 tools.
- The font source of truth for this site is `stranka/font-sources/tesla-slovak-uppercase-vector.svg`; it is a separate working copy of the artwork in `grafika/`, not automatically synchronized. If the source or generator changes, run `python3 scripts/generate_tesla_display_font.py` and `python3 scripts/test_tesla_display_font.py` from `stranka/`, then visually verify the output. Generation requires Python, FontTools and `woff2_compress`; tests also require `woff2_decompress`.
- For documentation-only changes, run `git diff --check`.
