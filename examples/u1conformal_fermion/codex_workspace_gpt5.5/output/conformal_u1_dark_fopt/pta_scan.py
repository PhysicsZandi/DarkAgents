"""Score FOPT benchmark points against the PTA violin windows."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import pandas as pd

from pta_spectrum import SELECTED_TEMPLATE, peak_diagnostics, spectrum_from_fopt

OUTDIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
WINDOWS = REPO_ROOT / "backend" / "pta_violin_windows.csv"
FOPT_CSV = OUTDIR / "fopt_benchmarks.csv"
OUT_CSV = OUTDIR / "pta_benchmark_scan.csv"


def score_spectrum(log_omega: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> tuple[int, float]:
    inside = (log_omega >= lo) & (log_omega <= hi)
    below = np.maximum(lo - log_omega, 0.0)
    above = np.maximum(log_omega - hi, 0.0)
    distance = float(np.sqrt(np.mean((below + above) ** 2)))
    return int(np.sum(inside)), distance


def main() -> None:
    windows = pd.read_csv(WINDOWS, usecols=["bin_i", "f_nHz", "log10_f_Hz", "ymin_log10_h2OmegaGW", "ymax_log10_h2OmegaGW"])
    freqs = 10.0 ** windows["log10_f_Hz"].to_numpy(dtype=float)
    lo = windows["ymin_log10_h2OmegaGW"].to_numpy(dtype=float)
    hi = windows["ymax_log10_h2OmegaGW"].to_numpy(dtype=float)
    fopt_rows = pd.read_csv(FOPT_CSV)

    fieldnames = [
        "spectrum_id",
        "name",
        "template",
        "v_D",
        "g_D",
        "y_D",
        "gb_X",
        "gf_psi",
        "beta_lambda",
        "status",
        "failure_reason",
        "alpha",
        "beta_H",
        "Treh",
        "f_peak_est",
        "inside_bins",
        "total_bins",
        "window_rms_distance_log10",
        "peak_frequency_Hz",
        "peak_h2OmegaGW",
    ]
    for i in range(len(freqs)):
        fieldnames.append(f"freq_{i + 1}_Hz")
        fieldnames.append(f"h2OmegaGW_{i + 1}")
        fieldnames.append(f"log10_h2OmegaGW_{i + 1}")

    rows = []
    for idx, row in fopt_rows.iterrows():
        fopt = row.to_dict()
        values = spectrum_from_fopt(freqs, fopt, template=SELECTED_TEMPLATE)
        log_values = np.log10(np.maximum(values, 1e-300))
        inside, distance = score_spectrum(log_values, lo, hi)
        peak = peak_diagnostics(fopt, template=SELECTED_TEMPLATE)
        out = {
            "spectrum_id": f"pta_{idx:04d}",
            "name": row.get("name", f"row_{idx}"),
            "template": SELECTED_TEMPLATE,
            "v_D": row.get("v_D", math.nan),
            "g_D": row.get("g_D", math.nan),
            "y_D": row.get("y_D", math.nan),
            "gb_X": row.get("gb_X", math.nan),
            "gf_psi": row.get("gf_psi", math.nan),
            "beta_lambda": row.get("beta_lambda", math.nan),
            "status": row.get("status", ""),
            "failure_reason": row.get("failure_reason", ""),
            "alpha": row.get("alpha", math.nan),
            "beta_H": row.get("beta_H", math.nan),
            "Treh": row.get("Treh", math.nan),
            "f_peak_est": row.get("f_peak_est", math.nan),
            "inside_bins": inside,
            "total_bins": len(freqs),
            "window_rms_distance_log10": distance,
            "peak_frequency_Hz": peak["peak_frequency_Hz"],
            "peak_h2OmegaGW": peak["peak_h2OmegaGW"],
        }
        for i, (freq, value, log_value) in enumerate(zip(freqs, values, log_values), start=1):
            out[f"freq_{i}_Hz"] = float(freq)
            out[f"h2OmegaGW_{i}"] = float(value)
            out[f"log10_h2OmegaGW_{i}"] = float(log_value)
        rows.append(out)

    rows.sort(
        key=lambda r: (
            -int(r["inside_bins"]),
            float(r["window_rms_distance_log10"]),
            abs(math.log10(max(float(r.get("peak_frequency_Hz") or 1e-300), 1e-300) / 1e-8)),
        )
    )
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT_CSV} with {len(rows)} rows")
    print("best rows:")
    for row in rows[:8]:
        print(
            row["spectrum_id"],
            row["name"],
            "score",
            f"{row['inside_bins']}/{row['total_bins']}",
            "distance",
            f"{row['window_rms_distance_log10']:.3g}",
        )


if __name__ == "__main__":
    main()
