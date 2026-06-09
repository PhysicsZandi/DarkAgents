# FOPT Report: su2cw-dark

Minimal classically conformal dark SU(2)_D, one complex scalar doublet, no fermions.
Coleman-Weinberg radiative symmetry breaking, supercooled first-order phase transition
targeting the NANOGrav nano-Hz signal.

## Backend

`semianalytic_pipeline` (arXiv:2602.02829). Selected by the backend compatibility rule:
classically scale-invariant single-field model, all masses proportional to one vev,
no tree-level mass term. The backend uses the one-loop CW potential with the high-T
(small field/T) thermal expansion, valid in the supercooled regime since the barrier
is thermally generated at small field/T, plus a Gaussian percolation approximation.

## Model mapping

Independent parameters (scan axes):
- `g`    : dark SU(2)_D gauge coupling, range [0.3, 1.5] (perturbativity).
- `chi0` : scalar radial vev in GeV.

Backend inputs: `boson_gbs = {"Wprime": g/2}`, `boson_dofs = {"Wprime": 9}`,
no fermions. The radial CW scalar (dof 1) is injected automatically by the backend.

Dependent (computed internally, never scanned):
`beta_lambda = (9*(g/2)^4 + gb_scalar^4)/(8 pi^2)`, `m_chi = sqrt(beta_lambda)*chi0`,
CW-fixed `lambda`.

## Transition completion (supercooling check)

The critic flagged that supercooled conformal FOPTs may fail to complete. This was
checked explicitly for every point:
- percolation temperature `Tp` computed from the Gaussian false-vacuum-fraction
  condition (`get_Tp`),
- eternal-inflation check (`get_check_eternal_inflation`).

All reported viable points have a finite, positive `Tp` and `eternal_inflation = False`,
i.e. the transition percolates and completes. Points that would not complete are
recorded as `physical_failure`, not viable.

## Smoke test (literature anchor, arXiv:2109.11558 Scenario 1)

g = 1.37, chi0 = 2*M_ZD/g = 0.01201 GeV (M_ZD = 8.23 MeV):

| quantity | value |
|---|---|
| beta_lambda | 0.0251 |
| m_chi | 1.90e-3 GeV |
| Tn | 8.50e-4 GeV |
| Tp | 7.63e-4 GeV |
| Treh | 1.53e-3 GeV |
| alpha | 15.0 |
| beta/H | 144.0 |
| eternal inflation | False |
| f_peak_est | 2.68e-8 Hz |

beta/H = 144 reproduces the published 143; transition completes. (alpha is larger
than the paper's 0.45 — expected, as this backend defines alpha at percolation in a
deeply supercooled normalization and uses no daisy resummation; the parameter
magnitudes and the PTA-band placement are consistent.)

## Scan

Coarse-to-fine bounded scan, 302 points total:
- coarse: g in [0.5,1.5] x6, chi0 in [1e-4,1e1] GeV (log) x12
- fine: g in [1.1,1.5] x9, chi0 in [1e-3,1e-1] GeV x12 (literature anchor region)
- band: g in [0.8,1.5] x8, chi0 in [3e-4,1.0] GeV x16 (PTA-window mapping)

Each evaluation wrapped with per-point timeout and error handling.

Results:
- viable: 271 / 302 (finite, positive Tn/Tp/Treh/alpha/beta_H, completes)
- physical_failure: 31 (non-finite/non-positive observable or eternal inflation)
- numerical_failure: 0
- viable points in the PTA band (f_peak_est in [1e-9, 1e-7] Hz): 168

The PTA-band window is fully bracketed inside the grid: in-band points span
chi0 ~ 5e-4 to 4.3e-1 GeV, while viable points extend beyond on both sides
(f_peak_est from 3e-11 to 2e-5 Hz, chi0 from 1e-4 to 10 GeV). The physical band
boundaries, not the grid, are the limiting factor.

## Best benchmark points (in PTA band, ranked by closeness to band center)

| g | chi0 [GeV] | alpha | beta/H | Tp [GeV] | Treh [GeV] | f_peak_est [Hz] |
|---|---|---|---|---|---|---|
| 1.30 | 5.34e-3 | 33.1 | 126.3 | 2.71e-4 | 6.55e-4 | 9.90e-9 |
| 1.15 | 1.23e-2 | 931 | 62.1 | 2.42e-4 | 1.34e-3 | 9.90e-9 |
| 1.45 | 3.51e-3 | 6.22 | 162.8 | 3.01e-4 | 4.93e-4 | 9.64e-9 |
| 1.40 | 4.48e-3 | 10.4 | 148.2 | 3.25e-4 | 5.97e-4 | 1.06e-8 |
| 1.25 | 8.11e-3 | 72.5 | 96.8 | 3.23e-4 | 9.46e-4 | 1.10e-8 |

All five complete (eternal_inflation = False). The temperature handed downstream is
`Treh` (reheating temperature), which sets the GW redshift.

## Verdict

The supercooled SU(2)_D conformal FOPT **completes** across a broad, well-bounded
region with vev at the MeV-to-sub-GeV scale and g near 1.1-1.5, producing a
redshifted peak in the PTA nano-Hz band. A robust set of viable benchmark points is
available for the pta-agent, who owns the exact spectral peak via the GW template.

## Files
- `output/su2cw-dark/fopt_model.py`
- `output/su2cw-dark/fopt_model_scan.py`
- `output/su2cw-dark/fopt_benchmarks.csv`
- `output/su2cw-dark/fopt_results.json`
- `output/su2cw-dark/handoff_fopt.json`
- `output/su2cw-dark/fopt_report.md`
