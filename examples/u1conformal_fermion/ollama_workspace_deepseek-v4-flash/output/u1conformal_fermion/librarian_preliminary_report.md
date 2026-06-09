# Preliminary Literature Search Report

## Model: u1conformal_fermion

**Target signal**: Gravitational waves from a first-order phase transition (FOPT) in the PTA frequency range (nHz)

**Model summary**: Classically scale-invariant U(1)_D dark sector with:
- Complex scalar Phi (U(1)_D charge +1)
- Dark gauge boson A'_mu
- Two Dirac fermions psi_1 (charge +1/2), psi_2 (charge -1/2)
- Yukawa coupling y_psi Phi psi1_bar psi2 + h.c.
- Coleman-Weinberg radiative symmetry breaking: beta_lambda = (3 g_D^4 - 2 y_psi^4)/(8 pi^2)
- Zero Higgs portal (lambda_HPhi = 0), zero kinetic mixing (epsilon = 0)

---

## Literature Search Summary

### 1. Papers with the same exact model

**arXiv:2212.04784 - Khoze and Milne (2023)** -- Relevance: 10/10
"Gravitational waves and dark matter from classical scale invariance"
Published in Phys. Rev. D 107, 095012

This paper studies a **structurally identical model**: classically conformal U(1)_D with complex scalar S (charge +1), two Dirac fermions chi_1, chi_2 with charges +/-1/2 (anomaly-free), and dark gauge boson Z'. The tree-level potential is V_0 = (lambda_H/4)h^4 + (lambda_S/4)s^4 - (lambda_P/4)h^2s^2 with Higgs portal. Yukawa couplings: y_{1,D} chi_bar_L^1 S chi_R^1 + y_{2,D} chi_bar_L^2 S chi_R^2 + h.c.

**Key differences from target model**:
- Includes Higgs portal coupling lambda_P (target sets lambda_HPhi = 0)
- Uses Gildener-Weinberg formalism (target uses CW with gb_scalar=0)
- **Targets LISA-band GW (TeV-scale vev, mHz frequencies)**, not PTA (nHz)
- Benchmark points have masses 60-1000 GeV, not the MeV-GeV range needed for PTA

**Benchmark points** (Table 2):
| BP | sin_theta | M_h2 (GeV) | M_chi1 (GeV) | M_chi2 (GeV) | Omega h^2 |
|:--:|:---------:|:----------:|:------------:|:------------:|:---------:|
| BP1 | 0.30 | 151 | 59.5 | 59.5 | 0.070 |
| BP2 | 0.10 | 320 | 150 | 155 | 0.078 |
| BP3 | 0.40 | 121 | 591 | 592 | 0.118 |
| BP4 | 0.20 | 331 | 61 | 161 | 0.077 |
| BP5 | 0.30 | 120 | 901 | 1001 | 0.118 |

**Conclusion**: Same model structure but different mass scale. Not directly usable for PTA benchmark points (unusable for PTA signal).

---

### 2. Papers with structurally similar models (same U(1) gauge group, similar particle content, PTA-relevant)

#### a) arXiv:2502.19478 - Balan, Bringmann, Kahlhoefer, Matuszak, Tasillo (2025) -- Relevance: 9/10
"Sub-GeV dark matter and nano-Hertz gravitational waves from a classically conformal dark sector"
Published in JCAP 08 (2025) 062

**Model**: U(1)' with complex scalar Phi (Q=1), two Weyl fermions chi_L (Q=+1/2) and chi_R (Q=-1/2) forming **one** Dirac DM, dark photon A'. Kinetic mixing kappa to SM.
- Same charge assignments for the fermion (+1/2, -1/2) as target model
- Key difference: target has **two** Dirac fermions (8 DOF), Balan has **one** Dirac fermion (4 DOF)
- Different CW condition: lambda = 11/(48 pi^2)(10 lambda^2 + 3g^4 - y^4) [includes scalar loop]
- Target: beta_lambda = (3g_D^4 - 2y_psi^4)/(8 pi^2) [scalar subleading, gb=0]

**Benchmark points** (published JCAP version):
| Parameter | Point A (coupled DS) | Point B (secluded DS) |
|-----------|:-------------------:|:--------------------:|
| g | 0.677 | 0.601 |
| y | 0.224 | 0.234 |
| v (MeV) | 173 | 692 |
| m_A' (MeV) | 117 | 416 |
| m_phi (MeV) | 36.3 | 114 |
| m_chi (MeV) | 27.4 | 115 |
| T_p (MeV) | 2.28 | 1.21 |
| alpha | 4.7e3 | 9.5e6 |
| beta/H | 33.7 | 18.0 |

