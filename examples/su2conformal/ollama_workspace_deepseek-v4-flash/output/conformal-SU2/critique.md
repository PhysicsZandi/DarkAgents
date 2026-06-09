# Model Critique: conformal-SU2

## Executive Summary

The conformal-SU2 model (classically scale-invariant SU(2)_X gauge theory with one complex scalar doublet, no fermions) is **physically consistent** after applying one minimal fix. One red flag was identified and corrected; three non-blocking warnings are noted for downstream consideration.

### Status: WARNING (1 red flag fixed, 3 warnings)

---

## 1. Field Content -- PASS

| Field | Type | Rep | dof (before SSB) | dof (after SSB) | Status |
|-------|------|-----|:---:|:---:|:------:|
| Phi | Complex scalar doublet | SU(2)_X fund | 4 | 1 radial + 3 Goldstones | OK |
| W^a_mu | Gauge boson triplet | SU(2)_X adj | 6 | 9 (3 massive vectors) | OK |

**DoF count**: 10 before SSB (4+6), 10 after SSB (1+9). Goldstones are absorbed as longitudinal polarizations. Consistent.

---

## 2. Lagrangian -- PASS

All three terms are gauge-invariant:
- `-1/4 W^a_{munu} W^{a,munu}`: standard Yang-Mills.
- `(D_mu Phi)^\dagger (D^mu Phi)` with D_mu = partial_mu + i g W^a_mu tau^a: standard covariant derivative.
- `lambda (Phi^dagger Phi)^2`: quartic, classically scale-invariant.

No fermions, no anomalies (no chiral fermions). No issues.

---

## 3. SSB Pattern and VEV Convention -- PASS

- **Pattern**: SU(2)_X -> nothing.
- **VEV**: Phi_0 = (0, chi0/sqrt(2))^T.
- **Verification**: All three SU(2) generators tau^1, tau^2, tau^3 are broken by this VEV (none leave the VEV invariant). No residual U(1).
- **Gauge boson mass**: Substituting the background into (D_mu Phi)^\dagger (D^mu Phi) gives:
  - (1/2) m_W^2 = g^2 chi^2/8 => m_W^2 = g^2 chi^2/4 => m_W = g*chi/2.
  - All three gauge bosons have equal mass. Consistent with the handoff.

---

## 4. CW Parameter: RED FLAG (FIXED)

### Issue: beta_lambda has a factor-of-3 error

**Original (proposer)**: `beta_lambda = 3 * g**4 / (128 * pi**2)`
**Correct**: `beta_lambda = 9 * g**4 / (128 * pi**2)`

**Derivation**:

The CW relation is:
```
beta_lambda = (1/(8*pi^2)) * sum_B n_B * gb^4
```

The sum runs over **real degrees of freedom**. For 3 massive SU(2) gauge bosons, each with 3 polarization states:
- Total real dof: n_B = 3 bosons x 3 polarizations = 9
- Each polarization contributes gb = g/2 to the mass: m^2 = (g/2)^2 * chi^2

Therefore:
```
beta_lambda = 9 * (g/2)^4 / (8*pi^2) = 9 * g^4 / (128 * pi^2)
```

**Why the proposer was wrong**: The proposer counted n_B = 3 (gauge boson species) instead of n_B = 9 (total real degrees of freedom contributing to the CW potential).

**Consequence**: The proposer's value would give scalar masses and vacuum energies that are sqrt(3) and 3 times too small, respectively.

**Fix applied**: Changed `beta_lambda` from `3 * g**4 / (128 * pi**2)` to `9 * g**4 / (128 * pi**2)`.

**All downstream dependent parameters** (m_chi2, gb_scalar, delta_V) scale linearly with beta_lambda and are automatically correct after this fix. The backend's own `get_beta_lambda()` method computes the correct value from the input dof and gb (9 dof x (g/2)^4), so the backend is consistent with the fixed expression.

---

## 5. Field-Dependent and Thermal Masses -- PASS (with notes)

### Field-dependent masses

| Particle | m^2(chi) | Verified? |
|----------|----------|:---------:|
| W^a (9 dof) | g^2 * chi^2 / 4 | YES: from covariant derivative |
| chi (1 dof) | beta_lambda * chi^2 | YES: from CW potential second derivative |

