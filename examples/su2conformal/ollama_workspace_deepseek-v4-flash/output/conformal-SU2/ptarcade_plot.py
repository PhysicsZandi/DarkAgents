#!/usr/bin/env python3
"""
Plot PTArcade posteriors and MAP spectrum for the conformal-SU2 model.
"""
import sys, os
from pathlib import Path
import numpy as np
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# PTArcade utilities
import ptarcade.chains_utils as c_utils
import ptarcade.plot_utils as p_utils
from getdist import MCSamples

# Backend
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from spectrum import Spectrum

output_dir = Path(__file__).resolve().parent
chains_dir = str(output_dir / "chains" / "np_model")

# --- Load chains ---
print(f"Loading chains from {chains_dir}")
params, chain = c_utils.import_chains(chains_dir)
param_names = list(params.keys())
print(f"Parameters: {param_names}")
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

# --- MCSamples for GetDist ---
samples = MCSamples(
    samples=filtered_array,
    names=filtered_params,
    ranges=filtered_priors,
    ignore_rows=1,
)

# --- Bayesian estimates ---
print("Computing Bayesian estimates...")
bayes_est = c_utils.get_bayes_est(samples, filtered_params)
max_pos = c_utils.get_max_pos(filtered_params, bayes_est, samples, filtered_priors)

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
        label: {"low": float(np.percentile(finite, lo)), "high": float(np.percentile(finite, hi))}
        for label, (lo, hi) in sigma_percentiles.items()
    }

# --- Save bayes JSON ---
output = {
    "bayes_est": {p: {"mean": float(v[0]), "std": float(v[1])} for p, v in bayes_est.items()},
    "map_est": max_pos,
    "sigma_regions": sigma_regions,
}
bayes_file = output_dir / "ptarcade_bayes.json"
with open(bayes_file, "w") as f:
    json.dump(output, f, indent=4)
print(f"Saved Bayesian estimates to {bayes_file}")
print(f"MAP estimates: {max_pos}")

# --- LaTeX parameter names for plotting ---
latex_names = {
    "g": r"$g$",
    "log10_chi0": r"$\log_{10}(\chi_0 / \mathrm{GeV})$",
    "log10_A_gw": r"$\log_{10} A_{\mathrm{GW}}$",
    "gamma_gw": r"$\gamma_{\mathrm{GW}}$",
}
par_plot_names = [latex_names.get(p, p) for p in filtered_params if p in latex_names or True]
# Use the full set of filtered params that appear in both list and chain
plot_params = [p for p in filtered_params if p in param_names or p.startswith("log10") or p.startswith("gamma") or p == "g"]
plot_names = [latex_names.get(p, p) for p in plot_params]

# --- Plot posteriors ---
print("Plotting posteriors...")
p_utils.plot_posteriors(
    [chain],
    [params],
    par_names=[plot_params],
    samples_name=["conformal-SU2"],
    model_name="conformal-SU2",
    plots_dir=str(output_dir / ""),
    save=True,
    verbose=True,
    hpi_levels=[0.68, 0.95, 0.99],
    levels=[0.68, 0.95, 0.99],
)
print(f"Saved posteriors to {output_dir}/conformal-SU2_posteriors.pdf")

# --- MAP-point spectrum ---
print("Computing MAP-point spectrum...")
sys.path.insert(0, str(output_dir))
from pta_spectrum import compute_spectrum

# Frequency grid
f = np.logspace(-9, -7, 200)

# Extract MAP values for model parameters
g_map = max_pos.get("g", None)
log10_chi0_map = max_pos.get("log10-chi0", None) or max_pos.get("log10_chi0", None)

# Also import the model
sys.path.insert(0, str(output_dir))

if g_map is not None and log10_chi0_map is not None:
    chi0_map = 10.0**log10_chi0_map
    print(f"MAP: g={g_map:.4f}, chi0={chi0_map:.6e} GeV")
    h2Omega_map = compute_spectrum(g_map, chi0_map, f)
    log10_h2_map = np.log10(np.maximum(h2Omega_map, 1e-30))

    # Plot spectrum
    fig, ax = plt.subplots(figsize=(8, 6))

    # Load and plot violins
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
    from plot_violins import load_violins, plot_violins
    h2_omega_viol, freqs_viol = load_violins(correlations=True)
    plot_violins(ax, h2_omega_viol, N_f=14, border="silver")

    # MAP spectrum curve
    ax.plot(np.log10(f), log10_h2_map, '-', color="#1f77b4", lw=2.5,
            label=f"MAP: $g={g_map:.2f},\ \chi_0={chi0_map:.3e}$ GeV")

    ax.set_xlabel(r"$\log_{10}(f / \mathrm{Hz})$", fontsize=14)
    ax.set_ylabel(r"$\log_{10}(h^2 \Omega_{\mathrm{GW}})$", fontsize=14)
    ax.set_title("Conformal SU(2) MAP Spectrum vs NANOGrav Violins", fontsize=14)
    ax.set_xlim(-9, -7)
    ax.set_ylim(-13, -5)
    ax.legend(fontsize=10, loc="lower left")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    map_spec_file = output_dir / "pta_ptarcade_spectrum.pdf"
    fig.savefig(str(map_spec_file), dpi=150)
    print(f"Saved MAP spectrum to {map_spec_file}")
else:
    print("Warning: Could not extract MAP values for g and log10_chi0")
    print(f"max_pos available keys: {max_pos.keys() if hasattr(max_pos, 'keys') else max_pos}")

print("Done.")