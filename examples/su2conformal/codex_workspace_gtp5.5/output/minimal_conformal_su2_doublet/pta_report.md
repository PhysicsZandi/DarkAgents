# PTA analysis for `minimal_conformal_su2_doublet`

## Template choice

Selected spectrum template: `dbf`, implemented through `backend/spectrum.py` via `output/minimal_conformal_su2_doublet/pta_spectrum.py`.

Reason: the PTA-steering FOPT region contains many strongly supercooled points with very large `alpha`. The local spectrum documentation states that the Higgsless template associated with arXiv:2209.04369 is validated only up to about `alpha = 0.5`, while the bulk-flow/dissipative-bulk-flow implementation associated with arXiv:2511.15687 is the documented option for very large `alpha`. The default is therefore DBF. Caveat: the FOPT backend does not compute wall velocity or microscopic efficiency, and the spectrum backend uses its default efficiency convention.

## Benchmark scan

The scan in `pta_scan.py` used only independent model parameters `gD` and `vD`. Each candidate point calls `fopt_model.evaluate_point(gD, vD)` directly, then evaluates the DBF spectrum at the 14 tabulated PTA violin frequencies in `backend/pta_violin_windows.csv`.

Best benchmark point:

- `spectrum_id`: `pta_00021`
- `gD = 0.95`
- `vD = 0.36043796 GeV`
- `Treh = 0.032372036 GeV`
- `alpha = 3.7326498e+08`
- `beta_H = 23.690379`
- `f_peak_est = 9.525809e-08 Hz`
- score: `13/14` bins inside the PTA violin windows

No 14/14 point was found in the direct-FOPT candidate/refinement scan. The benchmark plot is `pta_benchmark_spectrum.pdf`.

## PTArcade campaign

PTArcade was run with `N_samples = 100000` using priors on model parameters only:

- `gD ~ Uniform(0.45, 1.55)`
- `log10_vD ~ Uniform(-3.2, 0.7)`, with `vD = 10**log10_vD GeV`

A smoke test succeeded. The first final run had the MAP at the upper `log10_vD` prior boundary and was archived to `chains_prior_boundary_log10vD_upper`; the accepted final result is the widened-prior rerun in `chains/`.

Final PTArcade status: `ok`.

Bayes estimates:

- `gD = 0.88360545 +/- 0.035349102`
- `log10_vD = -0.053908401 +/- 0.17159915`

MAP estimate:

- `gD = 0.86317549`
- `log10_vD = 0.044548407`
- `vD = 1.1080221 GeV`
- MAP FOPT diagnostics: `Treh = 0.097822163 GeV`, `alpha = 2.1440419e+14`, `beta_H = 13.979819`, `f_peak_est = 1.7539608e-07 Hz`

`f_peak_est` is a steering estimate rather than the fitted spectrum peak; the PTArcade likelihood used the direct DBF spectrum computed from FOPT parameters at every sampled point.

## Outputs

- `pta_benchmark_scan.csv`
- `pta_benchmark_spectrum.pdf`
- `ptarcade_model.py`
- `ptarcade_config.py`
- `ptarcade_plot.py`
- `ptarcade_bayes.json`
- `pta_posteriors.pdf`
- `pta_ptarcade_spectrum.pdf`
- `handoff_pta.json`