### Thermal masses

| Particle | m_D^2 | Notes | Status |
|----------|-------|-------|:------:|
| W^a longitudinal (3 dof) | g^2 * T^2 | Debye mass for SU(2) with N_s=4 real scalars | OK |
| chi (1 dof) | 3/16 * g^2 * T^2 | From C_f * g^2 * T^2 / 4 with C_f = 3/4 | OK |
| Goldstones (3 dof) | 3/16 * g^2 * T^2 | Same as radial scalar in symmetric phase | OK |

### Warning: Debye mass explanatory note inconsistency

The proposer's note says "N_s=2 (one complex doublet = 2 real scalars in fundamental)" but one complex doublet has 4 real fields. The correct count is N_s=4 real scalars in the formula m_D^2 = g^2 T^2 (N/3 + N_s/12). The final expression g^2 T^2 is numerically correct, but the note contains an error.

---

## 6. Parameter Classification -- PASS

| Parameter | Classification | Notes |
|-----------|---------------|-------|
| g | Independent | Correct for a scan parameter |
| chi0 | Independent | Correct for a scan parameter |
| beta_lambda | Dependent (fixed) | Now correct: 9*g^4/(128*pi^2) |
| m_chi2 | Dependent | = beta_lambda * chi0^2 |
| gb_scalar | Dependent | = sqrt(beta_lambda) |
| delta_V | Dependent | = beta_lambda * chi0^4 / 16 |

The parameter basis correctly places the CW-fixed quartic under dependent. No scanning of dependent parameters.

---

## 7. Expression Format -- PASS

All expressions are valid Python/SymPy-compatible strings:
- `"9 * g**4 / (128 * pi**2)"` -- valid
- `"beta_lambda * chi0**2"`, `"beta_lambda * chi**2"` -- valid
- `"sqrt(beta_lambda)"` -- valid in sympy (note: the backend computes this internally)
- `"beta_lambda * chi0**4 / 16"` -- valid
- `"g**2 * chi**2 / 4"` -- valid
- `"g**2 * T**2"`, `"3 / 16 * g**2 * T**2"` -- valid

All symbols declared in `expression_symbols` or `parameter_basis` or `vev_convention`.

---

## 8. Backend Compatibility -- PASS

The model is compatible with `backend/semianalytic_pipeline.py`:
- boson_gbs: `{"W": "g/2"}`, boson_dofs: `{"W": 9}`
- No fermions
- Backend auto-computes scalar gb
- Backend evaluates CW relation internally

---

## 9. Non-Blocking Warnings

### W1: Stable dark sector and Delta N_eff (arXiv:2306.09411)

A completely secluded dark SU(2) sector without any coupling to the SM will contribute to Delta N_eff. Bringmann et al. (2023) found that stable dark sectors are strongly disfavored by BBN/CMB constraints. This is a known physical constraint on the model, not an inconsistency in the model formulation. It should be evaluated downstream by the constraint-agent.

### W2: Model not novel (arXiv:2109.11558)

The exact same model (SU(2)_D with one complex scalar doublet, CW mechanism, nHz GW target) was studied in Borah, Dasgupta, Kang (2021). This is a novelty consideration for the user, not a physical issue.

### W3: Debye mass note inconsistency

Minor error in the explanatory note for the gauge boson Debye mass: "N_s=2" should say "N_s=4 real scalars". The numerical value `g**2 * T**2` is correct.

---

## Summary

| Check | Result | Notes |
|-------|--------|-------|
| Field content | PASS | DoF count consistent before/after SSB |
| Lagrangian | PASS | All terms gauge-invariant |
| SSB pattern | PASS | SU(2) -> nothing; all generators broken |
| VEV convention | PASS | Standard (0, v/sqrt(2))^T |
| Field-dependent masses | PASS | m_W = g*chi/2 verified from covariant derivative |
| CW relation | FIXED | beta_lambda: 3 -> 9 (factor of 3 error) |
| Parameter classification | PASS | CW quartic correctly under dependent |
| Thermal masses | PASS | All expressions correct |
| Expression format | PASS | All Python/SymPy compatible |
| Backend compatibility | PASS | Directly compatible |