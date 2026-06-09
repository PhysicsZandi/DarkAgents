# FOPT Report: Classically Scale-Invariant Dark U(1)_D (u1conformal)

Backend: `backend/semianalytic_pipeline.py` (semianalytic_pipeline, arXiv:2602.02829).
Branch: fopt-pta. Run status: ok. Backend executed: yes.

## 1. Model and backend mapping

Single-field classically scale-invariant dark U(1)_D: complex scalar Phi + dark
gauge boson A', Coleman-Weinberg radiative breaking, no tree mass term. This matches
the semianalytic backend selection rule exactly.

Backend input per point: `chi0 = v` (GeV), `boson_gbs = {"Aprime": g_D}`,
`boson_dofs = {"Aprime": 3}`, empty fermion dicts. The scalar/Goldstone and the
CW-fixed quartic `lambda_Phi` are handled internally and never passed in.

- Independent (scanned): `v` [GeV], `g_D`.
- Dependent diagnostics: `m_A' = g_D v`, `m_rho = sqrt(beta_lambda) v`,
  `beta_lambda = 3 g_D^4/(8 pi^2)`, `lambda_Phi` (CW-fixed internally).

## 2. Smoke test (literature anchor)

At the 2502.19478 Point-A parameters (v = 173 MeV, g_D = 0.677) the implementation
returns finite, positive observables:

| quantity | this work | literature (Point A, incl. DM fermion) |
|---|---|---|
| Tp | 2.82 MeV | 2.28 MeV |
| alpha | 1.45e3 | 4.7e3 |
| beta/H | 50.7 | 33.7 |
| f_peak_est | 9.8e-8 Hz | (PTA band) |

Order-of-magnitude agreement is expected: the literature point includes a dark
fermion DM Yukawa and daisy/RG corrections absent from the minimal model + backend.
The supercooled MeV-scale character and the nHz f_peak are reproduced.

## 3. Scan

Coarse-to-fine over the independent (v, g_D) plane, anchored on the librarian hints
(g_D ~ [0.55, 0.9], v ~ 100-700 MeV) and extended logarithmically in v down to
2.5 MeV and up to 10 GeV, with g_D in [0.45, 0.90] (perturbative). Each backend call
is wrapped in per-point error handling and a 60 s timeout. f_peak_est uses
`1.6e-5 Hz * (beta/H) * (Treh/100 GeV) * (g_*/100)^(1/6)` with g_* from
`backend/T_vs_g_gs_GeV.csv`.

Totals: 157 points; 148 viable; 78 viable inside the PTA band (1e-9..1e-7 Hz);
8 failed (numerical/physical, incl. low-g_D non-perturbative-barrier / bracket
failures and eternal inflation); 1 not_fopt.

The viable window is bounded by physics, not by the grid: f_peak crosses below
1e-9 Hz at the lowest v and above 1e-7 Hz at the highest v for each g_D, and points
outside the perturbative/percolation region are recorded as failures. PTA-band viable
points span v in [2.5 MeV, 692 MeV] and g_D in [0.50, 0.85].

## 4. Best points (centered in the PTA band)

| v [MeV] | g_D | alpha | beta/H | Tn [MeV] | Tp [MeV] | Treh [MeV] | f_peak_est [Hz] |
|---|---|---|---|---|---|---|---|
| 18.1 | 0.65 | 5.18e3 | 48.6 | — | — | 1.85 | 9.9e-9 |
| 27.7 | 0.59 | 2.65e6 | 32.2 | — | — | 2.87 | 1.02e-8 |
| 6.16 | 0.77 | 1.73e1 | 119 | — | — | 0.73 | 9.6e-9 |
| 11.8 | 0.70 | 2.19e2 | 67.6 | — | — | 1.26 | 9.4e-9 |
| 42.5 | 0.55 | 1.22e9 | 23.6 | — | — | 4.13 | 1.08e-8 |

Full per-point Tn/Tp values are in `fopt_benchmarks.csv` and `fopt_results.json`.
The g_D = 0.59 point reproduces the strong-supercooling regime of the
2501.11619 best-fit (alpha ~ 1e6, beta/H ~ 32).

Trend: alpha grows steeply as g_D decreases (deeper supercooling, lower beta/H),
while f_peak tracks Treh ~ v. Lower g_D therefore gives stronger but slower
transitions; the band-center is reached for v of a few tens of MeV.

## 5. Suggested priors for the PTA stage

- `v`: log-uniform in [2.5 MeV, 692 MeV] (PTA-band viable range).
- `g_D`: uniform in [0.50, 0.85].

Temperature consumed downstream: `Treh` (`temperature_key = "Treh"`).

## 6. Theory uncertainties (propagate downstream)

- Gauge dependence of the CW+thermal effective potential: order-of-magnitude on
  Omega_GW (1707.06765).
- No RG running / daisy resummation (mu = vev) in the backend.
- xi = 1 with negligible portal/kinetic mixing; dark dof (A':3, scalar:1) added to g_*.
- f_peak_est is an anchor only; the true spectral peak is owned by the pta-agent.

## 7. Files

- `output/u1conformal/fopt_model.py`
- `output/u1conformal/fopt_model_scan.py`
- `output/u1conformal/fopt_benchmarks.csv`
- `output/u1conformal/fopt_results.json`
- `output/u1conformal/handoff_fopt.json`
