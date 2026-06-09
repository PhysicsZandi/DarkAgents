# PTA Analysis Report — u1conformal (classically scale-invariant dark U(1)_D)

## 1. Spectrum template selection

**Selected template: dissipative bulk flow (`dbf`), Lewicki et al. 2511.15687.**

The FOPT (from `handoff_fopt.json`) is in the **strong supercooling** regime: the
transition strength spans `alpha ~ 2` (at `g_D ~ 0.9`) up to `alpha ~ 1e16`
(at low `g_D`), with `beta/H ~ 12-160`. In this regime the latent heat is
vacuum-dominated, the bubble walls accelerate to large Lorentz factors, and the
released energy is carried by thin, free-streaming shells around the bubbles
("bulk flow") rather than by a long-lived acoustic fluid.

- The **higgsless** sound-wave template (2209.04369) is calibrated on
  hydrodynamic simulations for moderate `alpha <~ O(1)` where the plasma carries
  the energy. It is **outside its validity domain** here and was **not** used
  for scoring.
- Between **bf** and **dbf**: the pure bulk-flow (bf) limit assumes collisionless
  free runaway; the dissipative bulk flow (dbf) includes dissipation of the
  shells in the (dark) plasma, which is present in this thermal dark sector.
  **dbf** is therefore the physically representative choice; bf is retained only
  as a comparison.

Implementation: `output/u1conformal/pta_spectrum.py` (calls the deterministic
`backend/spectrum.py` `Spectrum(template="dbf")`).

**Caveats:** order-of-magnitude gauge dependence of the CW+thermal potential
(1707.06765) propagates into `alpha, beta_H, Treh`; `ksw=1` (justified in the
vacuum-dominated limit `K=alpha/(1+alpha)->1`).

## 2. Benchmark scan

Code: `pta_scan.py`; results: `pta_benchmark_scan.csv`. For every `(v, g_D)` the
actual FOPT backend computes `alpha, beta_H, Treh`, then the dbf spectrum is
evaluated at the 14 violin-bin frequencies and scored against
`backend/pta_violin_windows.csv`.

- Coarse + fine grids over `v in [1 MeV, 50 GeV]` (log) and `g_D in [0.48, 0.90]`
  (linear): 1271 viable scored points.
- An initial `v in [1 MeV, 2 GeV]` grid put the best points on the `v = 2 GeV`
  upper edge, so the range was **expanded to 50 GeV** (boundary expansion
  recorded in the handoff). The 14/14 window then closed **interior**:
  **`v in [0.35, 2.4] GeV`, `g_D in [0.51, 0.63]`** (101 points at 14/14).

Four maximally-diverse 14/14 benchmarks (in `log10 v`–`g_D` space) are plotted in
`pta_benchmark_spectrum.pdf`:

| v [MeV] | g_D | alpha | beta/H | score |
|--------:|----:|------:|-------:|------:|
| 748 | 0.560 | 1.2e9 | 21.4 | 14/14 |
| 2386 | 0.510 | 3.5e15 | 12.4 | 14/14 |
| 508 | 0.630 | 8.3e4 | 35.8 | 14/14 |
| 345 | 0.540 | 6.1e10 | 19.0 | 14/14 |

## 3. PTArcade campaign (NANOGrav 15yr)

Priors on **independent model parameters only** (model `ptarcade_model.py`,
config `ptarcade_config.py`):

- `log10_v` ~ Uniform(log10 1e-3, log10 50)  [GeV]  (log prior, spans orders)
- `g_D` ~ Uniform(0.45, 0.90)  (linear prior)

These are far wider than the 14/14 benchmark window (`v in [0.35,2.4] GeV`,
`g_D in [0.51,0.63]`): >2 orders of magnitude on each side in `v`, > 2x in `g_D`.
A smoke test (`N_samples=100`) validated the pipeline; the final campaign used
`N_samples = 1e5`, `mode=ceffyl`, `NG15`, completing in 2018 s at acceptance 0.385.

### Posterior results (`ptarcade_bayes.json`, `u1conformal_posteriors.pdf`)

| quantity | log10_v | v [GeV] | g_D |
|----------|--------:|--------:|----:|
| Bayes mean | -0.060 | 0.87 | 0.527 |
| MAP | +0.038 | 1.09 | 0.528 |
| 1σ (68%) | [-0.214, +0.091] | [0.61, 1.23] | [0.508, 0.546] |
| 2σ (95%) | [-0.476, +0.165] | [0.33, 1.46] | [0.504, 0.587] |
| 3σ (99.7%) | [-0.820, +0.215] | [0.15, 1.64] | [0.503, 0.636] |

The posterior peaks well inside the priors and falls off before the prior edges
(g_D 3σ lower 0.503 vs prior edge 0.45; log10_v 3σ in [-0.82, 0.22] vs prior
[-3, 1.70]); no boundary contact, so no prior enlargement was needed.

The MAP point (`v=1.09 GeV, g_D=0.528`) is a viable FOPT with
`alpha=3.6e12, beta/H=15.9, Treh=0.101 GeV`, peak `h^2 Omega_GW ~ 5.4e-9` at
`f ~ 2.3e-8 Hz`, and scores **14/14** in-violin bins. Its spectrum vs the
NANOGrav violins is shown in `pta_ptarcade_spectrum.pdf`.

## 4. Files

- `pta_spectrum.py`, `pta_scan.py`, `pta_benchmark_plot.py`
- `pta_benchmark_scan.csv`, `pta_benchmark_spectrum.pdf`
- `ptarcade_model.py`, `ptarcade_config.py`, `ptarcade_config_smoke.py`, `ptarcade_plot.py`
- `chains/np_model/` (1e5-sample chain), `ptarcade_bayes.json`
- `u1conformal_posteriors.pdf`, `pta_ptarcade_spectrum_plot.py`, `pta_ptarcade_spectrum.pdf`
- `handoff_pta.json`, logs in `logs/`
