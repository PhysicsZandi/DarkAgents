# PTArcade Contract

This document defines the generated PTArcade interface and runner behavior.

## PTArcade Model File

Write `output/<model-name>/ptarcade_model.py`. PTArcade expects a Python model file passed with `ptarcade -m`. For stochastic signals, the file must define:

```python
from ptarcade.models_utils import prior
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from spectrum import Spectrum

parameters = {"NAME_OF_PARAMETER": prior("Uniform", LOWER_VALUE, UPPER_VALUE), ...}

def spectrum(f, NAME_OF_PARAMETER, ...):
    ...
    return h2omegagw
```

Rules:
- The first argument of `spectrum` must be named `f`, followed by the PTArcade parameters.
- Return an array of `h^2 Omega_GW(f)` values.
- Use the deterministic `Spectrum` class from `backend/spectrum.py`; do not copy or reimplement the spectral formula inside the PTArcade model.
- Use FOPT results only to define physically motivated ranges for independent model parameters. PTArcade priors must be placed on independent model parameters, not directly on derived FOPT quantities such as `alpha`, `beta_H`, `Treh`, peak frequency or peak amplitude.
- Validate `f`, `alpha`, `beta_H`, and `Tr` inside `spectrum`; if inputs are non-finite or outside the physical domain, return a finite zero array with the same shape as `f`.
- If the posterior mass or the MAP estimate reaches a prior boundary, widen that prior and rerun before interpreting the result.
- Pay attention that the `NAME_OF_PARAMETER` in the argument of the function `spectrum` are lists and not scalar. So the spectrum function must be able to handle array inputs for the parameters. A simple solution is to add something like this at the beginning and then use the scalar `NAME_OF_PARAMETER` in the rest of the function:
```python
NAME_OF_PARAMETER = float(
        np.asarray(NAME_OF_PARAMETER).item()
        if np.asarray(NAME_OF_PARAMETER).size == 1
        else np.asarray(NAME_OF_PARAMETER).flat[0]
    )
```
- If you want a logarithmic prior, do not use `prior("LogUniform", ...)` because PTArcade does not support it. Instead, use `prior("Uniform", np.log10(LOWER_VALUE), np.log10(UPPER_VALUE))` and then recover the parameter inside the `spectrum` function with `10**` (i.e. base-10). Always work in base-10: use `np.log10` and `10**`, never `np.log`/`np.exp` (natural log), to avoid confusion between the two conventions.
- If a parameter spans several orders of magnitude, use a logarithmic prior. If it spans a small range, use a linear prior. 
- If the user asks for the contribution of supermassive black hole binaries (SMBHBs) to the PTA signal, simply add `smbhb = True` at the end of the model file. PTArcade will then automatically include them in the spectrum and marginalize over their contribution. Do not attempt to model the SMBHB contribution yourself or to add extra parameters for it, as this may lead to double-counting and incorrect results. 
```python

## PTArcade Config File

Write `output/<model-name>/ptarcade_config.py`.

Recommended conservative defaults:
```python
pta_data = "NG15"
mode = "ceffyl"
mod_sel = False
out_dir = "output/<model-name>/chains"
resume = False
N_samples = int(1e5)
red_components = 14
corr = False
gwb_components = 14
bhb_th_prior = True
```

Before a full campaign, the PTA agent must run a short dry-run or validation configuration to check dependencies, file paths and model execution. 

A smoke test validation configuration may use:
```python
N_samples = int(100)
```
Do NOT interpret the results of a smoke test as final or publishable. The purpose of the smoke test is solely to verify that the model and configuration are correctly set up and that PTArcade can execute without errors. Run a full campaign with the intended number of samples and proper convergence diagnostics before interpreting or publishing any results.

## PTArcade Plot File

Write `output/<model-name>/ptarcade_plot.py`. A template is 
```python
import numpy as np
import json
from ptarcade import chains_utils as c_utils
from ptarcade import plot_utils as p_utils
from getdist import MCSamples
chains_dir = "./output/<model-name>/chains/np_model/"
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
filename = "./output/<model-name>/ptarcade_bayes.json"
with open(filename, 'w') as f:
    json.dump(output, f, indent=4)
p_utils.plot_posteriors(
    [chain],
    [params],
    par_names=[["NAME_OF_PARAMETER", ...]],      
    samples_name=["model-name"],
    model_name="<model-name>", # this should be a string such that the plot file is named `<model-name>_posteriors.pdf`
    plots_dir="./output/<model-name>/",
    save=True,
    verbose=True,
    hpi_levels=[0.68, 0.95, 0.99],
    levels=[0.68, 0.95, 0.99],
)
```

The `chains_dir` ends in `np_model/` because PTArcade saves each run inside a
subfolder of `out_dir` named after the model's `name` attribute, which defaults
to `np_model` when the model file does not set one. If you set a custom `name`
in `ptarcade_model.py`, update this subfolder name to match.

For the name of the parameter in the plot, use a LaTeX string, while for the model-name in the plot, use a human-readable string.

The PTArcade plot file should produce a publication-quality posterior visualization for the free parameters and, if helpful, may also write a post-PTArcade best-fit spectrum figure using the same LaTeX styling conventions as the benchmark plot.

If the contributions of SMBHBs are included in the model, in the posterior plot, add at the end of the list of the parameters r"$A_{\rm SMBHB}$", r"$\gamma_{\rm SMBHB}$", which are the amplitude and slope of the SMBHB contribution. This allow to plot the posterior distribution of the SMBHB parameters.

If the user wants a plot of only the FOPT parameters, restrict the chains and params dict to only those parameters that are relevant for the FOPT model. For example
```python
plot_idx = [i for i, name in enumerate(param_names) if name in {"NAME_OF_PARAMETER_FOPT", ...}]
chain_FOPT = chain[:, plot_idx]
params_FOPT = {k: params[k] for k in param_names if k in {"NAME_OF_PARAMETER_FOPT", ...}}
```

## LaTeX Styling

When matplotlib is available, prefer LaTeX-styled axis labels, legends, and tick formatting for both benchmark and PTArcade plots. 

## Benchmark Spectrum Plot

The benchmark PTA plot should show only the actual NANOGrav violin bands together with the best-fit estimated point from the benchmark scan. Do not clutter this figure with unrelated posterior diagnostics.

## Post-PTArcade Spectrum Plot

After a successful PTArcade campaign, generate a second `h^2\Omega_{GW}(f)` versus `f` plot showing the actual NANOGrav violin bands together with the best-fit spectrum inferred from the PTArcade result.

Before plotting, verify that the actual PTArcade output directory exists and matches the configured `out_dir`. Do not interpret partial chains, incomplete posterior files or intermediate logs as final results.

## Runner

To run PTArcade:
```bash
conda run -n ptarcade ptarcade -m output/<model-name>/ptarcade_model.py -c output/<model-name>/ptarcade_config.py
```

To run the PTArcade plot:
```bash
conda run -n ptarcade python output/<model-name>/ptarcade_plot.py
```
