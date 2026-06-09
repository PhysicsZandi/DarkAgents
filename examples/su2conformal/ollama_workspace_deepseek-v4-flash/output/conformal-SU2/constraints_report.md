# Constraint Analysis Report: Conformal-SU2 Model

## Model Summary

The **conformal-SU2** model is a minimal classically scale-invariant SU(2) gauge theory with one complex scalar doublet. The gauge symmetry is fully broken (SU(2)_X -> nothing) via the Coleman-Weinberg mechanism. The model contains:
- **3 massive SU(2) gauge bosons** (W^a_mu), each with 3 polarizations = 9 dof
- **1 radial scalar mode** (pseudo-dilaton chi), 1 dof
- **No fermions**, **no tree-level couplings to the Standard Model**

## PTA-Preferred Parameter Region

**1-sigma PTArcade posterior (from NG15 fit):**
- g in [0.85, 0.91], MAP: 0.86
- chi0 in [0.62, 1.27] GeV, MAP: 1.12 GeV

**Derived masses at MAP:**
- m_W = g*chi0/2 = 0.48 GeV
- m_chi = sqrt(beta_lambda)*chi0 = 70 MeV

**Best 14/14 benchmark points (from violin scan):**
- g in [0.90, 1.05], chi0 in [0.39, 0.50] GeV
- m_W ~ 175-263 MeV, m_chi ~ 27-42 MeV
- T_reh ~ 40-50 MeV, alpha ~ 10^5-10^11, beta/H ~ 18-35

## Constraints Summary

| ID | Name | Class | Applicability | Requires Calc? |
|----|------|-------|--------------|----------------|
| C01 | Delta N_eff from dark radiation | Requires new backend | Full region if thermalized | High priority |
| C02 | BBN bound on percolation T | Direct (needs coupling info) | Best points safe, marginal points at risk | Already available |
| C03 | DM overproduction | Requires recast | Full region if no portal | High priority |
| C04 | SIDM constraints | Requires new backend | Full region if DM | Medium priority |
| C05 | Fifth force / EP constraints | Not applicable | m_chi ~ MeV too heavy | Not needed |
| C06 | Perturbativity | Direct | Trivially satisfied | Not needed |
| C07 | CMB annihilation constraints | Requires recast | Full region if DM with portal | Medium priority |
| C08 | Supernova cooling | Requires recast | Marginal (masses near T_SN) | Low priority |
| C09 | Higgs portal constraints | Requires recast | Only if portal added | Low priority |
| C10 | Eternal inflation | Direct | Already checked, safe | Not needed |
| C11 | Dark photon beam dump | Requires recast | Only if kinetic mixing added | Low priority |

## Key Constraints in Detail

### 1. Delta N_eff (C01) - Most Severe Cosmological Constraint

The stable dark SU(2) sector contributes to the effective number of neutrino species. With 13 bosonic dof, if it was in thermal equilibrium with the SM (xi = T_D/T_SM = 1), Delta N_eff ~ 0.64, well above the combined BBN+CMB bound of Delta N_eff < 0.18 (two-sided, 95% CL, Yeh et al. 2022).

**Key point:** The minimal model has NO SM coupling, so the sectors likely never equilibrated. However, the FOPT itself can reheat the dark sector, contributing to the dark radiation density. Bringmann et al. (2306.09411) found that stable dark sectors are strongly disfavored for PTA explanations.

**Required calculation:** Full thermal history including FOPT reheating to determine xi = T_D/T_SM at BBN and CMB epochs.

### 2. DM Overproduction (C03) - Severe Model-Building Constraint

The gauge bosons (m_W ~ 0.26-0.58 GeV) are stable in the minimal model (custodial SU(2) symmetry). Standard thermal freeze-out would vastly overproduce DM. Studies of minimal SU(2) vector DM (Frandsen et al. 2301.00041) find that masses below ~7.5 TeV are excluded for standard freeze-out.

Borah et al. (2109.11558) solved this by adding a tiny Higgs portal (lambda_2 ~ 10^{-9}) for freeze-in (FIMP) production, producing the correct relic abundance non-thermally. Without such a portal, overproduction is unavoidable.

**Required calculation:** Relic abundance for SU(2) gauge bosons including FOPT entropy dilution and potential portals.

### 3. BBN Percolation Temperature (C02) - Directly Checkable

The best 14/14 benchmark points have T_reh ~ 40-50 MeV, safely above the BBN bound (T > 1 MeV, or T > 3 MeV for strong transitions per Bai & Korwar 2022). The MAP point has T_reh ~ 14.5 MeV. Some scan points with T_p < 1 MeV are excluded.

**Data available:** T_p and T_reh are already computed in the FOPT benchmark CSV.

### 4. SIDM Constraints (C04) - Conditional on DM Status

If the gauge bosons are DM, their self-interaction cross section may be large (sigma ~ g^4/m_W^2). For g~0.86, m_W~0.48 GeV, the cross section is expected to be O(1-10) cm^2/g, potentially exceeding cluster bounds (<0.35 cm^2/g). This constraint is sub-leading to the DM overproduction question.

### 5. Fifth Force (C05) - Not Applicable

The radial mode mass m_chi ~ 38-89 MeV is too heavy for laboratory fifth-force tests (range ~ 10^{-11} cm). Moreover, in the purely conformal limit, the dilaton does not couple to SM matter at tree level (Damour & Donoghue 2010).

### 6. Perturbativity (C06) - Trivially Satisfied

g in [0.85, 0.91] is well below the perturbativity bound g < 3.5.

## Required New Calculations (Ranked by Priority)

1. **HIGH: Delta N_eff calculation** - Must track the dark sector temperature ratio xi through the FOPT and subsequent cosmological evolution. Without this, the most important cosmological constraint cannot be evaluated.

2. **HIGH: DM relic abundance** - Determine whether the gauge bosons overproduce DM. This requires computing the annihilation cross section and solving the Boltzmann equation with FOPT entropy dilution. Borah et al. provide a template for freeze-in with lambda_2 ~ 10^{-9}.

3. **MEDIUM: Self-interaction cross section** - If gauge bosons are DM, compute sigma_T/m including non-perturbative Sommerfeld enhancement.

## Conclusions

The conformal SU(2) model in its minimal form (completely secluded, no SM coupling) faces two fundamental challenges:
1. **Dark radiation overproduction** (Delta N_eff) from a stable dark sector
2. **Dark matter overproduction** from stable gauge bosons

Both can be addressed by adding a small portal to the SM:
- A tiny Higgs portal (lambda_2 ~ 10^{-9}) enables freeze-in DM production (Borah et al. 2109.11558)
- A larger portal (still evading constraints) would allow the dark sector to decay before BBN, avoiding the Delta N_eff problem (Bringmann et al. 2306.09411)

The BBN percolation temperature constraint is satisfied by all PTA-preferred points. The remaining constraints (fifth force, SN cooling, CMB annihilation, beam dump) are either not applicable or only relevant if specific portals are added.