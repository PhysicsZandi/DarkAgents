"""
Benchmark scan over independent model parameters (v, g_D) for u1conformal.

For each (v, g_D):
  - compute the FOPT (actual backend, no cache/interpolation),
  - compute h^2 Omega_GW(f) with the dbf template at the violin-bin frequencies,
  - score against backend/pta_violin_windows.csv (count bins inside the band).

Writes output/u1conformal/pta_benchmark_scan.csv.
"""

import os
import sys
import csv
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, _HERE)

from pta_spectrum import spectrum_from_params, TEMPLATE  # noqa: E402

VIOLIN_CSV = os.path.join(_ROOT, "backend", "pta_violin_windows.csv")
OUT_CSV = os.path.join(_HERE, "pta_benchmark_scan.csv")


def load_violin_bins():
    bins = []
    with open(VIOLIN_CSV) as fh:
        rd = csv.DictReader(fh)
        for row in rd:
            if not row["bin_i"]:
                continue
            bins.append({
                "bin_i": int(row["bin_i"]),
                "log10_f": float(row["log10_f_Hz"]),
                "ymin": float(row["ymin_log10_h2OmegaGW"]),
                "ymax": float(row["ymax_log10_h2OmegaGW"]),
            })
    return bins


def score_point(v, g_D, bins):
    f = np.array([10**b["log10_f"] for b in bins])
    h2, res = spectrum_from_params(f, v, g_D, template=TEMPLATE)
    if res["status"] != "viable":
        return None
    log_h2 = np.where(h2 > 0, np.log10(np.where(h2 > 0, h2, 1e-300)), -np.inf)
    inside = 0
    for i, b in enumerate(bins):
        if b["ymin"] <= log_h2[i] <= b["ymax"]:
            inside += 1
    return {
        "v": v, "g_D": g_D,
        "alpha": res["alpha"], "beta_H": res["beta_H"], "Treh": res["Treh"],
        "f_peak_est": res["f_peak_est"],
        "inside_bins": inside, "total_bins": len(bins),
        "log_h2_at_bins": log_h2,
    }


def run_grid(v_vals, g_vals, bins, label=""):
    rows = []
    for g_D in g_vals:
        for v in v_vals:
            r = score_point(float(v), float(g_D), bins)
            if r is None:
                continue
            r["grid"] = label
            rows.append(r)
    return rows


def main():
    bins = load_violin_bins()
    f_bins = [10**b["log10_f"] for b in bins]

    all_rows = []

    # Coarse grid: wide. v log-spaced over MeV-GeV (>= 2 orders both ways around
    # the FOPT f_peak_est scale ~ MeV-vev), g_D linear (small range, perturbative).
    v_coarse = np.logspace(np.log10(0.001), np.log10(50.0), 30)  # 1 MeV - 50 GeV
    g_coarse = np.linspace(0.48, 0.90, 22)
    all_rows += run_grid(v_coarse, g_coarse, bins, "coarse")

    # Fine grid around the best-scoring region (low g_D), kept wide enough to
    # show the gradient of the score across the viable window.
    v_fine = np.logspace(np.log10(0.05), np.log10(20.0), 32)
    g_fine = np.linspace(0.48, 0.70, 23)
    all_rows += run_grid(v_fine, g_fine, bins, "fine")

    # Write CSV
    header = ["grid", "v", "g_D", "alpha", "beta_H", "Treh", "f_peak_est",
              "inside_bins", "total_bins"]
    header += [f"log10_h2_bin{b['bin_i']}" for b in bins]
    header += [f"f_bin{b['bin_i']}_Hz" for b in bins]

    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in sorted(all_rows, key=lambda x: (-x["inside_bins"], x["v"])):
            row = [r["grid"], r["v"], r["g_D"], r["alpha"], r["beta_H"],
                   r["Treh"], r["f_peak_est"], r["inside_bins"], r["total_bins"]]
            row += [f"{x:.6g}" for x in r["log_h2_at_bins"]]
            row += [f"{x:.6g}" for x in f_bins]
            w.writerow(row)

    # Report
    best = [r for r in all_rows if r["inside_bins"] == len(bins)]
    print(f"Total scored points: {len(all_rows)}")
    print(f"Points with {len(bins)}/{len(bins)} in-violin bins: {len(best)}")
    top = sorted(all_rows, key=lambda x: -x["inside_bins"])[:15]
    for r in top:
        print(f"  v={r['v']:.4g} GeV g_D={r['g_D']:.3f} "
              f"alpha={r['alpha']:.2e} beta_H={r['beta_H']:.1f} "
              f"score={r['inside_bins']}/{r['total_bins']}")
    if best:
        vs = [r["v"] for r in best]
        gs = [r["g_D"] for r in best]
        print(f"14/14 window: v in [{min(vs):.4g},{max(vs):.4g}] GeV, "
              f"g_D in [{min(gs):.3f},{max(gs):.3f}]")


if __name__ == "__main__":
    main()
