# Prior Audit Report: Dark U(1) Conformal Model (u1conformal)

**Generated:** 2026-06-10
**Agent:** prior-agent
**Branch:** prior_audit

---

## 1. Executive Summary

This report audits all assumptions, priors, approximations, uncertainties, validity domains, caveats, limitations, and warnings across the entire Dark U(1) conformal model pipeline. The audit covers the model specification, literature context, FOPT computation, PTA analysis (including PTArcade Bayesian inference), and constraint evaluation.

**Total audit items identified: 38**, spanning severities 1-10.

### Key Findings by Severity

- **Severity 8-10 (critical uncontrolled issues):** 6 items
  - Unspecified portal couplings (A-003, A-020, A-021)
  - xi=1 thermalization assumption and Delta N_eff tension (A-004, A-024)
  - Contradictory assumptions about portals (A-005)
  - Missing decay width/freeze-in modules (A-038)

- **Severity 5-7 (significant uncertainties):** 13 items
  - FOPT approximations: fixed-scale CW, high-T expansion validity, beta/H breakdown for supercooled regime
  - GW spectrum: dbf template calibration range, runaway wall assumption, reheating computation
  - Sampling: PTArcade convergence diagnostics unreported
  - Literature: Athron challenge not directly addressed

- **Severity 1-4 (controlled or minor):** 19 items

### Central Tension

The model faces a core unresolved tension between:
1. **xi = 1 assumption** (thermalized sectors, hardcoded in backend)
2. **Unspecified small portal couplings** (epsilon, lambda_HPhi)

These are needed simultaneously: portals must be large enough for thermalization (epsilon >= 10^{-10}) but small enough to not affect FOPT dynamics. Furthermore, Delta N_eff ~ 0.57 from xi=1 exceeds Planck bounds. This tension propagates through the constraint analysis, where 19 of 23 constraints are unblocked only by specifying portal values.

---

## 2. Upstream Status Summary

| Handoff | Agent | Status | Key Issues |
|---------|-------|--------|------------|
| handoff_model.json | critic-agent | ok | 5 warnings: unspecified portals, xi=1, RG scheme, no DM |
| handoff_critique.json | critic-agent | ok | 0 red flags, 5 warnings |
| handoff_librarian_preliminary.json | preliminary-librarian-agent | ok | Model not_novel. 10 papers. Literature benchmarks provided. |
| handoff_fopt.json | fopt-agent | ok | 925 points, 680 viable, 204 numerical failures, 41 physical failures |
| handoff_pta.json | pta-agent | ok | 1600 benchmark points, PTArcade posteriors. Partial chain caveat. |
| handoff_constraints.json | constraint-agent | ok | 23 constraints. 4 directly testable (all passed). 19 blocked by unspecified portals. |

---

## 3. Assumption Inventory by Category

### 3.1 Model-Building Assumptions (Severity 3-9)

| ID | Item | Severity | Controlled? |
|----|------|----------|-------------|
| A-001 | Classical scale invariance | 3 | Yes (verified by critic) |
| A-002 | No fermionic DM | 4 | Yes (deliberate choice) |
| A-003 | Portal couplings unspecified (epsilon, lambda_HPhi) | 8 | **No** |
| A-004 | xi = T_dark/T_SM = 1 hardcoded | 8 | **No** |
| A-005 | Portals small for FOPT but large enough for thermalization | 9 | **No** |
| A-006 | No tree-level cross-quartic with SM Higgs | 3 | No (bound missing) |
| A-035 | Interpolated g_star(T) for SM particle content | 2 | Yes |

**Critical insight:** A-003, A-004, and A-005 form a chain of unresolved assumptions. Without knowing epsilon, one cannot verify thermalization (A-004) or the 'small portal' assumption (A-003). The constraint analysis cannot apply 19/23 constraints.

### 3.2 CW Mechanism and FOPT Computation (Severity 2-7)

| ID | Item | Severity | Controlled? |
|----|------|----------|-------------|
| A-007 | One-loop CW with fixed-scale logs, no RG improvement | 7 | **No** |
| A-008 | Daisy resummation via Arnold-Espinosa | 3 | Yes |
| A-009 | High-temperature expansion validity for extreme supercooling | 5 | **No** |
| A-010 | Gaussian approximation for false vacuum fraction | 4 | **No** |
| A-011 | beta/H parameterization may break down for supercooled regime | 7 | **No** |
| A-016 | CW-fixed scalar quartic (not scanned independently) | 2 | Yes |

