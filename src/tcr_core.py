"""Core utilities for the Temperature-Calibrated Reservoirs reproduction notebooks.

The functions here follow the reservoir construction and calibration protocol used in
M23 and the later path-comparison lineage. They are intentionally small and explicit so
that notebook-level experiments remain easy to audit.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
import numpy as np
import pandas as pd


def stable_int(text: str) -> int:
    """Deterministically map text to a small non-negative integer."""
    value = 0
    for ch in str(text):
        value = (value * 131 + ord(ch)) % 10_000_000
    return int(value)


def stable_softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax."""
    z = np.asarray(x, dtype=float) - np.max(x, axis=axis, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / (np.sum(exp_z, axis=axis, keepdims=True) + 1e-12)


def normalize_series(x: np.ndarray) -> np.ndarray:
    """Standardize a one-dimensional series using its own mean and standard deviation."""
    x = np.asarray(x, dtype=float)
    return (x - np.mean(x)) / (np.std(x) + 1e-12)


def add_bias(X: np.ndarray) -> np.ndarray:
    """Append a constant readout feature."""
    X = np.asarray(X, dtype=float)
    return np.concatenate([X, np.ones((len(X), 1))], axis=1)


def nrmse(y: np.ndarray, pred: np.ndarray) -> float:
    """Normalized RMSE, using the target standard deviation as the scale."""
    y = np.asarray(y, dtype=float).reshape(-1)
    pred = np.asarray(pred, dtype=float).reshape(-1)
    return float(np.sqrt(np.mean((pred - y) ** 2)) / (np.std(y) + 1e-12))


def bootstrap_ci_mean(values: Sequence[float], n_boot: int = 30000,
                      seed: int = 0) -> Tuple[float, float, float]:
    """Percentile bootstrap interval for a mean."""
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return np.nan, np.nan, np.nan
    if len(x) == 1:
        return float(x[0]), float(x[0]), float(x[0])
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(int(n_boot), len(x)))
    boot = x[idx].mean(axis=1)
    return float(x.mean()), float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))


