"""PTA benchmark scan for su2cw-dark.

Independent free model parameters: g (linear), chi0 [GeV] (logarithmic).
For each (g, chi0): compute FOPT (alpha, beta_H, Treh) with the actual backend,
then the dbf GW spectrum, and score against the PTA violin windows.
"""

import csv
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from fopt_model import compute_point  # noqa: E402
from pta_spectrum import h2OmegaGW, TEMPLATE  # noqa: E402

VIOLIN_CSV = _HERE.parents[1] / "backend" / "pta_violin_windows.csv"


def load_violin_bins():
    bins = []
    with open(VIOLIN_CSV) as fh:
        for row in csv.DictReader(fh):
            if not row.get("log10_f_Hz"):
                continue
            bins.append(
                dict(
                    log10_f=float(row["log10_f_Hz"]),
                    ymin=float(row["ymin_log10_h2OmegaGW"]),
                    ymax=float(row["ymax_log10_h2OmegaGW"]),
                )
            )
    return bins


def score_point(alpha, beta_H, Treh, bins):
    f = np.array([10 ** b["log10_f"] for b in bins])
    omega = h2OmegaGW(f, Treh, alpha, beta_H)
    log_omega = np.where(np.isfinite(omega) & (omega > 0), np.log10(omega), -np.inf)
    inside = 0
    for i, b in enumerate(bins):
        if b["ymin"] <= log_omega[i] <= b["ymax"]:
            inside += 1
    return inside, log_omega


def run_scan(g_grid, chi0_grid, bins, tag):
    rows = []
    for g in g_grid:
        for chi0 in chi0_grid:
            res = compute_point(g, chi0)
            row = dict(tag=tag, g=g, chi0=chi0, status=res["status"],
                       alpha=res["alpha"], beta_H=res["beta_H"],
                       Treh=res["Treh"], f_peak_est=res["f_peak_est"],
                       inside_bins=0, total_bins=len(bins))
            if res["status"] == "viable":
                inside, log_omega = score_point(res["alpha"], res["beta_H"],
                                                 res["Treh"], bins)
                row["inside_bins"] = inside
                # peak over the violin support
                peak_idx = int(np.argmax(log_omega))
                row["peak_log10_f"] = bins[peak_idx]["log10_f"]
                row["peak_log10_omega"] = float(log_omega[peak_idx])
            else:
                row["peak_log10_f"] = np.nan
                row["peak_log10_omega"] = np.nan
            rows.append(row)
    return rows


def main():
    bins = load_violin_bins()
    all_rows = []

    # Coarse scan: g linear, chi0 log; extended upward (best points hugged 0.1).
    g_coarse = np.linspace(0.8, 1.5, 15)
    chi0_coarse = np.logspace(-3, 1, 21)  # 1e-3 .. 10 GeV
    all_rows += run_scan(g_coarse, chi0_coarse, bins, "coarse")

    # Refine around best region (moderate g, larger chi0).
    g_fine = np.linspace(0.95, 1.35, 17)
    chi0_fine = np.logspace(-1.0, 1.0, 21)  # 0.1 .. 10 GeV
    all_rows += run_scan(g_fine, chi0_fine, bins, "fine")

    out = _HERE / "pta_benchmark_scan.csv"
    fields = ["tag", "g", "chi0", "status", "alpha", "beta_H", "Treh",
              "f_peak_est", "inside_bins", "total_bins",
              "peak_log10_f", "peak_log10_omega"]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in all_rows:
            w.writerow({k: r.get(k, "") for k in fields})

    viable = [r for r in all_rows if r["status"] == "viable"]
    viable.sort(key=lambda r: (-r["inside_bins"], abs(r["peak_log10_omega"])))
    print(f"template={TEMPLATE}  total={len(all_rows)} viable={len(viable)}")
    print("top 12 by inside_bins:")
    for r in viable[:12]:
        print(f"  g={r['g']:.3f} chi0={r['chi0']:.4e} alpha={r['alpha']:.2f} "
              f"betaH={r['beta_H']:.1f} Treh={r['Treh']:.3e} "
              f"inside={r['inside_bins']}/{r['total_bins']} "
              f"peak_logO={r['peak_log10_omega']:.2f}")


if __name__ == "__main__":
    main()
