# Critique: U(1)_D Conformal Dark Sector Model

## Model
- **Name**: `u1conformal_fermion`
- **Branch**: `fopt-pta`
- **Source**: Proposer-agent
- **Date**: 2026-06-08

## Executive Summary

The proposed classically scale-invariant U(1)_D dark sector model is **physically consistent** with no unresolved red flags. Three issues were identified and fixed during the critique: (1) an inconsistent Goldstone thermal mass expression, (2) a mislabeled quartic coupling relation, and (3) a missing supercooling constraint in the parameter documentation. The model is ready for the FOPT-PTA pipeline.

## Validation Summary

| Category | Status |
|----------|--------|
| Gauge groups | OK |
| Global symmetries | OK |
| Particle content | OK |
| Lagrangian terms | OK |
| Free parameters | OK (1 fix applied) |
| Parameter basis classification | OK (1 fix applied) |
| Anomalies | OK |
| SSB pattern | OK |
| VEV convention | OK |
| Tree-level potential | OK |
| Field-dependent masses | OK |
| Thermal masses | 1 fix applied |
| Backend compatibility | OK |

## 1. Gauge Anomalies (PASS)

**U(1)_D^3 anomaly**: Sum over Weyl fermions of q^3.
- psi_1 (charge +1/2): (+1/2)^3 + (+1/2)^3 = +1/4
- psi_2 (charge -1/2): (-1/2)^3 + (-1/2)^3 = -1/4
- **Total = 0. PASS.**

**U(1)_D-gravity mixed anomaly**: Sum over Weyl fermions of q.
- psi_1: (+1/2) + (+1/2) = +1
- psi_2: (-1/2) + (-1/2) = -1
- **Total = 0. PASS.**

**Mixed U(1)_D-U(1)_Y anomalies**: No SM-charged fermions in the dark sector. **PASS.**

The two Dirac fermions with opposite charges (+1/2, -1/2) are the minimal anomaly-free fermion content for a U(1)_D with a charged complex scalar.

## 2. Lagrangian Consistency (PASS)

All terms are gauge invariant, renormalizable, and CP-conserving:

| Term | Gauge Charge Sum | Result |
|------|-----------------|--------|
| `Phi * psi1_bar * psi2` | +1 + (-1/2) + (-1/2) = 0 | PASS |
| `(Phi*Phi)^2` | (0)^2 = 0 | PASS |
| `D_mu Phi` kinetic | covariant derivative ensures invariance | PASS |
| `psi_i_bar D_mu psi_i` | covariant derivative ensures invariance | PASS |

## 3. SSB Pattern and VEV Convention (PASS)

- **Pattern**: U(1)_D -> nothing (fully broken).
- **Convention**: `Phi = (chi + v)/sqrt(2)` in unitary gauge. Radial mode chi.
- The Goldstone theta is eaten by A'_mu, giving the gauge boson a longitudinal mode.
- **DOF before SSB**: A'_mu (2) + Phi (2) + psi_1 (4) + psi_2 (4) = 12.
- **DOF after SSB**: A'_mu (3) + chi (1) + psi_1 (4) + psi_2 (4) = 12. Conservation verified.

## 4. Field-Dependent Masses (PASS)

| Particle | m^2(chi) | Verified | DOF |
|----------|----------|----------|-----|
| A'_mu | g_D^2 * chi^2 | From scalar kinetic: |D_mu Phi|^2 | 3 |
| chi | beta_lambda * chi^2 | From CW curvature | 1 |
| psi | y_psi^2 * chi^2 / 2 | From Yukawa: y_psi*chi/sqrt(2) * psi_bar psi | 8 |

All field-dependent masses are consistent with the Lagrangian, the SSB pattern, and the vev convention.

## 5. Coleman-Weinberg Relation (PASS)

```
beta_lambda = (1/(8*pi^2)) * (sum_B n_B gb^4 - sum_F n_F gf^4)

Gauge:   3 * g_D^4
Fermion: 8 * (y_psi/sqrt(2))^4 = 2 * y_psi^4

beta_lambda = (3*g_D^4 - 2*y_psi^4)/(8*pi^2)
```