def safe_corr(a: Sequence[float], b: Sequence[float]) -> float:
    """Pearson correlation with finite/degenerate guards."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or np.std(a[ok]) <= 1e-15 or np.std(b[ok]) <= 1e-15:
        return np.nan
    return float(np.corrcoef(a[ok], b[ok])[0, 1])


def as_two_channel(u0: np.ndarray, u1: Optional[np.ndarray] = None) -> np.ndarray:
    """Return the two-channel input convention used by the synthetic studies."""
    u0 = np.asarray(u0, dtype=float)
    if u1 is None:
        u1 = np.zeros_like(u0)
    return np.stack([normalize_series(u0), normalize_series(u1)], axis=1)


def make_ar1(T: int, rng: np.random.Generator, rho: float = 0.94) -> np.ndarray:
    x = np.zeros(T)
    eps = rng.normal(size=T)
    for t in range(1, T):
        x[t] = rho * x[t - 1] + eps[t]
    return normalize_series(x)


def make_controlled(T: int, rng: np.random.Generator, delay: int = 20,
                    white: bool = True, distractor: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """Delayed AR(1) prediction task, optionally with observation noise and distractor."""
    extended = make_ar1(T + delay + 5, rng, rho=0.95)
    observed = extended[delay:delay + T].copy()
    target = extended[:T]
    if white:
        observed += 0.75 * rng.normal(size=T)
    if distractor:
        second = make_ar1(T, rng, rho=0.97) + 0.25 * rng.normal(size=T)
    else:
        second = np.zeros(T)
    return as_two_channel(observed, second), normalize_series(target)


def make_memory_d10(T: int, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    delay = 10
    extended = rng.uniform(-1.0, 1.0, size=T + delay + 1)
    return as_two_channel(extended[delay:delay + T]), normalize_series(extended[:T])


def make_narma10(T: int, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    order, warm = 10, 150
    length = T + warm + order + 2
    for _ in range(50):
        u = rng.uniform(0.0, 0.5, size=length)
        y = np.zeros(length)
        stable = True
        with np.errstate(over="ignore", invalid="ignore"):
            for t in range(order, length - 1):
                y[t + 1] = (0.3 * y[t]
                            + 0.05 * y[t] * np.sum(y[t - order + 1:t + 1])
                            + 1.5 * u[t - order + 1] * u[t] + 0.1)
                if not np.isfinite(y[t + 1]) or abs(y[t + 1]) > 100:
                    stable = False
                    break
        start = warm + order
        if stable and np.std(y[start:start + T]) > 1e-10:
            observed = 2.0 * (u[start:start + T] - 0.25)
            return as_two_channel(observed), normalize_series(y[start:start + T])
    raise RuntimeError("Unstable NARMA10 generation")


def make_lorenz_x(T: int, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    """One-step Lorenz-x prediction using the M23 Euler-discretized generator."""
    sigma, rho, beta, dt = 10.0, 28.0, 8.0 / 3.0, 0.01
    warm, total = 1200, T + 1200 + 1
    state = np.array([1.0 + 0.01 * rng.normal(),
                      1.0 + 0.01 * rng.normal(),
                      1.0 + 0.01 * rng.normal()])
    xs = np.zeros(total)
    for t in range(total):
        xs[t] = state[0]
        x, y, z = state
        state = state + dt * np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])
    series = normalize_series(xs[warm:warm + T + 1])
    return as_two_channel(series[:-1]), normalize_series(series[1:])


def make_mackey_glass(T: int, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    """One-step Mackey-Glass task used by the later feasibility-audit lineage."""
    tau, warm = 17, 500
    length = T + warm + tau + 2
    x = np.zeros(length)
    x[:tau + 1] = 1.2 + 0.05 * rng.normal(size=tau + 1)
    for t in range(tau, length - 1):
        delayed = x[t - tau]
        x[t + 1] = x[t] + 0.2 * delayed / (1.0 + delayed ** 10) - 0.1 * x[t]
    series = normalize_series(x[warm:warm + T + 1])
    return as_two_channel(series[:-1]), normalize_series(series[1:])


def make_task(task: str, T: int, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a named synthetic task."""
    if task == "controlled_d1_clean":
        return make_controlled(T, rng, delay=1, white=False, distractor=False)
    if task == "controlled_d20_clean":
        return make_controlled(T, rng, delay=20, white=False, distractor=False)
    if task == "controlled_d20_white_plus_distractor":
        return make_controlled(T, rng, delay=20, white=True, distractor=True)
    if task == "memory_d10":
        return make_memory_d10(T, rng)
    if task == "narma10":
        return make_narma10(T, rng)
    if task == "mackey_glass":
        return make_mackey_glass(T, rng)
    if task == "lorenz_x":
        return make_lorenz_x(T, rng)
    raise ValueError(f"Unknown task: {task}")


def make_split(task: str, trial: int, seed: int, lengths=(1200, 500, 500),
               washout: int = 100) -> Tuple[np.ndarray, ...]:
    """Generate train/validation/test segments with a deterministic per-task seed."""
    rng = np.random.default_rng(int(seed) + 100_000 * int(trial) + stable_int(task))
    out: List[np.ndarray] = []
    for T in lengths:
        U, y = make_task(task, int(T) + int(washout), rng)
        out.extend([U[washout:], y[washout:]])
    return tuple(out)


def rms_normalize_bulk(M: np.ndarray, s0: float = 1.0) -> np.ndarray:
    """Set element-wise recurrent RMS to s0/sqrt(N)."""
    N = M.shape[0]
    return s0 * M / (np.sqrt(N) * (np.sqrt(np.mean(M ** 2)) + 1e-12))


def make_base_substrate(N: int, input_dim: int, task: str, trial: int,
                        seed: int, input_scale: float = 0.8) -> Dict[str, np.ndarray]:
    """Sample fixed scores, signs, and input weights for one reservoir instance."""
    rng_seed = int(seed) + 7_000_000 + 100_000 * int(trial) + 1_000 * int(N) + stable_int(task)
    rng = np.random.default_rng(rng_seed)
    scores = rng.normal(size=(N, N))
    np.fill_diagonal(scores, -1e9)
    signs = rng.choice([-1.0, 1.0], size=(N, N))
    np.fill_diagonal(signs, 0.0)
    Win = rng.uniform(-input_scale, input_scale, size=(N, input_dim))
    return {"scores": scores, "signs": signs, "Win": Win}


