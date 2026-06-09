"""
ptarcade_plot.py -- Plot PTArcade posteriors and MAP spectrum for the conformal U(1)_D model.
"""

import sys
import os
import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Add backend to path
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Add output dir to path
_output_dir = os.path.dirname(os.path.abspath(__file__))
if _output_dir not in sys.path:
    sys.path.insert(0, _output_dir)

from ptarcade import chains_utils as c_utils
from ptarcade import plot_utils as p_utils
from getdist import MCSamples

# ============================================================
# Load chains and compute Bayesian estimates
# ============================================================
chains_dir = "./output/u1conformal_fermion/chains_v2/np_model/"
params, chain = c_utils.import_chains(chains_dir)

param_names = list(params.keys())
print(f"Parameter names: {param_names}")
print(f"Chain shape: {chain.shape}")

params_for_filter = np.array(param_names, dtype=object)
filtered = c_utils.chain_filter(chain, params_for_filter, None, None)
filtered_array = filtered[0]
filtered_params = filtered[1]
filtered_priors = {
    k.replace("_", "-"): v
    for k, v in params.items()
    if k.replace("_", "-") in filtered_params
    and (v is not None and not np.isnan(v).any())
}

print(f"Filtered params: {filtered_params}")
print(f"Filtered array shape: {filtered_array.shape}")

samples = MCSamples(
    samples=filtered_array,
    names=filtered_params,
    ranges=filtered_priors,
    ignore_rows=1,
)

bayes_est = c_utils.get_bayes_est(samples, filtered_params)
max_pos = c_utils.get_max_pos(filtered_params, bayes_est, samples, filtered_priors)

print(f"Bayesian estimates: {bayes_est}")
print(f"MAP position: {max_pos}")

# Compute credible regions
sigma_percentiles = {
    "1sigma": (15.865, 84.135),
    "2sigma": (2.275, 97.725),
    "3sigma": (0.135, 99.865),
}
sigma_regions = {}
for idx, param in enumerate(filtered_params):
    column = filtered_array[:, idx]
    finite = column[np.isfinite(column)]
    if finite.size == 0:
        continue
    sigma_regions[param] = {
        label: {
            "low": float(np.percentile(finite, lo)),
            "high": float(np.percentile(finite, hi)),
        }
        for label, (lo, hi) in sigma_percentiles.items()
    }

# Save Bayesian results to JSON (use original parameter names)
param_name_map = {"g-D": "g_D", "y-psi": "y_psi", "log10-v": "log10_v"}
output = {
    "bayes_est": {param_name_map.get(p, p): {"mean": float(v[0]), "std": float(v[1])} for p, v in bayes_est.items()},
    "map_est": {param_name_map.get(p, p): float(v) for p, v in max_pos.items()},
    "sigma_regions": {param_name_map.get(p, p): v for p, v in sigma_regions.items()},
}
filename = "./output/u1conformal_fermion/ptarcade_bayes.json"
with open(filename, 'w') as f:
    json.dump(output, f, indent=4)
print(f"Saved Bayesian results to {filename}")

# ============================================================
# Plot posteriors
# ============================================================
# Use LaTeX-compatible parameter names
par_names = [[r"$g_D$", r"$y_\psi$", r"$\log_{10}(v / \mathrm{GeV})$"]]

p_utils.plot_posteriors(
    [chain],
    [params],
    par_names=par_names,
    samples_name=["u1conformal_fermion"],
    model_name="u1conformal_fermion",
    plots_dir="./output/u1conformal_fermion/",
    save=True,
    verbose=True,
    hpi_levels=[0.68, 0.95, 0.99],
    levels=[0.68, 0.95, 0.99],
)

print("Saved posterior plot")

# ============================================================
# Plot MAP-point spectrum against PTA violins
# ============================================================
print("\nComputing MAP-point spectrum...")

# Import violin plotting functions
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

    freqs = c0.rn_freqs
    viol = c0(labels)
    dfreq = np.diff(np.concatenate((np.array([0]), freqs[::1])))
    H_0byh = 100 * nat.convert(nat.km * nat.s**-1 * nat.Mpc**-1, nat.Hz)
    h2_omega_viol = np.log10(
        24 * np.pi**4 * (10**viol) ** 2 * 1 / np.repeat(dfreq, 1) * freqs**5 / (3 * H_0byh**2)
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


# Get MAP parameters
map_g_D = max_pos["g-D"]
map_y_psi = max_pos["y-psi"]
map_log10_v = max_pos["log10-v"]
map_v = 10.0 ** map_log10_v

print(f"MAP parameters: g_D={map_g_D:.4f}, y_psi={map_y_psi:.4f}, v={map_v:.6f} GeV")

# Compute spectrum at MAP point
from fopt_model import compute_fopt, is_viable
from pta_spectrum import get_spectrum

f = np.logspace(-9.5, -6.5, 1000)
fopt_result = compute_fopt(map_g_D, map_y_psi, map_v)

if is_viable(fopt_result):
    h2OmegaGW = get_spectrum(f, fopt_result["Treh"], fopt_result["alpha"],
                              fopt_result["beta_H"], template="dbf")

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Load and plot violins
    h2_omega_viol, freqs = load_violins()
    plot_violins(ax, h2_omega_viol, N_f=14)

    # Plot MAP spectrum
    log10_f = np.log10(f)
    log10_h2OmegaGW = np.log10(np.maximum(h2OmegaGW, 1e-30))

    label = (f"MAP: $g_D={map_g_D:.3f}$, "
             f"$y_\\psi={map_y_psi:.3f}$, "
             f"$v={map_v:.4f}$ GeV")

    ax.plot(log10_f, log10_h2OmegaGW, color='#E41A1C', linewidth=2,
            label=label, alpha=0.9)

    # Axis labels
    ax.set_xlabel(r'$\log_{10}(f / \mathrm{Hz})$', fontsize=14)
    ax.set_ylabel(r'$\log_{10}(h^2 \Omega_{\mathrm{GW}})$', fontsize=14)
    ax.set_xlim(-9.0, -7.0)
    ax.set_ylim(-12, -5)
    ax.legend(fontsize=10, loc='lower left', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle=':')
    ax.set_title('Conformal U(1)$_D$ Dark Sector: MAP Spectrum vs PTA Violins',
                 fontsize=13)

    plt.tight_layout()
    plt.savefig("./output/u1conformal_fermion/pta_ptarcade_spectrum.pdf",
                dpi=150, bbox_inches='tight')
    print("Saved MAP spectrum plot to output/u1conformal_fermion/pta_ptarcade_spectrum.pdf")
    plt.close()
else:
    print("WARNING: MAP point is not viable!")
