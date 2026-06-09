# Field-Dependent Mass Recheck: conformal_u1_dark_fopt

Date: 2026-06-08

Scope: targeted critic-agent recheck of the field-dependent mass normalizations and their mapping to `backend/semianalytic_pipeline.py`. No FOPT or PTA calculation was performed.

## Inputs Checked

- `output/conformal_u1_dark_fopt/handoff_model.json`
- `output/conformal_u1_dark_fopt/handoff_critique.json`
- `output/conformal_u1_dark_fopt/model.md`
- `backend/semianalytic_pipeline.py`

## Convention

The validated model states

```text
Phi = chi / sqrt(2)
<chi> = v_D
q_Phi = 2
D_mu Phi = (partial_mu - i*q_Phi*g_D*X_mu) Phi
```

and the Weyl Yukawa terms

```text
-(y_D/2) Phi_dagger psi_plus psi_plus
-(y_D/2) Phi psi_minus psi_minus
+ h.c.
```

## Gauge Boson Mass

Substituting the real radial background into the scalar kinetic term gives

```text
|D_mu Phi|**2 contains q_Phi**2 * g_D**2 * X_mu * X_mu * |Phi|**2
                 = q_Phi**2 * g_D**2 * chi**2 * X_mu * X_mu / 2
```

The canonical massive real-vector term is

```text
(1/2) * m_X**2 * X_mu * X_mu
```

Therefore

```text
m_X**2(chi) = q_Phi**2 * g_D**2 * chi**2 = 4 * g_D**2 * chi**2
m_X(chi) = 2 * g_D * chi
```

So the backend mass-over-background mapping

```text
gb_X = 2*g_D
```

is correct. The alternatives `2*g_D**2*chi**2` and any mapping with `gb_X = sqrt(2)*g_D` would miss the canonical `1/2` real-vector mass-term normalization.

## Fermion Mass

For a left-handed Weyl fermion, the canonical Majorana mass term is

```text
-(1/2) * m * psi * psi + h.c.
```

Substituting `Phi = chi/sqrt(2)` gives

```text
-(y_D/2) * (chi/sqrt(2)) * psi * psi + h.c.
```

Matching to the canonical Weyl mass term gives

```text
m_psi(chi) = y_D * chi / sqrt(2)
m_psi**2(chi) = (y_D**2 / 2) * chi**2
```

The explicit `1/2` in the Yukawa is the standard Weyl mass normalization and should not be counted a second time. Therefore `(y_D**2/4)*chi**2` would be too small by a factor of 2.

## Backend Mapping

`backend/semianalytic_pipeline.py` consumes dictionaries of mass-over-background coefficients:

```text
m_boson(chi) = gb * chi
m_fermion(chi) = gf * chi
```

and computes the Coleman-Weinberg coefficient as

```text
(sum_B dof_B*gb_B**4 - sum_F dof_F*gf_F**4)/(8*pi**2)
```

With the validated model,

```text
boson_gbs = {"X_mu": 2*g_D}
boson_dofs = {"X_mu": 3}
fermion_gfs = {"psi_degenerate_majorana_pair": y_D/sqrt(2)}
fermion_dofs = {"psi_degenerate_majorana_pair": 4}
```

The fermion `dof=4` is correct for two degenerate left-handed Weyl Majorana mass eigenstates, each contributing 2 fermionic degrees of freedom. Combining them into one backend species is only a degeneracy bookkeeping choice; it is not a claim that the mass term is Dirac.

## Conclusion

No correction is needed. The existing validated formulas are internally consistent with the stated convention and with the semianalytic backend:

```text
m_X_squared(chi) = 4 * g_D**2 * chi**2
gb_X = 2*g_D
m_psi_squared(chi) = (y_D**2 / 2) * chi**2
gf_psi = y_D/sqrt(2)
fermion dof = 4
```

No changes were made to `handoff_model.json`, `model.md`, `handoff_critique.json`, or `critique.md`.
