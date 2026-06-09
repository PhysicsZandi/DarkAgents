# Minimal Conformal SU(2) Doublet Model

## Status

This is a candidate model for the `fopt-pta` branch. It has not been fitted to
NANOGrav or any PTA data at this stage. Its gravitational-wave signal must be
computed and tested by the downstream FOPT and PTA agents.

## Model Definition

The minimal conformal non-Abelian candidate is a dark `SU(2)_D` gauge theory
with one complex scalar doublet `Phi`. The scalar sector is classically
scale-invariant, so the tree-level potential contains no mass term:

```text
V0(Phi) = lambda_phi * (Phi_dag * Phi)^2
```

The background-field convention is

```text
Phi = (0, chi / sqrt(2))^T
```

so

```text
V0(chi) = lambda_phi * chi**4 / 4
```

The `SU(2)_D` symmetry is spontaneously broken by

```text
SU(2)_D -> nothing
```

and all three dark gauge bosons acquire the same field-dependent mass

```text
m_WD2(chi) = gD**2 * chi**2 / 4
```

The radial scalar is treated as the Coleman-Weinberg pseudo-dilaton. Its mass is
dependent rather than independent:

```text
beta_lambda = 1 / (8 * pi**2) * (9 * (gD / 2)**4)
m_chi2 = beta_lambda * vD**2
```

The quartic `lambda_phi` is fixed by the Coleman-Weinberg minimization
condition and should not be scanned as an independent parameter in the
semianalytic conformal backend.

## Lagrangian Terms

```text
L = -1/4 * FDa_munu * FDa_munu
    + (D_mu Phi)^dag * (D_mu Phi)
    - lambda_phi * (Phi_dag * Phi)**2
```

No new chiral fermions are introduced, so there is no new gauge anomaly.

## Parameters

Independent scan parameters:

- `gD`: dark `SU(2)_D` gauge coupling.
- `vD`: Coleman-Weinberg vev of the radial direction.

Dependent parameters:

- `beta_lambda = 1 / (8 * pi**2) * (9 * (gD / 2)**4)`.
- `m_chi2 = beta_lambda * vD**2`.
- `lambda_phi`: Coleman-Weinberg-fixed running quartic.
- `m_WD = gD * vD / 2`.

Fixed assumptions:

- No portal coupling to the Standard Model is included at proposal stage.
- No additional dark fermions are included.
- The scalar thermal mass is kept as a symbolic coefficient `c_phi * T**2`
  pending downstream convention choices.

## Backend Compatibility

The model is compatible with `backend/semianalytic_pipeline.py` because it is a
classically scale-invariant single-field model with all masses proportional to
one scalar background `chi` and no explicit tree-level mass term. The relevant
bosonic input is three massive vector bosons with total degrees of freedom `9`
and mass ratio `gb = gD / 2`.

## Warnings and Caveats

- This proposal does not claim a quantitative PTA fit.
- The downstream FOPT/PTA agents must test whether any parameter point produces
  a viable phase transition and PTA-compatible spectrum.
- The scalar thermal mass coefficient is recorded symbolically because backend
  conventions may choose whether to use only gauge-induced terms or include
  CW-fixed scalar self-interactions.
