# Prior Audit Report: u1conformal_fermion

**Date**: 2026-06-08
**Branch**: fopt-pta
**Auditor**: prior-agent

## Executive Summary

This report documents a comprehensive audit of all assumptions, priors, approximations, uncertainties, validity domains, caveats, and limitations across the entire analysis pipeline for the classically scale-invariant U(1)_D dark sector model with two Dirac fermions. The pipeline comprises model specification, literature review, FOPT analysis (semianalytic backend), PTA analysis (benchmark scan + PTArcade MCMC), and constraint analysis.

**38 audit items** were identified and classified by severity (1-10 scale, 10 = most critical). Of these, **10 items** are considered controlled (understanding and accounting for the issue is tested and documented). The remaining 28 items are uncontrolled and could materially affect the interpretation of the final results.

## Upstream Statuses

| File | Status | Note |
|------|--------|------|
| `handoff_model.json` | ok | Final validated model specification |
| `handoff_librarian_preliminary.json` | ok | Literature context, all papers verified |
| `handoff_critique.json` | warning | Critique passed; Goldstone mass fixed; gb_scalar=0 noted |
| `handoff_fopt.json` | ok | FOPT analysis complete; 40.8% numerical failure rate |
| `handoff_pta.json` | ok | PTA analysis complete; posteriors obtained |
| `handoff_constraints.json` | ok | 17 constraints considered; 10 require new backends |

## Top 3 Critical Issues (Severity 10)

### 1. xi = 1 assumption is inconsistent with zero portal couplings (A04, A28)
The model fixes xi = T_dark/T_SM = 1 while also setting epsilon = 0 and lambda_HPhi = 0. Without any portal coupling, the dark sector cannot maintain thermal equilibrium with the SM. The gravitational interaction rate Gamma_grav/H ~ 10^{-51} at T=1 GeV is completely negligible. Li & Nath (2602.14324) show that neglecting xi evolution can change GW power predictions by up to 4 orders of magnitude. This single assumption affects the FOPT analysis (which uses xi to set the Hubble rate), the PTA analysis (which inherits the FOPT parameters), and all constraint analyses (which depend on the DS temperature history).

**Required action**: Model the dark sector as an isolated thermal bath with its own temperature T_ds(t). Compute entropy injection from the FOPT and determine xi(T) at BBN, CMB, and today.

### 2. Dark matter relic abundance not computed (A22)
The lightest dark sector particle (chi, the CW pseudo-dilaton, m_chi ~ 20-120 MeV in the 1-sigma PTArcade region) is stable and constitutes a dark matter candidate. Its relic abundance from thermal freeze-out within the dark sector (secluded freeze-out via chi chi -> A A annihilation) has not been computed. Overproduction (Omega_DM h^2 > 0.12) would exclude large regions of the PTArcade posterior. This is the single most impactful missing calculation.

**Required action**: Implement a Boltzmann solver for secluded freeze-out. Compute the chi chi -> A A annihilation cross-section. Determine Omega_DM h^2 at each viable point.

### 3. High-temperature expansion breaks down in supercooling regime (A07)
The finite-T effective potential uses the high-temperature expansion, which assumes m/T << 1. For the benchmark points, m_A'/T_n ~ 50-150, severely violating this condition. Recent literature (Camargo-Molina et al. 2410.23210, Christiansen et al. 2511.02910) demonstrates that the 4D HT approach gives gauge-dependent results and large theoretical uncertainties for radiative symmetry breaking in the supercooled regime. The systematic alternative is dimensional reduction to a 3D EFT.

### 4. Renormalisation scale fixed without RG running (A09)
The renormalisation scale is fixed to the vev (mu=v) and coupling running is neglected. For supercooled transitions spanning many orders of magnitude in temperature, this is a significant uncontrolled approximation. Sher (PRD 24, 1699, 1981) demonstrated that including scale dependence changed the nucleation temperature by ~10 orders of magnitude in extreme cases. The modern literature (Christiansen et al. 2511.02910, Pascoli et al. 2602.02829) shows that consistent RG running is essential for reliable predictions.

**Required action**: Quantify the uncertainty by varying the scale by a factor of 2-4 around the reference value. Implement RG running of g_D and y_psi between mu=v and mu ~ pi*T.

## Other Critical Issues (Severity 7-8)

### No Daisy resummation (A08) -- Severity 7
The thermal effective potential lacks the leading IR-divergent contributions from zero-Matsubara mode resummation. Curtin, Meade, Ramani (1808.08849) find errors up to 40% in the critical temperature with unresummed potentials.

