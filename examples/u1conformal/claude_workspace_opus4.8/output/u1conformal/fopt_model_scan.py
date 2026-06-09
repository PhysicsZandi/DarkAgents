"""
Coarse-to-fine scan over the independent (v, g_D) plane for u1conformal,
targeting the nanohertz PTA band.

Independent axes (match parameter_basis.independent):
  - v   [GeV]
  - g_D [dimensionless]

Strategy:
  1. Coarse grid anchored on librarian benchmark hints
     (g_D ~ [0.55, 0.9], v ~ 100-700 MeV), extended.
  2. Refine around viable points whose f_peak_est falls in the PTA band.
Each backend call is wrapped in per-point error handling and a timeout.

Outputs:
  - output/u1conformal/fopt_benchmarks.csv
  - output/u1conformal/fopt_results.json
"""

import os
import sys
import json
import csv
import signal
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fopt_model import (  # noqa: E402
    evaluate_point,
    PTA_FMIN,
    PTA_FMAX,
)

OUTDIR = os.path.dirname(os.path.abspath(__file__))
PER_POINT_TIMEOUT_S = 60


class _Timeout(Exception):
    pass


def _handler(signum, frame):
    raise _Timeout()


def safe_evaluate(v, g_D):
    """Evaluate with a per-point timeout."""
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(PER_POINT_TIMEOUT_S)
    try:
        res = evaluate_point(v, g_D)
    except _Timeout:
        res = {
            "v": float(v), "g_D": float(g_D),
            "lambda_Phi": np.nan, "beta_lambda": np.nan,
            "m_Aprime_GeV": np.nan, "m_rho_GeV": np.nan,
            "Tn": np.nan, "Tp": np.nan, "Treh": np.nan,
            "alpha": np.nan, "beta_H": np.nan,
            "eternal_inflation": None, "f_peak_est": np.nan,
            "status": "numerical_failure", "failure_reason": "timeout",
        }
    except Exception as e:
        res = {
            "v": float(v), "g_D": float(g_D),
            "lambda_Phi": np.nan, "beta_lambda": np.nan,
            "m_Aprime_GeV": np.nan, "m_rho_GeV": np.nan,
            "Tn": np.nan, "Tp": np.nan, "Treh": np.nan,
            "alpha": np.nan, "beta_H": np.nan,
            "eternal_inflation": None, "f_peak_est": np.nan,
            "status": "numerical_failure",
            "failure_reason": f"scan_exception: {type(e).__name__}: {e}",
        }
    finally:
        signal.alarm(0)
    return res


def in_pta_band(f):
    return np.isfinite(f) and (PTA_FMIN <= f <= PTA_FMAX)


def run_grid(v_vals, g_vals, results, seen):
    for g_D in g_vals:
        for v in v_vals:
            key = (round(float(v), 9), round(float(g_D), 6))
            if key in seen:
                continue
            seen.add(key)
            res = safe_evaluate(v, g_D)
            results.append(res)
            tag = res["status"]
            if tag == "viable":
                tag += f" f_peak={res['f_peak_est']:.2e}"
            print(f"v={v*1e3:7.2f} MeV  g_D={g_D:5.3f}  -> {tag}")
    return results


