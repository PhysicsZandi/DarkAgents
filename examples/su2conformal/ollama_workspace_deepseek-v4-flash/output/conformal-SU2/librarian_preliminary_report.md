# Preliminary Literature Search Report: Conformal SU(2) Model

## Model Summary

- **Model**: classically scale-invariant SU(2) gauge theory with a single complex scalar doublet
- **SSB pattern**: SU(2)_X -> nothing (fully broken)
- **Free parameters**: gauge coupling g in [0.1, 3.0], VEV chi0 in [0.1, 10^4] GeV
- **No fermions**: minimal setup
- **Target signal**: Gravitational waves from a first-order phase transition in the PTA (nHz) band (NANOGrav)
- **Backend branch**: fopt-pta

## Literature Landscape

### Novelty Assessment: NOT NOVEL

The exact same model -- a classically scale-invariant SU(2) gauge theory with one complex scalar doublet, producing nHz GWs from a first-order phase transition -- has already been studied in the literature. All papers listed below have been verified against actual arXiv pages.

---

### 1. Exact Same Model (Verified)

#### arXiv:2109.11558 -- Borah, Dasgupta, Kang (2021)
**Title**: "A first order dark SU(2)_D phase transition with vector dark matter in the light of NANOGrav 12.5 yr data"
**Journal**: JCAP

**Relevance**: 10/10 -- This is the most relevant paper. It studies **exactly the same model** (classically conformal SU(2)_D with one complex scalar doublet) for **exactly the same target signal** (nHz GWs from FOPT to explain NANOGrav data).

**Model details**:
- Gauge group: SU(2)_D
- Scalar sector: one complex scalar doublet with classically conformal potential V = lambda (Phi^dagger Phi)^2
- Symmetry breaking: Coleman-Weinberg (radiative) at one loop
- No dark fermions; only gauge bosons + scalar doublet
- SM coupling: negligible Higgs portal (lambda_2 ~ 10^-9 for DM freeze-in)

**Benchmark points**:

| Parameter | BP1 | BP2 |
|-----------|-----|-----|
| g_D | 1.37 | 1.37 |
| M_{Z_D} | 8.23 MeV | 817 keV |
| T_n | 1.8 MeV | 190 keV |
| alpha | 0.45 | 0.36 |
| beta/H | 143 | 151 |
| v_w | 0.887 | 0.872 |

Both benchmarks produce GW spectra in the nHz range consistent with NANOGrav 12.5 yr data.

---

### 2. Structurally Similar Models (Verified)

#### arXiv:2602.09092 -- Bringmann, Konstandin, Matuszak, Schmidt-Hoberg, Tasillo (2026)
**Title**: "Tuning the violins: dark sector phase transition models for the PTA signal"

**Relevance**: 10/10 -- Comprehensive PTArcade-based study of three dark sector FOPT classes for the PTA signal. The **conformal (Coleman-Weinberg)** model is identified as the **most generic, least tuned** explanation for the PTA signal.