Requirement `beta_lambda > 0` gives: `y_psi < (3/2)^(1/4) * g_D ≈ 1.11 * g_D`.

The backend `semianalytic_pipeline.py` computes this automatically from the particle inputs. The model correctly maps:

- boson_gbs = {"gauge": g_D, "scalar": 0}, boson_dofs = {"gauge": 3, "scalar": 1}
- fermion_gfs = {"psi": y_psi/sqrt(2)}, fermion_dofs = {"psi": 8}

## 6. Thermal Masses (FIXED)

The backend uses a single combined thermal mass-squared `msq = g2sq * T^2 / 12` where:
```
g2sq = 3*g_D^2 + 2*y_psi^2
```

The A'_mu longitudinal and chi thermal masses were correctly listed as `(3*g_D**2 + 2*y_psi**2) * T**2 / 12`.

**ISSUE FIXED**: The Goldstone theta thermal mass was originally `g_D**2 * T**2 / 3`, which is physically inconsistent. The Goldstone is the angular component of the same complex scalar Phi and receives the same thermal corrections as the radial mode. It has been updated to `(3*g_D**2 + 2*y_psi**2) * T**2 / 12` to match the combined formula.

## 7. Parameter Classification (FIXED)

**Independent parameters** (scanned):
- g_D in [0.1, 4.0]: Dark gauge coupling
- y_psi in [0.0, 1.0]: Yukawa coupling (with additional constraints)
- v in [100, 10000] GeV: Dark Higgs vev

**Dependent parameters** (not scanned):
- lambda_Phi: CW-fixed quartic (derived from beta_lambda)
- beta_lambda: CW beta function parameter
- m_chi: scalar mass (from beta_lambda * v^2)
- m_Aprime: gauge boson mass
- m_psi: fermion mass
- gb_scalar: scalar coupling (set to 0 in backend)

**ISSUE FIXED**: The original handoff had `lambda_Phi` with a relation defining `beta_lambda` instead of `lambda_Phi` itself. These are now separated into two distinct entries with correct relations: `lambda_Phi = (3*g_D**4 - 2*y_psi**4)/(32*pi**2)` (since `lambda_Phi = beta_lambda/4` from the tree-level potential normalization) and `beta_lambda = (3*g_D**4 - 2*y_psi**4)/(8*pi**2)`.

**ISSUE FIXED**: The y_psi parameter notes now include the supercooling condition `g_D > y_psi/sqrt(2)` (from Feng-Zhang: m_A' > m_psi for FOPT viability), which is a tighter bound than the CW condition for most parameter values.

## 8. Supercooling Condition

From Feng-Zhang (2602.14866): `m_A' > m_psi` is required for strong first-order phase transition. This translates to:
```
g_D * v > y_psi * v / sqrt(2)  =>  g_D > y_psi / sqrt(2)
```

This is a tighter constraint than the CW condition `y_psi < (3/2)^(1/4)*g_D` for all g_D values. The condition is now documented in the parameter notes.

Comparison of constraints:
| g_D | CW: y_psi < 1.11*g_D | Supercooling: y_psi < 0.707*g_D |
|-----|---------------------|-------------------------------|
| 0.1 | 0.111 | 0.071 |
| 0.5 | 0.555 | 0.354 |
| 1.0 | 1.110 | 0.707 |
| 2.0 | 2.220 | 1.414 |

## 9. Issues and Repairs Summary

| # | Issue | Severity | Status |
|---|-------|----------|--------|
| 1 | Goldstone thermal mass `g_D**2*T**2/3` inconsistent with combined formula | Warning | Fixed |
| 2 | `lambda_Phi` dependent parameter relation mislabeled as `beta_lambda` | Warning | Fixed |
| 3 | Supercooling condition `g_D > y_psi/sqrt(2)` not documented | Warning | Fixed |
| 4 | `gb_scalar` set to 0 by backend (documentation-only) | Info | Noted |
| 5 | Perturbativity constraint at low g_D values | Info | Noted |

## 10. Conclusion

**No red flags remain.** The model is physically consistent, anomaly-free, and backend-compatible. The three warnings found have been fixed with minimal changes. The validated model specification is in `output/u1conformal_fermion/handoff_model.json`.
