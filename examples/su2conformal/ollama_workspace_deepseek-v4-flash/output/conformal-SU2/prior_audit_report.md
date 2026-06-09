# Prior Audit Report: conformal-SU2

**Date:** 2026-06-07
**Branch:** fopt-pta
**Auditor:** prior-agent

## Overview

This report documents 42 audit items (assumptions, priors, approximations, uncertainties, caveats, limitations, and warnings) identified across the entire conformal-SU2 pipeline. Each item is classified by category and severity (1-10 scale, where 10 is most critical).

### Upstream Status

| Handoff | Status |
|---|---|
| handoff_proposed_model.json | ok |
| handoff_librarian_preliminary.json | ok |
| handoff_critique.json | warning |
| handoff_model.json | ok |
| handoff_fopt.json | ok |
| handoff_pta.json | ok |
| handoff_constraints.json | ok |

### Severity Distribution

| Severity | Count | Controlled |
|---|---|---|
| 1 (lowest) | 2 | 2 |
| 2 | 4 | 4 |
| 3 | 8 | 5 |
| 4 | 6 | 2 |
| 5 | 9 | 2 |
| 6 | 4 | 0 |
| 7 | 3 | 0 |
| 8 | 3 | 0 |
| 9 | 2 | 0 |
| 10 (highest) | 1 | 0 |

**Total items:** 42
**Controlled:** 15 (36%)
**Uncontrolled:** 27 (64%)

---

## Critical Items (Severity 8-10)

### 1. Delta N_eff from stable dark radiation (Severity 8, Uncontrolled)

The stable dark SU(2) sector with 13 bosonic degrees of freedom contributes to Delta N_eff. If in thermal equilibrium with the SM (xi = 1), the contribution Delta N_eff ~ 0.64 exceeds the combined BBN+CMB bound of Delta N_eff < 0.18 (Yeh et al. 2022). The constraint agent flagged this as requiring a new backend module, which was not implemented.

**Impact:** Could invalidate the model entirely for the PTA-preferred region if the dark sector was ever in equilibrium with the SM.

**Reference:** handoff_constraints.json, C01

### 2. Dark matter overproduction from stable gauge bosons (Severity 8, Uncontrolled)

The SU(2) gauge bosons (m_W ~ 0.26-0.58 GeV in the 1-sigma posterior region) are stable in the secluded limit. Without a decay portal or annihilation mechanism, their thermal relic abundance would vastly exceed the observed Omega_DM h^2 ~ 0.12. Borah et al. (2021) invoke a tiny Higgs portal (lambda_2 ~ 10^{-9}) for freeze-in, but this is not part of the minimal model.

**Impact:** The minimal model is cosmologically inviable unless a portal is added. The model as analyzed (no SM coupling) is inconsistent with standard cosmology at a fundamental level.

**Reference:** handoff_constraints.json, C03

### 3. Unverifiable dbf template reference (Severity 7, Uncontrolled)

The primary GW spectrum template, identified as "dbf (dissipative bulk flow)" from arXiv:2511.15687, could not be verified through public searches. This arXiv ID (November 2025) does not appear to be published or indexed. The template is central to the PTA analysis, and its validation regime, assumptions, and limitations are unknown if the reference is incorrect.

**Impact:** The entire GW spectrum calculation rests on a potentially unverifiable reference. The template's caveat about moderate-alpha validity is acknowledged in the PTA report, but the reference itself needs to be confirmed.

**Reference:** handoff_pta.json, template_choice

### 4. Single MCMC chain convergence (Severity 7, Uncontrolled)

