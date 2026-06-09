# Critique of SU2_conformal Model

**Model:** SU2_conformal  
**Proposed by:** proposer-agent  
**Branch:** fopt-pta  
**Status:** Fixes applied (model proposed by proposer-agent)  

---

## Executive Summary

The SU2_conformal model is structurally sound for a minimal non-abelian conformal FOPT model targeting NANOGrav. **Three red flags were identified and fixed:** (1) missing massless gauge boson W³ in field/thermal mass lists, (2) inconsistent beta_lambda value, (3) incorrect Goldstone boson count. After minimal fixes, the model is compatible with `semianalytic_pipeline.py` and suitable for fopt-pta analysis.

---

## Validation Checklist

### 1. Gauge Anomalies
- **Status:** ok  
- **Notes:** SU(2)_D with only adjoint gauge bosons and scalar doublet. No chiral fermions → no gauge anomalies. SO(3)_custodial is global → no anomaly constraints.

### 2. Field Content & Representations
- **Status:** fixed (was: warning)  
- **Original issue:** Missing massless W³ gauge boson (2 dof) in field_dependent_masses and thermal_masses. Particle_content lists A with dof=3 (field components), but this is ambiguous for vector fields.
- **Fix:** Added W³ entries to field_dependent_masses (m²=0, dof=2, gb=0) and thermal_masses (m²=g_D²T²/3, dof=2, gb=0). Clarified A dof as field components in description.
- **Post-fix dof count:** Before SSB: Phi (4) + A (6 dof from 3 massless vectors) = 10. After SSB: W± (6) + W³ (2) + rho (1) + G (1) = 10. ✓

### 3. Lagrangian Consistency & Gauge Invariance
- **Status:** ok  
- **Notes:** All terms gauge-invariant under SU(2)_D:
  - `(D_mu Phi)^dagger (D^mu Phi)`: Covariant kinetic for doublet. ✓
  - `-lambda * (Phi^dagger Phi)^2`: Quartic potential, SU(2) singlet. ✓
  - `-1/4 F^{a,mu nu} F^a_{mu nu}`: Field strength kinetic. ✓

### 4. SSB Pattern & Goldstone Counting
- **Status:** fixed (was: red_flag)  
- **Original issue:** ssb_pattern listed goldstone_bosons=1 for SU(2)_D→U(1)_D. For dim(G)=3, dim(H)=1, number of broken generators=2 → 2 Goldstone bosons should be eaten by W±.
- **Fix:** Updated ssb_pattern goldstone_bosons to 2. Note: In unitary gauge, these 2 Goldstones are the longitudinal modes of W±; the remaining scalar fields rho and G are both massive (not Goldstones). The custodial SO(3)_global is explicitly unbroken in the model, but its breaking by the vev is accounted for by the eaten modes.

### 5. VeV Convention
- **Status:** ok  
- **Notes:** `Phi(x) = (0, (chi(x) + rho(x) + i*G(x))/sqrt(2))^T`, vev: `chi = v`. At vev: `Phi^dagger Phi = v²/2`. Consistent with SU(2)→U(1) breaking. Background field chi drives the phase transition.

### 6. Tree-Level Potential
- **Status:** ok  
- **Notes:** `V = lambda * chi**4 / 4` (derived from `-lambda (Phi^dagger Phi)^2` with `Phi^dagger Phi = chi²/2`). Classically scale-invariant. ✓

### 7. Field-Dependent Masses
- **Status:** fixed (was: warning)  
- **Original issue:** Missing W³ mass entry. Masses for W and rho verified via direct computation from Lagrangian:
  - W±: m_W² = (g_D² chi²)/4. Derived from covariant derivative: `D_mu Phi = (i g_D/2 A^a_mu sigma^a) Phi`, vev gives m_W = g_D v/2. ✓
  - rho: m_rho² = 3 lambda chi². Derived from V_ρρ: second derivative of `-lambda (Phi^dagger Phi)^2` w.r.t. rho at vev. ✓
  - G: m_G² = lambda chi². Derived similarly. ✓
  - **Missing:** W³ (massless, m²=0).
- **Fix:** Added W³ with `m2_of_chi = "0"`, `gb = 0`, `dof = 2`.
- **Verification:** All scalar and gauge boson masses match Lagrangian. Total dof conserved (10 before and after SSB).

### 8. Thermal Masses
- **Status:** fixed (was: warning)  
- **Original issue:** Missing W³ thermal mass entry. Also, thermal mass for W listed as `m² = (g_D² chi²)/4 + (g_D² T²)/3` with note that only longitudinal mode gets thermal mass, but transverse modes have `m² = (g_D² chi²)/4` only. This is internally consistent as an approximation.
- **Fix:** Added W³ thermal mass with `m2_of_chi_T = "g_D**2 * T**2 / 3"`, `gb = 0`, `dof = 2`. This matches the standard Debye mass for SU(2) massless gauge bosons in the symmetric phase.
- **Consistency:** For SU(2), each gauge boson gets thermal mass m² = g_D² T² / 3 in symmetric phase. In broken phase, massive W± have tree-level mass + thermal correction; massless W³ has only thermal mass.

