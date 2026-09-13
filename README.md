# Temperature-Calibrated Reservoirs

Reproducibility package for **Temperature-Calibrated Reservoirs: Safe Operating Regions and Test-Time Path Indicators**.

**Author:** Ildefons Magrans de Abril  
**Affiliation:** Universitat Politècnica de Catalunya - BarcelonaTech (UPC)

## What is in this repository

The repository contains the manuscript v18.3 source, frozen manuscript tables and figures,
publication-facing notebooks, common reservoir utilities, and verification checks.

The computational record has two provenance classes:

1. **Original executed analyses:** M23, SRP04b, and SRP05. Their original full-execution outputs
   are retained in the notebooks and the original notebook files are archived unchanged.
2. **Publication reconstructions:** M19a-d, M20a, M20b, M20c2, and M21. The original June 2026
   notebook binaries could not be recovered. The repository preserves their historical manuscript
   results and provides clean, explicitly labelled protocol reproductions instead of presenting
   reconstructed files as originals. See `PROVENANCE.md`.

## Notebook order

| # | Notebook | Role | Current execution status |
|---|---|---|---|
| 01 | `01_safe_region_transfer_M19a.ipynb` | Core validation-safe-region transfer | Executed fresh replication |
| 02 | `02_safe_region_controls_M19b.ipynb` | Same-width and inside/outside controls | Executed fresh replication |
| 03 | `03_indicator_reliability_M19c.ipynb` | Prediction-variation indicators | Executed fresh replication |
| 04 | `04_standard_tasks_M19d.ipynb` | Standard-task boundary panel | Executed fresh replication |
| 05 | `05_structural_path_ablation_M20a.ipynb` | Temperature/gain/leak/sparsity comparison | Executed fresh replication |
| 06 | `06_appliances_energy_M20b.ipynb` | UCI Appliances Energy | Preflight executed; requires public data |
| 07 | `07_air_quality_M20c2.ipynb` | UCI Air Quality | Preflight executed; requires public data |
| 08 | `08_structural_audit_M21.ipynb` | Width/tolerance/structural audit | Executed |
| 09 | `09_grid_size_robustness_M23.ipynb` | Grid-density and reservoir-size robustness | Original full execution retained; current-environment smoke test passed |
| 10 | `10_distribution_shift_SRP04b.ipynb` | Held-out shift feasibility audit | Original full execution retained; current-environment smoke test passed |
| 11 | `11_shift_postprocessing_SRP05.ipynb` | Shift-audit post-processing | Original full execution retained |

## Recommended run sequence

Create the environment, then run notebooks 01 through 11 in numerical order. Notebooks 06 and
07 need the public UCI files described in `data/README.md`.

```bash
conda env create -f environment.yml
conda activate temperature-calibrated-reservoirs
jupyter lab
```

To run the repository-level verification checks:

```bash
python tests/verify_repository.py
```

## Historical versus fresh numbers

`results/frozen/` preserves the historical numerical records assembled with manuscript v18.1.
`results/reproduced/` contains fresh outputs produced by the publication reconstruction. They are
deliberately kept separate, and the reconstructed notebooks are not tuned to reproduce historical
point estimates. The current v18.3 publication tables are in `manuscript/tables/`; v18.3 applies the
safe-region metric-consistency corrections documented in `manuscript/CHANGELOG_V18_3.md`.

## Manuscript

The `manuscript/` directory contains the v18.3 LaTeX source, bibliography, publication tables,
version changelogs, Overleaf notes, and the compiled v18.3 preview. The v18.3 consistency update
uses each study's native safe-region tolerance and a common full-test best-safe gain definition.

## License

Source code and computational notebooks in this repository are released under
the MIT License. The manuscript and third-party datasets are not covered by
this software license and remain subject to their respective copyright and
licensing terms.
