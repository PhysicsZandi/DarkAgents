# PTA Analysis Report: u1conformal

Date: 2026-06-10

## Inputs and Scope

This PTA stage used the validated `u1conformal` FOPT upstream outputs:

- `output/u1conformal/handoff_model.json`
- `output/u1conformal/handoff_critique.json`
- `output/u1conformal/handoff_librarian_preliminary.json`
- `output/u1conformal/handoff_fopt.json`
- `output/u1conformal/fopt_model.py`
- `output/u1conformal/fopt_benchmarks.csv`

Only the independent model parameters `v` and `g_D` were scanned or assigned
PTArcade priors. Derived quantities such as `alpha`, `beta_H`, `Tn`, `Tp`,
`Treh`, and peak-frequency diagnostics were recomputed for each sampled model
point by calling `output/u1conformal/fopt_model.py`.

## Spectrum Template

The benchmark FOPT points in the PTA band are strongly supercooled, with very
large `alpha` and best-scoring `beta/H` values around 17-32. I selected the
implemented `bf` template from the bulk-flow family associated with
arXiv:2511.15687. The `higgsless` sound-wave template from arXiv:2209.04369 and
the `dbf` template were checked in the scan, but `bf` is the selected template.

Validity caveat: this is a closest implemented template choice. The model stage
does not compute microscopic wall friction, runaway conditions, or the precise
bulk-flow versus dissipative-bulk-flow partition, so the template validity is
recorded as `warning`.

## Benchmark Scan

Generated files:

- `output/u1conformal/pta_spectrum.py`
- `output/u1conformal/pta_scan.py`
- `output/u1conformal/pta_benchmark_scan.csv`
- `output/u1conformal/pta_benchmark_scan_meta.json`
- `output/u1conformal/pta_benchmark_spectrum.pdf`

Scan summary:

- Direct FOPT model points evaluated: 343
- CSV rows including template comparisons: 1038
- Selected template: `bf`
- Boundary expansions: none needed
- Best selected points reached 14/14 violin bins

Top benchmark points:

| rank | v [GeV] | g_D | alpha | beta/H | Treh [GeV] | bins |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.511087 | 0.600000 | 2.101e6 | 29.377 | 0.045705 | 14/14 |
| 2 | 1.798453 | 0.540000 | 2.094e11 | 17.097 | 0.152685 | 14/14 |
| 3 | 0.983417 | 0.617143 | 4.254e5 | 31.718 | 0.090264 | 14/14 |
| 4 | 0.756904 | 0.531429 | 9.385e11 | 16.839 | 0.070596 | 14/14 |

## PTArcade Campaign

Generated files:

- `output/u1conformal/ptarcade_model.py`
- `output/u1conformal/ptarcade_config.py`
- `output/u1conformal/ptarcade_plot.py`
- `output/u1conformal/logs/ptarcade_smoke.log`
- `output/u1conformal/logs/ptarcade_final.log`
- `output/u1conformal/chains/np_model/chain_0/chain_1.txt`
- `output/u1conformal/pta_posteriors.pdf`
- `output/u1conformal/pta_ptarcade_spectrum.pdf`
- `output/u1conformal/ptarcade_bayes.json`

The smoke test with `N_samples = 100` completed. The full campaign used
`N_samples = 100000` and completed in 1169.15 seconds with acceptance rate
0.45414. The chain import and plotting completed after correcting the LaTeX
parameter labels used by the PTArcade plotting helper.

Priors:

- `v`: log-uniform via `log10_v ~ Uniform(log10(0.003), log10(5.0))`
- `g_D`: `Uniform(0.42, 1.05)`

Posterior summary from `output/u1conformal/ptarcade_bayes.json`:

- Bayes estimate: `log10_v = -0.0451 +/- 0.2263`, `g_D = 0.5488 +/- 0.0266`
- MAP estimate: `v = 1.33875 GeV`, `g_D = 0.535734`
- 68% interval: `v = [0.5364, 1.4745] GeV`, `g_D = [0.5231, 0.5739]`
- 95% interval: `v = [0.2501, 1.8628] GeV`, `g_D = [0.5088, 0.6135]`
- 99.7% interval: `v = [0.0992, 2.4878] GeV`, `g_D = [0.5058, 0.6599]`

## Status

`handoff_pta.json` is schema-populated and marked `warning`: the benchmark scan
and PTArcade campaign completed, but template validity and convergence remain
caveated. No constraint, prior-audit, or report agent was invoked.
