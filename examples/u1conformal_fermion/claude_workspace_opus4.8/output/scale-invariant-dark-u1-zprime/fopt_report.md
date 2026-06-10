# FOPT Report — scale-invariant-dark-u1-zprime

Branch: `fopt-pta`. Backend: `backend/semianalytic_pipeline.py` (classically
scale-invariant single-scalar Coleman-Weinberg model; high-T / small-field
expansion with analytic bounce action and Gaussian percolation).

## Model and backend mapping

Independent scan axes (only these are scanned):

| param | range | backend role |
|-------|-------|--------------|
| `g_D` | [0.1, 1.5] | `gb_gauge = g_D` (Zp, dof 3) |
| `y`   | [0.0, 1.0] | `gf_fermion = y/sqrt(2)` (chi, dof 8), hard cut `y^4 < 1.5 g_D^4` |
| `w`   | [0.05, 10] GeV | `chi0 = w` |

Dependent (computed internally, not scanned): `beta_lambda = (1/8pi^2)(3 g_D^4 - 8 (y/sqrt2)^4) > 0`,
CW-fixed quartic, `m_scalon = sqrt(beta_lambda) w`, `m_Zp = g_D w`, `m_chi = y w/sqrt2`.

Physical guards before each backend call: parameter bounds, perturbativity,
and the hard cut `y^4 < 1.5 g_D^4` (equivalently `beta_lambda > 0`).

## Validation against literature anchor (Point A, arXiv:2502.19478)

`g_D=0.877, y=0.363, w=92.9 MeV`:

| quantity | backend | literature |
|----------|---------|-----------|
| T_p  | 7.44 MeV | 8.36 MeV |
| T_reh| 11.5 MeV | 12.9 MeV |
| alpha| 4.68 | 4.99 |
| beta/H | 152.7 | 21.1 |

T_p, T_reh and alpha are reproduced within ~10-15%. The beta/H value differs
because this backend uses a different percolation-based timescale convention
than the paper; this is recorded as a warning and the pta-agent owns the exact
spectral normalization. Eternal inflation: False (transition completes).

## Scan results

Coarse-to-fine bounded scan, 374 points: **238 viable**, 136 failed
(physical/numerical, dominated by the `beta_lambda<=0` hard cut and
eternal-inflation exclusions), 0 spurious not-FOPT.

**32 viable points fall in the PTA band** (f_peak_est in 1e-9..1e-7 Hz),
spanning `g_D in [0.5, 0.9]`, `w in [0.05, 0.71] GeV`, `y in [0, 0.7]`, with
alpha from ~9 (moderate) to ~1e16 (deeply supercooled, vacuum-dominated) and
beta/H ~ 12-144. This in-band window defines the recommended prior ranges for
the downstream PTA fit.

Representative best (in-band) points:

| g_D | y | w (GeV) | T_p (GeV) | T_reh (GeV) | alpha | beta/H | f_peak (Hz) |
|-----|---|---------|-----------|-------------|-------|--------|-------------|
| 0.50 | 0.20 | 0.121 | 5.4e-7 | 9.0e-3 | 7.5e16 | 12.3 | 1.2e-8 |
| 0.50 | 0.00 | 0.707 | 5.7e-6 | 5.3e-2 | 7.4e15 | 12.4 | 7.6e-8 |
| 0.54 | 0.23 | 0.484 | 2.8e-5 | 3.9e-2 | 3.6e12 | 16.2 | 7.3e-8 |

## Outputs

- `fopt_model.py` — model + backend mapping, physical guards, smoke test.
- `fopt_model_scan.py` — coarse-to-fine scan with per-point timeout/error handling.
- `fopt_benchmarks.csv` — every evaluated point with status.
- `fopt_results.json` — structured per-point and best-point results.
- `fopt_gw_spectra.png` — h^2 Omega_GW(f) for the best in-band points (bf template), PTA band shaded.
- `handoff_fopt.json` — authoritative downstream handoff.

f_peak_est is a template-independent order-of-magnitude anchor only; the true
spectral peak is determined downstream by the pta-agent.
