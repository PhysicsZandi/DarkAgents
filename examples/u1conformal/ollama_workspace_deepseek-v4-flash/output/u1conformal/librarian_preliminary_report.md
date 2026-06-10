# Preliminary Literature Search Report: Dark U(1) Conformal Model

## Model Summary

The user proposes a classically scale-invariant dark U(1)_D extension of the SM with a complex scalar Phi and dark gauge boson A'. Symmetry breaking occurs via the Coleman-Weinberg mechanism. The target signal is gravitational waves from a first-order phase transition compared to PTA data.

**Free parameters:** vev v (or equivalently the dark scalar mass m_rho) and gauge coupling g_D.

## Literature Search Results

### Executive Summary

**The user's model is NOT novel** -- it has been extensively studied in the literature, with several papers having already performed exactly the analysis requested (GW from FOPT in a conformal dark U(1) sector compared to PTA data). Several papers provide explicit benchmark points that can be used directly for comparison.

---

### Top Papers (in order of relevance)

#### 1. Goncalves, Marfatia, Morais & Pasechnik (2025) -- arXiv:2501.11619
**Relevance: 10/10 -- Same model, same target signal, PTArcade analysis**
- **Title:** "Supercooled phase transitions in conformal dark sectors explain NANOGrav data"
- **Journal:** Physics Letters B 869:139829 (2025)
- **Model:** Dark U(1)' extension with conformal dark sector (singlet scalar sigma) breaking via CW. SM Higgs retains mass term (only dark sector is conformal). Small kinetic mixing (g_12 = 2e-10) for thermalisation.
- **Target signal:** GW from supercooled FOPT fitting NANOGrav 15-year data via PTArcade (ceffyl mode)
- **Key benchmark (best-fit):** g_L = 0.59, M_h2 (dark scalar) = 12.4 MeV, M_Z' = 107.3 MeV, T_RH = 11.7 MeV, alpha = 2.60e5, beta/H = 39.5
- **68% CL ranges:** g_L in [0.57, 0.86], lambda_sigma in [-0.062, -0.028], O(1-100) MeV masses
- **Key claim:** Conformal models circumvent the Athron et al. (2024) completion issues because S_E -> 0 as T -> 0
- **Conventions:** RG scale mu = max[M_Z'(phi_s), pi T]; LISA Cosmology Working Group GW templates; CosmoTransitions for bounce action

**Use for user's analysis:** Most directly applicable benchmark. The model is structurally identical to the user's (conformal U(1)' with CW). Can use the best-fit point and 68% CL ranges as starting points for PTArcade inference.

#### 2. Balan, Bringmann, Kahlhoefer, Matuszak & Tasillo (2025) -- arXiv:2502.19478
**Relevance: 10/10 -- Structurally very similar, with explicit benchmark vev values**
- **Title:** "Sub-GeV dark matter and nano-Hertz gravitational waves from a classically conformal dark sector"
- **Journal:** JCAP 08 (2025) 062
- **Model:** Classically conformal U(1)' with complex scalar Phi, dark photon A'_mu, and chiral fermion DM. Yukawa coupling y. Tree-level V = lambda |Phi|^4. Kinetic mixing to SM.
- **Target signal:** GW from FOPT fitting NANOGrav (via PTArcade), plus DM relic abundance (GAMBIT global fit)
- **Benchmark Point A (coupled scenario):** v = 92.9 MeV, g = 0.877, y = 0.363, lambda = 0.056, T_p = 8.36 MeV, alpha = 4.99, beta/H = 21.1, m_A' = 81.4 MeV, m_phi = 32.6 MeV
- **Benchmark Point B (secluded scenario):** v = 343 MeV, g = 0.790, y = 0.401, T_p = 15.2 MeV, alpha = 62.6, beta/H = 13.3
- **Key insight:** Minimum g ~ 0.6 for FOPT completion (consistent with 2501.11619)

**Use for user's analysis:** The user's model is the same without the DM Yukawa term. The benchmark points provide explicit vev values (not just derived from masses) and can be adapted by setting y -> 0 or large.

#### 3. Costa, Hoefken Zink, Lucente, Pascoli & Rosauro-Alcaraz (2025) -- arXiv:2501.15649
**Relevance: 10/10 -- Same gauge structure, best-practice methodology**
- **Title:** "Supercooled Dark Scalar Phase Transitions explanation of NANOGrav data"
- **Journal:** Physics Letters B 868:139634 (2025)
- **Model:** U(1)_D with complex scalar phi (not conformal -- has mass term mu^2). Dark gauge boson Z'. Same field content as user model.
- **Key methodology:** Checks percolation AND completion (following Athron 2024), uses NLO friction (Bodeker-Moore), uses mean bubble separation R* instead of beta/H, explicitly computes sound speed c_s(T).
- **Benchmark points:** BP1: v = 0.5 GeV, g_D = 0.75, lambda = 0.006, T_p = 12.5 MeV, alpha = 342; BP2: v = 1 GeV, g_D = 0.75, T_p = 22.5 MeV; BP3: v = 10 GeV, g_D = 0.75, T_p = 194 MeV; BP4: v = 1 GeV, g_D = 0.86, T_p = 38 MeV
- **g_D^roll condition:** g_D = [16 pi^2 lambda/3 * (1 - lambda/(8pi^2)(5+2ln2))]^{1/4}
- **Key result:** Strong supercooling leads to m_phi << m_Z' hierarchy; sound waves dominate GW

**Use for user's analysis:** Methodology reference for careful phase transition analysis. The benchmark points illustrate viable parameter space for PTA signals even though the model uses a mass term rather than CW.

#### 4. Feng & Zhang (2026) -- arXiv:2602.14866
**Relevance: 8/10 -- Gauge-independent method, parameter space mapping**
- **Title:** "Gauge-independent gravitational waves from a minimal dark U(1) sector with viable dark matter candidates"
- **Model:** Minimal U(1)_X with dark Higgs (mass term, not CW). Optionally vectorlike dark fermion.
- **Key contribution:** Nielsen identity for gauge-independent effective action in high-T and low-T regimes
- **Parameter space mapping:** v_x ~ 10-100 MeV gives nHz PTA signals; v_x ~ 1-100 GeV gives mHz LISA signals
- **No explicit benchmark point tables** -- results shown as Monte Carlo scan maps

**Use for user's analysis:** Methodological reference for gauge dependence. Confirms the vev scale needed for PTA signals.

#### 5. Banik, Cui, Tsai & Tsai (2024) -- arXiv:2412.16282
**Relevance: 8/10 -- Non-CW U(1) best-fit to combined PTA data**
- **Title:** "The Sound of Dark Sectors in Pulsar Timing Arrays"
- **Model:** U(1) with scalar Phi, fermion DM (standard Higgs mechanism, not CW)
- **Key benchmarks (U(1) no fermions):** mu = 2.4 MeV, lambda = 0.03, g_D = 1.2, T* = 2.4 MeV, alpha = 0.96, beta/H = 47, m_phi ~ 3 MeV
- **Key benchmarks (U(1) with fermions):** mu = 2.7 MeV, lambda = 0.06, g_D = 1.5, T* = 2.5 MeV, alpha = 0.76, beta/H = 38
- **2-sigma ranges:** m_phi ~ 3 +/- 0.6 MeV, g_D ~ 1.25 +/- 0.05, lambda ~ 0.04 +/- 0.01

**Use for user's analysis:** The alpha values (~1) are much smaller than conformal model predictions (~10^2-10^5), indicating different PT dynamics. Useful for comparison but not directly applicable to the CW model.

#### 6. Khoze & Milne (2023) -- arXiv:2212.04784
**Relevance: 7/10 -- Conformal U(1) CW, but LISA (not PTA) focus**
- **Title:** "Gravitational waves and dark matter from classical scale invariance"
- **Journal:** PRD 107, 095012 (2023)
- **Model:** Minimal classically conformal U(1) with fermionic DM, Gildener-Weinberg CW mechanism
- **Target:** GW signal for LISA (mHz, TeV-scale vev), not PTA nHz
- **No explicit benchmark points for PTA**

**Use for user's analysis:** Theoretical foundation for CW mechanism in conformal U(1). The methodological framework (one-loop effective potential, Gildener-Weinberg) is directly applicable.

#### 7. Christiansen, Madge, Puchades-Ibanez, Ramirez-Quezada & Schwaller (2025) -- arXiv:2511.02910
**Relevance: 7/10 -- Identical model, methodology focus**
- **Title:** "Beyond the Daisy Chain: Running and the 3D EFT View of Supercooled Phase Transitions"
- **Model:** Classically scale-invariant dark U(1)_D Abelian Higgs model (IDENTICAL to user model)
- **Methodology:** Compares OPA, 4D HT+Daisy, and 3D EFT for supercooled PT predictions
- **Key result:** Proper RG running is essential; 4D HT with Daisy at mu = pi T matches 2-loop 3D EFT
- **Parameter space:** g in [0.5, 1.0], lambda = 0 (tree-level), v ~ 10^4-10^6 GeV (TeV scale, not sub-GeV)

**Use for user's analysis:** Validates the methodology for computing the FOPT in the conformal limit. Note the vev scale here is TeV (for LISA signals), not the sub-GeV needed for PTA.

#### 8. Li & Nath (2026) -- arXiv:2602.14324
**Relevance: 7/10 -- Thermal history treatment methodology**
- **Title:** "Gravitational waves from supercooled phase transitions and pulsar timing array signals"
- **Model:** Hidden U(1)_X (not conformal/CW)
- **Key contribution:** Shows temperature ratio xi = T_h/T_v can change GW predictions by up to 4 orders of magnitude
- **Benchmark points at GeV-scale percolation temperatures:**
  - BP1: g_x = 2.5, T_h_p = 0.778 GeV, alpha_tot = 0.284, alpha_h = 305, xi_p = 0.585
  - BP2: g_x = 2.7, T_h_p = 1.318 GeV, alpha_h = 337, xi_p = 0.709

**Use for user's analysis:** If the user extends beyond xi = 1, this methodology is crucial. The large gauge couplings (g_x ~ 2-2.7) are much larger than the CW model regime (g ~ 0.6-0.9).

#### 9. Athron, Fowlie, Lu, Morris, Wu, Wu & Xu (2024) -- arXiv:2306.17239, PRL 132, 221001
**Relevance: 8/10 -- Critical challenge paper (background context)**
- **Title:** "Can supercooled phase transitions explain the gravitational wave background observed by pulsar timing arrays?"
- **Key findings:**
  - Challenge 1: Supercooled FOPTs cannot complete at T_p ~ 100 MeV (false vacuum trapping)
  - Challenge 2: Even if completion works, Universe reheats to ~36 GeV, making nHz predictions unreliable
  - Benchmark: T_p ~ 100 MeV, T_reh ~ 36 GeV, GW amplitude > 7 orders below NANOGrav
- **Model:** Non-linearly realized EW symmetry (template model, not actual U(1) gauge sector)

**Use for user's analysis:** The user's conformal model must address these challenges. Later papers (2501.11619, 2501.15649, 2602.14324) argue that conformal models circumvent them. The user should verify that their analysis passes the Athron et al. completion and reheating checks.

---

### Novelty Assessment

**Verdict: NOT NOVEL**

The exact class of model (conformal dark U(1) with CW symmetry breaking and GW from FOPT for PTA signals) has been studied in multiple papers, with arXiv:2501.11619 (Goncalves et al. 2025) being the most directly relevant -- it uses PTArcade to fit the same kind of model to NANOGrav 15-year data and provides benchmark parameter ranges.

The user's specific Lagrangian (complex scalar Phi, dark gauge boson A', no fermionic DM, scalar portal and kinetic mixing assumed small) is a subset of the models studied in the literature, which typically add DM candidates, Higgs portal couplings, or kinetic mixing. This means the user's model is a cleaner, minimal version of what has been studied, but the core physics (CW breaking, FOPT, GW signal) is well-established.

### Benchmark Hints

| Source | Confidence | Key Numerical Values |
|--------|-----------|---------------------|
| 2501.11619 (same model, PTArcade) | **DIRECT** | g_L = 0.59, M_Z' = 107.3 MeV, M_h2 = 12.4 MeV, alpha = 2.6e5, beta/H = 39.5 |
| 2502.19478 (CW + DM, PTArcade) | **ADAPTABLE** | v = 92.9/343 MeV, g = 0.88/0.79, T_p = 8.4/15.2 MeV, alpha = 5/63, beta/H = 21/13 |
| 2501.15649 (non-CW U(1), method) | **ADAPTABLE** | v = 0.5-10 GeV, g_D = 0.75-0.86, T_p = 12-194 MeV, alpha = 100-520 |
| 2412.16282 (non-CW U(1), PTA fit) | **QUALITATIVE** | T* = 2.4-2.5 MeV, alpha = 0.8-1.0, beta/H = 38-47 |
| 2602.14324 (U(1)_X, thermal history) | **QUALITATIVE** | T_h_p = 0.7-2.0 GeV, alpha_h = 220-2770, xi_p = 0.53-0.71 |

### Key Finding: Parameter Space for PTA Signals

Across all relevant papers, the viable parameter space for explaining PTA nHz signals with a dark U(1) sector FOPT requires:

- **Gauge coupling g_D:** 0.5 - 0.9 (CW models) or larger ~1.2 (non-CW models)
- **Dark sector mass scale:** 1-100 MeV (for nHz signals)
- **Percolation temperature T_p:** MeV scale (few to ~200 MeV)
- **vev v:** 0.1-10 GeV (CW models), with T_p << v indicating strong supercooling
- **Phase transition strength alpha:** 10^2 - 10^5 (strongly supercooled)
- **Inverse duration beta/H:** 10 - 100

### Conventions and Caveats

For the user's analysis with the fopt-pta pipeline, the following convention mismatches between papers should be noted:

1. **vev convention:** All papers use the standard expansion Phi = (phi_b + ...)/sqrt(2), matching the user's convention
2. **Effective potential:** One-loop CW + thermal + daisy is standard; the RG-improved scheme (2501.11619) or on-shell scheme (2501.15649) may give different results
3. **GW templates:** LISA Cosmology Working Group templates (Caprini et al. 2024) are used in 2501.11619; the pipeline should specify its template choice
4. **PT parameter definitions:** The beta/H parameter is conventional for weak transitions but breaks down for strong supercooling; several papers advocate for mean bubble separation R* instead
5. **Bubble wall velocity:** Runaway (v_w -> 1) is typically assumed but NLO friction may reduce it
6. **GW source:** Sound waves vs bubble collisions -- debated for strongly supercooled transitions
7. **Thermal history:** The user assumes xi = 1 (dark and visible sectors thermalised), which is also assumed in 2501.11619 and 2502.19478. Going beyond this requires the methodology of 2602.14324.

### Theory Uncertainties to Track

1. Gauge dependence of finite-T effective potential
2. Renormalisation scheme and RG scale dependence
3. False vacuum trapping / completion conditions
4. Reheating temperature after supercooled FOPT
5. Temperature ratio xi between hidden and visible sectors
6. Dominant GW source (sound waves vs bubble collisions)
7. Bubble wall velocity (runaway vs limited by friction)

### Recommended Next Steps

1. **Primary reference:** Use arXiv:2501.11619 (Goncalves et al. 2025) as the direct template for PTArcade analysis of the conformal dark U(1) model
2. **Secondary validation:** Cross-check against arXiv:2502.19478 (Balan et al. 2025) benchmark points, adapting by setting DM Yukawa to zero
3. **Methodology for completion:** Follow arXiv:2501.15649 (Costa et al. 2025) for proper percolation/completion checks
4. **Consistency check:** Verify the user's m_rho^2 = 3 g_D^4 v^2/(8 pi^2) relation using the benchmark: g_L = 0.59 implies m_rho should be compared with M_h2 = 12.4 MeV at v = 107.3/0.59 ~ 182 MeV
5. **Address Athron challenges:** Ensure the FOPT completes (check percolation) and that the reheating temperature does not shift the GW spectrum out of the nHz band
6. **PTArcade setup:** Use the ceffyl mode following the PTArcade manual (arXiv:2306.16377) and the implementation in arXiv:2501.11619 with LISA Cosmology Working Group templates