**Key finding:** The fixed-scale CW approximation (A-007) is a known systematic uncertainty. Christiansen et al. (2025, arXiv:2511.02910) showed that proper RG running is essential for the conformal Abelian Higgs model, and the simpler approximation may give quantitatively different results. The high-T expansion (A-009) may be formally invalid for the deepest supercooling (T ~ 10^{-6} GeV, m_A'/T ~ O(100-1000)). The beta/H parameterization (A-011) is also known to break down for alpha >> 1, where mean bubble separation R* is the correct variable.

### 3.3 GW Spectrum Modeling (Severity 2-5)

| ID | Item | Severity | Controlled? |
|----|------|----------|-------------|
| A-012 | Single dbf template (no averaging/marginalization) | 4 | **No** |
| A-013 | dbf calibration range may be pushed for alpha~10^11-10^15 | 5 | **No** |
| A-014 | Runaway bubble walls (v_w -> 1) assumed | 5 | **No** |
| A-030 | GW source type (sound waves vs collisions) debated | 5 | **No** |
| A-034 | No non-Gaussianity, polarization, or c_s(f) effects | 2 | No |

**Key finding:** The dbf template choice is physically motivated (most appropriate for alpha >> 1), but the extreme alpha values (10^11-10^15) in the PTA-preferred region may exceed the calibration range of the template. Additionally, the runaway wall assumption (also built into dbf) has not been verified against NLO friction calculations.

### 3.4 PTA Bayesian Inference (Severity 3-6)

| ID | Item | Severity | Controlled? |
|----|------|----------|-------------|
| A-018 | No convergence diagnostics (R-hat, ESS) reported | 6 | **No** |
| A-019 | Prior sensitivity not checked | 4 | **No** |
| A-031 | Benchmark scan uses simple bin-counting, not likelihood | 4 | **No** |
| A-032 | Bayes factor vs SMBHB not computed | 5 | **No** |
| A-033 | PTArcade used partial chains (~5700 post-burn-in samples) | 5 | **No** |
| A-037 | MAP vs benchmark BP1 v differs by factor ~2.5 | 3 | No |

**Key finding:** The PTArcade inference posterior (v ~ [0.62, 1.23] GeV, g_D ~ [0.509, 0.545]) is the main quantitative output, but its robustness is limited by: (a) partial chain samples, (b) no formal convergence diagnostics, and (c) no Bayes factor for model comparison. The discrepancy between PTArcade MAP (v=1.07 GeV) and benchmark BP1 (v=0.43 GeV) highlights the limitations of the simple benchmark scoring method.

### 3.5 Experimental Constraints (Severity 1-10)

| ID | Item | Severity | Controlled? |
|----|------|----------|-------------|
| A-020 | epsilon unspecified: all A' constraints blocked | 8 | **No** |
| A-021 | lambda_HPhi unspecified: all rho constraints blocked | 8 | **No** |
| A-022 | BBN gives LOWER bound on epsilon (often misunderstood) | 5 | **No** |
| A-023 | Visible vs invisible A' decay competition uncomputed | 6 | **No** |
| A-024 | Delta N_eff ~ 0.57 > Planck 0.3 bound | 9 | **No** |
| A-025 | rho freeze-in yield uncomputed | 7 | **No** |
| A-026 | Partial coverage of rho constraints (30-50 MeV gap) | 3 | No |
| A-036 | Theory constraints (4) all satisfied | 1 | Yes |
| A-038 | No backend modules for decay widths/freeze-in/xi(T) | 10 | **No** |

**Critical finding:** This is the most impactful category. Only 4 of 23 constraints are directly testable (and all pass: perturbativity, CW consistency, scale invariance). The remaining 19 require either epsilon, lambda_HPhi, or dedicated computation modules that do not exist. The Delta N_eff constraint (A-024) is arguably the most serious: with xi=1 and 4 dark dofs, Delta N_eff ~ 0.57, exceeding the Planck 95% CL bound of 0.3.

---

## 4. Controlled vs Uncontrolled Uncertainties

| Severity Range | Controlled Items | Uncontrolled Items |
|----------------|-----------------|-------------------|
| 1-3 | A-001, A-008, A-016, A-017, A-028, A-035, A-036 | A-006, A-026, A-034, A-037 |
| 4-6 | A-002 | A-009, A-010, A-012, A-013, A-014, A-015, A-019, A-022, A-023, A-027, A-029, A-030, A-031, A-032, A-033 |
| 7-10 | - | A-003, A-004, A-005, A-007, A-011, A-018, A-020, A-021, A-024, A-025, A-038 |

**12 items are controlled** (mostly model-building choices and standard approximations that are verified or well-established).
**26 items are uncontrolled**, encompassing the major uncertainties that affect the interpretation of results.

---

## 5. Severity Distribution

- **Severity 10** (1 item): Missing backend modules for decay widths/freeze-in/thermal history -- blocks all experimental constraints.
- **Severity 9** (2 items): Delta N_eff tension from xi=1; contradictory portal assumptions.
- **Severity 8** (3 items): Unspecified portals blocking all constraint applications; xi=1 hardcoded.
- **Severity 7** (3 items): Fixed-scale CW approximation; beta/H breakdown for supercooled transitions; rho freeze-in uncomputed.
- **Severity 6** (5 items): Reheating computation incompleteness; PTArcade convergence diagnostics; invisible vs visible decay competition; Athron challenge; visible/invisible branching computation.
- **Severity 5** (5 items): High-T expansion validity; dbf calibration range; runaway wall assumption; BBN lower bound understanding; GW source modeling; Bayes factor missing; partial chains.
- **Severity 4** (5 items): Gaussian approximation; single template; prior sensitivity; numerical failures; benchmark scoring metric.
- **Severity 3** (4 items): Scale invariance; no DM; g_star interpolation; portal cross-quartic; MAP discrepancy; partial constraint coverage; eternal inflation.
- **Severity 2** (5 items): CW-fixed quartic; non-Gaussianity; g_star; theory constraints.
- **Severity 1** (1 item): Theory constraint satisfaction.

---

## 6. Ten Most Important Uncontrolled Uncertainties

Ranked by combined severity and impact on final interpretation:

1. **Severity 10: Missing computational modules** (A-038). The pipeline cannot compute A' decay widths, rho lifetimes, freeze-in yields, or dark sector thermal history. Without these, 19 of 23 experimental constraints cannot be definitively applied.

2. **Severity 9: Delta N_eff from dark radiation** (A-024). With xi=1 and 4 dark dofs, Delta N_eff ~ 0.57, exceeding Planck 95% CL bound (0.3). The supercooled PT may dilute this away, but the computation has not been done.

3. **Severity 9: Contradictory portal assumptions** (A-005). Portals must simultaneously be 'small enough for FOPT' and 'large enough for thermalization (xi=1)'. These are quantitative constraints that have not been reconciled.

4. **Severity 8: Unspecified epsilon** (A-020). Without epsilon, no dark photon constraint (LHCb, BaBar, NA64, NA62, BBN) can be applied. The viable window 10^{-9} < epsilon < 10^{-4} exists but cannot be verified.

5. **Severity 8: Unspecified lambda_HPhi** (A-021). Without the Higgs portal coupling, no dark scalar constraint (BBN, CMB, beam dumps, Higgs decays) can be applied.

6. **Severity 8: Hardcoded xi=1** (A-004). The literature (Li & Nath 2026) shows xi can change GW predictions by up to 4 orders of magnitude. The hardcoded assumption does not capture this.

7. **Severity 7: Fixed-scale CW approximation** (A-007). No RG improvement or scheme comparison. The literature (Christiansen et al. 2025) shows this matters for conformal models.

8. **Severity 7: beta/H breakdown for supercooled transitions** (A-011). The proper variable for strong supercooling is mean bubble separation R*, not beta/H. Using beta/H may introduce systematic errors in GW amplitude.

9. **Severity 7: rho freeze-in yield uncomputed** (A-025). Without this, the cosmological beam dump constraints (BBN+CMB) cannot be evaluated, leaving the rho viability unknown.

10. **Severity 6: PTArcade convergence diagnostics missing** (A-018). No R-hat or effective sample size reported for the 2D posterior from ~5700 post-burn-in samples.

---

## 7. What Could Still Be Missing? (Literature-Informed Insights)

Beyond the items explicitly documented in upstream handoffs, the following issues were identified through literature search and reasoning:

1. **Gauge dependence of the effective potential**: The backend computes the effective potential and tunneling action in a fixed gauge. Feng & Zhang (2026, arXiv:2602.14866) show that Nielsen identities can make predictions gauge-independent, but this is not yet standard practice. The current pipeline does not address gauge dependence.

2. **Cannibalism regime in the dark sector**: For strongly supercooled transitions, the dark sector may enter a cannibalism regime where number-changing interactions (3->2) maintain thermal contact. This changes the equation of state and affects the GW spectrum (arXiv:2602.14324).

3. **Bubble wall profile and thickness effects**: The dbf template assumes thin-wall bubbles. For strongly supercooled transitions with very high alpha, bubble walls may be thick, modifying the GW spectrum shape (arXiv:2005.13537).

4. **Temperature-dependent sound speed**: In strongly supercooled transitions, the sound speed can deviate from c_s^2 = 1/3 in the plasma, affecting the GW spectrum from sound waves (if relevant).

5. **Effective number of relativistic species at reheating**: The fixed g* ~ 10 approximation may miss reheating temperature evolution, as g* changes rapidly in the MeV-GeV range due to QCD phase transition and muon/electron annihilations.

6. **Neutrino decoupling during the PT epoch**: If the supercooled FOPT occurs near the MeV scale, it could affect neutrino decoupling, which is tightly constrained by CMB and BBN.

7. **Thermal friction from the SM plasma**: For dark sectors coupled via kinetic mixing, friction from the SM thermal bath (electromagnetic and QCD plasma) could affect bubble dynamics, even for small epsilon.

8. **Dark photon absorption during the PT**: The dense plasma during the supercooled epoch could absorb A' bosons, modifying the energy budget available for GW production.

---

## 8. Required Followups (Prioritized)

### High Priority (4 items)

| ID | Action | Blocked By | Assumptions Addressed |
|----|--------|------------|----------------------|
| F-001 | Compute A' decay widths and branching fractions (visible + invisible) | epsilon unspecified | A-020, A-023, A-038, A-022 |
| F-002 | Specify benchmark or prior values for epsilon and lambda_HPhi | User input | A-003, A-020, A-021, A-005 |
| F-003 | Implement xi(T) thermal history calculation | epsilon, lambda_HPhi unspecified | A-004, A-024, A-005, A-038 |
| F-004 | Compute rho freeze-in yield and decay lifetime | lambda_HPhi unspecified | A-021, A-025, A-038 |

### Medium Priority (4 items)

| ID | Action | Blocked By | Assumptions Addressed |
|----|--------|------------|----------------------|
| F-005 | Compute mean bubble separation R* directly | FOPT backend modification | A-011, A-010 |
| F-006 | Complete PTArcade with convergence diagnostics | PTA run time | A-018, A-032, A-033 |
| F-007 | Quantify RG scheme dependence of FOPT parameters | RG-improved potential implementation | A-007, A-009 |
| F-008 | Check runaway wall assumption with NLO friction | FOPT backend extension | A-014 |

### Low Priority (2 items)

| ID | Action | Blocked By | Assumptions Addressed |
|----|--------|------------|----------------------|
| F-009 | Extend benchmark scan with finer resolution | None | A-027 |
| F-010 | Template sensitivity study (dbf vs alternatives) | Multiple template implementation | A-012, A-013, A-030 |

---

## 9. Conclusions

1. **The pipeline produces physically plausible results**: the Dark U(1) conformal model with v ~ 0.6-1.2 GeV and g_D ~ 0.51-0.55 can produce a GW signal matching the NANOGrav 15-year data.

2. **However, the interpretation is severely limited** by the 38 identified uncontrolled uncertainties (26 uncontrolled, 12 controlled). The most impactful are the unspecified portal couplings, which block 19 of 23 experimental constraints.

3. **The xi=1 + Delta N_eff tension** is the single most serious cosmological concern. Without computing the post-PT dark sector abundance and temperature evolution, the model's cosmological viability remains unverified.

4. **The FOPT computation uses several approximations** (fixed-scale CW, high-T expansion, beta/H parameterization) that are known from the literature to potentially introduce systematic uncertainties of O(10-100%) for extreme supercooling.

5. **The PTA inference provides statistical posteriors** but lacks formal convergence diagnostics and Bayes factor comparison. The results should be considered preliminary until the full PTArcade campaign converges.

6. **Eight missing computational modules** (identified by the constraint agent) are needed to bridge the gap between 'this model could explain the PTA signal' and 'this model is consistent with all experimental constraints'.

### Final Assessment

The model passes the theory-level checks (perturbativity, CW consistency, anomaly freedom). The GW signal matches PTA data across a well-defined parameter region. However, the unresolved portal couplings and the Delta N_eff tension prevent a definitive statement about the model's overall phenomenological viability. The pipeline results should be interpreted as: "If the portal couplings are chosen to satisfy all constraints (epsilon in 10^{-9} to 10^{-4}, sin^2(theta) < 10^{-11}), then the dark U(1) conformal model with v ~ 0.6-1.2 GeV and g_D ~ 0.51-0.55 provides a viable explanation of the NANOGrav 15-year signal."