### Bubble wall velocity not computed (A14) -- Severity 7
The DBF template assumes ultra-relativistic walls (v_w ~ 1). Garcia Garcia et al. (2212.10572) show that friction from massive gauge bosons (present in this model as A') creates a maximum dynamic pressure that can prevent runaway. Whether the walls reach v_w ~ 1 or the transition is deflagration-like is unknown.

### Extreme alpha values outside DBF template calibration range (A35) -- Severity 7
The benchmark points have alpha values up to ~10^10, while the DBF template was calibrated for alpha ranging from weak to moderate supercooling. For vacuum-dominated transitions, standard Hubble-normalised FOPT parameters lose their meaning.

### y_psi posterior degeneracy (A21) -- Severity 7
The marginal posterior for y_psi extends to the prior boundary without a well-defined lower bound at 68% HPDI. This indicates the NANOGrav data cannot constrain y_psi from below within the prior range, and the prior dominates the inference. The degeneracy arises because y_psi mainly affects beta_lambda, which becomes independent of y_psi for y_psi << g_D.

### BBN/CMB constraint on PT energy injection (A27) -- Severity 7
The Bai-Korwar bound (T_* > ~2 MeV for strong PTs) was derived assuming the latent heat reheats SM photons. In this secluded model, only the DS is reheated. However, the DS energy density at BBN could still affect the expansion rate and effective neutrino count.

### All constraint conclusions are conditional on xi=1 (A30) -- Severity 7
The mass ranges used to conclude that Delta N_eff and BBN constraints are satisfied are derived from the PTArcade posterior, which itself assumes xi=1. This circular dependency means that if xi is relaxed, all constraint conclusions could change.

## Moderate Issues (Severity 5-6)

### DBF template choice and GW source dominance (A15, A16)
The DBF template from Lewicki & Vaskonen (2025) is appropriate for strongly supercooled transitions, but the extreme alpha values in the benchmark points may lie outside its calibrated range. The assumption that fluid motion (via DBF) dominates over bubble collisions is also untested for this secluded model with no radiation bath.

### PTArcade prior sensitivity and chain convergence (A18, A19)
Uniform priors on couplings with boundaries that truncate the posterior (y_psi 68% HPDI lower boundary at the prior edge) are a concern. The single-chain MCMC with 7,501 post-burnin samples is modest; no R-hat diagnostic is available and ESS is not reported.

### Numerical failure rate (A17)
40.8% of FOPT scan points failed numerically, mostly at g_D > 1.5. While the PTArcade posterior lies within the stable region (g_D ~ 0.53-0.65), the excluded high-coupling region may contain viable (or excluded) points that could affect the global parameter space interpretation.

### Discrepancy between benchmark and PTArcade regions (A29)
The FOPT benchmark scan found best PTA-compatible points at v ~ 10-20 MeV, while the PTArcade Bayesian posterior favours v ~ 0.65-1.45 GeV. These are two different mass regimes that point to different physical interpretations (sub-GeV vs GeV-scale DS).

### No RG running of couplings with temperature (A33)
Related to A09, the running of gauge and Yukawa couplings with the temperature scale is not included. This affects the barrier height and nucleation rate.

## Low Severity Items (Severity 1-4)

These include the controlled model-building assumptions (classical scale invariance, anomaly-free fermion content, CP conservation, fermion mass degeneracy, eternal inflation check, perturbative unitarity bound, Delta N_eff analysis, zero Higgs portal, zero kinetic mixing), along with the Gaussian and single-field approximations for the bounce action (standard in the literature and well-understood). While systematic uncertainties remain, they are either explicitly controlled, well-understood in the literature, or small compared to the severe issues above.

## Required Follow-ups (Priority-ordered)

### High Priority
1. **R01**: Self-consistent xi(T) evolution from the FOPT to today
2. **R02**: Dark matter relic abundance from secluded freeze-out
3. **R03**: RG scale uncertainty quantification with running couplings
4. **R04**: Bubble wall velocity from friction pressure balance

### Medium Priority
5. **R05**: PTArcade chain convergence (4+ chains, R-hat, ESS, prior sensitivity)
6. **R06**: Benchmark vs PTArcade posterior consistency check
7. **R07**: DBF template validity for extreme alpha > 10^4
8. **R08**: Direct numerical bounce action validation

### Low Priority
9. **R09**: Perturbative unitarity check
10. **R10**: DM self-interaction cross-section
11. **R11**: Fully chi-squared PTA likelihood
12. **R12**: Loop-induced kinetic mixing estimate

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total audit items | 38 |
| Critical (severity 10) | 3 |
| Major (severity 7-8) | 8 |
| Moderate (severity 5-6) | 11 |
| Minor (severity 1-4) | 16 |
| Controlled items | 10 |
| Unresolved items | 28 |