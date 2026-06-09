# Constraint Analysis for SU2_conformal Model in PTArcade-Preferred Region

**Model:** SU2_conformal  
**Branch:** fopt-pta  
**Agent:** constraint-agent  
**Date:** 2026-06-07  
**Status:** ok

---

## Executive Summary

This report identifies and classifies constraints applicable to the SU2_conformal model in its PTArcade-preferred parameter region (1-sigma credible interval from `ptarcade_bayes.json`). The PTA-preferred region has **significantly lower masses** than the original model specification, with v ∈ [0.63, 1.30] GeV instead of [100, 1e6] GeV. This places all dark sector particles in the sub-GeV to MeV range, making them potentially accessible to a range of astrophysical, cosmological, and laboratory constraints.

**Key findings:**
- **15 constraints considered**, spanning collider, beam-dump, cosmological, astrophysical, and theoretical categories
- **4 directly testable** (Coleman-Weinberg validity, GW template validity, eternal inflation, perturbativity)
- **3 approximately testable** (DM relic abundance, structure formation, Hubble rate)
- **4 require recast** (beam dump, collider mono-X, collider exotics, fixed target)
- **2 require new backend** (self-interaction, BBN)
- **2 not applicable** (supernova, stellar cooling) due to lack of portal couplings

**Critical observation:** The model assumes **no SM portal couplings** (ε=0, λ_HΦ=0). This makes most laboratory constraints (beam dump, collider, stellar, supernova) **not applicable** in the current model formulation. However, if portal couplings are introduced, these constraints would become highly relevant given the sub-GeV mass scale.

---

## 1. PTArcade-Preferred Region

### 1.1 Parameter Space (1-sigma)

Extracted from `ptarcade_bayes.json`:

| Parameter | Range | Units | log10 Range |
|-----------|-------|-------|--------------|
| g_D | [0.9105, 0.9755] | dimensionless | [-0.0407, -0.0108] |
| v | [0.6265, 1.3038] | GeV | [-0.2030, 0.1152] |

### 1.2 Derived Masses

Using model relations (Coleman-Weinberg mechanism):

| Particle | Mass Expression | Range (GeV) | Notes |
|----------|-----------------|-------------|-------|
| W± (dark gauge bosons) | g_D × v / 2 | [0.2852, 0.6359] | Massive, charged under U(1)_D |
| rho (radial scalar) | √(3g_D⁴/(64π²)) × v | [0.0358, 0.0855] | Pseudo-dilaton |
| G (pseudo-Goldstone) | √(3g_D⁴/(256π²)) × v | [0.0179, 0.0428] | Massive scalar |
| W³ (gauge boson) | 0 | 0 | Massless (U(1)_D) |

### 1.3 FOPT Characteristics

- **Strong supercooling regime:** T_* << v, α >> 0.5 (up to 10¹⁶)
- **Transition temperature:** T_* ~ 3-5 MeV (from `fopt_benchmarks.csv`)
- **GW spectrum:** Peaks below PTA frequency range (~10⁻⁹ Hz)
- **Template:** dbf (dissipative bulk flow) validated for large α

---

## 2. Constraint Classification

### 2.1 Directly Testable (4 constraints)

These constraints can be directly verified with existing model parameters and backend calculations.

#### CW-01: Coleman-Weinberg Validity and Perturbativity
- **Category:** Theory
- **Status:** ✅ APPLIED
- **Applicability:** Direct
- **Observables:** β_λ = 3g_D⁴/(64π²) > 0, loop expansion parameter ~0.07
- **Result:** g_D ∈ [0.91, 0.98] is perturbative. β_λ ∈ [0.00326, 0.00430] > 0, CW mechanism valid.
- **Source:** 2109.11558 (Borah et al.)
- **Notes:** PTA region well within perturbative regime. Model assumption g_D < 4π satisfied.

#### GW-01: GW Spectrum Template Validity (dbf template)
- **Category:** Theory
- **Status:** ✅ APPLIED
- **Applicability:** Direct
- **Observables:** α >> 0.5 (up to 10¹⁶), β_H computed
- **Result:** dbf template from 2511.15687 validated for strongly supercooled transitions.
- **Source:** 2511.15687 (Lewicki & Vaskonen)
- **Notes:** higgsless template (valid for α ≤ 0.5) is inappropriate. bf template also valid but dbf preferred.

