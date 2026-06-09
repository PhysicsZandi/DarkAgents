# Proposed Model: conformal_u1_dark_fopt

## Scope

This proposal addresses the user question:

> Can a conformal U(1) BSM extension with a dark scalar, a dark gauge bosons and a dark fermion explain the NANOGrav signal with a cosmological FOPT?

The model is designed for the implemented `fopt-pta` branch. It is a classically scale-invariant single-field Coleman-Weinberg dark-sector model whose finite-temperature effective potential can be mapped to `backend/semianalytic_pipeline.py`. No numerical FOPT or PTA result is claimed here; the downstream FOPT and PTA agents must compute the transition parameters, gravitational-wave spectrum, and comparison to PTA data.

## Gauge Symmetry and Field Content

Gauge symmetry:

- Standard Model gauge group, with all new fields neutral under it.
- Dark gauge group `U(1)_D`.

New fields:

| Field | Type | Spin | SM representation | U(1)_D charge | Degrees of freedom | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `Phi` | complex scalar | 0 | `(1,1,0)` | `+2` | 2 real | Dark scalar that breaks `U(1)_D` radiatively. |
| `X_mu` | gauge boson | 1 | `(1,1,0)` | adjoint | 3 massive | Dark gauge boson after symmetry breaking. |
| `psi_+` | Weyl fermion | 1/2 | `(1,1,0)` | `+1` | 2 | Dark fermion Weyl component. |
| `psi_-` | Weyl fermion | 1/2 | `(1,1,0)` | `-1` | 2 | Oppositely charged dark fermion Weyl component. |

The fermion sector is anomaly-free because `(+1)^3 + (-1)^3 = 0` and `(+1) + (-1) = 0`. The Yukawa terms `Phi^dagger psi_+ psi_+` and `Phi psi_- psi_-` are gauge invariant and give two degenerate Majorana-like dark fermion states when the scalar gets a vev. This is the minimal anomaly-safe way to include a conformal dark fermion mass from the same U(1)-breaking scalar.

## Lagrangian

The relevant dark-sector Lagrangian is

```text
L_dark =
  -1/4 X_munu X^munu
  + |D_mu Phi|^2
  + i psi_+^dagger bar_sigma^mu D_mu psi_+
  + i psi_-^dagger bar_sigma^mu D_mu psi_-
  - (y_D/2 Phi^dagger psi_+ psi_+ + y_D/2 Phi psi_- psi_- + h.c.)
  - V0(Phi)
```

with

```text
V0(Phi) = lambda_D (Phi^dagger Phi)^2
```

and no explicit scalar mass term. The Higgs portal term `lambda_HP (H^dagger H)(Phi^dagger Phi)` is set to zero for the backend scan and may be treated as a small perturbation only in later phenomenology. Kinetic mixing `epsilon/2 B_munu X^munu` is also set to zero for the FOPT backend; constraints can later revisit small nonzero `epsilon`.

## Symmetry Breaking and Coleman-Weinberg Parameterization

Use the radial background convention

```text
Phi = chi / sqrt(2)
<chi> = v_D
```

The field-dependent masses are

```text
m_X^2(chi) = 4 * g_D**2 * chi**2
m_psi^2(chi) = (y_D**2 / 2) * chi**2
m_chi^2 = beta_lambda * v_D**2
```

The Coleman-Weinberg relation is represented in the backend-compatible mass-over-vev basis:

```text
gb_X = 2 * g_D
gf_psi = y_D / sqrt(2)
beta_lambda = (1 / (8*pi**2)) * (3*gb_X**4 - 4*gf_psi**4)
m_chi^2 = beta_lambda * v_D**2
```

Radiative symmetry breaking requires `beta_lambda > 0`, so the dark gauge contribution must dominate over the dark fermion contribution.

## Independent Parameters

Recommended scan/prior inputs for downstream agents:

- `v_D`: dark scalar radial vev, in GeV.
- `g_D`: dark gauge coupling.
- `y_D`: dark Yukawa coupling.

The quartic `lambda_D` is not an independent scan parameter for the semianalytic Coleman-Weinberg backend. The scalar radial mass is a dependent output fixed by `beta_lambda`.

## FOPT Ingredients

This model has the branch-relevant ingredients needed by the `fopt-pta` branch:

- Single scalar order parameter `chi`.
- Conformal tree-level potential with no mass term.
- All relevant field-dependent masses proportional to `chi`.
- Bosonic gauge contribution able to generate a thermal barrier.
- Fermionic contribution included analytically and constrained by `beta_lambda > 0`.

The downstream FOPT agent must compute nucleation/percolation, `alpha`, `beta/H`, transition temperature or percolation temperature, latent heat, and the gravitational-wave source parameters. The downstream PTA agent must test whether the resulting stochastic gravitational-wave spectrum can match the PTA/NANOGrav-preferred region.

## Assumptions and Caveats

- The proposal is intentionally minimal and dark-sector-only.
- Higgs portal and gauge kinetic mixing are fixed to zero for backend compatibility.
- The model is proposed in a convention suitable for deterministic downstream checks; the critic agent should verify charge conventions, anomaly cancellation, and whether an exactly minimal fermion sector is acceptable.
- No numerical claim is made about explaining NANOGrav/PTA; this is a candidate model to be tested by the implemented pipeline.
