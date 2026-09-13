# Execution status

Submission-layer execution pass completed on **2026-09-13** and frozen for the *Neural Networks* v19.5 submission.

## M19-M21

- **M19a-M19d:** clean current-protocol executions completed and saved with outputs.
- **M20a:** clean current four-path execution completed and saved with outputs.
- **M20b (Appliances Energy):** four deterministic chronological splits executed on the official UCI CSV.
- **M20c2 (Air Quality):** four deterministic chronological splits executed on the official UCI CSV with explicit decimal-comma and timestamp parsing.
- **M21:** regenerated from executable M20 outputs; no archived audit constants are used.

Key real-data temperature results:
- Appliances Energy: mean best-safe gain `0.006847`, safe-minus-control `-0.009347` with 95% split-bootstrap interval `[-0.032746, 0.019329]`.
- UCI Air Quality: mean best-safe gain `0.008563`, safe-minus-control `+0.039252` with 95% split-bootstrap interval `[0.011101, 0.079618]`.

## Retained original analyses

- **M23:** original full execution retained; current-environment smoke test available.
- **SRP04b:** original full execution retained; current-environment smoke test available.
- **SRP05:** original full execution retained.

## Verification

The executable-evidence reset passed both repository-level and submission-layer verification before the v19.5 formatting freeze. V19.5 changes no experimental outputs or publication-facing numerical values.

Run:

```bash
python tests/verify_repository.py
python tests/verify_submission_layer.py
```