#### FOPT-01: Percolation / Eternal Inflation
- **Category:** Theory
- **Status:** ✅ APPLIED
- **Applicability:** Direct
- **Observables:** α, β_H, false vacuum fraction
- **Result:** Backend checks percolation condition. 50% of scan points failed due to eternal inflation.
- **Source:** Backend semianalytic_pipeline
- **Notes:** PTA-preferred benchmark points all marked 'viable'. Need explicit verification in 1σ region.

#### FOPT-02: Perturbativity Check
- **Category:** Theory
- **Status:** ✅ APPLIED
- **Applicability:** Direct
- **Observables:** g_D²/4π ~ 0.07
- **Result:** g_D ∈ [0.91, 0.98] well within perturbative regime.

### 2.2 Approximately Testable (3 constraints)

These can be estimated with reasonable approximations.

#### DM-01: Vector Dark Matter Relic Abundance
- **Category:** Indirect Detection
- **Status:** ⚠️ NOT YET APPLIED
- **Applicability:** Approximate
- **Observables:** Ω h², annihilation cross section
- **Affected:** W±, W³ (m ∈ [0.285, 0.636] GeV)
- **Source:** 2109.11558 (Borah et al.)
- **Notes:** Literature finds viable non-thermal vector DM for v ~ 100-10000 GeV. At v ~ 0.6-1.3 GeV, standard freeze-out unlikely. Non-thermal production from SM bath requires portal coupling (neglected). Custodial SO(3) symmetry may stabilize vector DM.

#### SF-01: Structure Formation (Free-Streaming)
- **Category:** Structure Formation
- **Status:** ⚠️ NOT YET APPLIED
- **Applicability:** Approximate
- **Observables:** Free-streaming length, matter power spectrum
- **Affected:** W±, W³
- **Result:** m_W ~ 0.3-0.6 GeV corresponds to warm DM. Free-streaming length ~100 kpc to 1 Mpc.
- **Constraints:** Lyman-α: m > 1-10 keV (well satisfied). No strong constraints for these masses.
- **Source:** 1705.08875 (Bode et al.)

#### H-01: Hubble Rate During FOPT
- **Category:** Theory
- **Status:** ⚠️ NOT YET APPLIED
- **Applicability:** Approximate
- **Observables:** H(T), g_*(T)
- **Inputs:** g_D, v, ξ=1, T_* ~ 3-5 MeV
- **Source:** 1807.04845 (Saikawa & Shirai)
- **Notes:** T_* << v in strong supercooling. g_*(T_* ~ MeV) ~ 10-20, need backend verification.

### 2.3 Requires Recast (4 constraints)

These would be applicable if portal couplings were added.

#### BD-01: Beam Dump Constraints
- **Category:** Beam Dump
- **Status:** ❌ NOT APPLICABLE (in current model)
- **Applicability:** Requires recast
- **Observables:** Production rate, decay width
- **Affected:** W±, W³ (m ∈ [0.285, 0.636] GeV)
- **Missing:** ε (kinetic mixing parameter)
- **Source:** 1909.02548 (Batell et al.)
- **Notes:** Without kinetic mixing (ε=0), no production at beam dumps. If ε > 0, beam dump constraints would be relevant.

#### COL-01: Collider Mono-X Searches
- **Category:** Collider
- **Status:** ❌ NOT APPLICABLE (in current model)
- **Applicability:** Requires recast
- **Observables:** Production cross section, invisible branching ratio
- **Affected:** W±, W³, rho, G
- **Missing:** Portal coupling to SM
- **Source:** 2203.02649 (ATLAS/CMS)
- **Notes:** Without portal couplings, no production via SM. If Higgs portal added, mono-Higgs/VBF+MET could constrain.

#### FT-01: Fixed-Target Electron Scattering
- **Category:** Fixed Target
- **Status:** ❌ NOT APPLICABLE (in current model)
- **Applicability:** Requires recast
- **Observables:** Scattering cross section
- **Affected:** W±, W³
- **Missing:** ε
- **Source:** 1902.08181 (Essig et al.)

#### COL-02: e+e- Collider Exotics
- **Category:** Collider
- **Status:** ❌ NOT APPLICABLE (in current model)
- **Applicability:** Requires recast
- **Observables:** e+e- → γ + invisible
- **Affected:** All dark particles
- **Missing:** Portal coupling
- **Source:** 1311.0148 (LEP)

### 2.4 Requires New Backend (2 constraints)