def main():
    results = []
    seen = set()

    # ---- Stage 1: coarse grid anchored on librarian hints (extended) ----
    print("=== Stage 1: coarse grid ===")
    v_coarse = np.array([0.05, 0.1, 0.173, 0.3, 0.5, 0.692, 1.0])  # GeV
    g_coarse = np.array([0.50, 0.55, 0.59, 0.65, 0.70, 0.80, 0.90])
    run_grid(v_coarse, g_coarse, results, seen)

    # ---- Stage 2: extend toward lower scales to map the PTA window ----
    # f_peak scales ~ Treh ~ v, so lower v lowers f_peak into the band.
    print("=== Stage 2: extend lower scales (log v) ===")
    v_low = np.geomspace(0.005, 0.1, 8)  # GeV: 5 MeV .. 100 MeV
    g_low = np.array([0.55, 0.59, 0.65, 0.70, 0.80])
    run_grid(v_low, g_low, results, seen)

    # ---- Stage 3: extend higher scales to find upper boundary ----
    print("=== Stage 3: extend higher scales (log v) ===")
    v_high = np.geomspace(1.0, 10.0, 6)  # GeV
    g_high = np.array([0.55, 0.59, 0.65, 0.70, 0.80])
    run_grid(v_high, g_high, results, seen)

    # ---- Stage 4: refine around viable PTA-band points ----
    print("=== Stage 4: refine around PTA-band viable points ===")
    band_pts = [r for r in results
                if r["status"] == "viable" and in_pta_band(r["f_peak_est"])]
    if band_pts:
        v_band = sorted(set(r["v"] for r in band_pts))
        g_band = sorted(set(r["g_D"] for r in band_pts))
        vlo, vhi = min(v_band), max(v_band)
        glo, ghi = min(g_band), max(g_band)
        v_ref = np.geomspace(max(vlo * 0.5, 1e-3), vhi * 2.0, 8)
        g_ref = np.linspace(max(glo - 0.05, 0.45),
                            min(ghi + 0.05, 1.0), 6)
        run_grid(v_ref, g_ref, results, seen)
    else:
        print("No PTA-band viable points found in stages 1-3.")

    # ---- Write CSV ----
    fieldnames = [
        "v", "g_D", "lambda_Phi", "beta_lambda", "m_Aprime_GeV", "m_rho_GeV",
        "Tn", "Tp", "Treh", "alpha", "beta_H", "eternal_inflation",
        "f_peak_est", "status", "failure_reason",
    ]
    csv_path = os.path.join(OUTDIR, "fopt_benchmarks.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in results:
            row = {k: r.get(k, "") for k in fieldnames}
            w.writerow(row)

    # ---- Summaries ----
    viable = [r for r in results if r["status"] == "viable"]
    viable_band = [r for r in viable if in_pta_band(r["f_peak_est"])]

    def score(r):
        # prefer center of PTA band (log) and lower beta/H (stronger signal)
        f = r["f_peak_est"]
        center = np.sqrt(PTA_FMIN * PTA_FMAX)
        return abs(np.log10(f) - np.log10(center))

    best = sorted(viable_band, key=score)[:5] if viable_band else \
        sorted(viable, key=lambda r: abs(np.log10(r["f_peak_est"])
               - np.log10(np.sqrt(PTA_FMIN * PTA_FMAX)))
               if np.isfinite(r["f_peak_est"]) else 1e9)[:5]

    summary = {
        "total_points": len(results),
        "viable_points": len(viable),
        "viable_in_pta_band": len(viable_band),
        "failed_points": len([r for r in results
                              if r["status"] in ("numerical_failure",
                                                 "physical_failure")]),
        "excluded_points": len([r for r in results
                                if r["status"] == "not_fopt"]),
    }

    out = {
        "summary": summary,
        "pta_band_hz": [PTA_FMIN, PTA_FMAX],
        "all_points": results,
        "best_points": best,
    }
    json_path = os.path.join(OUTDIR, "fopt_results.json")
    with open(json_path, "w") as f:
        json.dump(out, f, indent=2, default=lambda o: None
                  if o is None else (float(o) if isinstance(o, np.floating)
                                     else o))

    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"\nViable points in PTA band: {len(viable_band)}")
    for r in best:
        print(f"  v={r['v']*1e3:.2f} MeV g_D={r['g_D']:.3f} "
              f"alpha={r['alpha']:.3g} beta_H={r['beta_H']:.3g} "
              f"Treh={r['Treh']*1e3:.3g} MeV f_peak={r['f_peak_est']:.3g} Hz")
    print(f"\nCSV : {csv_path}")
    print(f"JSON: {json_path}")
    return out


if __name__ == "__main__":
    main()