The PTArcade analysis used a single MCMC chain with only 7501 effective samples after thinning and burn-in. Standard PTA analyses (including NANOGrav's own) use multiple independent chains with the Gelman-Rubin criterion R-1 < 0.05. A single chain cannot verify convergence and may not have fully explored the posterior.

**Impact:** The inferred 1-sigma posteriors (g = 0.852-0.912, chi0 = 0.62-1.27 GeV) may not be reliable. The posterior may have non-trivial correlations or even multi-modality that a single chain could miss.

**Reference:** handoff_pta.json, ptarcade_campaign and warnings

---

## High-Severity Items (Severity 5-6)

### 5. High-temperature expansion validity (Severity 6, Uncontrolled)

The high-temperature (small-field) expansion of the one-loop finite-temperature effective potential is used throughout. For models with strong supercooling (alpha >> 1), the field value at the true minimum can be much larger than the temperature, where the HT expansion breaks down. The bounce trajectory stays in the HT-valid region, but the minimum evaluation uses the zero-T CW potential. This partial validity is subtle and not quantified.

**Reference:** handoff_model.json, assumptions; confirmed via literature (arXiv:2312.12413)

### 6. Numerical failures in FOPT scan (Severity 6, Uncontrolled)

198 out of 680 FOPT scan points (29%) result in numerical failures ("non-finite backend output"). These failures are concentrated at g < 0.5 and at parameter extremes. The viable region may be biased by these failures.

**Reference:** handoff_fopt.json, benchmark_summary

### 7. Eternal inflation check condition (Severity 6, Uncontrolled)

The condition `3 + Tp * I_prime(Tp) < 0` used in the backend is a simplified criterion. The standard literature condition is `Gamma/H^4 < 9/(4*pi)` (Rudelius 2019, arXiv:1905.05198). While 14/1660 points were excluded, the difference between these conditions is not quantified.

**Reference:** backend/semianalytic_pipeline.py, get_check_eternal_inflation

### 8. No Daisy resummation (Severity 5, Uncontrolled)

No Daisy (ring) resummation is included in the thermal effective potential. For SU(2) gauge theories, Debye screening provides a thermal mass for longitudinal gauge bosons that affects the critical temperature and nucleation rate.

**Reference:** handoff_fopt.json, approximations

### 9. No RG running (Severity 5, Uncontrolled)

The effective potential uses a fixed renormalization scale set to chi0, with no RG improvement. Kierkla et al. (2023, arXiv:2210.07075) showed that fixed-scale calculations can give qualitatively different results from RG-improved calculations for SU(2) CW models.

**Reference:** handoff_fopt.json, approximations

### 10. Post-hoc prior truncation (Severity 5, Uncontrolled)

The PTArcade prior boundaries (g in [0.5, 3.0], log10_chi0 in [-5, 0.699]) were truncated from the model ranges based on the FOPT scan results. While no posterior mass hits boundaries, this is a post-hoc adjustment that introduces selection bias.

**Reference:** handoff_pta.json, ptarcade_campaign

### 11. dbf template validity for moderate alpha (Severity 5, Uncontrolled)

The dbf template is used for all points, including moderate alpha ~ O(1-10) where its validity is less established. These points typically produce small GW amplitudes, but their exclusion from the analysis is not justified.

**Reference:** handoff_pta.json, template_choice

### 12. Alpha discrepancy with literature (Severity 7, Uncontrolled)

Comparison with arXiv:2109.11558 BP1 shows a factor ~33 discrepancy in alpha (ours: 15, theirs: 0.45). beta/H matches within 1% (144 vs 143). The alpha difference is attributed to DOF counting but not fully resolved. This systematic discrepancy could affect conclusions about model viability.

**Reference:** handoff_pta.json, literature_comparison

---

## Moderate-Severity Items (Severity 3-4)

- **A02:** One-loop CW approximation; higher-order corrections neglected (Severity 4)
- **A07/A11:** Renormalization scale set to chi0; sensitivity not quantified (Severity 4)
- **A08:** Gaussian approximation for false-vacuum fraction (Severity 4)
- **A12:** Scheme dependence of CW calculation (Severity 4)
- **A17:** Wall velocity derived from FOPT pipeline, not free (Severity 4)
- **A19:** Efficiency factors not explicitly documented (Severity 4)
- **A23:** Ceffyl mode approximation (Severity 4)
- **A34:** Null f_peak_est values for many FOPT points (Severity 4)
- **A39:** Tension between best scan points and MAP posterior (Severity 4)

---

## Controlled Items (Severity 1-3)

Items that are well-understood and either inherent to the model choice or adequately documented:

- **A01:** Classical scale invariance (defining assumption, Severity 3, controlled)
- **A03:** No fermions (deliberate minimal choice, Severity 2, controlled)
- **A05:** Perturbative regime (satisfied for all preferred points, Severity 2, controlled)
- **A06:** No U(1)_Y (self-consistent model, Severity 1, controlled)
- **A21:** Log-uniform prior on chi0 (natural for scale-invariant model, Severity 3)
- **A35:** Model not novel (documented, Severity 1, controlled)
- **A36:** Unverifiable paper IDs in earlier handoffs (documented, Severity 2, controlled)
- **A41:** Hubble/g_star interpolation (standard approach, Severity 3)

---

## Required Follow-ups

| Priority | ID | Description |
|---|---|---|
| High | F01 | Resolve Delta N_eff constraint with dedicated calculation |
| High | F02 | Resolve DM overproduction with relic abundance calculation |
| High | F03 | Cross-check eternal inflation condition against literature |
| High | F04 | Run additional MCMC chains for convergence verification |
| Medium | F05 | Resolve alpha convention discrepancy with literature |
| Medium | F06 | Validate or replace dbf template reference |
| Medium | F07 | Quantify RG scale uncertainty |
| Medium | F08 | Include Daisy resummation |
| Low | F09 | Investigate numerical failures in FOPT scan |
| Low | F10 | Investigate tension between scan and MAP results |

---

## Summary

The conformal-SU2 pipeline is well-structured and produces plausible results, but it relies on several uncontrolled assumptions that significantly affect the interpretation of the final result. The three most critical unresolved issues are:

1. **Cosmological viability:** The Delta N_eff and DM overproduction constraints have not been quantified, and existing literature suggests they may rule out the model entirely (Severity 8).

2. **GW template provenance:** The central dbf template (arXiv:2511.15687) cannot be verified through public searches, which is a systematic concern for the reliability of the GW spectrum calculation (Severity 7).

3. **Statistical robustness:** A single MCMC chain with 7501 effective samples does not meet standard convergence criteria for PTA Bayesian analyses (Severity 7).

Addressing these three items should be the top priority before the results can be considered robust for publication.