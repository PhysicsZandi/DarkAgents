"""
PTArcade posterior plotting script for the Dark U(1)_D conformal model.

Reads PTArcade chains and generates posterior plots and Bayesian estimates.

Usage:
    conda run -n ptarcade python3 output/u1conformal/ptarcade_plot.py
"""
import sys
import os
import numpy as np
import json
from pathlib import Path

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add backend for spectrum
_backend_dir = os.path.join(OUTPUT_DIR, "..", "..", "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Add model directory
if OUTPUT_DIR not in sys.path:
    sys.path.insert(0, OUTPUT_DIR)


def main():
    chains_dir = os.path.join(OUTPUT_DIR, "chains", "np_model")

    if not os.path.isdir(chains_dir):
        print(f"ERROR: Chains directory not found: {chains_dir}")
        print("Has the PTArcade campaign been run?")
        return

    from ptarcade import chains_utils as c_utils
    from ptarcade import plot_utils as p_utils
    from getdist import MCSamples

    # Import chains
    print(f"Importing chains from: {chains_dir}")
    params, chain = c_utils.import_chains(chains_dir)

    param_names = list(params.keys())
    print(f"Found parameters: {param_names}")

    # Filter chains to model parameters only
    params_for_filter = np.array(param_names, dtype=object)
    filtered = c_utils.chain_filter(chain, params_for_filter, None, None)
    filtered_array = filtered[0]
    filtered_params = filtered[1]

    print(f"Filtered parameters: {filtered_params}")
    print(f"Chain shape: {filtered_array.shape}")

    # Build filtered priors dict
    filtered_priors = {
        k.replace("_", "-"): v
        for k, v in params.items()
        if k.replace("_", "-") in filtered_params
        and (v is not None and not np.isnan(v).any())
    }

    # Create MCSamples object
    samples = MCSamples(
        samples=filtered_array,
        names=filtered_params,
        ranges=filtered_priors,
        ignore_rows=1,
    )

    # Get Bayesian estimates
    bayes_est = c_utils.get_bayes_est(samples, filtered_params)
    max_pos = c_utils.get_max_pos(filtered_params, bayes_est, samples, filtered_priors)

    print("Bayesian estimates:")
    for p, v in bayes_est.items():
        print(f"  {p}: mean = {v[0]:.6f}, std = {v[1]:.6f}")
    print(f"MAP estimates: {max_pos}")

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

    # Save Bayesian estimates to JSON
    output = {
        "bayes_est": {p: {"mean": float(v[0]), "std": float(v[1])}
                      for p, v in bayes_est.items()},
        "map_est": max_pos,
        "sigma_regions": sigma_regions,
    }

    bayes_file = os.path.join(OUTPUT_DIR, "ptarcade_bayes.json")
    with open(bayes_file, "w") as f:
        json.dump(output, f, indent=4)
    print(f"\nSaved Bayesian estimates to: {bayes_file}")

    # Plot posteriors
    print("\nGenerating posterior plot...")

    # Parameter names for plot (must match filtered_params exactly)
    par_names_plot = [filtered_params]  # List of lists, one per model

    try:
        p_utils.plot_posteriors(
            [chain],
            [params],
            par_names=par_names_plot,
            samples_name=["u1conformal"],
            model_name="u1conformal",
            plots_dir=OUTPUT_DIR,
            save=True,
            verbose=True,
            hpi_levels=[0.68, 0.95, 0.99],
            levels=[0.68, 0.95, 0.99],
        )
        print("Posterior plot saved.")
    except Exception as e:
        print(f"Error generating posterior plot: {e}")
        print("Attempting alternative plotting method...")
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            fig, axes = plt.subplots(2, 2, figsize=(10, 8))
            n_params = len(filtered_params)
            for i, (pname, ax_row) in enumerate(zip(filtered_params, axes)):
                for j, (pname2, ax_col) in enumerate(zip(filtered_params, ax_row)):
                    if i == j:
                        col = filtered_array[:, i]
                        col = col[np.isfinite(col)]
                        ax_col.hist(col, bins=50, density=True, alpha=0.7, color="steelblue")
                        ax_col.set_xlabel(pname, fontsize=10)
                        ax_col.set_ylabel("density", fontsize=10)
                    elif j > i:
                        x = filtered_array[:, j]
                        y = filtered_array[:, i]
                        finite = np.isfinite(x) & np.isfinite(y)
                        ax_col.scatter(x[finite], y[finite], s=1, alpha=0.3, color="steelblue")
                        ax_col.set_xlabel(pname2, fontsize=10)
                        ax_col.set_ylabel(pname, fontsize=10)
                    else:
                        ax_col.set_visible(False)
            plt.tight_layout()
            out_path = os.path.join(OUTPUT_DIR, "pta_posteriors.pdf")
            fig.savefig(out_path, dpi=150, bbox_inches="tight")
            print(f"Alternative posterior plot saved to: {out_path}")
            plt.close()
        except Exception as e2:
            print(f"Both plotting methods failed: {e2}")


if __name__ == "__main__":
    main()