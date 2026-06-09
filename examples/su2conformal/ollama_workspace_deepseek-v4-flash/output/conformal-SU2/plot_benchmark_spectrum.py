#!/usr/bin/env python3
"""
Plot the best PTA benchmark spectra from the scan, overlaid on the NANOGrav violins.
"""
import sys, os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from spectrum import Spectrum

# --- import the spectrum wrapper ---
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pta_spectrum import compute_spectrum

# --- Violin SVG data from backend/plot_violins.py ---
import natpy as nat
import la_forge.core as co

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


# --- Best benchmark points from the scan (maximally diverse, 14/14 points) ---
# From the scan output, choosing 4 maximally different points
best_points = [
    {"g": 0.90, "chi0": 0.5,    "label": r"$g=0.90,\ \chi_0=0.5$ GeV"},
    {"g": 1.00, "chi0": 0.3897, "label": r"$g=1.00,\ \chi_0=0.39$ GeV"},
    {"g": 0.95, "chi0": 0.5,    "label": r"$g=0.95,\ \chi_0=0.5$ GeV"},
    {"g": 1.05, "chi0": 0.5,    "label": r"$g=1.05,\ \chi_0=0.5$ GeV"},
]

# Frequency grid for plotting (smooth curves)
f = np.logspace(-9, -7, 200)

# Colors for the 4 curves
colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]

# Load violins
print("Loading violins...")
h2_omega_viol, freqs_viol = load_violins(correlations=True)
print(f"Violins loaded: {h2_omega_viol.shape[1]} frequency bins")

# Create plot
fig, ax = plt.subplots(figsize=(8, 6))

# Plot violins (first 14 bins)
plot_violins(ax, h2_omega_viol, N_f=14, border="silver")

# Mark the violin window boxes from pta_violin_windows.csv
violin_windows = np.array([
    (1.99, -11, -9),
    (3.98, -10, -8.5),
    (5.96, -10, -8),
    (7.94, -10, -7.75),
    (10.00, -9.5, -7.5),
    (12.68, -10.7, -6.5),
    (14.79, -10.4, -6.4),
    (16.9, -10.1, -6.3),
    (19.01, -9.8, -6.2),
    (21.13, -9.6, -6.1),
    (23.24, -9.4, -6.0),
    (25.35, -9.25, -6.0),
    (27.46, -9.1, -6.0),
    (29.58, -8.95, -6.0),
])
f_violin_hz = violin_windows[:, 0] * 1e-9
ylow = violin_windows[:, 1]
yhigh = violin_windows[:, 2]

for i in range(len(f_violin_hz)):
    ax.plot([np.log10(f_violin_hz[i])]*2, [ylow[i], yhigh[i]], 'k-', lw=0.5, alpha=0.3)

# Add spectrum curves
for i, bp in enumerate(best_points):
    print(f"Computing spectrum for g={bp['g']}, chi0={bp['chi0']}...")
    h2Omega = compute_spectrum(bp["g"], bp["chi0"], f)
    log10_h2Omega = np.log10(np.maximum(h2Omega, 1e-30))
    ax.plot(np.log10(f), log10_h2Omega, '-', color=colors[i], lw=1.5, label=bp["label"])

# Axis labels
ax.set_xlabel(r"$\log_{10}(f / \mathrm{Hz})$", fontsize=14)
ax.set_ylabel(r"$\log_{10}(h^2 \Omega_{\mathrm{GW}})$", fontsize=14)
ax.set_title("Conformal SU(2) GW Spectrum vs NANOGrav Violins", fontsize=14)

ax.set_xlim(-9, -7)
ax.set_ylim(-13, -5)
ax.legend(fontsize=10, loc="lower left")
ax.grid(True, alpha=0.3)

fig.tight_layout()
outfile = Path(__file__).resolve().parent / "pta_benchmark_spectrum.pdf"
fig.savefig(str(outfile), dpi=150)
print(f"Saved benchmark spectrum to {outfile}")