# Temperature-Calibrated Reservoirs - Overleaf Project (v18)

Main file: `main.tex`

This project is self-contained for Overleaf upload. It uses a manual `thebibliography` block inside `main.tex`, so BibTeX/Biber is not required. `references.bib` is included as a convenience/back-up reference file.

Recommended Overleaf settings:
- Compiler: pdfLaTeX
- Main document: `main.tex`

Submission author: Ildefons Magrans de Abril, Universitat Politecnica de Catalunya - BarcelonaTech (UPC), Barcelona, Spain, ildefons.magrans@upc.edu.

## Version 18

Version 18 is the human-reader and reproducibility consolidation. It foregrounds allocation temperature as a distinct reservoir structural axis, replaces notebook-centric prose with self-contained experimental descriptions, simplifies specialized terminology, expands the distribution-shift protocol, improves section/table/figure cross-referencing, updates adjacent related work, and preserves the v17 entropy-notation clarification.

See `CHANGELOG_V18.md` for the detailed change list.

## V18.1 note

V18.1 is a minimal consensus cleanup of v18. It removes wording that could imply allocation temperature is a smoothed/generalized form of sparsity. No science or results changed.


## v18.2 repository update

The manuscript now links to the public reproducibility repository and documents the distinction between retained original executed notebooks and publication-reconstruction notebooks.

Repository: https://github.com/ildefons/temperature-calibrated-reservoirs

## v18.3 consistency update

V18.3 applies the native safe-region tolerance of each audited study and uses a single full-test best-safe gain definition across the path-comparison, real-data, and M21 summary tables. See `CHANGELOG_V18_3.md`.

## v18.4 provenance clarification

V18.4 clarifies that the real-data table contains retained historical summaries. Full repaired executions of the public-data reconstruction notebooks preserve the documented structural temperature path but do not numerically recover the historical operational point estimates. See `CHANGELOG_V18_4.md`.