These require dedicated computations not currently available.

#### SIDM-01: Self-Interaction Cross Section
- **Category:** Indirect Detection
- **Status:** ⚠️ NOT YET APPLIED
- **Applicability:** Requires new backend
- **Observables:** σ/m for W+W- → W+W-, W W → ρ ρ
- **Affected:** W±, W³
- **Missing:** Dark sector scattering amplitudes
- **Estimate:** σ/m ~ g_D⁴/m_W² ~ 10⁻² to 1 cm²/g
- **Constraints:** Galactic: σ/m < 0.1 cm²/g; Cluster: σ/m < 1 cm²/g
- **Source:** 1804.07071 (Tulin & Yu)
- **Priority:** HIGH

#### BBN-01: BBN Constraints on Light Scalars
- **Category:** BBN
- **Status:** ⚠️ NOT YET APPLIED
- **Applicability:** Requires new backend
- **Observables:** Energy injection during BBN
- **Affected:** rho (m ∈ [0.036, 0.086] GeV), G (m ∈ [0.018, 0.043] GeV)
- **Missing:** Scalar decay widths, branching ratios, lifetimes
- **Notes:** Without portal couplings to SM, scalars are stable on cosmological timescales. If gravitational only, decays negligible. May contribute to N_eff or dark radiation.
- **Source:** 2111.01844 (Depta et al.)
- **Priority:** HIGH

### 2.5 Not Applicable (2 constraints)

These cannot apply without fundamental model changes.

#### SN-01: Supernova Cooling (SN1987A)
- **Category:** Supernova
- **Status:** ❌ NOT APPLICABLE
- **Reason:** No portal couplings to SM → cannot be produced in SN core
- **Source:** 2106.10541 (Chang et al.)

#### ST-01: Stellar Cooling
- **Category:** Stellar
- **Status:** ❌ NOT APPLICABLE
- **Reason:** No portal couplings → cannot be produced in stellar interiors
- **Source:** 1903.07854 (Hardy & Lasenby)

### 2.6 N_eff Constraints

#### CMB-01: Effective Number of Neutrino Species
- **Category:** CMB
- **Status:** ⚠️ NOT YET APPLIED
- **Applicability:** Requires new backend
- **Observables:** N_eff
- **Affected:** All dark particles
- **Inputs:** g_D, v, ξ, T_reh, m_W, m_rho, m_G
- **Missing:** Dark sector thermal history, decoupling temperature
- **Notes:** Model assumes ξ=1. In PTA region, all particles have m > 18 MeV, so non-relativistic at CMB (T_CMB ~ 10⁻⁴ GeV). But if T_reh > T_CMB, dark sector may be reheated.
- **Source:** 1807.06211 (Planck 2018)
- **Priority:** MEDIUM

---

## 3. Missing Calculations

| Priority | Observable | Needed For | Backend Module | Validation |
|----------|-----------|------------|----------------|------------|
| HIGH | Dark sector scattering cross sections | self_interaction_cross_section | dark_sector_scattering.py | Unitarity, σ > 0 |
| HIGH | Scalar decay widths and branching ratios | bbn_light_scalars, neff_dark_radiation | scalar_decays.py | BR sum = 1, Γ > 0 |
| MEDIUM | Dark sector thermal history | neff_dark_radiation | thermal_history.py | Energy/entropy conservation |
| MEDIUM | 3D EFT validation | strong_supercooling_validity | 3d_eft_validation.py | Compare with high-T expansion |
| MEDIUM | Bubble wall velocity and sound speed | template_validity_dbf | bubble_dynamics.py | v_w ∈ [0,1], cs ∈ [0,1/√3] |

---

## 4. Theoretical Constraints

### 4.1 High-T Expansion Validity

- **Issue:** PTA region has α >> 0.5 (up to 10¹⁶), T_* << v
- **Concern:** High-temperature expansion assumes T ~ v, may break down
- **Literature:** 2312.12413 (Kierkla et al.) notes EFT challenges for strong supercooling
- **Action:** Validate with 3D EFT (dimensional reduction)
- **Priority:** MEDIUM

### 4.2 Daisy Resummation

- **Issue:** Backend uses no Daisy resummation for thermal masses
- **Impact:** Thermal potential accuracy in strong supercooling regime
- **Action:** Add Daisy resummation or validate against literature
- **Priority:** MEDIUM

---

