# Prior Audit Report: SU2_conformal Model

**Agent:** prior-agent  
**Date:** 2026-06-07  
**Branch:** fopt-pta  
**Model:** SU2_conformal (SU(2)_D gauge group + complex scalar doublet, classically conformal)  
**Status:** ok  

---

## Executive Summary

This report audits all assumptions, priors, approximations, uncertainties, validity domains, caveats, limitations, and warnings across the complete SU2_conformal pipeline workflow. The audit identifies **42 items** (15 assumptions/priors, 6 approximations, 6 uncertainties, 4 validity domain caveats, 4 limitations, 4 warnings) with **severity scores ranging from 2 to 9** (scale: 1-10, higher = more serious).

### Critical Findings (Severity 8-9)

| ID | Severity | Category | Description |
|----|----------|----------|-------------|
| no_portal_interactions | 9 | Model-building assumption | SM-Higgs portal and kinetic mixing neglected → secluded dark sector |
| uncertainty_large_alpha | 9 | Theoretical | alpha up to 10^16 in PTA region; approximations may break down |
| warning_strong_supercooling | 9 | Theoretical | Strong supercooling regime affects multiple approximations |
| validity_high_T_supercool | 9 | Validity domain | High-T expansion may be invalid in T_* << v regime |
| approx_high_T_expansion | 8 | Computational | High-T expansion for thermal potential (core uncertainty) |
| uncertainty_eternal_inflation | 8 | Computational | 50% scan failure due to eternal inflation |
| uncertainty_f_peak_below_PTA | 8 | Observational | Spectra peak below PTA frequency range |
| uncertainty_parameter_shift | 8 | Model-building | v ~ 0.6-1.3 GeV vs original [100, 1e6] GeV range |
| coupled_to_SM_thermally | 8 | Theoretical | xi=1 assumed without coupling mechanism justification |
| prior_v_fopt | 7 | Prior | FOPT scan v range differs from model range by orders of magnitude |

### Control Status

- **Controlled items:** 13/42 (31.0%)
- **Uncontrolled items:** 29/42 (69.0%)
- **High-severity uncontrolled:** 15 items (severity >= 8)

### Key Recommendations

1. **HIGH PRIORITY:** Validate high-temperature expansion and all approximations in strong supercooling regime (3D EFT methods needed)
2. **HIGH PRIORITY:** Add SM portal couplings (epsilon, lambda_HPhi) and re-study FOPT and constraints
3. **MEDIUM PRIORITY:** Reconcile FOPT scan range with original model motivation
4. **MEDIUM PRIORITY:** Implement RG running of couplings
5. **MEDIUM PRIORITY:** Compute scalar decays for BBN analysis
6. **MEDIUM PRIORITY:** Compute DM self-interaction cross sections
7. **MEDIUM PRIORITY:** Compute dark sector thermal history for N_eff analysis

---

## 1. Upstream Status

All upstream handoffs are validated with status `ok`:

| File | Agent | Status |
|------|-------|--------|
| handoff_model.json | critic-agent | ok |
| handoff_librarian_preliminary.json | preliminary-librarian-agent | ok |
| handoff_critique.json | critic-agent | ok |
| handoff_fopt.json | fopt-agent | ok |
| handoff_pta.json | pta-agent | ok |
| handoff_constraints.json | constraint-agent | ok |

---

## 2. Model-Building Assumptions

### 2.1 Core Model Structure

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| minimal_field_content | 6 | No | Only Phi (doublet) + SU(2)_D gauge bosons; no fermions/extra scalars | Simplifies dynamics; may limit parameter space | Add fields for robustness testing |
| classical_conformal_invariance | 8 | No | Tree-level potential: V = -lambda (Phi^dagger Phi)^2 only | Defines conformal model class; all masses radiative | Consider explicit mass terms |
| no_portal_interactions | **9** | **No** | **SM-Higgs portal and kinetic mixing neglected** | **FOPT analysis dark-sector only; secluded model** | **Add portal couplings** |
| custodial_symmetry | 5 | Yes | SO(3) custodial symmetry protects vector DM | Stabilizes DM candidates | Verify implications |
| unspecified_DM_candidate | 5 | No | Model doesn't specify DM candidate | Ambiguous interpretation | State DM candidate explicitly |

