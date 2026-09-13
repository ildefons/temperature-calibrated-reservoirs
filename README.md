# Temperature-Calibrated Reservoirs

Reproducibility package for **Temperature-Calibrated Reservoirs: Safe Operating Regions and Test-Time Path Indicators**.

**Author:** Ildefons Magrans de Abril  
**Affiliation:** Universitat Politècnica de Catalunya - BarcelonaTech (UPC)

## Submission evidence policy

Manuscript v19.0 uses executable current-protocol results for every M19-M21 claim. Archived development-era numerical summaries are retained under `results/frozen/` for history only and are not used by the submission layer.

M23, SRP04b, and SRP05 retain their original full executed analyses.

## Notebook order

| # | Notebook | Role | Submission status |
|---|---|---|---|
| 01 | `01_safe_region_transfer_M19a.ipynb` | Core validation-safe-region transfer | Fresh executable evidence |
| 02 | `02_safe_region_controls_M19b.ipynb` | Same-width and inside/outside controls | Fresh executable evidence |
| 03 | `03_indicator_reliability_M19c.ipynb` | Prediction-variation indicators | Fresh executable evidence |
| 04 | `04_standard_tasks_M19d.ipynb` | Standard-task panel | Fresh executable evidence |
| 05 | `05_structural_path_ablation_M20a.ipynb` | Temperature/gain/leak/sparsity comparison | Fresh executable evidence |
| 06 | `06_appliances_energy_M20b.ipynb` | UCI Appliances Energy, four splits | Fresh executable evidence |
| 07 | `07_air_quality_M20c2.ipynb` | UCI Air Quality, four splits | Fresh executable evidence |
| 08 | `08_structural_audit_M21.ipynb` | Derived width/tolerance/structural audit | Fresh executable evidence |
| 09 | `09_grid_size_robustness_M23.ipynb` | Grid-density and reservoir-size robustness | Original full execution retained |
| 10 | `10_distribution_shift_SRP04b.ipynb` | Held-out shift feasibility audit | Original full execution retained |
| 11 | `11_shift_postprocessing_SRP05.ipynb` | Shift-audit post-processing | Original full execution retained |

Notebooks 06 and 07 require the public UCI files described in `data/README.md`.

```bash
conda env create -f environment.yml
conda activate temperature-calibrated-reservoirs
jupyter lab
```

Verification:

```bash
python tests/verify_repository.py
python tests/verify_submission_layer.py
```

## Manuscript

`manuscript/` contains the v19.0 LaTeX source, generated publication tables, changelog, Overleaf notes, and compiled preview.

## License

Source code and computational notebooks are released under the MIT License. The manuscript and third-party datasets remain subject to their respective copyright and licensing terms.
