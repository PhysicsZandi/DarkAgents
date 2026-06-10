"""PTA benchmark scan for scale-invariant dark U(1)_D (CW) model.

For each (g_D, y, w) point:
  1. compute FOPT parameters with the actual backend (fopt_model.evaluate_point),
  2. compute h^2 Omega_GW(f) at the 14 PTA violin-bin frequencies with the
     dbf template (pta_spectrum.omega_gw),
  3. score against backend/pta_violin_windows.csv: a bin is "in" if
     ymin <= log10(Omega) <= ymax at that bin frequency.

No caching / interpolation: every point calls the real model + spectrum.
"""

import sys
import itertools
import csv
from pathlib import Path
import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_ROOT / "backend"))

from fopt_model import evaluate_point  # noqa: E402
from pta_spectrum import omega_gw, TEMPLATE  # noqa: E402

VIOLIN_CSV = _ROOT / "backend" / "pta_violin_windows.csv"
OUT_CSV = _HERE / "pta_benchmark_scan.csv"


def load_windows():
    bins = []
    with open(VIOLIN_CSV) as fh:
        for row in csv.DictReader(fh):
            if not row.get("bin_i"):
                continue
            bins.append((
                int(row["bin_i"]),
                10 ** float(row["log10_f_Hz"]),
                float(row["ymin_log10_h2OmegaGW"]),
                float(row["ymax_log10_h2OmegaGW"]),
            ))
    bins.sort(key=lambda b: b[0])
    f = np.array([b[1] for b in bins])
    ymin = np.array([b[2] for b in bins])
    ymax = np.array([b[3] for b in bins])
    return f, ymin, ymax


def score_point(g_D, y, w, fbins, ymin, ymax):
    r = evaluate_point(g_D, y, w)
    if r["status"] != "viable":
        return r, None, 0
    om = omega_gw(fbins, r["Treh"], r["alpha"], r["beta_H"])
    with np.errstate(divide="ignore"):
        logom = np.log10(np.where(om > 0, om, 1e-300))
    inside = (logom >= ymin) & (logom <= ymax)
    return r, logom, int(np.sum(inside))


def run_grid(g_grid, y_grid, w_grid, fbins, ymin, ymax, rows, tag):
    best = []
    for g_D, y, w in itertools.product(g_grid, y_grid, w_grid):
        r, logom, sc = score_point(g_D, y, w, fbins, ymin, ymax)
        row = {"grid": tag, "g_D": g_D, "y": y, "w": w,
               "status": r["status"], "alpha": r.get("alpha"),
               "beta_H": r.get("beta_H"), "Treh": r.get("Treh"),
               "f_peak_est": r.get("f_peak_est"), "score": sc}
        if logom is not None:
            for i, lo in enumerate(logom, start=1):
                row[f"logOmega_bin{i}"] = lo
        rows.append(row)
        if sc > 0:
            best.append((sc, g_D, y, w))
    best.sort(reverse=True)
    return best


def main():
    fbins, ymin, ymax = load_windows()
    rows = []

    # --- coarse scan: wide, anchored on f_peak_est ~ nHz band ---
    # w scanned in log (spans orders of mag), couplings linear.
    g_coarse = np.round(np.linspace(0.15, 1.4, 8), 4)
    y_coarse = np.round(np.linspace(0.0, 0.9, 7), 4)
    w_coarse = np.round(np.geomspace(0.05, 10.0, 9), 6)
    print(f"[coarse] {len(g_coarse)*len(y_coarse)*len(w_coarse)} points, template={TEMPLATE}")
    best_c = run_grid(g_coarse, y_coarse, w_coarse, fbins, ymin, ymax, rows, "coarse")
    print("  coarse best:", best_c[:6])

    # --- refine around best coarse points ---
    if best_c:
        sc0, g0, y0, w0 = best_c[0]
        g_fine = np.round(np.linspace(max(0.1, g0 - 0.25), min(1.5, g0 + 0.25), 7), 4)
        y_fine = np.round(np.linspace(max(0.0, y0 - 0.25), min(1.0, y0 + 0.25), 7), 4)
        w_fine = np.round(np.geomspace(max(0.05, w0 / 4), min(10.0, w0 * 4), 9), 6)
        print(f"[fine] around (g={g0},y={y0},w={w0}); "
              f"{len(g_fine)*len(y_fine)*len(w_fine)} points")
        best_f = run_grid(g_fine, y_fine, w_fine, fbins, ymin, ymax, rows, "fine")
        print("  fine best:", best_f[:6])

    # write csv
    keys = ["grid", "g_D", "y", "w", "status", "alpha", "beta_H", "Treh",
            "f_peak_est", "score"] + [f"logOmega_bin{i}" for i in range(1, 15)]
    with open(OUT_CSV, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=keys)
        wtr.writeheader()
        for row in rows:
            wtr.writerow({k: row.get(k, "") for k in keys})

    allbest = sorted([(r["score"], r["g_D"], r["y"], r["w"])
                      for r in rows if r["score"] and r["score"] > 0], reverse=True)
    n14 = [b for b in allbest if b[0] == 14]
    print(f"\nTotal points: {len(rows)}")
    print(f"Points with 14/14 bins: {len(n14)}")
    print("Top 10:", allbest[:10])
    print(f"Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
