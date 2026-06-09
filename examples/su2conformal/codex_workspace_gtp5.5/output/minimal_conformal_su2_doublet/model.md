# Model: minimal_conformal_su2_doublet

## Definition

The validated model is a classically conformal dark `SU(2)_D` gauge theory with one complex scalar doublet `Phi` and no new fermions. All new fields are Standard Model singlets, and the Higgs portal is set to zero for the minimal FOPT/PTA analysis.

The scalar background convention is

```text
Phi = (0, chi / sqrt(2))^T
<chi> = vD
```

The spontaneous symmetry breaking pattern is

```text
SU(2)_D -> nothing
```

All three dark vectors acquire the common field-dependent mass

```text
m_WD2(chi) = gD**2 * chi**2 / 4
m_WD = gD * vD / 2
```

## Lagrangian

The dark-sector Lagrangian terms needed for the branch are

```text
L_dark includes -1 / 4 * FDa_munu * FDa_munu
L_dark includes Dmu_Phi_dag * Dmu_Phi
V0(Phi) = lambda_phi * (Phi_dag_Phi)**2
V0(chi) = lambda_phi * chi**4 / 4
```

Classical scale invariance forbids explicit scalar mass terms.

## Parameter Basis

Independent scan parameters:

- `gD > 0`
- `vD > 0`

Dependent parameters:

- `beta_lambda = 1 / (8 * pi**2) * (9 * (gD / 2)**4)`
- `m_chi2 = beta_lambda * vD**2`
- `lambda_phi`, fixed by the Coleman-Weinberg minimization convention and not independently scanned
- `m_WD = gD * vD / 2`
- `gb_WD = gD / 2`
- `gb_scalar = sqrt(beta_lambda)`

Fixed assumptions:

- Higgs portal coupling is zero.
- No new dark fermions are included.

## FOPT Backend Mapping

For `backend/semianalytic_pipeline.py`, use

```text
chi0 = vD
boson_gbs = {"W_D": gD / 2}
boson_dofs = {"W_D": 9}
fermion_gfs = {}
fermion_dofs = {}
```

The backend computes the Coleman-Weinberg scalar contribution internally from the mass-ratio dictionaries, so the scalar must not be added as an independent scanned bosonic mass ratio.

Thermal masses for downstream daisy bookkeeping are

```text
Pi_Phi = (lambda_phi / 2 + 3 * gD**2 / 16) * T**2
Pi_WD_longitudinal = 5 * gD**2 * T**2 / 6
```

