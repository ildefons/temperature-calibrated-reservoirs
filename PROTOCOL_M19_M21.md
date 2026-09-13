# Frozen M19-M21 submission protocol

This protocol is fixed for manuscript v19.0.

## Common reservoir path

- Allocation-temperature grid: 13 log-spaced values from 0.08 to 3.50.
- Reference temperature for gain/leak paths: 1.0.
- Gain grid: 13 values from 0.25 to 1.75.
- Leak grid: 13 values from 0.10 to 1.0.
- Hard sparsity: 13 top-k values spanning 1 to N-1.
- Input scale: 0.8.
- Bulk recurrent RMS target: `s0=1`.
- Safe-region rule: connected component containing the validation-best candidate under `max(epsilon_abs, epsilon_rel * validation utility range)`.
- `epsilon_rel=0.10` unless explicitly varied in the M21 sensitivity audit.

## M19a-M19c

- Tasks: controlled delayed signal with white noise + distractor, delayed memory, NARMA10, Lorenz-x.
- 12 trials per task.
- N=60, K=13, train/validation/test=1200/500/500 after washout 100.
- ridge=1e-5.
- seeds: M19a 20260621, M19b 20260622, M19c 20260623.
- M19c windows: length 50, stride 25; uncertainty resamples task-trial clusters.

## M19d

- Tasks: Lorenz-x, Mackey-Glass, delayed memory, NARMA10.
- 8 trials per task.
- seed=20260718; other reservoir settings as above.

## M20a

- Tasks: controlled d1 clean, controlled d20 clean, controlled d20 white+distractor, delayed memory, NARMA10, Mackey-Glass, Lorenz-x.
- 4 trials per task.
- seed=20260718, N=60, K=13, ridge=1e-5.
- `epsilon_abs=0.005`.

## M20b Appliances Energy

- Official UCI `energydata_complete.csv`.
- Target: `log1p(Appliances[t+6])`.
- 32 input features after time encodings.
- 4 deterministic chronological splits, each 2500/1000/1000.
- Split starts are evenly spaced from 0 to the latest complete block.
- N=50, K=13, ridge=1e-4, seed=20260718.
- `epsilon_abs=0.002`.

## M20c2 Air Quality

- Official UCI `AirQualityUCI.csv`.
- CSV parsing: `sep=';'`, `decimal=','`; missing sentinel -200 is interpolated; datetime format `%d/%m/%Y %H.%M.%S`.
- Target: future `C6H6(GT)` at h=1 hour.
- 19 input features after time encodings.
- 4 deterministic chronological splits, each 1500/600/600.
- N=50, K=13, ridge=1e-4, seed=20260718.
- `epsilon_abs=0.002`.

## M21

M21 is derived from the executable M20 outputs. The synthetic tolerance sensitivity re-evaluates M20a at `epsilon_rel` in {0.05, 0.10, 0.15, 0.20}. Secondary threshold summaries are derived from executable M19c/M20b/M20c2 window tables.

## Uncertainty

Bootstrap summaries use 30,000 resamples. Real-data confidence intervals resample the four chronological split-level units. M19c high-minus-low indicator uncertainty resamples complete task-trial clusters.
