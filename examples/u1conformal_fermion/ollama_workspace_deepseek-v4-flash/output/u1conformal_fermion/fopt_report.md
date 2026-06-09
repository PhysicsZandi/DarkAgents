# FOPT Analysis Report: Conformal U(1)_D Dark Sector

## Model

Classically scale-invariant U(1)_D dark sector with:
- Complex scalar Phi (charge +1) -- dark Higgs
- Dark gauge boson A'_mu
- Two Dirac fermions psi_1 (charge +1/2), psi_2 (charge -1/2) with Yukawa y_psi Phi psi_1_bar psi_2 + h.c.
- Tree-level potential: V_tree = lambda_Phi chi^4/4 (conformal, no mass term)
- CW condition: beta_lambda = (3 g_D^4 - 2 y_psi^4)/(8 pi^2) > 0

## Backend

**SemiAnalyticPipeline** from `backend/semianalytic_pipeline.py`.

This backend is designed for classically scale-invariant single-field models. It uses the high-temperature expansion of the finite-temperature effective potential (valid in the supercooling regime) and a Gaussian approximation for the false vacuum fraction to compute FOPT observables analytically.

## Scan Strategy

Five scans were performed with a coarse-to-fine strategy:

| Scan | g_D range | y_psi range | v range (GeV) | Grid | Points |
|------|-----------|-------------|---------------|------|--------|
| 1. Initial broad | [0.3, 1.5] | [0.05, 0.5] | [0.01, 10] | 8x6x10 | 480 |
| 2. Refined lower vev | [0.4, 1.2] | [0.05, 0.4] | [0.01, 1] | 10x8x12 | 960 |
| 3. Extended higher g_D | [0.3, 2.0] | [0.01, 0.6] | [0.001, 1] | 12x10x12 | 1440 |
| 4. Low vev for PTA | [0.3, 2.0] | [0.01, 0.6] | [0.0001, 0.1] | 12x10x10 | 1200 |
| 5. High vev | [0.3, 2.0] | [0.01, 0.6] | [1, 100] | 8x6x8 | 384 |
| **Total** | | | | | **4464** |

## Results Summary

| Category | Count | Percentage |
|----------|-------|------------|
| Total points | 4464 | 100% |
| Viable | 2247 | 50.3% |
| Numerical failures | 1822 | 40.8% |
| Physical failures | 395 | 8.8% |
| In PTA band (10^-9 - 10^-7 Hz) | 871 | 19.5% |

## Viable Parameter Space

The viable region spans:
- **g_D**: 0.3 - 2.0 (strongest transitions at g_D ~ 0.5-0.8)
- **y_psi**: 0.01 - 0.6 (constrained by CW condition y_psi < 1.11 g_D and supercooling condition g_D > y_psi/sqrt(2))
- **v**: 0.1 MeV - 100 GeV

## PTA-Band Points

871 viable points have estimated peak frequencies in the PTA band (10^-9 - 10^-7 Hz).

### Top 5 PTA-band points (closest to PTA center ~ 10^-8 Hz)

| # | g_D | y_psi | v (GeV) | alpha | beta/H | Tp (GeV) | Treh (GeV) | f_peak_est (Hz) |
|---|-----|-------|---------|-------|--------|----------|------------|-----------------|
| 1 | 0.6429 | 0.2300 | 0.0215 | 2.87e+04 | 42.4 | 1.52e-04 | 1.98e-03 | 1.00e-08 |
| 2 | 0.7636 | 0.4033 | 0.0100 | 8.84e+01 | 78.8 | 3.38e-04 | 1.04e-03 | 1.00e-08 |
| 3 | 0.7636 | 0.5344 | 0.0123 | 4.91e+02 | 65.2 | 2.66e-04 | 1.25e-03 | 9.94e-09 |
| 4 | 0.7556 | 0.3500 | 0.0100 | 7.49e+01 | 79.6 | 3.50e-04 | 1.03e-03 | 1.01e-08 |
| 5 | 0.9182 | 0.6000 | 0.0035 | 5.65e+00 | 180.4 | 2.80e-04 | 4.50e-04 | 9.90e-09 |

