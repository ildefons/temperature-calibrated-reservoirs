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
- M20b and M20c2 are executable real-data reconstructions using the official UCI datasets.
  The reconstruction passes the native real-data `epsilon_abs=0.002` explicitly. M20c2 also parses
  the official CSV's decimal commas and `HH.MM.SS` time strings explicitly.
- M21 is a post-hoc audit. It preserves the historical audit record and also summarizes fresh
  reconstructed M20a outputs when available.

## Real-data reconstruction audit

Fresh executions of M20b and M20c2 on the official UCI files confirm that the current reconstructed
protocols are not numerically equivalent to the lost historical June experiments. For the temperature
path, the fresh full-test best-safe gains are `0.0223057595` for Appliances Energy and `0.0` for Air
Quality, compared with the retained publication-facing values `0.00014` and `0.01635`, respectively.

This discrepancy is retained as provenance evidence. It is **not** resolved by tuning the reconstructed
notebooks to force agreement, and it is **not** used to silently replace the historical publication
numbers. The fresh summaries live under `results/reproduced/`.

## Historical frozen results

`results/frozen/` preserves the numerical records assembled with manuscript v18.1. These files
remain archival evidence and are not silently rewritten to match later manuscript cleanup.

## Manuscript v18.4 publication layer

The current publication source is manuscript v18.4. Its numerical publication-facing tables remain
those of v18.3: native safe-region absolute tolerances are used for each audited study and a single
full-test `safe_best_gain_vs_default` definition is used across the path-comparison, real-data, and
M21 summary tables. Version 18.4 does not change those values. It clarifies that the two real-data
rows are retained historical summaries because the repaired public-data reconstructions do not
numerically recover their operational point estimates. See `manuscript/CHANGELOG_V18_3.md` and
`manuscript/CHANGELOG_V18_4.md`.

This means that `results/frozen/`, `results/reproduced/`, and `manuscript/tables/` serve different
purposes: the first preserves the historical archive, the second records fresh reconstruction outputs,
and the third is the current publication-facing layer.

## Fresh results

`results/reproduced/` contains outputs generated in this repository. Fresh results are kept
separate from the historical manuscript values so discrepancies remain visible.
