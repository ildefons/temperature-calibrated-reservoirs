# Execution status

Verification/reconstruction pass updated on **2026-09-13**.

## Fresh executions in this environment

- **M19a, M19b, M19c, M19d:** reconstructed publication protocols executed from clean notebook kernels and saved with outputs.
- **M20a:** reconstructed four-path protocol executed from a clean notebook kernel and saved with outputs.
- **M21:** reconstructed structural audit executed from a clean notebook kernel and saved with outputs.
- **M20b (Appliances Energy):** full reconstructed numerical protocol executed with the official UCI CSV. The v18.3 native real-data tolerance `epsilon_abs=0.002` is passed explicitly. The fresh temperature-path safe gain is `0.0223057595`, which does not reproduce the publication-facing historical value `0.00014`.
- **M20c2 (Air Quality):** full reconstructed numerical protocol executed with the official UCI CSV after explicit parsing of decimal commas and `HH.MM.SS` time strings. The v18.3 native real-data tolerance `epsilon_abs=0.002` is passed explicitly. The fresh temperature-path safe gain is `0.0`, which does not reproduce the publication-facing historical value `0.01635`.
- **M23:** the publication notebook retains the original full execution. A fresh current-environment smoke execution was rerun successfully in `tests/M23_smoke_executed.ipynb`.
- **SRP04b:** the publication notebook retains the original full execution. A fresh current-environment smoke execution was rerun successfully in `tests/SRP04b_smoke_executed.ipynb`.
- **SRP05:** the publication notebook retains the original full execution and its ten retained validity checks.

## Real-data reconstruction interpretation

The M20b/M20c2 fresh outputs are **protocol reconstructions**, not recovered historical experiments. The original June 2026 notebook binaries were not recoverable, so exact numerical agreement with the historical manuscript point estimates cannot be claimed. The fresh outputs are stored only under `results/reproduced/` and do not overwrite `manuscript/tables/table_real_world.csv` or `results/frozen/`.

For M20c2, the official UCI Air Quality CSV itself requires two explicit parser details that were absent from the earlier reconstructed notebook: `decimal=','` and datetime format `%d/%m/%Y %H.%M.%S`.

## Repository checks

The previous repository verification pass reported **48/48 passing checks**. Those checks predate the repaired full M20b/M20c2 execution and should be rerun after these repaired artifacts are integrated into the repository.

Historical manuscript values and fresh reconstructed outputs remain deliberately separated. The reconstructed M19--M21 notebooks are protocol replications, not falsely presented as recovered June-2026 binaries, and they are not tuned to force exact agreement with historical point estimates.