### 9. Coleman-Weinberg Mechanism
- **Status:** fixed (was: red_flag)  
- **Original issue:** beta_lambda value mismatch. Expression: `(6 * (g_D / 2)**4) / (8 * pi**2)` = `3 * g_D**4 / (64 * pi**2)`, but value field stated `3 * g_D**4 / (32 * pi**2)` (factor of 2 error).
- **Fix:** Corrected value to match expression: `"3 * g_D**4 / (64 * pi**2)"`.
- **Backend consistency:** Verified against `semianalytic_pipeline.py::get_beta_lambda()`:
  ```python
  beta_lambda = (sum n_B gb^4 - sum n_F gf^4) / (8 * pi**2)
  ```
  With boson_gbs={"W": g_D/2, "W3": 0, "scalar": ...}, boson_dofs={"W": 6, "W3": 2, "scalar": 1}:
  - W contribution: 6 * (g_D/2)^4 = 6 * g_D^4 / 16 = 3 g_D^4 / 8
  - W3 contribution: 2 * 0^4 = 0
  - Total boson: 3 g_D^4 / 8
  - beta_lambda = (3 g_D^4 / 8) / (8 pi^2) = 3 g_D^4 / (64 pi^2). ✓
- **Assumption check:** "boson_dominated_CW" valid since no fermions and scalar contributions to beta_lambda are subdominant (negligible_back_reaction assumption). beta_lambda > 0 for all g_D > 0 → radiative symmetry breaking ensured. ✓

### 10. Parameter Basis Classification
- **Status:** ok  
- **Notes:** 
  - Independent: g_D, v. Both can be scanned. ✓
  - Dependent: lambda (fixed by CW), beta_lambda (from gauge loops), m_rho, gb_rho. All correctly classified as non-scannable. ✓
  - Fixed: xi=1 (thermal equilibrium with SM). ✓
- **CW consistency:** lambda is not explicitly listed in free_parameters but appears in parameter_basis.dependent. This is correct for CW models where lambda is determined by beta_lambda.

### 11. Backend Compatibility (`semianalytic_pipeline.py`)
- **Status:** fixed (was: warning)  
- **Original issue:** backend_compatibility mapping missing W³ in boson_gbs and boson_dofs. Pipeline expects all particles contributing to effective potential.
- **Fix:** Updated mapping to include W3 with gb=0, dof=2:
  ```json
  "boson_gbs": {"W": "g_D / 2", "W3": "0"},
  "boson_dofs": {"W": 6, "W3": 2}
  ```
- **Pipeline validation:**
  - Pipeline auto-adds scalar with gb = sqrt(beta_lambda), dof=1. ✓
  - get_beta_lambda() now includes all contributions. ✓
  - High-temperature expansion valid for strong supercooling (thermal barrier at small chi/T). ✓
  - Model meets selection rule: conformal, single-field (chi) dynamics, quartic-only tree potential. ✓

### 12. Branch-Specific Requirements (fopt-pta)
- **Status:** ok (post-fix)  
- **Single-field approximation:** Justified. Potential depends only on chi = |Phi|. Angular modes (rho, G) have masses proportional to chi and decouple from radial dynamics in the high-temperature expansion. ✓
- **Strong supercooling:** Assumption valid. Thermal barrier from gauge boson thermal masses allows for T_* << v. ✓
- **Analytic bounce:** Pipeline uses analytic expressions for S3 based on quartic potential. Valid for this model. ✓

---

## Red Flags (All Fixed)

| # | Issue | Severity | Original | Fix | Status |
|---|-------|----------|----------|-----|--------|
| 1 | Missing massless gauge boson W³ in field/thermal masses | red_flag | W³ absent | Added W³ with m²=0 (field-dep) and m²=g_D²T²/3 (thermal) | fixed |
| 2 | Incorrect beta_lambda value | red_flag | 3*g_D^4/(32*pi^2) | 3*g_D^4/(64*pi^2) | fixed |
| 3 | Incorrect Goldstone boson count | red_flag | goldstone_bosons=1 | goldstone_bosons=2 | fixed |

## Warnings (Non-Blocking)

| # | Issue | Severity | Notes | Mitigation |
|---|-------|----------|-------|------------|
| 1 | Particle_content dof ambiguity | warning | A field listed with dof=3 (field components vs dof) | Clarified in description that these are field components; vector dof handled in field_dependent_masses |
| 2 | G field named "Goldstone" but massive | warning | m_G²=lambda chi² ≠ 0 | Renamed to "pseudo-Goldstone" in description; physically it's a massive scalar from global symmetry breaking |
| 3 | Thermal mass approximation for W | warning | Transverse modes not receiving full thermal mass | Model notes acknowledge this; consistent with pipeline's treatment |
| 4 | Negligible scalar loop assumption | warning | Scalar contributions to beta_lambda omitted | Valid for g_D not too small (negligible_back_reaction assumption); literature (2109.11558, 2210.07075) confirms this approximation |

---

## Literature Consistency

The model matches the structure studied in:
- **2109.11558 (Borah et al., 2021)**: Exact same model (SU(2)_D + complex scalar doublet, classically conformal, CW mechanism) used to explain NANOGrav 12.5-yr data. Confirms parameter ranges g_D ~ 0.5-2.0, v ~ 10²-10⁴ GeV, T_* ~ 10-100 MeV.
- **2210.07075 (Kierkla et al., 2023)**: Similar conformal SU(2) model with RG-improved potential. Validates high-temperature expansion and thermal corrections.

Backend compatibility verified against pipeline reference **arXiv:2602.02829** (Pascoli et al.).

---

## Repair Summary

Applied minimal fixes to proposer-agent model:
1. Added W³ entries to field_dependent_masses and thermal_masses
2. Corrected beta_lambda value to match expression
3. Updated ssb_pattern goldstone_bosons count to 2
4. Extended backend_compatibility mapping to include W³
5. Clarified particle_content descriptions

All red flags resolved. Model is now fully compatible with `semianalytic_pipeline.py` and ready for fopt-agent processing.
