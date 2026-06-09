import numpy as np
import json
from ptarcade import chains_utils as c_utils
from ptarcade import plot_utils as p_utils
from getdist import MCSamples

chains_dir = "./output/u1conformal/chains/np_model/"
params, chain = c_utils.import_chains(chains_dir)
param_names = list(params.keys())
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
samples = MCSamples(
    samples=filtered_array,
    names=filtered_params,
    ranges=filtered_priors,
    ignore_rows=1,
)
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
        label: {
            "low": float(np.percentile(finite, lo)),
            "high": float(np.percentile(finite, hi)),
        }
        for label, (lo, hi) in sigma_percentiles.items()
    }

output = {
    "bayes_est": {p: {"mean": v[0], "std": v[1]} for p, v in bayes_est.items()},
    "map_est": max_pos,
    "sigma_regions": sigma_regions,
}
filename = "./output/u1conformal/ptarcade_bayes.json"
with open(filename, "w") as f:
    json.dump(output, f, indent=4)

p_utils.plot_posteriors(
    [chain],
    [params],
    par_names=[[r"$\log_{10}(v/\mathrm{GeV})$", r"$g_D$"]],
    samples_name=["Conformal $U(1)_D$ FOPT"],
    model_name="u1conformal",
    plots_dir="./output/u1conformal/",
    save=True,
    verbose=True,
    hpi_levels=[0.68, 0.95, 0.99],
    levels=[0.68, 0.95, 0.99],
)
print("MAP:", max_pos)
print("BAYES:", bayes_est)