**Critical Assessment:** The `no_portal_interactions` assumption is the most severe model-building choice. While it simplifies the FOPT analysis to the dark sector only, it makes the model **secluded**, severely limiting:
- Applicability of collider/beam-dump constraints (most become N/A)
- Dark matter production mechanisms (requires non-thermal or gravitational production)
- Cosmological connections to SM (xi=1 is assumed but not motivated)

### 2.2 Thermal Assumptions

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| thermal_equilibrium_dark | 7 | Yes | Dark sector in thermal equilibrium with itself | Validates thermal potential | Verify conditions |
| coupled_to_SM_thermally | **8** | **No** | **T_D = T_SM (xi = 1) assumed** | **Affects Hubble rate, g_star, FOPT** | **Study xi != 1** |
| strong_supercooling | 7 | No | T_* << v regime assumed | Justifies high-T expansion | Validate in this regime |
| boson_dominated_CW | 5 | Yes | Gauge loops dominate beta_lambda | Valid for g_D not too small | Include scalar loops |

**Critical Assessment:** The `coupled_to_SM_thermally` assumption (xi=1) lacks physical motivation. Without portal couplings, there's no mechanism to maintain thermal equilibrium with the SM bath. This is internally inconsistent.

---

## 3. Parameter Priors

### 3.1 Original Model Ranges

| Parameter | Range | Justification | Severity | Controlled |
|-----------|-------|---------------|----------|------------|
| g_D | [0.01, 12.56] | Perturbativity (g_D < 4π) | 3 | Yes |
| v | [100, 10^6] GeV | FOPT temperature range for PTA | 4 | No |

### 3.2 FOPT Scan Ranges

| Parameter | Range | Issue | Severity | Controlled |
|-----------|-------|-------|----------|------------|
| g_D | [0.5, 3.0] | Narrower than model range | 4 | No |
| v | [0.01, 10] GeV | **Much lower than model range** | **7** | **No** |

**Critical Assessment:** The FOPT scan used **v ∈ [0.01, 10] GeV** vs original **[100, 10^6] GeV**, a **2-3 order of magnitude shift**. This was necessary to obtain f_peak in the PTA frequency band, but:
- Changes all particle masses significantly (m_W ~ 0.28-0.64 GeV in PTA region)
- May be inconsistent with original model motivation
- Requires reconciliation with literature (2109.11558 reports sub-GeV T_* for v ~ 100 GeV)

### 3.3 PTArcade Campaign Priors

- **log10_g_D:** Uniform(-0.3010, 0.4771) → g_D ∈ [0.5, 3.0]
- **log10_v_GeV:** Uniform(-2.0, 1.0) → v ∈ [0.01, 10] GeV
- **Status:** Standard log-uniform priors for Bayesian inference; controlled (severity 3)

### 3.4 PTA-Preferred Region (1-sigma)

- **g_D:** [0.9105, 0.9755]
- **v:** [0.6265, 1.3038] GeV
- **Derived masses:** m_W ∈ [0.2852, 0.6359] GeV, m_rho ∈ [0.0358, 0.0855] GeV, m_G ∈ [0.0179, 0.0428] GeV

---

## 4. Computational Approximations

### 4.1 Thermal Effective Potential

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| approx_high_T_expansion | **8** | **No** | **High-T expansion (small field/T regime)** | **Core to all FOPT calculations** | **3D EFT needed** |
| approx_no_daisy | **7** | **No** | **No Daisy resummation for thermal masses** | **IR-divergent terms not resummed** | **Implement Daisy** |
| approx_fixed_renormalization | **7** | **No** | **Fixed mu = v, no RG running** | **Scale dependence not quantified** | **Implement RG running** |

