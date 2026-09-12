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
- M21 is a post-hoc audit. It preserves the historical audit table and also summarizes fresh
  reconstructed M20a outputs when available.

## Frozen results

`results/frozen/` contains the numerical tables integrated into manuscript v18.1. These files are
archival records of the manuscript claims, not outputs reverse-engineered by the reconstructed
notebooks.

## Fresh results

`results/reproduced/` contains outputs generated in this repository. Fresh results are kept
separate from the historical manuscript values so discrepancies remain visible.
