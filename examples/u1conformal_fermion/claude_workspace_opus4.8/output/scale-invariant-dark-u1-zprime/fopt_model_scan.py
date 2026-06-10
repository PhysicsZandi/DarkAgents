"""Bounded coarse-to-fine scan over the INDEPENDENT parameters (g_D, y, w)
of the scale-invariant dark U(1)_D model.

Writes:
    fopt_benchmarks.csv   (every evaluated point, with status)
    fopt_results.json     (structured per-point + best-point results)

Independent scan axes (must match parameter_basis.independent):
    g_D in [0.1, 1.5]  (linear; small range)
    y   in [0.0, 1.0]  (linear; small range, hard cut y^4 < 1.5 g_D^4)
    w   in [0.05, 10.0] GeV (logarithmic; spans ~2.3 decades)

Anchor: literature Point A (g_D=0.877, y=0.363, w=92.9 MeV) and Costa BPs.
PTA band f_peak ~ 1e-9 .. 1e-7 Hz.
"""

import csv
import json
import signal
from pathlib import Path
import numpy as np

import fopt_model as fm

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "fopt_benchmarks.csv"
JSON_PATH = HERE / "fopt_results.json"

PER_POINT_TIMEOUT_S = 30


class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout()


def eval_with_timeout(g_D, y, w):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(PER_POINT_TIMEOUT_S)
    try:
        return fm.evaluate_point(g_D, y, w)
    except _Timeout:
        return {"g_D": g_D, "y": y, "w": w,
                "beta_lambda": fm.beta_lambda(g_D, y),
                "m_Zp": g_D * w, "m_chi": y * w / np.sqrt(2),
                "m_scalon": np.nan,
                "Tn": np.nan, "Tp": np.nan, "Treh": np.nan,
                "alpha": np.nan, "beta_H": np.nan,
                "eternal_inflation": None, "f_peak_est": np.nan,
                "status": "numerical_failure",
                "failure_reason": "per-point timeout"}
    finally:
        signal.alarm(0)


CSV_FIELDS = ["g_D", "y", "w", "beta_lambda", "m_Zp", "m_chi", "m_scalon",
              "Tn", "Tp", "Treh", "alpha", "beta_H", "eternal_inflation",
              "f_peak_est", "status", "failure_reason"]


def run_grid(g_vals, y_vals, w_vals, results, seen):
    for g_D in g_vals:
        for y in y_vals:
            # skip points violating the hard cut up front
            if y**4 >= 1.5 * g_D**4:
                continue
            for w in w_vals:
                key = (round(g_D, 6), round(y, 6), round(w, 8))
                if key in seen:
                    continue
                seen.add(key)
                r = eval_with_timeout(g_D, y, w)
                results.append(r)


def main():
    results = []
    seen = set()

    # --- coarse broad grid over all three independent directions ---
    g_coarse = np.linspace(0.3, 1.5, 7)          # 0.3..1.5
    y_coarse = np.linspace(0.0, 0.8, 5)          # 0..0.8
    w_coarse = np.geomspace(0.05, 10.0, 7)       # 0.05..10 GeV (log)
    run_grid(g_coarse, y_coarse, w_coarse, results, seen)

    # --- include literature anchors explicitly ---
    anchors = [
        (0.877, 0.363, 92.9e-3),   # Point A
        (0.790, 0.401, 343.0e-3),  # Point B
        (0.75, 0.0, 0.5),          # Costa BP1 (small y limit)
        (0.75, 0.0, 1.0),          # Costa BP2
        (0.75, 0.0, 10.0),         # Costa BP3
        (0.86, 0.0, 1.0),          # Costa BP4-ish
        (0.59, 0.0, 0.1073/0.59),  # Goncalves (w from m_Zp/g_D ~ 0.182 GeV)
    ]
    for g_D, y, w in anchors:
        key = (round(g_D, 6), round(y, 6), round(w, 8))
        if key not in seen:
            seen.add(key)
            results.append(eval_with_timeout(g_D, y, w))

    # --- fine refinement around viable / near-viable region ---
    # locate viable points to center refinement
    viable = [r for r in results if r["status"] == "viable"]
    if viable:
        gs = sorted(set(round(r["g_D"], 3) for r in viable))
        ws = sorted(set(r["w"] for r in viable))
        g_lo, g_hi = max(0.3, min(gs) - 0.2), min(1.5, max(gs) + 0.2)
        w_lo, w_hi = max(0.05, min(ws) / 3), min(10.0, max(ws) * 3)
        g_fine = np.linspace(g_lo, g_hi, 6)
        y_fine = np.linspace(0.0, 0.7, 4)
        w_fine = np.geomspace(w_lo, w_hi, 8)
        run_grid(g_fine, y_fine, w_fine, results, seen)

    # write CSV
    with open(CSV_PATH, "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        wtr.writeheader()
        for r in results:
            wtr.writerow({k: r.get(k) for k in CSV_FIELDS})

    viable = [r for r in results if r["status"] == "viable"]
    in_band = [r for r in viable
               if np.isfinite(r["f_peak_est"])
               and fm.PTA_BAND[0] <= r["f_peak_est"] <= fm.PTA_BAND[1]]

    # rank best points: prefer in-band, then strongest alpha
    def score(r):
        in_b = (fm.PTA_BAND[0] <= r["f_peak_est"] <= fm.PTA_BAND[1])
        return (in_b, r["alpha"])
    best = sorted(viable, key=score, reverse=True)[:8]

    summary = {
        "total_points": len(results),
        "viable_points": len(viable),
        "in_pta_band": len(in_band),
        "failed_points": sum(r["status"] in ("numerical_failure",
                             "physical_failure") for r in results),
        "not_fopt": sum(r["status"] == "not_fopt" for r in results),
    }

    out = {
        "summary": summary,
        "pta_band_Hz": list(fm.PTA_BAND),
        "all_points": results,
        "viable_points": viable,
        "best_points": best,
    }
    with open(JSON_PATH, "w") as f:
        json.dump(out, f, indent=2, default=lambda o: None if o is None else float(o)
                  if isinstance(o, (np.floating,)) else o)

    print(json.dumps(summary, indent=2))
    print("\nBest points:")
    for r in best:
        print(f"  g_D={r['g_D']:.3f} y={r['y']:.3f} w={r['w']:.4g} GeV | "
              f"Tp={r['Tp']:.3g} Treh={r['Treh']:.3g} alpha={r['alpha']:.3g} "
              f"beta_H={r['beta_H']:.3g} f_peak={r['f_peak_est']:.3g} Hz")
    return out


if __name__ == "__main__":
    main()