**Critical Assessment:** These three approximations are **interrelated and critical** for the strong supercooling regime:
- High-T expansion may break down when T_* << v
- Daisy resummation is particularly important for supercooled transitions (2312.12413)
- Fixed renormalization scale introduces unquantified scale uncertainty
- Literature (2210.07075) uses RG-improved effective potential

### 4.2 Percolation and Nucleation

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| approx_gaussian_percolation | 6 | No | Gaussian approximation for false vacuum fraction | Percolation temperature accuracy | Exact criterion |

### 4.3 Coleman-Weinberg Mechanism

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| approx_CW_automatic | 5 | Yes | lambda from beta_lambda = 3*g_D^4/(64*pi^2) | CW relation accuracy | Verify implementation |
| limitation_scalar_loop | 5 | Yes | Scalar loops omitted from beta_lambda | CW beta function | Include scalar loops |

### 4.4 GW Spectrum Template

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| approx_bulk_flow_template | 6 | No | dbf template with vw=1.0, cs=1/sqrt(3) | GW spectrum shape/amplitude | Study vw, cs dependence |

**Note:** dbf template from 2511.15687 was correctly selected (valid for alpha >> 0.5), but extrapolation to alpha ~ 10^16 is uncertain.

---

## 5. Major Uncertainties

### 5.1 Theoretical Uncertainties

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| uncertainty_large_alpha | **9** | **No** | **alpha up to 10^16 in PTA region** | **All approximations may break down** | **Systematic validation** |
| warning_strong_supercooling | **9** | **No** | **Strong supercooling (alpha >> 0.5)** | **Multiple approximations affected** | **3D EFT methods** |
| validity_high_T_supercool | **9** | **No** | **High-T expansion validity in T_* << v** | **Nucleation rate, FOPT parameters** | **Alternative methods** |

**Critical Assessment:** The **large alpha values (up to 10^16)** are a defining feature of this model in the PTA-preferred region. This is **both a prediction and a major uncertainty**, as:
- Standard approximations (high-T expansion, Daisy resummation, Gaussian percolation) may not be valid
- Perturbative calculations may break down
- GW spectrum template validation is unclear at such extreme values
- Literature (2312.12413) explicitly discusses EFT challenges for supercooled transitions

### 5.2 Computational Uncertainties

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| uncertainty_eternal_inflation | **8** | **No** | **50% scan failure due to eternal inflation** | **Incomplete parameter space** | **Investigate criterion** |
| uncertainty_T_peak_discrepancy | 7 | No | Backend vs literature T_p discrepancy | FOPT temperature | Reconcile conventions |

**Critical Assessment:** The **50% failure rate** is exceptionally high and indicates:
- Significant parameter space may be physically invalid (eternal inflation)
- Numerical issues in the backend
- Need to understand if this is a physical or computational limitation

### 5.3 Observational Uncertainties

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| uncertainty_f_peak_below_PTA | **8** | **No** | **All spectra peak at lowest PTA bin** | **PTA signal interpretation** | **Extend frequency range** |

**Critical Assessment:** If the **actual GW peak is below PTA sensitivity**, then:
- The model cannot explain the NANOGrav signal as currently formulated
- The PTA-preferred region may be an artifact of the frequency window
- Need to verify if the spectrum can be adjusted to peak within PTA range

### 5.4 Model-Building Uncertainties

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| uncertainty_parameter_shift | **8** | **No** | **v ~ 0.6-1.3 GeV vs [100, 1e6] GeV** | **Mass scale, phenomenology** | **Re-evaluate motivation** |
| uncertainty_secluded_sector | 7 | No | No portal couplings; secluded sector | Testability, constraints | Add portals |

---

## 6. Validity Domains

### 6.1 Perturbativity

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| validity_perturbativity | 5 | Yes | g_D < 4π ~ 12.56 assumed | Calculations | Monitor perturbativity |