def temperature_matrix(base: Dict[str, np.ndarray], tau: float, s0: float = 1.0) -> np.ndarray:
    allocation = stable_softmax(base["scores"] / float(tau), axis=1)
    return rms_normalize_bulk(base["signs"] * allocation, s0=s0)


def make_path_bank(path: str, base: Dict[str, np.ndarray], N: int, K: int = 13,
                   tau_min: float = 0.08, tau_max: float = 3.50,
                   reference_tau: float = 1.0, gain_min: float = 0.25,
                   gain_max: float = 1.75, leak_min: float = 0.10,
                   leak_max: float = 1.0, s0: float = 1.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Construct temperature, gain, leak-rate, or hard top-k candidate banks."""
    Wref = temperature_matrix(base, reference_tau, s0=s0)
    if path == "temperature":
        values = np.exp(np.linspace(np.log(tau_min), np.log(tau_max), K))
        bank = np.stack([temperature_matrix(base, v, s0=s0) for v in values])
        leaks = np.ones(K)
    elif path == "gain":
        values = np.linspace(gain_min, gain_max, K)
        bank = np.stack([float(g) * Wref for g in values])
        leaks = np.ones(K)
    elif path == "leak":
        values = np.linspace(leak_min, leak_max, K)
        bank = np.repeat(Wref[None, :, :], K, axis=0)
        leaks = values.astype(float)
    elif path == "sparsity":
        values = np.rint(np.linspace(1, N - 1, K)).astype(int)
        order = np.argsort(base["scores"], axis=1)[:, ::-1]
        rows = np.arange(N)[:, None]
        matrices = []
        for kval in values:
            mask = np.zeros((N, N))
            mask[rows, order[:, :int(kval)]] = 1.0
            np.fill_diagonal(mask, 0.0)
            matrices.append(rms_normalize_bulk(base["signs"] * mask, s0=s0))
        bank = np.stack(matrices)
        leaks = np.ones(K)
    else:
        raise ValueError(path)
    return np.asarray(values), bank, np.asarray(leaks, dtype=float)


def rollout_bank(W_bank: np.ndarray, Win: np.ndarray, U: np.ndarray,
                 leaks: Optional[np.ndarray] = None) -> np.ndarray:
    """Roll out all candidate reservoirs in parallel from the zero state."""
    U = np.asarray(U, dtype=float)
    if U.ndim == 1:
        U = U[:, None]
    K, N, _ = W_bank.shape
    states = np.zeros((K, N))
    history = np.zeros((K, len(U), N))
    if leaks is None:
        leaks = np.ones(K)
    leaks = np.asarray(leaks, dtype=float).reshape(K, 1)
    for t, u in enumerate(U):
        recurrent = np.einsum("kij,kj->ki", W_bank, states, optimize=True)
        drive = Win @ u
        proposal = np.tanh(recurrent + drive[None, :])
        states = (1.0 - leaks) * states + leaks * proposal
        history[:, t, :] = states
    return history


def train_readout_bank(X_bank: np.ndarray, y: np.ndarray, ridge: float) -> np.ndarray:
    """Fit one ridge readout per reservoir candidate."""
    target = np.asarray(y, dtype=float).reshape(-1, 1)
    outputs = []
    for X in X_bank:
        Xb = add_bias(X)
        lhs = Xb.T @ Xb + float(ridge) * np.eye(Xb.shape[1])
        outputs.append(np.linalg.solve(lhs, Xb.T @ target))
    return np.stack(outputs)


def predict_readout_bank(X_bank: np.ndarray, Wout_bank: np.ndarray) -> np.ndarray:
    return np.stack([(add_bias(X) @ Wout).reshape(-1) for X, Wout in zip(X_bank, Wout_bank)])


def spectral_radius(W: np.ndarray) -> float:
    return float(np.max(np.abs(np.linalg.eigvals(W))))


def structural_metrics(W: np.ndarray) -> Dict[str, float]:
    """Entropy-based effective support and scale diagnostics for one recurrent matrix."""
    absolute = np.abs(W)
    p = absolute / (absolute.sum(axis=1, keepdims=True) + 1e-12)
    H = -np.sum(p * np.log(p + 1e-12), axis=1)
    support = np.exp(H)
    return {
        "effective_support_mean": float(support.mean()),
        "effective_support_fraction": float(support.mean() / W.shape[0]),
        "row_entropy_mean": float(H.mean()),
        "rms_weight": float(np.sqrt(np.mean(W ** 2))),
        "spectral_radius": spectral_radius(W),
    }


def near_optimal_mask(scores: Sequence[float], abs_tol: float = 0.005,
                      rel_tol: float = 0.10) -> np.ndarray:
    scores = np.asarray(scores, dtype=float)
    span = float(scores.max() - scores.min())
    tol = max(float(abs_tol), float(rel_tol) * max(span, 0.0))
    return scores >= float(scores.max()) - tol


def component_containing(mask: Sequence[bool], idx: int) -> np.ndarray:
    """Connected True component containing idx on a one-dimensional grid."""
    mask = np.asarray(mask, dtype=bool)
    out = np.zeros_like(mask)
    lo = hi = int(idx)
    while lo > 0 and mask[lo - 1]:
        lo -= 1
    while hi + 1 < len(mask) and mask[hi + 1]:
        hi += 1
    out[lo:hi + 1] = True
    return out


def calibrate_safe_region(validation_scores: Sequence[float], abs_tol: float = 0.005,
                          rel_tol: float = 0.10) -> Dict[str, object]:
    validation_scores = np.asarray(validation_scores, dtype=float)
    default_idx = int(np.argmax(validation_scores))
    safe_mask = component_containing(near_optimal_mask(validation_scores, abs_tol, rel_tol), default_idx)
    safe_idxs = np.where(safe_mask)[0]
    return {"default_idx": default_idx, "safe_idxs": safe_idxs,
            "safe_low_idx": int(safe_idxs[0]), "safe_high_idx": int(safe_idxs[-1]),
            "safe_width": int(len(safe_idxs))}


def all_contiguous_intervals(K: int, width: int) -> List[np.ndarray]:
    width = max(1, min(int(width), int(K)))
    return [np.arange(lo, lo + width) for lo in range(K - width + 1)]


def matched_interval_stats(test_scores: Sequence[float], default_idx: int,
                           width: int, abs_tol: float = 0.005,
                           rel_tol: float = 0.10) -> Dict[str, float]:
    test_scores = np.asarray(test_scores, dtype=float)
    near = near_optimal_mask(test_scores, abs_tol, rel_tol)
    oracle_idx = int(np.argmax(test_scores))
    default_score = float(test_scores[default_idx])
    intervals = all_contiguous_intervals(len(test_scores), width)
    return {
        "matched_near_rate": float(np.mean([np.any(near[ii]) for ii in intervals])),
        "matched_oracle_rate": float(np.mean([oracle_idx in ii for ii in intervals])),
        "matched_best_gain": float(np.mean([test_scores[ii].max() - default_score for ii in intervals])),
    }


def evaluate_case(task: str, trial: int, path: str, seed: int,
                  N: int = 60, K: int = 13, lengths=(1200, 500, 500),
                  washout: int = 100, input_scale: float = 0.8,
                  ridge: float = 1e-5, abs_tol: float = 0.005,
                  rel_tol: float = 0.10, return_predictions: bool = False) -> Dict[str, object]:
    """Train/calibrate/evaluate one task-trial-path case."""
    U_train, y_train, U_val, y_val, U_test, y_test = make_split(task, trial, seed, lengths, washout)
    base = make_base_substrate(N, U_train.shape[1], task, trial, seed, input_scale)
    values, W_bank, leaks = make_path_bank(path, base, N=N, K=K)
    X_train = rollout_bank(W_bank, base["Win"], U_train, leaks)
    Wout = train_readout_bank(X_train, y_train, ridge)
    pred_val = predict_readout_bank(rollout_bank(W_bank, base["Win"], U_val, leaks), Wout)
    pred_test = predict_readout_bank(rollout_bank(W_bank, base["Win"], U_test, leaks), Wout)
    val_nrmse = np.asarray([nrmse(y_val, p) for p in pred_val])
    test_nrmse = np.asarray([nrmse(y_test, p) for p in pred_test])
    val_scores, test_scores = -val_nrmse, -test_nrmse
    cal = calibrate_safe_region(val_scores, abs_tol, rel_tol)
    safe_idxs, default_idx = cal["safe_idxs"], int(cal["default_idx"])
    oracle_idx = int(np.argmax(test_scores))
    near = near_optimal_mask(test_scores, abs_tol, rel_tol)
    matched = matched_interval_stats(test_scores, default_idx, len(safe_idxs), abs_tol, rel_tol)
    structural = pd.DataFrame([structural_metrics(W) for W in W_bank])
    row = {
        "task": task, "trial": int(trial), "path": path,
        "default_idx": default_idx, "safe_low_idx": int(safe_idxs[0]),
        "safe_high_idx": int(safe_idxs[-1]), "safe_width": int(len(safe_idxs)),
        "safe_width_fraction": float(len(safe_idxs) / K),
        "near_contained": int(np.any(near[safe_idxs])),
        "exact_contained": int(oracle_idx in safe_idxs),
        "matched_near_rate": matched["matched_near_rate"],
        "matched_oracle_rate": matched["matched_oracle_rate"],
        "safe_gain": float(test_scores[safe_idxs].max() - test_scores[default_idx]),
        "full_gain": float(test_scores[oracle_idx] - test_scores[default_idx]),
        "matched_best_gain": matched["matched_best_gain"],
        "safe_minus_matched_gain": float(test_scores[safe_idxs].max() - test_scores[default_idx] - matched["matched_best_gain"]),
        "default_test_nrmse": float(test_nrmse[default_idx]),
        "safe_best_test_nrmse": float(test_nrmse[safe_idxs].min()),
        "full_best_test_nrmse": float(test_nrmse.min()),
        "support_range": float(structural.effective_support_mean.max() - structural.effective_support_mean.min()),
        "spectral_radius_range": float(structural.spectral_radius.max() - structural.spectral_radius.min()),
    }
    if return_predictions:
        row.update({"candidate_values": values, "pred_test": pred_test, "y_test": y_test,
                    "safe_idxs": safe_idxs, "test_scores": test_scores,
                    "train_target_scale": float(np.std(y_train) + 1e-12)})
    return row


def run_panel(tasks: Sequence[str], trials: int, paths: Sequence[str], seed: int,
              **kwargs) -> pd.DataFrame:
    """Run a Cartesian task × trial × path panel."""
    rows = []
    for task in tasks:
        for trial in range(int(trials)):
            for path in paths:
                rows.append(evaluate_case(task, trial, path, seed, **kwargs))
    return pd.DataFrame(rows)


def window_rows(case: Dict[str, object], window_size: int = 50,
                stride: int = 25) -> pd.DataFrame:
    """Compute label-free prediction-variation indicators and labelled opportunity per window."""
    pred = np.asarray(case["pred_test"])
    y = np.asarray(case["y_test"])
    safe_idxs = np.asarray(case["safe_idxs"], dtype=int)
    default_idx = int(case["default_idx"])
    scale = float(case["train_target_scale"])
    values = np.asarray(case["candidate_values"], dtype=float)
    rows = []
    if len(y) <= window_size:
        starts = [0]
    else:
        starts = range(0, len(y) - window_size + 1, stride)
    for wid, lo in enumerate(starts):
        hi = min(lo + window_size, len(y))
        pw, yw = pred[:, lo:hi], y[lo:hi]
        utilities = -np.sqrt(np.mean((pw - yw[None, :]) ** 2, axis=1)) / (scale + 1e-12)
        gain = float(utilities[safe_idxs].max() - utilities[default_idx])
        if len(safe_idxs) >= 2:
            safe_pred = pw[safe_idxs]
            dispersion = float(np.mean(np.std(safe_pred, axis=0)) / scale)
            anchor = float(np.sqrt(np.mean((pw[safe_idxs[0]] - pw[safe_idxs[-1]]) ** 2)) / scale)
            terms = []
            z = np.log(np.asarray(values, dtype=float)) if np.all(values > 0) else np.arange(len(values), dtype=float)
            for left, right in zip(safe_idxs[:-1], safe_idxs[1:]):
                denom = max(abs(z[right] - z[left]), 1e-12)
                terms.append(float(np.sqrt(np.mean((pw[right] - pw[left]) ** 2)) / scale / denom))
            local = float(np.mean(terms))
        else:
            dispersion = anchor = local = np.nan
        rows.append({"window_id": wid, "safe_gain": gain, "safe_dispersion": dispersion,
                     "anchor_spread": anchor, "local_sensitivity": local,
                     "positive_safe_gain": int(gain > 1e-12)})
    return pd.DataFrame(rows)


def evaluate_arrays(U_train: np.ndarray, y_train: np.ndarray,
                    U_val: np.ndarray, y_val: np.ndarray,
                    U_test: np.ndarray, y_test: np.ndarray,
                    case_name: str, trial: int, path: str, seed: int,
                    N: int, K: int, ridge: float, input_scale: float = 0.8,
                    abs_tol: float = 0.005, rel_tol: float = 0.10,
                    return_predictions: bool = False) -> Dict[str, object]:
    """Evaluate a path on preconstructed train/validation/test arrays."""
    U_train = np.asarray(U_train, float); U_val = np.asarray(U_val, float); U_test = np.asarray(U_test, float)
    y_train = np.asarray(y_train, float); y_val = np.asarray(y_val, float); y_test = np.asarray(y_test, float)
    base = make_base_substrate(N, U_train.shape[1], case_name, trial, seed, input_scale)
    values, W_bank, leaks = make_path_bank(path, base, N=N, K=K)
    X_train = rollout_bank(W_bank, base["Win"], U_train, leaks)
    Wout = train_readout_bank(X_train, y_train, ridge)
    pred_val = predict_readout_bank(rollout_bank(W_bank, base["Win"], U_val, leaks), Wout)
    pred_test = predict_readout_bank(rollout_bank(W_bank, base["Win"], U_test, leaks), Wout)
    val_nrmse = np.asarray([nrmse(y_val, p) for p in pred_val])
    test_nrmse = np.asarray([nrmse(y_test, p) for p in pred_test])
    val_scores, test_scores = -val_nrmse, -test_nrmse
    cal = calibrate_safe_region(val_scores, abs_tol, rel_tol)
    safe_idxs, default_idx = cal["safe_idxs"], int(cal["default_idx"])
    oracle_idx = int(np.argmax(test_scores))
    near = near_optimal_mask(test_scores, abs_tol, rel_tol)
    matched = matched_interval_stats(test_scores, default_idx, len(safe_idxs), abs_tol, rel_tol)
    structural = pd.DataFrame([structural_metrics(W) for W in W_bank])
    row: Dict[str, object] = {
        "task": case_name, "trial": int(trial), "path": path,
        "default_idx": default_idx, "safe_low_idx": int(safe_idxs[0]),
        "safe_high_idx": int(safe_idxs[-1]), "safe_width": int(len(safe_idxs)),
        "safe_width_fraction": float(len(safe_idxs) / K),
        "near_contained": int(np.any(near[safe_idxs])), "exact_contained": int(oracle_idx in safe_idxs),
        "matched_near_rate": matched["matched_near_rate"], "matched_oracle_rate": matched["matched_oracle_rate"],
        "safe_gain": float(test_scores[safe_idxs].max() - test_scores[default_idx]),
        "full_gain": float(test_scores[oracle_idx] - test_scores[default_idx]),
        "matched_best_gain": matched["matched_best_gain"],
        "safe_minus_matched_gain": float(test_scores[safe_idxs].max() - test_scores[default_idx] - matched["matched_best_gain"]),
        "default_test_nrmse": float(test_nrmse[default_idx]), "safe_best_test_nrmse": float(test_nrmse[safe_idxs].min()),
        "full_best_test_nrmse": float(test_nrmse.min()),
        "support_range": float(structural.effective_support_mean.max() - structural.effective_support_mean.min()),
        "spectral_radius_range": float(structural.spectral_radius.max() - structural.spectral_radius.min()),
    }
    if return_predictions:
        row.update({"candidate_values": values, "pred_test": pred_test, "y_test": y_test,
                    "safe_idxs": safe_idxs, "test_scores": test_scores,
                    "train_target_scale": float(np.std(y_train) + 1e-12)})
    return row
