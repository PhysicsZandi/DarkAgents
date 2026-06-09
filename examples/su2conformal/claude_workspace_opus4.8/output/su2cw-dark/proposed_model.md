# su2cw-dark: Minimal Classically Conformal Dark SU(2) Model

## Summary

The minimal classically scale-invariant (conformal) non-abelian gauge model able to
explain the NANOGrav PTA signal through a supercooled cosmological first-order phase
transition (FOPT). Scale invariance is broken radiatively by the Coleman-Weinberg (CW)
mechanism (dimensional transmutation), driven by the dark gauge bosons.

## Gauge group and field content

- Gauge group: **SU(2)_D** (dark, non-abelian), coupling `g`.
- Scalar: one complex SU(2)_D **doublet** `Phi` (4 real dof). This is the minimal scalar
  representation that fully breaks the group radiatively.
- No fermions (avoids any gauge/chiral anomaly trivially and guarantees boson domination).

## Symmetries

- Gauged: SU(2)_D.
- Global: classical scale (conformal) invariance — no dimensionful parameters in the
  Lagrangian. Broken radiatively via CW. Accidental custodial SO(4) of the single-doublet
  quartic potential.

## Lagrangian (classically scale invariant, no mass term)

```
L = -1/4 W^a_{mu nu} W^{a mu nu} + (D_mu Phi)^dagger (D^mu Phi) - lambda (Phi^dagger Phi)^2
D_mu Phi = (d_mu - i g (sigma^a/2) W^a_mu) Phi,   a = 1,2,3
```

No `mu^2 Phi^dagger Phi` term is allowed by classical scale invariance.

## Symmetry breaking

`SU(2)_D -> nothing`. In unitary gauge `Phi = (1/sqrt(2))(0, chi)^T`, `<chi> = chi0`.
The 3 Goldstones are eaten; the 3 dark gauge bosons become massive (9 vector dof); one
radial CW pseudo-dilaton `chi` remains.

## Background-field masses

- Gauge bosons: `m_W^2(chi) = g^2 chi^2 / 4`  =>  `gb_W = m_W/chi = g/2`, dof `n_W = 9`.
- Radial scalar: `m_chi^2(chi) = beta_lambda * chi^2`  =>  `gb_scalar = sqrt(beta_lambda)`,
  dof 1 (added automatically by the backend; not double-counted).

## Coleman-Weinberg relation (dependent quantities)

Model-independent form used by the backend:

```
beta_lambda = 1/(8 pi^2) * ( n_W * gb_W^4 + 1 * gb_scalar^4 )
            = 1/(8 pi^2) * ( 9 (g/2)^4 + beta_lambda^2 )      (scalar back-reaction negligible)
m_chi^2 = beta_lambda * chi0^2
```

Boson domination (`beta_lambda > 0`) is automatic since there are no fermions, so radiative
symmetry breaking and a real CW pseudo-dilaton mass are guaranteed.

## Parameters

Independent (scannable / PTArcade priors):
- `g` in [0.3, 1.5]: dark gauge coupling; sets FOPT strength and amount of supercooling.
- `chi0` in [1e-4, 1e2] GeV: symmetry-breaking scale; sets the GW peak frequency in the PTA band.

Dependent (computed, never scanned):
- `lambda` (CW-fixed, scale-dependent; not needed by backend),
- `beta_lambda`, `gb_scalar = sqrt(beta_lambda)`, `m_chi = sqrt(beta_lambda) chi0`.

Fixed: `n_W = 9`, scalar dof = 1, no fermions.

## Backend compatibility

Compatible with `backend/semianalytic_pipeline.py`: single-field classically scale-invariant
model, all masses proportional to one vev, no tree-level mass term. Mapping:

```python
chi0 = chi0
boson_gbs = {"Wprime": g/2}
boson_dofs = {"Wprime": 9}
fermion_gfs = {}
fermion_dofs = {}
# scalar gb and dof added automatically by SemiAnalyticPipeline
```

## Assumptions, caveats, approximations

- Dark sector thermalized with the SM bath (`xi = 1` in the backend).
- High-temperature expansion (small field/T) of the thermal potential — valid in the
  intended strong-supercooling regime per `docs/BACKEND_COMPATIBILITY.md`.
- Perturbativity assumed for `g` up to ~1.5.
- Single radial background direction; doublet flat direction lifted by CW.

## Local novelty

The `output/` directory contains no other model; this is locally novel by construction
(minimal dark SU(2) + single doublet, no fermions).