### 6.2 High-T Expansion

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| validity_high_T_supercool | **9** | **No** | **Valid when T^2 >> m^2; may break down** | **Core FOPT calculations** | **3D EFT needed** |

### 6.3 Template Validity

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| validity_alpha_template | 6 | Yes | dbf valid for alpha >> 0.5; higgsless for alpha <= 0.5 | GW spectrum | Validate at extreme alpha |
| validity_no_portal | 6 | Yes | Constraints with portals N/A due to epsilon=0, lambda_HPhi=0 | Experimental | Document clearly |

---

## 7. Limitations

### 7.1 Cosmological Limitations

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| limitation_bbn | 7 | No | Light scalars may affect BBN | BBN predictions | Compute decays |
| limitation_neff | 6 | No | Dark sector may contribute to N_eff | CMB observations | Compute thermal history |

**Critical Assessment:** In the PTA-preferred region:
- **m_rho ~ 36-86 MeV**, **m_G ~ 18-43 MeV** → BBN constraints may apply if lifetimes > 1s
- Without portal couplings, scalars are **stable on cosmological timescales** (only gravitational decays)
- Dark sector thermal history **not computed**; decoupling temperature unknown
- If T_reh > T_CMB, particles could be reheated and contribute to N_eff

### 7.2 Astrophysical Limitations

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| limitation_self_interaction | 7 | No | DM self-interaction ~ 10^{-2} to 1 cm^2/g | Structure formation | Compute scattering |

**Critical Assessment:** Vector DM self-interaction cross section:
- σ/m ~ g_D^4 / m_W^2 ~ (0.9)^4 / (0.5 GeV)^2 ~ 10^{-2} to 1 cm^2/g
- **Galactic constraints:** σ/m < 0.1 cm^2/g
- **Cluster constraints:** σ/m < 1 cm^2/g
- **→ May be marginally allowed or excluded depending on exact values**
- Requires explicit computation of scattering amplitudes

### 7.3 Computational Limitations

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| limitation_no_running | 6 | No | No RG running; fixed mu = v | Scale dependence | Implement RG |

---

## 8. Documentation Caveats

### 8.1 Minor Issues

| ID | Severity | Controlled | Description | Impact | Resolution |
|----|----------|------------|-------------|--------|------------|
| caveat_dof_ambiguity | 2 | Yes | Gauge boson dof=3 ambiguous | Documentation | Clarified |
| caveat_G_named_goldstone | 2 | Yes | G is massive, not Goldstone | Naming | Renamed |
| caveat_thermal_mass_uniform | 4 | Yes | Thermal mass same for all dof | Accuracy | Investigate |

**Status:** Documentation issues are minor and mostly resolved.

---

## 9. Required Follow-ups (Priority Order)

### 9.1 High Priority

1. **validate_high_T_in_supercooling** (HIGH)
   - **Issue:** High-T expansion may be invalid in strong supercooling regime
   - **Blocked by:** approx_high_T_expansion, approx_no_daisy, limitation_no_running
   - **Action:** Implement 3D EFT (dimensional reduction) methods
   - **References:** 2312.12413, 2210.07075

2. **add_portal_couplings** (HIGH)
   - **Issue:** No SM portal couplings; secluded sector limits constraints
   - **Blocked by:** no_portal_interactions, uncertainty_secluded_sector
   - **Action:** Extend model with epsilon (kinetic mixing) and lambda_HPhi (Higgs portal)
   - **Impact:** Enables collider/beam-dump constraints; DM production via portals

### 9.2 Medium Priority

3. **extend_scan_range** (MEDIUM)
   - **Issue:** FOPT scan v range differs from original model range
   - **Blocked by:** prior_v_fopt, uncertainty_parameter_shift
   - **Action:** Run scans with v ∈ [100, 1e6] GeV; investigate why PTA prefers low v

4. **compute_scalar_decays** (MEDIUM)
   - **Issue:** BBN impact of light scalars unknown
   - **Blocked by:** limitation_bbn
   - **Action:** Develop backend for scalar decay calculations