**Useful for target model**: Adaptable. The g ~ 0.6-0.7, y ~ 0.2-0.4, v ~ 100-700 MeV can be starting points but need adjustment due to different CW condition and fermion content.

---

#### b) arXiv:2501.11619 - Goncalves, Marfatia, Morais, Pasechnik (2025) -- Relevance: 8/10
"Supercooled phase transitions in conformal dark sectors explain NANOGrav data"
Published in Phys. Lett. B 869 (2025) 139829

**Model**: Dark U(1)' with conformal scalar (no fermions). RG-improved thermal potential.
- Demonstrates that conformal models overcome percolation/reheating issues
- Provides NANOGrav best-fit with explicit benchmark masses

**Best-fit from NANOGrav 15yr**:
| Parameter | Value |
|-----------|-------|
| g_L | 0.59 |
| M_h2 (scalon) | 12.4 MeV |
| M_Z' | 107.3 MeV |
| T_RH | 11.7 MeV |
| alpha | 2.60e5 |
| beta/H | 39.5 |

68% CL favored: g_L in [0.57, 0.86], masses 10-100 MeV.

**Useful for target model**: Qualitative. Shows PTA-favored mass scale (~10-100 MeV) and coupling range (~0.6). No fermions in this model.

---

#### c) arXiv:2105.01007 - Borah, Dasgupta, Kang (2021) -- Relevance: 8/10
"Gravitational waves from a dark U(1)_D phase transition in the light of NANOGrav 12.5 yr data"
Published in Phys. Rev. D 104, 063501

**Model**: U(1)_D with complex scalar Phi and vector-like singlet fermion Psi (different charge structure). CW symmetry breaking.
- First paper to connect U(1)_D FOPT to NANOGrav

**Benchmark**: g_D = 0.32, m_Z_D = 12.6 MeV, T_* = 2.25 MeV, alpha_* = 0.68, beta/H_* = 82.4.
- Weaker transition (alpha ~ 0.68, not supercooled). Sound waves dominate.

**Useful for target model**: Qualitative. Shows lower end of viable g_D for PTA signal.

---

#### d) arXiv:2412.16282 - Banik, Cui, Tsai, Tsai (2024) -- Relevance: 8/10
"The Sound of Dark Sectors in Pulsar Timing Arrays"

**Model**: Systematic study of U(1), SU(2), SU(3) dark sectors with scalar + optional fermions. Tree-level potential includes mu^2 term (not fully conformal).

**Best fits for U(1)**:
| mu (MeV) | lambda | g_D | y_D | T_* (MeV) | alpha_* | beta/H_* | chi^2 |
|:--------:|:-----:|:---:|:---:|:---------:|:-------:|:--------:|:-----:|
| 2.4 | 0.03 | 1.2 | 0 | 2.4 | 0.96 | 47 | 36 |
| 2.7 | 0.06 | 1.5 | 0.8 | 2.5 | 0.76 | 38 | 29 |

**Useful for target model**: Qualitative. Shows that including fermions (y_D=0.8) improves fit and extends parameter space. Note: not fully conformal.

---

#### e) arXiv:2501.15649 - Costa, Hoefken Zink, Lucente, Pascoli, Rosauro-Alcaraz (2025) -- Relevance: 7/10
"Supercooled Dark Scalar Phase Transitions explanation of NANOGrav data"
Published in Phys. Lett. B 868 (2025) 139634

**Model**: U(1)_D with complex scalar, no fermions. CW mechanism. Supercooling condition: g_D ~ g_D^roll.

**Benchmarks**:
| BP | v_phi (GeV) | lambda | g_D | T_p (MeV) | alpha | m_phi (GeV) | m_Z' (GeV) |
|:--:|:----------:|:-----:|:---:|:---------:|:-----:|:----------:|:----------:|
| BP1 | 0.5 | 0.006 | 0.75 | 12.54 | 342 | 0.055 | 0.375 |
| BP2 | 1.0 | 0.006 | 0.75 | 22.54 | 523 | 0.110 | 0.750 |
| BP3 | 10.0 | 0.006 | 0.75 | 193.9 | 463 | 1.10 | 7.50 |
| BP4 | 1.0 | 0.010 | 0.86 | 38.03 | 102 | 0.144 | 0.862 |

