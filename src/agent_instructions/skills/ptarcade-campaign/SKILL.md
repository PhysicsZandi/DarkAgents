---
name: ptarcade-campaign
description: Choose model-parameter priors, prepare and run a PTArcade inference campaign from PTA benchmark priors, and plot the posteriors and best-fit spectrum.
---

# PTArcade Campaign Skill

## Overview

Use this skill to prepare and run a PTArcade inference campaign to obtain the Bayesian posteriors on the model parameters. 

## Task Workflow

1. Propose PTArcade priors on model parameters only, not on derived FOPT quantities such as `alpha`, `beta_H`, transition temperature, peak frequency, or peak amplitude. The priors must cover the viable PTA benchmark region and be much broader than the successful benchmark scan ranges, with enough width to keep the whole benchmark-compatible region away from the prior edges. This means that the priors must be at least two orders of magnitude wider in both directions than the benchmark scan ranges if the parameters span several orders of magnitude, and at least twice wider if the parameters span a small range. Anchor the prior center on the scale set by the FOPT `f_peak_est` and the benchmark scan, not on literature benchmarks tuned to other frequency bands.
2. Write the PTArcade model and config under `output/<model-name>/`, following the documentation in `docs/PTARCADE.md`. In the model file, you should provide the prior distributions and the implementation of the functions that from the model parameters compute the FOPT parameters and the gravitational-wave spectrum. In the config file, you should set the MCMC parameters, including at least `N_samples = int(1e5)`. It is better to run a shorter smoke test first with `N_samples = int(100)` to check that the model and config are correct and that the campaign can start, but do not interpret the results of the smoke test as final inference. 
3. Using the documented `ptarcade` conda environment that the orchestrator provides, run the campaign and preserve logs under `output/<model-name>/logs/`. This step can take time, so monitor the logs and wait until the process exits or clearly fails before interpreting outputs.
4. After the PTArcade process exits, validate logs and chain outputs. Write the plot file, following the documentation in `docs/PTARCADE.md`. Run the plot file inside the `ptarcade` environment to generate the posterior plot PDF. If the posterior distributions are flat, check that the model file is correctly implemented and that the MCMC parameters are correctly set. If the MAP point lies on a prior boundary or the marginalised posterior does not fall off towards zero near the prior edges or the 3σ contours touches the prior edges, enlarge the priors and rerun the campaign before interpreting results, repeating this enlarge-and-rerun loop until the posterior peak and its fall-off are well inside the priors and not on their edges. 
5. Plot the MAP-point spectrum with the PTA violins from the PTArcade outputs and save it as `output/<model-name>/pta_ptarcade_spectrum.pdf` with the same style as the benchmark spectrum. As for the benchmark plot, copy the `load_violins` and `plot_violins` functions verbatim from `backend/plot_violins.py` into the plot file to draw the violins, and overlay the MAP spectrum vs frequency curve in the same `\log_{10}(f)`–`\log_{10}(h^2\Omega_{GW})` coordinates so the curve and the violins share the same log scale.

## Rules


- Use only independent free model parameters. Do not scan dependent parameters but compute them from their defining relations. 
- Do not set priors on derived FOPT quantities such as `alpha`, `beta_H`, transition temperature, peak frequency, or peak amplitude.
- Do not implement, use or rely on cache system or interpolation. Each sampled model-parameter point must be evaluated by calling the actual model, FOPT and spectrum functions directly. 
- Use the whole free model parameter space, including vevs and couplings. Do NOT restrict the scan to a subspace of the model parameters by setting free parameters to fixed values.
- Do not invent or fabricate results. You must only set up the code, run it and read the outputs.
- Always choose logarithmic steps if the parameters span several orders of magnitude, and linear steps if the parameters span a small range. As a rule of thumbs, vevs are usually scanned in log space, while dimensionless couplings are usually scanned in linear space. It is always better to start with a broader prior and narrow it down than to start with a narrow one and risk cutting the posterior.
- For the MCMC in the PTArcade config, choose at least `N_sample = int(1e5)` unless the documented PTArcade workflow requires a different field name. If a shorter smoke test is run first, label it as a smoke test and do not interpret it as the final inference. 
- The spectrum vs frequency plot should show `\log_{10}(h^2\Omega_{GW}(f))` versus `\log_{10}(f/\mathrm{Hz})` with only the actual NANOGrav violin bands coming from the backend and the best-fit estimated point overlaid, using LaTeX-styled axes, labels, and legend text where supported, and with a slightly expanded frequency domain around the violin support, for example `\log_{10}(f/\mathrm{Hz}) \in [-9,-7]`. Draw the violins by copying the `load_violins` and `plot_violins` functions from `backend/plot_violins.py` directly into the plot file, and overlay the spectrum curve in the same `\log_{10}(f)`–`\log_{10}(h^2\Omega_{GW})` coordinates so they share the same log scale.
- Keep the spectrum plot axes linear. `plot_violins` already places the violins at pre-`\log_{10}` positions, so do not call `set_xscale("log")` or `set_yscale("log")`, otherwise the violins fall outside the plotted range and are not drawn. Apply `np.log10` to the spectrum data instead and keep the axes linear in `\log_{10}(f)`–`\log_{10}(h^2\Omega_{GW})`.
- The posterior plot should use the existing PTArcade posterior plot template in `docs/PTARCADE.md`, but with correct LaTeX-compatible parameter names, readable axis labels on any log-scaled axes, and a clean publication-style layout.
- Typical source of errors are identified by the fact the posterior distributions are flat, so check that the PTArcade model file is correctly implemented.

For the `fopt-pta` branch, keep in mind that the target signal is gravitational waves from a first-order phase transition in the PTA frequency range. All other frequency ranges will give different benchmark points that are not relevant. A rule of thumb is that the vev and then the transition temperature should be around MeV-GeV scale to give a signal in the PTA range, but this depends on the details of the model and the phase transition. 