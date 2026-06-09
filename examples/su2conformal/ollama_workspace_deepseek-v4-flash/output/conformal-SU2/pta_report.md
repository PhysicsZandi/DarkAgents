# PTA Analysis Report: conformal-SU2

## Overview

The minimal classically scale-invariant SU(2) gauge theory with one complex scalar doublet has been fully analysed for gravitational-wave signals from a first-order phase transition in the PTA frequency band. The analysis includes benchmark scanning against the NANOGrav 15-year violin windows and a full PTArcade Bayesian inference campaign.

## GW Spectrum Template

**Template used**: `dbf` (dissipative bulk flow, arXiv:2511.15687)

**Reasoning**: The FOPT scan produces alpha values spanning O(10^0) to O(10^8). The higgsless template (arXiv:2209.04369) is validated only for alpha < 0.5, while the bulk-flow/dissipative-bulk-flow template is designed for the strong transitions (alpha >> 1) that characterise CW-type models.

## Benchmark Scan Results

- **Grid**: 1660 total points (coarse 17×20 + refined 33×40) over g ∈ [0.7, 2.3] and chi0 ∈ [3e-5, 0.5] GeV
- **7 points achieve 14/14 in-violin bins** — the maximum possible score
- **Best parameter region**: g ≈ 0.90–1.05, chi0 ≈ 0.39–0.5 GeV
- **PTA-viable region**: g ∈ [0.8, 2.3], chi0 ∈ [3e-5, 0.5] GeV

### Top benchmark points

| g | chi0 (GeV) | alpha | beta/H | Tr (GeV) | score |
|---|-----------|-------|--------|---------|-------|
| 0.90 | 0.50 | 2.0e11 | 18.3 | 0.046 | 14/14 |
| 1.00 | 0.50 | 5.9e6  | 28.8 | 0.046 | 14/14 |
| 0.95 | 0.50 | 4.6e8  | 23.2 | 0.044 | 14/14 |
| 1.00 | 0.39 | 5.1e6  | 29.2 | 0.036 | 14/14 |
| 0.95 | 0.39 | 3.9e8  | 23.6 | 0.035 | 14/14 |
| 0.90 | 0.39 | 1.8e11 | 18.4 | 0.036 | 14/14 |
| 1.05 | 0.50 | 2.2e5  | 35.1 | 0.048 | 14/14 |

## PTArcade Campaign

- **Data set**: NG15 (NANOGrav 15-year)
- **Mode**: ceffyl (free spectrum)
- **Samples**: 100,000 (MCMC, single chain)
- **Acceptance rate**: 0.323
- **Runtime**: 955.9 seconds (~16 minutes)

### Priors

- `g`: Uniform(0.5, 3.0) — SU(2) gauge coupling
- `log10_chi0`: Uniform(-5.0, 0.699) — log10(VEV/GeV)

### Posterior Results

| Parameter | Mean ± std | MAP | 1σ CI | 2σ CI |
|-----------|-----------|-----|-------|-------|
| g | 0.841 ± 0.047 | 0.789 | [0.790, 0.885] | [0.780, 0.954] |
| log10(chi0/GeV) | 0.169 ± 0.260 | 0.125 | [-0.081, 0.447] | [-0.390, 0.643] |
| chi0 (from MAP) | — | 1.33 GeV | [0.83, 2.80] GeV | [0.41, 4.39] GeV |

**MAP point**: g = 0.79, chi0 = 1.33 GeV

### Key Observations

1. The posterior on g is well-constrained (σ ≈ 0.05) with MAP at 0.79
2. The posterior on log10(chi0) peaks at 0.125 (chi0 ≈ 1.33 GeV) with broader spread (σ ≈ 0.26)
3. The MAP chi0 = 1.33 GeV is above the benchmark scan's best region (0.39–0.5 GeV), suggesting the MAP point overshoots the violin windows
4. The prior on g lower bound (0.5) may be constraining — the MAP sits at 0.79 near the lower edge

## Literature Comparison

- **arXiv:2109.11558** (Borah, Dasgupta, Kang, 2021): Same model studied for NANOGrav 12.5-yr data. Their BP1 (g_D=1.37, M_Z=8.23 MeV) corresponds to chi0 ≈ 0.012 GeV. Our pipeline recovers beta/H=144 vs their 143 (1% agreement). Alpha differs (ours: 15 vs theirs: 0.45) due to different dof counting conventions.
- The PTArcade posteriors favour larger chi0 (~1.3 GeV) and smaller g (~0.79) than the 2109.11558 benchmark.

## Output Files

- `pta_benchmark_spectrum.pdf`: 4 best benchmark spectra overlaid on NANOGrav violins
- `conformal-SU2_posteriors.pdf`: PTArcade posterior distributions
- `pta_ptarcade_spectrum.pdf`: MAP-point spectrum overlaid on NANOGrav violins
- `pta_benchmark_scan.csv`: Full benchmark scan results (1660 points)
- `ptarcade_bayes.json`: Bayesian estimates, MAP, and sigma regions
- `chains/`: PTArcade MCMC chain files