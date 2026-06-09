# Model: conformal_u1_dark_fopt

Validated branch: `fopt-pta`

## Gauge Structure

The model extends the Standard Model by a dark Abelian gauge group `U(1)_D`. All dark-sector fields are Standard Model singlets.

```text
G = SU(3)_c x SU(2)_L x U(1)_Y x U(1)_D
```

The dark gauge coupling is `g_D`. Hypercharge-dark kinetic mixing is allowed by symmetry but fixed to zero for the backend-compatible scan:

```text
epsilon = 0
```

## Field Content

| Field | Type | Spin | U(1)_D charge | Dof | Role |
| --- | --- | --- | --- | --- | --- |
| `Phi` | complex scalar | 0 | `+2` | 2 | Coleman-Weinberg order parameter |
| `X_mu` | gauge boson | 1 | adjoint | 3 after SSB | dark photon |
| `psi_plus` | left-handed Weyl fermion | 1/2 | `+1` | 2 | dark fermion component |
| `psi_minus` | left-handed Weyl fermion | 1/2 | `-1` | 2 | dark fermion component |

The two Weyl fermions cancel the `U(1)_D^3` and mixed gravitational anomalies.

## Lagrangian Terms

The dark-sector terms relevant for the FOPT backend are

```text
-1/4 * X_munu * X_munu
+ abs(D_mu_Phi)**2
+ I*psi_plus_dagger*bar_sigma_mu*D_mu_psi_plus
+ I*psi_minus_dagger*bar_sigma_mu*D_mu_psi_minus
- 1/2*y_D*Phi_dagger*psi_plus*psi_plus
- 1/2*y_D*Phi*psi_minus*psi_minus
+ h.c.
- V0
```

with

```text
V0 = lambda_D * chi**4 / 4
Phi = chi / sqrt(2)
<chi> = v_D
```

There is no explicit scalar mass term and no explicit fermion mass term at tree level.

## Parameters

Independent scan parameters:

```text
v_D > 0
g_D > 0
y_D >= 0
```

Dependent quantities:

```text
gb_X = 2*g_D
gf_psi = y_D/sqrt(2)
beta_lambda = (1/(8*pi**2))*(3*gb_X**4 - 4*gf_psi**4)
m_chi_squared = beta_lambda * v_D**2
lambda_D = Coleman-Weinberg dependent quartic
```

Fixed assumptions:

```text
lambda_HP = 0
epsilon = 0
q_Phi = 2
q_psi_plus = 1
q_psi_minus = -1
```

The scan must enforce `beta_lambda > 0` and perturbative couplings.

## Field-Dependent Masses

Backend-compatible mass mapping:

```text
m_X_squared(chi) = 4 * g_D**2 * chi**2
m_psi_squared(chi) = (y_D**2 / 2) * chi**2
m_chi_squared(v_D) = beta_lambda * v_D**2
```

The fermion entry represents two degenerate Majorana Weyl mass eigenstates with total fermionic `dof = 4`, compressed into one backend species with `gf_psi = y_D/sqrt(2)`.

## Backend Compatibility

The model is compatible with `backend/semianalytic_pipeline.py` with warnings:

```text
chi0 = v_D
boson_gbs = {"X_mu": 2*g_D}
boson_dofs = {"X_mu": 3}
fermion_gfs = {"psi_degenerate_majorana_pair": y_D/sqrt(2)}
fermion_dofs = {"psi_degenerate_majorana_pair": 4}
```

The backend uses mass-over-vev couplings and degrees of freedom to construct the effective potential. It does not directly consume the explicit thermal mass placeholders from the model handoff.

## Literature Use

The preliminary literature benchmarks are suitable only as seed regions and convention checks. They are not exact reproductions of this validated charge-normalized, zero-portal, zero-kinetic-mixing backend limit.
