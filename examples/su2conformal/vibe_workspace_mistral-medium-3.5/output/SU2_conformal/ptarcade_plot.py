"""
PTArcade plotting script for SU2_conformal model.
Generates posterior plots and best-fit spectrum visualization.
"""
import numpy as np
import json
from ptarcade import chains_utils as c_utils
from ptarcade import plot_utils as p_utils
from getdist import MCSamples
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))


def main():
    chains_dir = "./output/SU2_conformal/chains/np_model/"
    
    try:
        params, chain = c_utils.import_chains(chains_dir)
    except Exception as e:
        print(f"Error loading chains: {e}")
        print("Chains not found. PTArcade may not have run yet.")
        return
    
    param_names = list(params.keys())
    params_for_filter = np.array(param_names, dtype=object)
    
    # Filter chain
    filtered = c_utils.chain_filter(chain, params_for_filter, None, None)
    filtered_array = filtered[0]
    filtered_params = filtered[1]
    filtered_priors = {
        k.replace("_", "-"): v
        for k, v in params.items()
        if k.replace("_", "-") in filtered_params
        and (v is not None and not np.isnan(v).any())
    }
    
    # Create MCSamples
    samples = MCSamples(
        samples=filtered_array,
        names=filtered_params,
        ranges=filtered_priors,
        ignore_rows=1,
    )
    
    # Compute Bayes estimates
    bayes_est = c_utils.get_bayes_est(samples, filtered_params)
    max_pos = c_utils.get_max_pos(filtered_params, bayes_est, samples, filtered_priors)
    
    # Compute sigma regions
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
    
    # Save Bayesian estimates
    output = {
        "bayes_est": {p: {"mean": v[0], "std": v[1]} for p, v in bayes_est.items()},
        "map_est": max_pos,
        "sigma_regions": sigma_regions,
    }
    filename = "./output/SU2_conformal/ptarcade_bayes.json"
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)
    print(f"Saved Bayesian estimates to {filename}")
    
    # Plot posteriors
    # Use LaTeX-style parameter names
    par_names_display = []
    for param in filtered_params:
        if param == "log10_g_D":
            par_names_display.append([r"\log_{10} g_D"])
        elif param == "log10_v_GeV":
            par_names_display.append([r"\log_{10} (v / \text{GeV}) "])
        else:
            par_names_display.append([param])
    
    try:
        p_utils.plot_posteriors(
            [chain],
            [params],
            par_names=par_names_display,
            samples_name=["SU2_conformal"],
            model_name="SU2_conformal",
            plots_dir="./output/SU2_conformal/",
            save=True,
            verbose=True,
            hpi_levels=[0.68, 0.95, 0.99],
            levels=[0.68, 0.95, 0.99],
        )
        print("Posterior plots saved successfully")
    except Exception as e:
        print(f"Error plotting posteriors: {e}")
    
    # Also save a simple text summary
    with open("./output/SU2_conformal/ptarcade_summary.txt", "w") as f:
        f.write("PTArcade Summary for SU2_conformal\n")
        f.write("=" * 50 + "\n")
        f.write(f"Number of samples: 100000\n")
        f.write(f"Parameters: {filtered_params}\n")
        f.write("\nBayesian Estimates:\n")
        for p, v in bayes_est.items():
            f.write(f"  {p}: {v[0]:.4f} +/- {v[1]:.4f}\n")
        f.write("\nMAP Estimates:\n")
        for p, v in max_pos.items():
            f.write(f"  {p}: {v:.4f}\n")
        f.write("\nCredible Regions:\n")
        for sigma, regions in sigma_regions.items():
            f.write(f"  {sigma}:\n")
            for p, bounds in regions.items():
                f.write(f"    {p}: [{bounds['low']:.4f}, {bounds['high']:.4f}]\n")
    
    print("Summary saved to ./output/SU2_conformal/ptarcade_summary.txt")


if __name__ == "__main__":
    main()
