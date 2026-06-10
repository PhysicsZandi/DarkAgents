# FOPT Report: u1conformal

## Backend

Selected backend: `backend/semianalytic_pipeline.py`.
Mapping: `chi0=v`, `boson_gbs={"Aprime": g_D}`, `boson_dofs={"Aprime": 3}`, no fermions, `xi=1`.

## Scan

Total evaluated points: 120
Viable FOPT points: 79
Failed/not-FOPT points: 40
Perturbativity/physical exclusions: 1

Scan notes:
- literature_seeded_coarse: evaluating 120 new points

The independent scan columns are exactly `v` [GeV] and `g_D`. `lambda_Phi`, `beta_lambda`, `m_Aprime`, and `m_rho` are dependent diagnostics and were not scanned.

## Best Points

| v [GeV] | g_D | alpha | beta/H | Tn [GeV] | Tp [GeV] | Treh [GeV] | f_peak_est [Hz] |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.016681 | 0.65 | 5222.5 | 48.7214 | 0.000255553 | 0.000202637 | 0.0017227 | 9.25603e-09 |
| 0.0278256 | 0.6 | 771184 | 34.4989 | 0.000130972 | 9.71254e-05 | 0.00287821 | 1.09555e-08 |
| 0.016681 | 0.677 | 795.361 | 57.4832 | 0.00039946 | 0.000325543 | 0.00172936 | 1.09629e-08 |
| 0.0774264 | 0.5 | 4.35543e+14 | 14.571 | 2.47535e-06 | 1.49963e-06 | 0.00685083 | 1.10178e-08 |
| 0.0278256 | 0.57 | 3.66474e+07 | 28.0723 | 5.05795e-05 | 3.60605e-05 | 0.00280571 | 8.69009e-09 |

## Caveats

- `f_peak_est` uses the template-independent estimate `1.6e-5 Hz * (beta/H) * (Treh/100 GeV) * (g_*/100)^(1/6)` and is only an order-of-magnitude PTA scale anchor.
- The semi-analytic backend omits portal and kinetic-mixing effects in the thermal potential, as requested by the upstream critic handoff.
- `lambda_Phi` is Coleman-Weinberg/backend-fixed but not exported numerically by the backend; it is recorded as dependent and never scanned.
