# FOPT Report: Dark U(1)_D Conformal Model

Generated: 2026-06-10

## Model

- **Model**: Dark U(1)_D with complex scalar Phi
- **Backend**: `semianalytic_pipeline`
- **Independent parameters**: v (vev in GeV), g_D (gauge coupling)
- **Dependent parameters**: lambda_Phi, m_rho, m_A', beta_lambda

## Scan Summary

| Metric | Value |
|--------|-------|
| Total points scanned | 925 |
| Viable points | 680 |
| Points in PTA band | 243 |
| Physical failures | 41 |
| Numerical failures | 204 |

## Scan Ranges

| Parameter | Min | Max | Units |
|-----------|-----|-----|-------|
| v | 1e-2 | 1e1 | GeV |
| g_D | 0.3 | 1.5 | 1 |

## Best Points in PTA Band

| v (GeV) | g_D | alpha | beta/H | Tn (GeV) | Tp (GeV) | Tr (GeV) | f_peak (Hz) |
|---------|-----|-------|--------|----------|----------|----------|-------------|
| 2.3714e-02 | 0.6000 | 7.3993e+05 | 34.80 | 1.1366e-04 | 8.4463e-05 | 2.4772e-03 | 1.0025e-08 |
| 1.3367e-02 | 0.6816 | 5.9587e+02 | 59.85 | 3.4694e-04 | 2.8464e-04 | 1.4069e-03 | 9.7861e-09 |
| 9.0202e-03 | 0.7289 | 6.1172e+01 | 83.65 | 4.1675e-04 | 3.5788e-04 | 1.0049e-03 | 9.7589e-09 |
| 1.9810e-02 | 0.6342 | 2.0489e+04 | 43.64 | 2.1981e-04 | 1.6992e-04 | 2.0330e-03 | 1.0317e-08 |
| 4.3506e-02 | 0.5395 | 1.0032e+10 | 21.50 | 2.0061e-05 | 1.3122e-05 | 4.1528e-03 | 1.0385e-08 |
| 6.0868e-03 | 0.7763 | 1.4859e+01 | 125.04 | 4.0765e-04 | 3.6608e-04 | 7.3053e-04 | 1.0588e-08 |
| 7.8486e-02 | 0.4921 | 7.1779e+15 | 13.38 | 1.2560e-06 | 7.4257e-07 | 6.8350e-03 | 1.0639e-08 |
| 2.4116e-02 | 0.5868 | 3.7150e+06 | 31.72 | 7.8522e-05 | 5.6896e-05 | 2.4979e-03 | 9.2167e-09 |
| 5.0000e-03 | 0.8237 | 5.9042e+00 | 145.78 | 4.4447e-04 | 4.0064e-04 | 6.4942e-04 | 1.0961e-08 |
| 2.9357e-02 | 0.5868 | 4.0693e+06 | 31.40 | 9.3243e-05 | 6.7475e-05 | 3.0306e-03 | 1.1069e-08 |

## Prior Ranges (for PTArcade)

- v: [5.0000e-03, 1.0000e+01] GeV (log-uniform)
- g_D: [0.4921, 1.3000] (uniform)

## Dependent Parameter Summary

| Param | Min | Max | Unit |
|-------|-----|-----|------|
| lambda_Phi | 5.5706e-04 | 2.7130e-02 | 1 |
| m_rho | 2.3602e-04 | 3.2942e+00 | GeV |
| m_A' | 2.4605e-03 | 1.3000e+01 | GeV |
| beta_lambda | 2.2282e-03 | 1.0852e-01 | 1 |

## Failure Analysis

- Physical failures: 41
- Numerical failures: 204

### Physical Failure Reasons

- 41x: eternal inflation occurs

## Approximations

1. High-temperature expansion (small phi/T) used for effective potential
2. Gaussian approximation for false vacuum fraction
3. Daisy resummation via Arnold-Espinosa scheme
4. CW-fixed scalar quartic (not scanned independently)
5. xi = Tdark/TSM = 1 (thermalised sectors)
6. f_peak_est uses fixed g* = 10 approximation for MeV-scale

## Literature Comparison

| Source | v (GeV) | g_D | alpha | beta/H | f_peak (Hz) |
|--------|---------|-----|-------|--------|-------------|
| 2501.11619 (best-fit) | 0.182 | 0.59 | 2.6e5 | 39.5 | ~nHz |
| 2502.19478 (coupled) | 0.0929 | 0.877 | 4.99 | 21.1 | ~nHz |
| 2501.15649 (BP1) | 0.5 | 0.75 | 342 | - | ~nHz |
| This scan | range | range | range | range | range |
