# Agent notes

## Repository layout

- `zaloha-data/` is the original HTTrack mirror of teslakatalog.cz. Treat it as source archival material: do not rewrite mirrored HTML, paths, `hts-cache/`, or `hts-log.txt` unless the task explicitly targets the raw mirror.
- `zaloha-dataset-clean/` is the processed archival dataset, not Hugo content. Its `index.md` files are metadata, and scans/PDFs stay beside their corresponding component records.
- `stranka/` is reserved for a future presentation site; it currently has no implementation or build configuration.

## Dataset changes

- When changing component inventory, verify the category totals in `zaloha-dataset-clean/STRUCTURE.md` and the paths in `zaloha-dataset-clean/MANIFEST.tsv` remain accurate.
- `zaloha-dataset-clean/AUDIT_COMPARISON.md` documents the HTML-only mirror audit. Do not claim it verifies image or PDF bytes against the live site.
- The processed dataset contains 2,853 unique component types. The 58 IO-package records are separate package entries, not component types.

## Assets and verification

- PDFs are tracked through Git LFS (`.gitattributes`); do not replace them with ordinary Git blobs.
- There are no detected build, test, lint, formatter, or package-manager commands. For documentation-only changes, run `git diff --check`.