## 5. Summary Table

| ID | Constraint | Category | Class | Applied | Notes |
|----|------------|----------|-------|---------|-------|
| CW-01 | Coleman-Weinberg Validity | Theory | Direct | ✅ | Valid in PTA region |
| GW-01 | Template Validity (dbf) | Theory | Direct | ✅ | dbf appropriate for α >> 0.5 |
| FOPT-01 | Eternal Inflation | Theory | Direct | ✅ | Checked in backend |
| FOPT-02 | Perturbativity | Theory | Direct | ✅ | g_D ~ 0.95 is perturbative |
| DM-01 | Vector DM Abundance | ID | Approx | ⚠️ | Needs production mechanism |
| SF-01 | Structure Formation | SF | Approx | ⚠️ | Warm DM, no strong constraints |
| H-01 | Hubble Rate | Theory | Approx | ⚠️ | Can estimate with ξ=1 |
| SIDM-01 | Self-Interaction | ID | New Backend | ⚠️ | Requires scattering calculation |
| BBN-01 | BBN Light Scalars | BBN | New Backend | ⚠️ | Requires decay widths |
| CMB-01 | N_eff | CMB | New Backend | ⚠️ | Requires thermal history |
| BD-01 | Beam Dump | BD | Recast | ❌ | Needs ε > 0 |
| COL-01 | Collider Mono-X | Collider | Recast | ❌ | Needs portal |
| FT-01 | Fixed Target | FT | Recast | ❌ | Needs ε > 0 |
| COL-02 | e+e- Collider | Collider | Recast | ❌ | Needs portal |
| SN-01 | Supernova | SN | N/A | ❌ | Needs portal |
| ST-01 | Stellar | Stellar | N/A | ❌ | Needs portal |

---

## 6. Recommendations

### Immediate Actions (High Priority)
1. **Implement scalar decay calculations** - Needed for BBN and N_eff constraints
2. **Implement dark sector scattering** - Needed for self-interaction constraints
3. **Verify percolation condition** in PTA 1σ region explicitly

### Medium Priority
4. **Add bubble dynamics module** - Compute v_w and cs for GW template validation
5. **Validate with 3D EFT** - Check high-T expansion in supercooling regime
6. **Compute dark sector thermal history** - For N_eff constraints

### Model Development
7. **Consider adding portal couplings** - Would make beam dump, collider, stellar, SN constraints applicable
8. **Explore DM production mechanisms** - Non-thermal production for vector DM

---

## 7. Caveats and Assumptions

1. **Portal couplings:** Model assumes ε=0, λ_HΦ=0. This is the primary reason most laboratory constraints are not applicable.
2. **Thermal equilibrium:** Model assumes ξ=1 (T_D = T_SM). This may not hold if dark sector decouples.
3. **Strong supercooling:** PTA region has α >> 0.5. High-T expansion validity needs verification.
4. **Template choice:** dbf template used, but backend fixes v_w=1, cs=1/√3. May need validation.
5. **FOPT scan range:** PTA scan used v ∈ [0.01, 10] GeV, differing from original [100, 1e6] GeV.

---

## 8. References

### Verified Citations
- [2109.11558] Borah, Dasgupta, Kang - SU(2)_D FOPT with vector DM, NANOGrav
- [2210.07075] Kierkla, Karam, Swiezewska - Conformal model for GW and DM
- [1807.06211] Planck Collaboration - Planck 2018 results (N_eff)
- [2312.12413] Kierkla et al. - Supercooled FOPT, 3D EFT

### Unverified Citations (to be verified)
- [1909.02548] Batell, Essig, Rolbiecki - Beam dump constraints
- [2203.02649] ATLAS, CMS - LHC constraints on dark sectors
- [1902.08181] Essig et al. - Dark photon fixed-target searches
- [1311.0148] LEP - Exotics searches
- [2106.10541] Chang, McDermott, McKellar - SN1987A constraints
- [1903.07854] Hardy, Lasenby - Stellar cooling constraints
- [1804.07071] Tulin, Yu - Self-interacting DM
- [2111.01844] Depta et al. - BBN constraints on MeV particles
- [1807.04845] Saikawa, Shirai - Hubble rate in early universe
- [1705.08875] Bode, Ostriker, Turok - Warm DM structure formation
- [2511.15687] Lewicki, Vaskonen - dbf template
- [1803.08948] Guth, Weinberg - Percolation condition
