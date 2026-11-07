# Agent notes

## Repository layout

- `zaloha-data/` is the original HTTrack mirror of teslakatalog.cz. Treat it as source archival material: do not rewrite mirrored HTML, paths, `hts-cache/`, or `hts-log.txt` unless the task explicitly targets the raw mirror.
- `zaloha-dataset-clean/` is the processed archival dataset, not Hugo content. Its `index.md` files are metadata, and scans/PDFs stay beside their corresponding component records.
- `stranka/` is the Hugo presentation site, using the Hextra Hugo module. It is a self-contained project: keep its build and font-generation inputs inside `stranka/`; do not make them depend on sibling directories. See `stranka/README.md`.

## Dataset changes

- When changing component inventory, verify the category totals in `zaloha-dataset-clean/STRUCTURE.md` and the paths in `zaloha-dataset-clean/MANIFEST.tsv` remain accurate.
- `zaloha-dataset-clean/AUDIT_COMPARISON.md` documents the HTML-only mirror audit. Do not claim it verifies image or PDF bytes against the live site.
- The processed dataset contains 2,853 unique component types. The 58 IO-package records are separate package entries, not component types.

## Assets and verification

- PDFs are tracked through Git LFS (`.gitattributes`); do not replace them with ordinary Git blobs.
- The site can be built with `hugo` or previewed with `hugo server` from `stranka/`. Hugo and Go are required; resolving its Hextra module may require network access.
- The header uses the pre-generated `stranka/static/fonts/tesla-katalog-display.woff2`; normal Hugo builds do not regenerate the font and do not require Python or WOFF2 tools.
- The font source of truth for this site is `stranka/font-sources/tesla-slovak-uppercase-vector.svg`; it is a separate working copy of the artwork in `grafika/`, not automatically synchronized. If the source or generator changes, run `python3 scripts/generate_tesla_display_font.py` and `python3 scripts/test_tesla_display_font.py` from `stranka/`, then visually verify the output. Generation requires Python, FontTools and `woff2_compress`; tests also require `woff2_decompress`.
- For documentation-only changes, run `git diff --check`.