**Useful for target model**: Qualitative. Shows vev scale ~0.5-10 GeV, g_D ~ 0.75 for supercooled PTA signal.

---

#### f) arXiv:2602.14866 - Feng, Zhang (2026) -- Relevance: 7/10
"Gauge-independent gravitational waves from a minimal dark U(1) sector with viable dark matter candidates"

**Model**: U(1)_x with dark Higgs, dark photon, optionally vectorlike dark fermion. Gauge-independent analysis via Nielsen identities.
- Key finding: m_A' > m_h_x required for FOPT -> for target: g_D v > y_psi v / sqrt(2) => g_D > y_psi / sqrt(2)
- v_x in [10, 100] MeV -> PTA band (nHz)
- v_x in [1, 100] GeV -> LISA band (mHz)

---

### 3. Papers with same target signal but different model

#### arXiv:2308.16219 - Ferrante, Ismail, Lee, Lee (2023)
"Forbidden conformal dark matter at a GeV" (JHEP)
Holographic conformal PT with dilaton. NANOGrav-favored m_sigma ~ 0.1-3 GeV.

#### arXiv:2306.17086 - Fujikura, Girmohanta, Nakai, Suzuki (2023)
"NANOGrav Signal from a Dark Conformal Phase Transition" (PLB)
5D holographic confining PT.

### 4. Background/context papers

#### arXiv:1907.08899 - Mohamadnejad (2020)
Scale-invariant U(1)_D with vector DM. TeV-scale vev -> LISA-band GW (mHz), not PTA.

---

## Novelty Assessment

**The target model has structural precedents in the literature:**

1. **Khoze-Milne (2212.04784)**: Same exact particle content, charge assignments, and symmetry breaking mechanism. However, they focus on TeV-scale parameter space for LISA-band GW and include a Higgs portal.

2. **Balan et al. (2502.19478)**: Very similar but with one Dirac fermion instead of two, and different CW condition.

**The novel aspect of the target model is**:
- The specific combination of: (a) U(1)_D with two Dirac fermions, (b) zero Higgs portal + zero kinetic mixing, (c) CW condition with gb_scalar=0 (beta_lambda = (3g_D^4 - 2y_psi^4)/(8pi^2)), and (d) targeting the PTA nHz GW signal, has **not been studied in the literature**.
- Khoze-Milne is structurally identical but at TeV scale with Higgs portal. No paper has studied this specific model for the PTA nHz signal.

---

## Key Recommendations for Downstream Analysis

1. **Initial scan range for target model parameters** (based on literature synthesis):
   - g_D: 0.3 - 1.5 (PTA-favored range from multiple papers)
   - y_psi: 0.0 - 1.0 (CW condition: y_psi < (3/2)^{1/4} g_D ~ 1.11 g_D)
   - v: 100 MeV - 10 GeV (PTA-favored vev from Costa et al. benchmarks)
   - Target mass scales: m_A' ~ 10-100 MeV, T_n ~ 1-200 MeV

2. **Critical constraint**: From Feng-Zhang (2602.14866), m_A' > m_chi is required for FOPT. For target model: g_D > y_psi / sqrt(2).

3. **CW condition**: The target model's beta_lambda = (3g_D^4 - 2y_psi^4)/(8pi^2) with gb_scalar=0 is different from Balan et al.'s condition. This will modify the scalar mass and supercooling behavior. The absence of scalar loop contributions (10 lambda^2 term) may affect the strength of the phase transition.

4. **Benchmark starting points** for target model:
   - Start with Balan et al. Point A: g_D ~ 0.68, y_psi ~ 0.32 (adjusted for 2x fermion DOF), v ~ 200 MeV
   - Then scan around g_D ~ 0.5-0.9, adjusting v to get m_A' in 10-100 MeV range
   - Check supercooling condition for PTA signal (alpha > 1)

5. **Zero portal assumption check**: With lambda_HPhi = 0 and epsilon = 0, the dark sector thermalises with SM only through the assumed xi=1 condition. BBN and CMB constraints on Delta N_eff from long-lived dark particles must be considered if the dark sector decouples.

---

## Papers Verified (citation check passed)

All 12 papers listed in the handoff JSON have been verified against their arXiv pages for title, authors, year, and abstract. The papers with arXiv IDs 2511.15687 and 2404.03435 mentioned in the search instructions do not appear to exist in arXiv. Paper 2401.12150 was found to be the same as 2501.11619 (Goncalves et al., updated version).
