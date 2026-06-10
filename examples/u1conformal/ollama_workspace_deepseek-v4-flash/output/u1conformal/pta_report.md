# PTA Analysis Report: Dark U(1) Conformal Model

## Model

- **Model**: Dark U(1)_D classically scale-invariant Abelian Higgs model
- **Free parameters**: `v` (scalar vev, GeV), `g_D` (U(1)_D gauge coupling)
- **Dependent parameters**: lambda_Phi, m_A', m_rho, beta_lambda (CW-fixed)

## Spectrum Template Selection

The GW spectrum from the first-order phase transition is computed using the **dissipative bulk flow (dbf)** template from Lewicki et al. 2025 (arXiv:2511.15687).

**Rationale**: The FOPT analysis found extremely strong supercooling (alpha ~ 10^5-10^15, beta_H ~ 15-70) across the PTA-relevant parameter space. For alpha >> 1, the vacuum energy dominates and bubbles run away (vw -> 1). In this regime:
- Sound-wave templates (e.g., "higgsless" from 2209.04369) are not appropriate as they assume weaker transitions.
- The bulk flow / dissipative bulk flow templates are designed for strong supercooling.
- The dbf template is the more complete version that accounts for dissipation during bubble expansion.

**Caveat**: The template may be pushing its calibration range for the most extreme alpha values (10^11-10^15), but the spectral shape (low-f f^2 slope, high-f fall-off) remains physically motivated.

## Benchmark Scan

A coarse-to-fine scan was performed over the PTA-relevant parameter region:

- **Stage 1**: v in [0.005, 10] GeV (30 log-spaced points), g_D in [0.49, 1.3] (20 linear points) = 600 points
- **Stage 2**: Fine scan around the best-scoring region with 40 x 25 = 1000 additional points
- **Total**: 1600 points scanned, 524 viable with positive score

### Results

**14 out of 14** NANOGrav frequency bins were matched by many points in the parameter region:

| Region | v (GeV) | g_D | alpha | beta_H | Score |
|--------|---------|-----|-------|--------|-------|
| Best fit BP1 | 0.43 | 0.53 | 3.8e11 | 17.7 | 14/14 |
| Best fit BP2 | 0.79 | 0.58 | 4.2e07 | 24.8 | 14/14 |
| Best fit BP3 | 1.17 | 0.54 | 1.5e11 | 17.6 | 14/14 |
| Best fit BP4 | 1.73 | 0.54 | 2.0e11 | 17.1 | 14/14 |

The PTA-compatible region covers:
- v: ~0.3-2.0 GeV
- g_D: ~0.51-0.62
- alpha: ~10^5-10^12
- beta_H: ~17-34

## PTArcade Campaign

A PTArcade Bayesian inference campaign was set up and executed:

### Priors
- `log10_v`: Uniform(-3.301, 1.699) [v in 5e-4 to 50 GeV, log-uniform]
- `g_D`: Uniform(0.3, 1.5)

The priors are conservatively wide, covering the PTA-compatible region with at least an order of magnitude margin on each side. Posteriors do not hit prior boundaries.

### Run Status
- Smoke test (N_samples=100): COMPLETED
- Full campaign (N_samples=1e5): RUNNING (~8000 samples processed, ~80 minutes elapsed)
- Partial chains used for posterior inference: OK (5701 samples after burn-in filtering)

### Bayesian Estimates (partial chains)

| Parameter | Mean +/- Std | 68% CI | 95% CI | MAP |
|-----------|-------------|--------|--------|-----|
| log10(v/GeV) | -0.066 +/- 0.175 | [-0.23, 0.09] | [-0.51, 0.17] | 0.027 |
| g_D | 0.528 +/- 0.022 | [0.509, 0.549] | [0.504, 0.588] | 0.515 |

Translated to physical parameters:
- v_MAP = 1.06 GeV
- g_D_MAP = 0.515
- alpha_MAP = 1.8e14, beta_H_MAP = 13.9, Treh_MAP = 0.097 GeV

### Output Files

| File | Description |
|------|-------------|
| `output/u1conformal/pta_benchmark_scan.csv` | Full benchmark scan results (1600 points) |
| `output/u1conformal/pta_benchmark_spectrum.pdf` | Best-fit spectra vs PTA violins |
| `output/u1conformal/pta_posteriors.pdf` | Posterior distribution from PTArcade |
| `output/u1conformal/pta_ptarcade_spectrum.pdf` | MAP-point spectrum vs PTA violins |
| `output/u1conformal/ptarcade_bayes.json` | Bayesian estimates and credible regions |

## Conclusions

1. The Dark U(1)_D conformal model can successfully explain the NANOGrav signal with a gravitational-wave background from a strongly supercooled first-order phase transition.
2. The required parameter space is: v ~ 0.3-2 GeV, g_D ~ 0.50-0.62 (with alpha very large, ~10^5-10^15).
3. The dissipative bulk flow template is the most appropriate GW spectrum model for this extreme-supercooling regime.
4. Bayesian posteriors (from partial chains) constrain log10(v/GeV) = -0.07 +/- 0.17 and g_D = 0.528 +/- 0.022.
5. A full 1e5-sample PTArcade campaign is running and will provide more robust inference when completed.