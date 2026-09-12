# Execution status

Verification pass completed on **2026-09-13**.

## Fresh executions in this environment

- **M19a, M19b, M19c, M19d:** reconstructed publication protocols executed from clean notebook kernels and saved with outputs.
- **M20a:** reconstructed four-path protocol executed from a clean notebook kernel and saved with outputs.
- **M21:** reconstructed structural audit executed from a clean notebook kernel and saved with outputs.
- **M20b (Appliances Energy)** and **M20c2 (Air Quality):** notebook preflight and preprocessing definitions executed successfully. The full numerical cells are intentionally gated until the two public UCI CSV files are present in `data/`. This runtime has no direct external-file network access, so the datasets were not silently replaced or mocked.
- **M23:** the publication notebook retains the original full execution. A fresh current-environment smoke execution was rerun successfully in `tests/M23_smoke_executed.ipynb`.
- **SRP04b:** the publication notebook retains the original full execution. A fresh current-environment smoke execution was rerun successfully in `tests/SRP04b_smoke_executed.ipynb`.
- **SRP05:** the publication notebook retains the original full execution and its ten retained validity checks.

## Repository checks

`python tests/verify_repository.py` reports **48/48 passing checks**.

Historical manuscript values and fresh reconstructed outputs are deliberately kept separate. The reconstructed M19--M21 notebooks are protocol replications, not falsely presented as recovered June-2026 binaries, and they are not tuned to force exact agreement with the historical point estimates.

## Important release note

Before public archival release, run notebooks 06 and 07 with the official UCI CSV files. The repository's `data/README.md` gives the expected filenames and official sources.
