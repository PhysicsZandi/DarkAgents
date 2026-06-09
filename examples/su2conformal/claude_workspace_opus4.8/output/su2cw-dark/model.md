# Validated Model: su2cw-dark

**Branch:** fopt-pta | **Validated by:** critic-agent (no red flags, no fixes) | **Date:** 2026-06-07

Minimal classically conformal non-abelian dark gauge model that can explain the
NANOGrav PTA signal through a supercooled first-order phase transition. This is the
authoritative specification cleared for downstream fopt-agent and pta-agent.

## Gauge group and symmetries

- **Gauge:** dark SU(2)_D, coupling `g`. Fully broken by the doublet vev; no light
  non-abelian remnant.
- **Classical scale (conformal) invariance:** no dimensionful parameter; broken
  radiatively via Coleman-Weinberg dimensional transmutation.
- Accidental custodial SO(4) of the single-doublet quartic (not gauged).

## Field content

| Field | Spin | SU(2)_D rep | dof | Role |
|-------|------|-------------|-----|------|
| Phi | 0 | fundamental (doublet) | 4 | complex scalar; source of breaking |
| W_D^a | 1 | adjoint (a=1,2,3) | 9 | three massive dark vectors after SSB |
| chi | 0 | singlet (radial) | 1 | CW pseudo-dilaton, m_chi^2 = beta_lambda chi0^2 |

No fermions (so no anomalies). dof balance: 10 before SSB = 10 after (3 Goldstones eaten).

## Lagrangian

- Scalar kinetic: `(D_mu Phi)^dag (D^mu Phi)`, `D_mu Phi = (d_mu - i g sigma^a/2 W^a_mu) Phi`
- Gauge kinetic: `-1/4 W^a_{mu nu} W^{a mu nu}`
- Potential: `lambda (Phi^dag Phi)^2` (pure quartic, no mu^2 term)

## SSB, vev convention, background masses

- Pattern: `SU(2)_D -> nothing`.
- vev: `Phi = (1/sqrt2)(0, chi)^T`, `<chi> = chi0`.
- Gauge bosons: `m_W^2(chi) = g^2 chi^2/4`, gb = g/2, dof = 9 (degenerate triplet).
- Radial scalar: `m^2(chi) = beta_lambda chi^2`, gb = sqrt(beta_lambda), dof = 1
  (injected automatically by the backend; do not double-count).

## Parameters

- **Independent:** `g` in [0.3, 1.5]; `chi0` in [1e-4, 1e2] GeV (PTA-band fits near
  MeV scale, chi0 ~ 1e-3 to 1 GeV).
- **Dependent:** `beta_lambda = (9*(g/2)^4 + gb_scalar^4)/(8 pi^2) > 0`;
  `gb_scalar = sqrt(beta_lambda)`; `m_chi = sqrt(beta_lambda) chi0`; CW-fixed
  `lambda` (scale-dependent, never scanned).

## Backend mapping (semianalytic_pipeline)

`boson_gbs = {"Wprime": g/2}`, `boson_dofs = {"Wprime": 9}`, no fermions; scalar
added automatically. `beta_lambda > 0` ensures radiative SSB and positive
pseudo-dilaton mass.

## Downstream notes (warnings)

1. Verify transition completion/percolation (supercooled conformal FOPT risk).
2. Focus chi0 near MeV scale for PTA band.
3. High-T thermal expansion accuracy degrades in deep supercooling.
