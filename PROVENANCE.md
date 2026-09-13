# Computational provenance

This release separates **historical manuscript evidence** from **fresh publication reproductions**.
That distinction is intentional.

## Original executed notebooks retained

- `09_grid_size_robustness_M23.ipynb`
- `10_distribution_shift_SRP04b.ipynb`
- `11_shift_postprocessing_SRP05.ipynb`

The main publication copies retain the original full-execution outputs. The byte-level originals
are also stored under `archive/original_notebooks/`.

## Reconstructed publication notebooks

The original June 2026 notebook binaries for M19a-d, M20a, M20b, M20c2, and M21 were not
recoverable from the project archive. Their filenames, scientific roles, manuscript summaries,
and many experimental settings were recovered from the manuscript history and project record.

The repository therefore does **not** pretend that reconstructed files are the lost originals.

- M19a-c preserve the exact historical summary values and also run fresh protocol replications.
  The recovered M19a settings `TRIALS=12` and seed `20260621` are used where applicable, while
  unrecovered task-composition details are explicitly identified.
- M19d and M20a run fresh protocol replications using the preserved M23/M26 implementation
  lineage and the recovered task lists/settings.
- M20b and M20c2 contain executable real-data reconstructions and preserve the historical
  manuscript values. They require the public UCI files in `data/`.
- M21 is a post-hoc audit. It preserves the historical audit record and also summarizes fresh
  reconstructed M20a outputs when available.

## Historical frozen results

`results/frozen/` preserves the numerical records assembled with manuscript v18.1. These files
remain archival evidence and are not silently rewritten to match later manuscript cleanup.

## Manuscript v18.3 consistency layer

The current publication source is manuscript v18.3. Its publication-facing tables live under
`manuscript/tables/`. Version 18.3 applies the native safe-region absolute tolerance of each audited
study and a single full-test `safe_best_gain_vs_default` definition across the path-comparison,
real-data, and M21 summary tables. The exact changes are documented in
`manuscript/CHANGELOG_V18_3.md`.

This means that `results/frozen/` and `manuscript/tables/` serve different purposes: the former
preserves the historical record, while the latter is the current publication layer.

## Fresh results

`results/reproduced/` contains outputs generated in this repository. Fresh results are kept
separate from the historical manuscript values so discrepancies remain visible.