**Conformal benchmark (U(1)' gauge group)**:

| Parameter | Value |
|-----------|-------|
| g | 0.692 |
| v (vev) | 140 MeV |
| T_nuc | 3.16 MeV |
| T_p | 2.58 MeV |
| T_reh | 14.5 MeV |
| alpha | 821 |
| beta/H | 57.9 |
| ln(L) | -103.28 |

Key finding: Conformal models naturally produce alpha ~ O(10^2-10^6) and beta/H ~ O(30-100). For the SU(2) case (3x gauge dof), the benchmarks would shift but the qualitative picture remains similar.

#### arXiv:2501.11619 -- Goncalves, Marfatia, Morais, Pasechnik (2025)
**Title**: "Supercooled phase transitions in conformal dark sectors explain NANOGrav data"
**Journal**: Physics Letters B 869 (2025) 139829

Best-fit: g_L = 0.59, M_{Z'} = 107.3 MeV, T_RH = 11.7 MeV, alpha ~ O(10^5), beta/H = 39.5. Shows that supercooled conformal transitions evade percolation issues because the Euclidean action asymptotically approaches zero as T -> 0.

#### arXiv:2210.07075 -- Kierkla, Karam, Swiezewska (2023)
**Title**: "Conformal model for gravitational waves and dark matter: A status update"
**Journal**: JHEP 03 (2023) 007

Studies SU(2)cSM: same SU(2)_X gauge group and scalar doublet, but includes SM Higgs and Higgs portal coupling. Benchmark points have TeV-scale VEVs and produce GW in the LISA (mHz) band, not the nHz band. Provides important qualitative insight: the SU(2)_X conformal model produces very strong transitions (alpha up to ~600) with fast bubble nucleation (beta/H up to ~450).

#### arXiv:1809.11129 -- Prokopec, Rezacek, Swiezewska (2019)
**Title**: "Gravitational waves from conformal symmetry breaking"
**Journal**: JCAP 02 (2019) 009

Earlier analysis of the same SU(2)cSM model with full two-field effective potential. Same GW band (mHz, LISA). Groundwork for 2210.07075.

#### arXiv:2502.19478 -- Balan, Bringmann, Kahlhoefer, Matuszak, Tasillo (2025)
**Title**: "Sub-GeV dark matter and nano-Hertz gravitational waves from a classically conformal dark sector"
**Journal**: JCAP 08 (2025) 062

Studies conformal dark U(1)' with sub-GeV DM and nHz GWs. Preferred parameter region: g ~ 0.57-0.75, v ~ 60-900 MeV, beta/H ~ 15-45, alpha >> 1.

#### arXiv:2306.14856 -- Madge et al. (2023)
**Title**: "Primordial gravitational waves in the nano-Hertz regime and PTA data"
Metadata-only: proposes U(1) Coleman-Weinberg benchmark for PTA signals.

---

### 3. Same Target Signal, Different Model

#### arXiv:2306.09411 -- Bringmann, Depta, Konstandin, Schmidt-Hoberg, Tasillo (2023)
**Title**: "Does NANOGrav observe a dark sector phase transition?"
**Journal**: JCAP 11 (2023) 053

Bayesian analysis finding stable dark sectors **strongly disfavored** by Delta N_eff constraints, but **decaying dark sectors viable** with Bayes factor ~200. Important: any stable dark sector FOPT (including the minimal SU(2) model without SM coupling) will face this constraint.

---

### 4. What Could NOT Be Verified

The following arXiv IDs from the **previous handoff** could **not** be verified through actual arXiv/INSPIRE searches:
- 2006.02713
- 2204.02988
- 2006.04903
- 2103.09824
- 2110.02921
- 2009.13556
- 1906.04260
- 2105.04639
- 2004.09398

These IDs either do not exist on arXiv or correspond to papers on unrelated topics. **They should not be used downstream.**

---

## Key Findings for Backend Compatibility

### Convention Checks (Verified Benchmark vs Proposed Model)

| Feature | Proposed Model | Borah et al. (2109.11558) | Match? |
|---------|----------------|---------------------------|--------|
| Gauge group | SU(2)_X | SU(2)_D | YES |
| Scalar rep | Complex doublet | Complex doublet | YES |
| Tree-level pot | lambda (Phi^dagger Phi)^2 | lambda (Phi^dagger Phi)^2 | YES |
| SSB pattern | SU(2)->nothing | SU(2)->nothing | YES |
| CW mechanism | Yes (one-loop) | Yes (one-loop) | YES |
| VEV convention | (0, chi0/sqrt(2)) | (0, v_D/sqrt(2)) | YES |
| Gauge boson mass | m_W = g*chi0/2 | M_{Z_D} = g_D*v_D/2 | YES |
| No fermions | Yes | Yes | YES |
| Free params | (g, chi0) | (g_D, v_D) | YES |

**No convention mismatches between the proposed model and the literature.**

### Key Differences to Note

1. **Scale**: Borah et al. focus on **MeV-scale VEVs** (v_D ~ 2-16 MeV giving M_{Z_D} ~ 0.8-8 MeV) for nHz GWs. The proposed model's VEV range [0.1, 10^4] GeV covers this region.

2. **Portal coupling**: Borah et al. include a tiny lambda_2 ~ 10^-9 portal for DM freeze-in, which is negligible for the phase transition dynamics. The proposed model has no portal. This is fine for the FOPT itself but has implications for DM overproduction and Neff.

3. **FOPT parameters**: Borah et al. find moderate alpha (0.36-0.45) and beta/H (143-151) at the MeV-scale transition. The conformal U(1)' benchmarks (Bringmann et al.) find much larger alpha (O(10^2-10^6)) and slower transitions (beta/H ~ 30-60). This difference is likely due to the different gauge groups and VEV scales.

### Critical Constraints for the Minimal SU(2) Model

1. **Delta N_eff constraint**: A completely stable dark SU(2) sector with no coupling to the SM will contribute to Neff. Bringmann et al. (2023) found that stable dark sectors are strongly disfavored compared to the SMBHB interpretation. The minimal model needs a mechanism to avoid this constraint:
   - Decays to SM particles before BBN (T > 2 MeV)
   - Or a sufficiently suppressed dark sector energy density

2. **BBN timing**: The percolation temperature T_p should be > 1 MeV to avoid disrupting BBN. Borah et al.'s BP2 (T_n = 190 keV) is marginally in tension.

3. **DM overproduction**: Without a portal to the SM, the massive SU(2) gauge bosons are stable. Their abundance could overclose the Universe unless there is a depletion mechanism.

## Recommendations

1. **Proceed to critic-agent**: The model is not novel (2109.11558 covers the exact same model and signal), but the critic should evaluate whether the proposed analysis adds value beyond the existing literature.

2. **Proceed to fopt-agent**: Use benchmark points from 2109.11558 as initial validation targets. Recommended initial scan: g in [0.5, 2.0], chi0 in [1, 100] MeV (MeV-scale VEV for nHz GWs).

3. **Critical warning**: The previous handoff contained unverified arXiv IDs. Only papers with citation_verified=true should be used downstream.

4. **The Delta N_eff constraint must be addressed**: If the minimal SU(2) model has no SM coupling, the dark sector is stable and contributes to Neff. This is a significant constraint from Bringmann et al. (2023).