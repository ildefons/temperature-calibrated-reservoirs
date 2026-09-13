# Real-data reconstruction audit (v18.3)

Date: 2026-09-13  
Base manuscript/repository checkpoint: v18.3 / commit `d1ca02bf50edf79eb5c601d276f95d81f4f6d797`

The official UCI Appliances Energy Prediction and Air Quality archives were used for fresh execution
of the reconstructed M20b and M20c2 notebooks.

## Repairs required for faithful execution of the stated v18.3 reconstruction

1. M20b and M20c2 now pass `abs_tol=0.002` explicitly, matching the native real-data tolerance stated
   in manuscript v18.3.
2. M20c2 parses the official UCI CSV with `decimal=','`.
3. M20c2 parses the official `Time` field using `%H.%M.%S` as part of the explicit
   `%d/%m/%Y %H.%M.%S` datetime format.

These are execution/provenance repairs. No attempt was made to tune parameters to recover historical
point estimates.

## Fresh reconstructed temperature-path results

| Study | Fresh safe width | Fresh default test NRMSE | Fresh best-safe test NRMSE | Fresh full-test safe gain | Publication-facing v18.3 gain |
|---|---:|---:|---:|---:|---:|
| Appliances Energy | 3/13 | 1.0152766569 | 0.9929708973 | 0.0223057595 | 0.00014 |
| Air Quality | 2/13 | 0.8039739340 | 0.8039739340 | 0.0000000000 | 0.01635 |

The fresh reconstructions therefore do not numerically reproduce the historical real-data point
estimates. This is consistent with the repository's provenance statement that the original June 2026
M20b/M20c2 notebook binaries were not recoverable.

The publication-facing v18.3 table is intentionally left unchanged. Fresh results are stored in
`results/reproduced/m20b_replication_summary.csv` and
`results/reproduced/m20c2_replication_summary.csv`.