5. **compute_DM_self_interaction** (MEDIUM)
   - **Issue:** DM self-interaction cross sections unknown
   - **Blocked by:** limitation_self_interaction
   - **Action:** Develop backend for dark sector scattering

6. **compute_thermal_history** (MEDIUM)
   - **Issue:** Dark sector thermal history and decoupling unknown
   - **Blocked by:** limitation_neff
   - **Action:** Develop backend for thermal history computation

7. **implement_RG_running** (MEDIUM)
   - **Issue:** Fixed renormalization scale; no RG running
   - **Blocked by:** limitation_no_running, approx_fixed_renormalization
   - **Action:** Add RG running to backend

---

## 10. Summary Statistics

### 10.1 Severity Distribution

| Severity | Total | Controlled | Uncontrolled |
|----------|-------|------------|--------------|
| 2 | 2 | 2 | 0 |
| 3 | 2 | 2 | 0 |
| 4 | 3 | 1 | 2 |
| 5 | 6 | 5 | 1 |
| 6 | 8 | 2 | 6 |
| 7 | 10 | 1 | 9 |
| 8 | 7 | 0 | 7 |
| 9 | 4 | 0 | 4 |
| **Total** | **42** | **13** | **29** |

### 10.2 Category Distribution

| Category | Count | Average Severity | Controlled |
|----------|-------|------------------|------------|
| model_building | 7 | 6.0 | 2/7 |
| theoretical | 7 | 6.4 | 3/7 |
| parameter_range | 5 | 4.8 | 3/5 |
| computational | 11 | 6.9 | 2/11 |
| validity_domain | 4 | 6.5 | 2/4 |
| cosmological | 2 | 6.5 | 0/2 |
| astrophysical | 1 | 7 | 0/1 |
| documentation | 2 | 2.5 | 2/2 |
| warning | 4 | 7.5 | 0/4 |

### 10.3 Control Status by Severity

| Severity Range | Total | Controlled | Uncontrolled | % Controlled |
|---------------|-------|------------|--------------|--------------|
| 1-5 | 13 | 12 | 1 | 92.3% |
| 6-7 | 18 | 3 | 15 | 16.7% |
| 8-10 | 11 | 0 | 11 | 0.0% |

---

## 11. Conclusion

The SU2_conformal pipeline has **significant uncontrolled uncertainties** concentrated in three areas:

1. **Strong supercooling regime** (alpha >> 0.5, up to 10^16): The core computational approximations (high-T expansion, no Daisy resummation, fixed renormalization scale) may not be valid in this regime. This is the **most critical theoretical uncertainty**.

2. **Secluded sector assumption**: The lack of SM portal couplings (epsilon=0, lambda_HPhi=0) makes the model **secluded**, limiting the applicability of most experimental constraints and DM production mechanisms. This is the **most critical model-building assumption**.

3. **Parameter range shift**: The FOPT scan used v ∈ [0.01, 10] GeV vs the original [100, 1e6] GeV, changing all mass scales by 2-3 orders of magnitude. This requires **reconciliation with the original model motivation and literature**.

### Recommendations

- **Do not trust FOPT and GW predictions at face value** without validating approximations in the strong supercooling regime
- **Add portal couplings** to make the model testable and physically complete
- **Re-run scans** with the original v range to understand the parameter shift
- **Implement 3D EFT methods** for more reliable supercooled transition calculations
- **Develop backends** for scalar decays, DM scattering, and thermal history to address cosmological limitations

### Overall Assessment

The SU2_conformal model can **potentially explain the NANOGrav signal** as shown by the PTA analysis, but the **theoretical uncertainties are substantial**. The **strong supercooling regime** and **secluded sector assumption** introduce controlled and uncontrolled uncertainties that affect the reliability of the predictions. Addressing the high-priority follow-ups would significantly improve the robustness of the results.

---

*This report was generated by the prior-agent following the prior-audit skill instructions. All upstream handoffs were inspected and cross-referenced with literature where applicable.*
