"""Benchmark PTA scan and plot for minimal_conformal_su2_doublet."""

from __future__ import annotations

import csv
import itertools
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import natpy as nat
import la_forge.core as co
import numpy as np
import pandas as pd


MODEL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = MODEL_DIR.parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from pta_spectrum import TEMPLATE, h2omega_from_fopt, fopt_from_model_parameters  # noqa: E402


WINDOWS_FILE = BACKEND_DIR / "pta_violin_windows.csv"
FOPT_FILE = MODEL_DIR / "fopt_benchmarks.csv"
SCAN_FILE = MODEL_DIR / "pta_benchmark_scan.csv"
PLOT_FILE = MODEL_DIR / "pta_benchmark_spectrum.pdf"


def load_violins(correlations=False):
    def find_core(filename: str) -> Path:
        repo_root = Path(__file__).resolve().parents[2]
        matches = list(repo_root.rglob(filename))
        if matches:
            return matches[0]
        matches = list(Path.cwd().rglob(filename))
        if matches:
            return matches[0]
        return None

    filename = "30fCP_30fiRN_3A.core" if correlations else "30fCP_30fiRN_2A.core"
    corepath = find_core(filename)
    label_correlations = correlations
    if corepath is None and not correlations:
        corepath = find_core("30fCP_30fiRN_3A.core")
        label_correlations = True
    if corepath is None:
        raise FileNotFoundError(f"Could not find PTA core file: {filename}")

    c0 = co.Core(corepath=str(corepath))
    if label_correlations:
        labels = [p for p in c0.params if "gw_hd" in p]
    else:
        labels = [p for p in c0.params if "rho" in p]
    if not labels:
        raise ValueError(f"No PTA violin parameters found in {corepath}")

    freqs = c0.rn_freqs  # array of frequencies

    # load free spec samples
    viol = c0(labels)  # this is now a numpy array of Nsamples x Nfreq

    dfreq = np.diff(np.concatenate((np.array([0]), freqs[::1])))

    H_0byh = 100 * nat.convert(nat.km * nat.s**-1 * nat.Mpc**-1, nat.Hz)  # H_0/h in Hz
    h2_omega_viol = np.log10(
        24
        * np.pi**4
        * (10**viol) ** 2
        * 1
        / np.repeat(dfreq, 1)
        * freqs**5
        / (3 * H_0byh**2)
    )
    return h2_omega_viol, freqs


def plot_violins(ax, h2_omega_viol, N_f=14, border="silver"):
    Tspan = 505861299.1401644
    n_freq = min(N_f, h2_omega_viol.shape[1])
    freqs = np.arange(1, n_freq + 1) / Tspan

    v1 = ax.violinplot(
        h2_omega_viol[:, :n_freq],
        positions=np.log10(freqs),
        widths=0.05,
        showextrema=False,
    )

    for pc in v1["bodies"]:
        pc.set_facecolor("silver")
        pc.set_edgecolor(border)
        pc.set_linestyle("solid")

    return


def score_spectrum(log_values: np.ndarray, windows: pd.DataFrame) -> tuple[int, float]:
    inside = (log_values >= windows["ymin_log10_h2OmegaGW"].to_numpy()) & (
        log_values <= windows["ymax_log10_h2OmegaGW"].to_numpy()
    )
    centers = 0.5 * (
        windows["ymin_log10_h2OmegaGW"].to_numpy() + windows["ymax_log10_h2OmegaGW"].to_numpy()
    )
    half_width = 0.5 * (
        windows["ymax_log10_h2OmegaGW"].to_numpy() - windows["ymin_log10_h2OmegaGW"].to_numpy()
    )
    distance = np.abs(log_values - centers) / np.maximum(half_width, 1.0e-12)
    return int(inside.sum()), float(np.nanmean(distance))


