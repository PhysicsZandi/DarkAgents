---
name: pta-analysis
description: Scan the model parameter space and find benchmark points that can visually match the PTA violins.
---

# PTA Analysis Skill

## Overview

Use this skill to perform a benchmark scan over the model parameter space, compute the gravitational-wave spectrum at the PTA frequencies, and find points that can visually match the PTA violins. This skill is used after the correct spectrum template has been selected.

## Task Workflow

1. Based on the model definition, the preliminary librarian and the FOPT report, identify the probable ranges of the independent free model parameters that can lead to a PTA-violin-matching spectrum. Use the `f_peak_est` field in the FOPT handoff to anchor the scan to the region whose redshifted peak falls in the PTA band, rather than seeding from literature benchmarks alone, since literature benchmarks are often tuned to other frequency bands (e.g. LISA or LIGO/Virgo) and would set the wrong scale. 
2. For each model-parameter point, compute the FOPT quantities (strength, characteristic timescale, transition temperature) through the model implementation, then compute the gravitational-wave spectrum at the PTA frequencies using the selected spectrum template and score it against `backend/pta_violin_windows.csv`. Use a single file called `output/<model-name>/pta_scan.py` and save results in `output/<model-name>/pta_benchmark_scan.csv`. For the first scan, use a coarse grid over a wide parameter range. Identify perfect candidates that score 14/14 in-violin bins. Also check whether the peak frequency and peak amplitude are close to the PTA range.
3. Refine the grid around the best-scoring points to find the region of the model parameter space that can visually match the PTA violins. If the best point lies on a scan boundary, expand the corresponding model-parameter range and rerun before accepting it. Do not let the refinement shrink the explored support to a narrow neighborhood around one point, keep the scan wide enough to show the surrounding PTA-compatible region. The idea is to find a sort of gradient of the score in the model parameter space.
4. Plot at most four of the best-scoring points that are also maximally different in independent model-parameter space against the PTA violins. To draw the violins, copy the `load_violins` and `plot_violins` functions verbatim from `backend/plot_violins.py` into your plot file and call them, do not reimplement the violin computation. On top of the violins, plot the gravitational-wave spectrum versus frequency for the selected points as smooth curves. Pay close attention to the log scale: `plot_violins` already places the violins in `\log_{10}(f/\mathrm{Hz})` versus `\log_{10}(h^2\Omega_{GW})` coordinates, so your spectrum curves must be plotted in the exact same coordinates (take `np.log10` of both the frequency and the spectrum, do not pass linear values onto the violin axes). Save the plot as `output/<model-name>/pta_benchmark_spectrum.pdf`. 

## Rules

- Choose logarithmic steps if the parameters span several orders of magnitude. Choose linear steps if the parameters span a small range. DO NOT choose exponential steps. Typically, vevs and mass parameters are scanned in logarithmic steps, while dimensionless couplings are scanned in linear steps.
- Do not treat a boundary-touching best-fit point as a final result, rerun with wider scan ranges first.
- Use only independent free model parameters. Do not scan dependent parameters but compute them from their defining relations. 
- Do not set priors on derived FOPT quantities such as `alpha`, `beta_H`, transition temperature, peak frequency, or peak amplitude.
- Do not implement, use or rely on cache system or interpolation. Each sampled model-parameter point must be evaluated by calling the actual model, FOPT and spectrum functions directly. 
- Do not extrapolate PTA violin windows beyond their tabulated range in `backend/pta_violin_windows.csv`.
- When multiple viable points achieve 14/14 in-violin bins, select up to four for plotting by determining the maximally different points in independent model-parameter space.
- Do not invent or fabricate results. You must only set up the code, run it and read the outputs.
- Do not edit upstream files. Only write code fiels and outputs inside `output/<model-name>/`.
- When selecting the spectrum template, pay attention to the range of validity of the FOPT parameters (strength, characteristic timescale, bubble wall velocity, etc...) and the assumptions behind each template. 
- The spectrum vs frequency plot should show `\log_{10}(h^2\Omega_{GW}(f))` versus `\log_{10}(f/\mathrm{Hz})` with only the actual NANOGrav violin bands coming from the backend and the best-fit estimated point overlaid, using LaTeX-styled axes, labels, and legend text where supported, and with a slightly expanded frequency domain around the violin support, for example `\log_{10}(f/\mathrm{Hz}) \in [-9,-7]`. Draw the violins by copying the `load_violins` and `plot_violins` functions from `backend/plot_violins.py` directly into the plot file, and overlay the spectrum curve in the same `\log_{10}(f)`–`\log_{10}(h^2\Omega_{GW})` coordinates so they share the same log scale.
- Do not plot the raw spectrum points as lines or dots against the raw `backend/pta_violin_windows.csv` rows. Copy the `load_violins` and `plot_violins` functions from `backend/plot_violins.py` directly into your plot file to draw the violins, and overlay the spectrum as a smooth curve in the same `\log_{10}(f)`–`\log_{10}(h^2\Omega_{GW})` coordinates used by those functions, so the curve and the violins share the same log scale.
- Keep the plot axes linear. `plot_violins` already places the violins at pre-`\log_{10}` positions, so do not call `set_xscale("log")` or `set_yscale("log")`, otherwise the violins fall outside the plotted range and are not drawn. Apply `np.log10` to the spectrum data instead and keep the axes linear in `\log_{10}(f)`–`\log_{10}(h^2\Omega_{GW})`.
- If no viable point can fit the PTA targets after reasonable refinement, report that no benchmark-compatible PTA region was found instead of fabricating anything.
- Try to start with a wide parameter range, which means that you can scan logarithmically and include at least two orders of magnitude above and below the scale anchored by the FOPT `f_peak_est`. Cross-check against the preliminary librarian suggestions, but only after verifying that they correspond to the PTA band, since literature benchmarks tuned to other frequency bands would set the wrong scale. If neither is available, use your best judgment to set a wide parameter range based on the model definition and the FOPT report.

For the `fopt-pta` branch, keep in mind that the target signal is gravitational waves from a first-order phase transition in the PTA frequency range. All other frequency ranges will give different benchmark points that are not relevant. A rule of thumb is that the vev and then the transition temperature should be around MeV-GeV scale to give a signal in the PTA range, but this depends on the details of the model and the phase transition. 