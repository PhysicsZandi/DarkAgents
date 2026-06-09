"""Bounded coarse-to-fine scan over the independent parameters (g, chi0)
for the su2cw-dark conformal SU(2)_D FOPT model.

Independent axes:
    g    in [0.3, 1.5]  (perturbative, linear steps; small range)
    chi0 in GeV         (log steps; spans many orders of magnitude)

We anchor on arXiv:2109.11558 (g_D=1.37, chi0 ~ 1-12 MeV) and steer toward the
PTA band f_peak ~ 1e-9 - 1e-7 Hz. Each backend evaluation is wrapped with a
per-point timeout and error handling; failures are recorded, not discarded.
"""

import csv
import json
import multiprocessing as mp
from pathlib import Path

import numpy as np

from fopt_model import compute_point, PTA_F_LOW, PTA_F_HIGH

OUTDIR = Path(__file__).resolve().parent
CSV_PATH = OUTDIR / "fopt_benchmarks.csv"
JSON_PATH = OUTDIR / "fopt_results.json"

PER_POINT_TIMEOUT = 60  # seconds

CSV_FIELDS = [
    "g", "chi0", "beta_lambda", "m_chi",
    "Tn", "Tp", "Treh", "alpha", "beta_H", "gstar_eff",
    "eternal_inflation", "f_peak_est", "status", "failure_reason",
]


def _worker(g, chi0, q):
    try:
        q.put(compute_point(g, chi0))
    except Exception as e:  # pragma: no cover
        q.put({"g": g, "chi0": chi0, "status": "numerical_failure",
               "failure_reason": f"worker exception: {e}"})


def compute_point_timed(g, chi0):
    q = mp.Queue()
    p = mp.Process(target=_worker, args=(g, chi0, q))
    p.start()
    p.join(PER_POINT_TIMEOUT)
    if p.is_alive():
        p.terminate()
        p.join()
        return {"g": g, "chi0": chi0, "beta_lambda": np.nan, "m_chi": np.nan,
                "Tn": np.nan, "Tp": np.nan, "Treh": np.nan, "alpha": np.nan,
                "beta_H": np.nan, "gstar_eff": np.nan, "eternal_inflation": None,
                "f_peak_est": np.nan, "status": "numerical_failure",
                "failure_reason": "per-point timeout"}
    try:
        return q.get_nowait()
    except Exception:
        return {"g": g, "chi0": chi0, "beta_lambda": np.nan, "m_chi": np.nan,
                "Tn": np.nan, "Tp": np.nan, "Treh": np.nan, "alpha": np.nan,
                "beta_H": np.nan, "gstar_eff": np.nan, "eternal_inflation": None,
                "f_peak_est": np.nan, "status": "numerical_failure",
                "failure_reason": "no result from worker"}


def build_grid(g_vals, chi0_vals):
    pts = []
    for g in g_vals:
        for chi0 in chi0_vals:
            # physical guards before calling backend
            if not (0.3 <= g <= 1.5):
                continue
            if chi0 <= 0:
                continue
            pts.append((float(g), float(chi0)))
    return pts


def run_scan():
    results = []
    seen = set()

    def add_stage(g_vals, chi0_vals, label):
        grid = build_grid(g_vals, chi0_vals)
        for (g, chi0) in grid:
            key = (round(g, 6), round(np.log10(chi0), 6))
            if key in seen:
                continue
            seen.add(key)
            r = compute_point_timed(g, chi0)
            results.append(r)
        print(f"[{label}] cumulative points: {len(results)}")

    # Stage 1: coarse broad grid.
    g_coarse = np.linspace(0.5, 1.5, 6)              # 0.5..1.5
    chi0_coarse = np.geomspace(1e-4, 1e1, 12)        # 0.1 MeV .. 10 GeV
    add_stage(g_coarse, chi0_coarse, "coarse")

    # Stage 2: refine around literature anchor (g~1.37, chi0~MeV) and any
    # viable region found so far.
    g_fine = np.linspace(1.1, 1.5, 9)
    chi0_fine = np.geomspace(1e-3, 1e-1, 12)         # 1 MeV .. 100 MeV
    add_stage(g_fine, chi0_fine, "fine")

    # Stage 3: map the PTA window boundaries in chi0 around viable region.
    g_band = np.linspace(0.8, 1.5, 8)
    chi0_band = np.geomspace(3e-4, 1.0, 16)
    add_stage(g_band, chi0_band, "band")

    return results


def summarize(results):
    statuses = {}
    for r in results:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    viable = [r for r in results if r["status"] == "viable"]
    in_band = [r for r in viable
               if np.isfinite(r["f_peak_est"])
               and PTA_F_LOW <= r["f_peak_est"] <= PTA_F_HIGH]
    return statuses, viable, in_band


def write_csv(results):
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in results:
            row = {k: r.get(k, "") for k in CSV_FIELDS}
            w.writerow(row)


def _clean(v):
    if isinstance(v, float) and not np.isfinite(v):
        return None
    return v


def write_json(results, viable, in_band):
    def pack(r):
        return {k: _clean(r.get(k)) for k in CSV_FIELDS}

    # rank best points: in-band viable by closeness to PTA band center
    center = np.sqrt(PTA_F_LOW * PTA_F_HIGH)
    ranked = sorted(
        in_band,
        key=lambda r: abs(np.log10(r["f_peak_est"]) - np.log10(center)),
    )
    payload = {
        "model": "su2cw-dark",
        "total_points": len(results),
        "viable_points": len(viable),
        "in_pta_band_points": len(in_band),
        "pta_band_hz": [PTA_F_LOW, PTA_F_HIGH],
        "all_points": [pack(r) for r in results],
        "viable": [pack(r) for r in viable],
        "in_band": [pack(r) for r in in_band],
        "best_points": [pack(r) for r in ranked[:5]],
    }
    with open(JSON_PATH, "w") as f:
        json.dump(payload, f, indent=2)


if __name__ == "__main__":
    results = run_scan()
    statuses, viable, in_band = summarize(results)
    write_csv(results)
    write_json(results, viable, in_band)

    print("\n=== SCAN SUMMARY ===")
    print("status counts:", statuses)
    print(f"viable: {len(viable)}   in PTA band: {len(in_band)}")
    if in_band:
        center = np.sqrt(PTA_F_LOW * PTA_F_HIGH)
        best = sorted(in_band,
                      key=lambda r: abs(np.log10(r["f_peak_est"]) - np.log10(center)))
        print("\nBest in-band points:")
        for r in best[:5]:
            print(f"  g={r['g']:.3f} chi0={r['chi0']:.4g} GeV | "
                  f"alpha={r['alpha']:.3g} beta_H={r['beta_H']:.4g} "
                  f"Tp={r['Tp']:.3g} Treh={r['Treh']:.3g} "
                  f"f_peak={r['f_peak_est']:.3g} Hz")
    print(f"\nCSV : {CSV_PATH}")
    print(f"JSON: {JSON_PATH}")