def candidate_grid() -> list[tuple[float, float]]:
    fopt = pd.read_csv(FOPT_FILE)
    viable = fopt[fopt["status"] == "viable"].copy()
    pta = viable[viable["in_pta_band_est"] == True].copy()  # noqa: E712
    base = pta[["gD", "vD"]].drop_duplicates()
    steering = pd.DataFrame(
        [
            {"gD": 0.9, "vD": 0.04200999215387282},
            {"gD": 1.37, "vD": 0.0120146},
        ]
    )
    near_best = []
    for _, row in pta.sort_values("f_peak_est").iloc[:: max(1, len(pta) // 80)].iterrows():
        for dg, lv in itertools.product(np.linspace(-0.06, 0.06, 5), np.linspace(-0.18, 0.18, 5)):
            near_best.append({"gD": float(row.gD + dg), "vD": float(row.vD * 10**lv)})
    grid = pd.concat([base, steering, pd.DataFrame(near_best)], ignore_index=True)
    grid = grid[(grid["gD"] > 0.0) & (grid["gD"] < math.sqrt(4.0 * math.pi)) & (grid["vD"] > 0.0)]
    grid["gD"] = grid["gD"].round(10)
    grid["vD"] = grid["vD"].map(lambda x: float(f"{x:.12g}"))
    return [tuple(x) for x in grid.drop_duplicates().to_numpy()]


def run_scan():
    windows = pd.read_csv(WINDOWS_FILE, index_col=False)
    frequencies = 10 ** windows["log10_f_Hz"].to_numpy(dtype=float)
    rows = []
    total_bins = len(frequencies)
    for idx, (gD, vD) in enumerate(candidate_grid(), start=1):
        row = {"spectrum_id": f"pta_{idx:05d}", "gD": gD, "vD": vD, "template": TEMPLATE}
        try:
            fopt = fopt_from_model_parameters(gD, vD)
            spectrum = h2omega_from_fopt(frequencies, fopt["Treh"], fopt["alpha"], fopt["beta_H"])
            log_spectrum = np.full_like(spectrum, -np.inf, dtype=float)
            good = np.isfinite(spectrum) & (spectrum > 0)
            log_spectrum[good] = np.log10(spectrum[good])
            inside_bins, mean_center_distance = score_spectrum(log_spectrum, windows)
            row.update(fopt)
            row.update(
                {
                    "pta_score": inside_bins,
                    "inside_bins": inside_bins,
                    "total_bins": total_bins,
                    "mean_center_distance": mean_center_distance,
                    "peak_frequency_Hz": float(frequencies[np.nanargmax(spectrum)]),
                    "peak_h2OmegaGW": float(np.nanmax(spectrum)),
                    "pta_status": "ok" if np.all(np.isfinite(spectrum)) else "nonfinite_spectrum",
                }
            )
            for i, value in enumerate(frequencies, start=1):
                row[f"f{i}_Hz"] = float(value)
                row[f"h2OmegaGW_bin{i}"] = float(spectrum[i - 1])
                row[f"log10_h2OmegaGW_bin{i}"] = float(log_spectrum[i - 1])
        except Exception as exc:
            row.update({"pta_score": 0, "inside_bins": 0, "total_bins": total_bins, "pta_status": "failed", "failure_reason": repr(exc)})
        rows.append(row)
    df = pd.DataFrame(rows)
    df.sort_values(["pta_score", "mean_center_distance"], ascending=[False, True], inplace=True, na_position="last")
    df.to_csv(SCAN_FILE, index=False, quoting=csv.QUOTE_MINIMAL)
    return df, windows, frequencies


def diverse_best(df: pd.DataFrame, n: int = 4) -> pd.DataFrame:
    ok = df[df["pta_status"] == "ok"].copy()
    if ok.empty:
        return ok
    ok = ok.sort_values(["pta_score", "mean_center_distance"], ascending=[False, True]).head(80)
    selected = [ok.iloc[0]]
    while len(selected) < min(n, len(ok)):
        best_i, best_d = None, -1.0
        for i, row in ok.iterrows():
            if any(row["spectrum_id"] == s["spectrum_id"] for s in selected):
                continue
            d = min(
                math.hypot((row["gD"] - s["gD"]) / 0.5, (math.log10(row["vD"]) - math.log10(s["vD"])) / 1.0)
                for s in selected
            )
            if d > best_d:
                best_i, best_d = i, d
        selected.append(ok.loc[best_i])
    return pd.DataFrame(selected)


def plot_best(df: pd.DataFrame, windows: pd.DataFrame):
    best = diverse_best(df)
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    try:
        viol, _ = load_violins(False)
        plot_violins(ax, viol, N_f=len(windows))
    except Exception:
        for _, row in windows.iterrows():
            ax.fill_between(
                [row["log10_f_Hz"] - 0.025, row["log10_f_Hz"] + 0.025],
                row["ymin_log10_h2OmegaGW"],
                row["ymax_log10_h2OmegaGW"],
                color="silver",
                alpha=0.55,
            )
    dense_f = np.logspace(windows["log10_f_Hz"].min() - 0.15, windows["log10_f_Hz"].max() + 0.15, 300)
    for _, row in best.iterrows():
        spectrum = h2omega_from_fopt(dense_f, row["Treh"], row["alpha"], row["beta_H"])
        good = np.isfinite(spectrum) & (spectrum > 0)
        ax.plot(np.log10(dense_f[good]), np.log10(spectrum[good]), lw=1.6, label=fr"$g_D={row['gD']:.3g}$, $v_D={row['vD']:.3g}$ GeV")
    ax.set_xlabel(r"$\log_{10}(f/{\rm Hz})$")
    ax.set_ylabel(r"$\log_{10}(h^2\Omega_{\rm GW})$")
    ax.set_xlim(windows["log10_f_Hz"].min() - 0.2, windows["log10_f_Hz"].max() + 0.2)
    ax.set_ylim(windows["ymin_log10_h2OmegaGW"].min() - 1.0, windows["ymax_log10_h2OmegaGW"].max() + 0.8)
    ax.legend(fontsize=8, frameon=False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(PLOT_FILE)


if __name__ == "__main__":
    df, windows, _ = run_scan()
    plot_best(df, windows)
    print(df[["spectrum_id", "gD", "vD", "pta_score", "inside_bins", "total_bins", "mean_center_distance"]].head(10).to_string(index=False))