### Strongest transitions (by alpha)

| # | g_D | y_psi | v (GeV) | alpha | beta/H | f_peak_est (Hz) |
|---|-----|-------|---------|-------|--------|-----------------|
| 1 | 0.4545 | 0.2722 | 1.00e-04 | 9.66e+24 | 9.40 | 7.24e-12 |
| 2 | 0.4545 | 0.1411 | 1.00e-04 | 1.76e+19 | 12.6 | 9.94e-12 |
| 3 | 0.4545 | 0.0100 | 4.64e-04 | 7.09e+18 | 12.4 | 4.52e-11 |

## Physical Guards Applied

1. **CW condition**: beta_lambda = (3 g_D^4 - 2 y_psi^4)/(8 pi^2) > 0 => y_psi < (3/2)^(1/4) g_D ~ 1.11 g_D
2. **Supercooling condition**: g_D > y_psi / sqrt(2) (ensures m_A' > m_psi for FOPT viability, per Feng-Zhang 2602.14866)
3. **Perturbativity**: g_D < 4 pi, y_psi < 4 pi
4. **Eternal inflation**: Points where get_check_eternal_inflation() returns True are excluded
5. **Finite positive observables**: alpha > 0, beta/H > 0, Tp > 0, Treh > 0, Tn > 0

## Failure Diagnostics

### Numerical failures (1822 points, 40.8%)
- Primarily occur at high g_D (> 1.5) where the bounce action computation encounters numerical issues
- The backend's `get_S3` method returns NaN when the thermal barrier is too weak or the potential coefficients produce invalid configurations
- RuntimeWarning for divide-by-zero in log at extreme parameter values (caught and recorded as numerical failures)

### Physical failures (395 points, 8.8%)
- CW condition violation: y_psi too large relative to g_D
- Supercooling condition violation: g_D <= y_psi / sqrt(2)

## Key Observations

1. **PTA-favored parameter space**: g_D ~ 0.6-0.9, y_psi ~ 0.2-0.6, v ~ 3-20 MeV produces f_peak_est ~ 10^-8 Hz, right in the PTA band.

2. **Supercooling strength**: alpha ranges from O(1) to O(10^25), with the strongest supercooling at low g_D (~0.45) and low vev (~0.1 MeV). These extremely supercooled points have f_peak_est below the PTA band.

3. **Transition speed**: beta/H ranges from ~9 (very slow, strongly supercooled) to ~360 (fast, weakly supercooled). PTA-band points have beta/H ~ 30-180.

4. **Temperature scales**: Tp ranges from ~10^-5 GeV to ~10^-1 GeV for viable points. PTA-band points have Tp ~ 10^-4 - 10^-3 GeV (0.1-1 MeV).

5. **Consistency with literature**: The Balan et al. (2502.19478) benchmark (g=0.677, y=0.224, v=173 MeV) gives alpha=4700, beta/H=33.7, Tp=2.28 MeV. Our model with the same parameters (but different CW condition due to two Dirac fermions and gb_scalar=0) gives alpha=3145, beta/H=47, Tp=2.1 MeV -- qualitatively similar but with quantitative differences due to the different CW condition.

## Caveats

1. The backend neglects scalar loop contributions (gb_scalar = 0), which may affect the CW condition and the strength of the phase transition.
2. No RG running of couplings is included; the renormalisation scale is fixed to the vev.
3. No Daisy resummation is included, which may affect the thermal potential at high temperatures.
4. f_peak_est is a template-independent order-of-magnitude estimate. The true spectral peak depends on the GW template (sound waves, bubble collisions, turbulence) used by the pta-agent.
5. The high-temperature expansion is valid in the supercooling regime, but may become less accurate for very weak transitions (alpha ~ O(1)).
