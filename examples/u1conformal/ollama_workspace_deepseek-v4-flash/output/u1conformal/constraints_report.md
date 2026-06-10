# Constraints Report for the Dark U(1) Conformal Model (u1conformal)

## Analysis Mode: PTArcade 1-sigma Posterior Region

**Date**: 2026-06-10
**Agent**: constraint-agent

---

## 1. Input Region Summary

The 1-sigma credible region from PTArcade Bayesian analysis of NG15 data is:

| Parameter | Range | MAP |
|-----------|-------|-----|
| v (vev) | [0.6166, 1.2303] GeV | 1.0691 GeV |
| g_D (gauge coupling) | [0.509, 0.545] | 0.508 |
| m_A' = g_D * v | [0.3138, 0.6705] GeV | 0.5431 GeV |
| m_rho = sqrt(3/8) * g_D^2 * v / pi | [0.03114, 0.07123] GeV | 0.05378 GeV |
| beta_lambda = 3*g_D^4/(8*pi^2) | [0.00255, 0.00335] | 0.00253 |

**Critical unknowns**:
- Kinetic mixing epsilon (unspecified, assumed small)
- Higgs portal lambda_HPhi (unspecified, assumed small)

---

## 2. Constraint Overview

A total of **23 constraints** were considered across all categories:

| Category | Applied | Direct | Approx. | Recast | New Backend | N/A |
|----------|---------|--------|---------|--------|-------------|-----|
| **Collider** | 0 | 1 | 0 | 2 | 0 | 1 |
| **Beam dump** | 0 | 2 | 0 | 1 | 0 | 0 |
| **BBN** | 0 | 1 | 2 | 0 | 0 | 0 |
| **CMB** | 0 | 0 | 1 | 0 | 0 | 0 |
| **Delta N_eff** | 0 | 0 | 2 | 0 | 0 | 0 |
| **Theory** | 4 | 0 | 0 | 0 | 0 | 0 |
| **Stellar/SN** | 0 | 0 | 0 | 0 | 0 | 4 |
| **Direct detection** | 0 | 0 | 0 | 0 | 0 | 1 |
| **Structure form.** | 0 | 0 | 0 | 0 | 0 | 1 |
| **Thermalization** | 0 | 0 | 1 | 0 | 0 | 0 |

**Counts**: 4 directly testable, 6 approximately testable, 4 recast-needed, 0 requires new backend, 9 not applicable

---

## 3. Key Constraint Highlights

### 3.1 Dark Photon A' (m = 0.31 - 0.67 GeV)

**Most Important Constraints**:

1. **LHCb prompt A' -> mu+mu-** (PRL 124, 041801): World-leading constraint for m_A' = 214-740 MeV. Excludes epsilon > few x 10^{-4} at 90% CL assuming BR(A'->mu+mu-) ~ 1. The full 1-sigma range is covered by this search.

2. **BaBar invisible A'** (PRL 119, 131804): Excludes epsilon > (2-4)x10^{-4} for invisible decays. Complementary to LHCb search; covers m_A' = 20 MeV - 8 GeV.

3. **NA64** (electron beam): Most sensitive for m_A' < 350 MeV. Only lower edge (0.31 GeV) of 1-sigma region overlaps.

4. **NA62** (beam dump): Excludes m_A' = 215-550 MeV for visible mu+mu- decays. Covers lower portion of 1-sigma range.

5. **BBN lower bound on epsilon**: Dark photons must decay before BBN (tau' < 0.2 s), giving epsilon > 10^{-9} to 10^{-8} for m_A' ~ 300-700 MeV. This is a LOWER bound, not upper bound.

**Crucial caveat**: All these constraints depend on the unknown epsilon and on whether A' decays visibly or invisibly. If both channels are open (A' -> SM via epsilon and A' -> rho + A'* via g_D), the actual branching ratio determines which constraints apply.

### 3.2 Dark Scalar rho (m = 0.031 - 0.071 GeV)

**Most Important Constraints**:

1. **Cosmic beam dump constraints** (Fradette et al. 2018): BBN and CMB jointly exclude mixing angles sin^2(theta) from ~10^{-11} up to ~10^{-7} for scalars with mass ~ 50-100 MeV. The combined BBN+CMB exclusion covers nearly the entire natural range of the Higgs portal.

2. **BBN constraint**: For m_rho = 50-100 MeV decaying to e+e-, BBN excludes sin^2(theta) > few x 10^{-7} (short lifetime, entropy injection).

3. **CMB constraint**: Planck CMB power spectrum excludes sin^2(theta) ~ 10^{-11} - 10^{-10} for tau_rho > 10^13 s (long lifetimes).

4. **PS191 beam dump**: Constrains sin^2(theta) ~ 10^{-7} - 3x10^{-7} for m_rho = 100-150 MeV; partially overlaps upper end of 1-sigma range.

5. **Higgs exotic decays**: CMS EXO-24-034 probes h->SS for m_S > 0.4 GeV; our m_rho is too light. Kaon experiments (NA62, E949) provide complementary coverage.

**Crucial caveat**: All constraints depend on the unknown lambda_HPhi/sin^2(theta). For sin^2(theta) < 10^{-6}, the scalar is produced via freeze-in with yield Y ~ 3e11*theta^2, which must then decay before BBN/CMB.

### 3.3 Cosmological Constraints (Delta N_eff)

**Most Important**: The xi = T_dark/T_SM = 1 assumption is in tension with Delta N_eff constraints. For temperatures well above m_A' and m_rho, the dark sector contributes:
- 3 dofs (A') + 1 dof (rho) = 4 bosonic dofs
- Delta N_eff = 4 * (8/7) * (xi)^4 * (g_dark_eff/g_gamma_eff) ~ 0.57 for xi=1
- Planck 2018: Delta N_eff < 0.3 at 95% CL
- BBN: Delta N_eff < 0.4

This tension is mitigated by:
1. The supercooled PT exponentially dilutes dark sector number densities
2. After PT, the dark sector reheats, but massive particles may have negligible abundance at BBN
3. If portals are inefficient, xi may be smaller than 1

### 3.4 Theory Constraints

Both satisfied:
- **Perturbativity**: g_D^2/(4*pi) = 0.082-0.095 << 1 (satisfied)
- **CW consistency**: beta_lambda = 0.0025-0.0034 > 0 (satisfied)

---

## 4. Constraint Diagram (A' mass vs. epsilon)

For the dark photon A' in the 0.31-0.67 GeV mass range, the applicable constraints on epsilon are:

```
    epsilon > 1e-3: LHCb prompt A'->mu+mu- EXCLUDES [if BR(visible)=1]
    epsilon > 3e-4: BaBar invisible A' EXCLUDES [if BR(invisible)=1]
    epsilon ~ 1e-9 to 1e-8: BBN requires DECAY BEFORE BBN (lower bound)
    epsilon < 1e-9: A' too long-lived for BBN (potential overclosure)
```

The actual allowed window depends on the branching ratio between visible and invisible channels, which requires computing A' partial widths to SM vs rho+A'*.

## 5. Constraint Diagram (rho mass vs. mixing angle)

For the dark scalar rho in the 0.031-0.071 GeV mass range:

```
    sin^2(theta) > 1e-6: THERMALIZATION AND OVERPRODUCTION (excluded)
    sin^2(theta) ~ 1e-7 to 1e-6: BBN EXCLUDES (short lifetime, entropy injection)
    sin^2(theta) ~ 1e-10 to 1e-7: CMB EXCLUDES (long lifetime, energy injection)
    sin^2(theta) < 1e-11: ALLOWED (no direct constraints)
```

---

## 6. Missing Calculations (Priority: High)

These observables must be computed before any constraint can be definitively applied:

| Observable | Needed For | Inputs Required |
|------------|-----------|-----------------|
| A' decay width & lifetime | CONST-001,-002,-003,-004,-018 | m_A', epsilon, R-ratio |
| A' branching fractions | All A' constraints | m_A', epsilon, g_D, m_rho |
| rho decay width & lifetime | CONST-005,-006,-010,-011,-021 | m_rho, lambda_HPhi/sin^2(theta) |
| rho branching fractions | All rho constraints | m_rho, sin^2(theta) |
| rho freeze-in yield Y_rho | CONST-005,-006,-023 | m_rho, sin^2(theta), production Xsec |
| Dark sector xi(T) evolution | CONST-007,-015,-017 | epsilon, lambda_HPhi, masses |
| Post-PT residual abundance | CONST-015,-017 | T_reh, alpha, beta/H |

---

## 7. Conclusions

1. **A' constraints** cannot be applied without knowing epsilon. If epsilon > few x 10^{-4}, LHCb+BaBar+NA62 cover the full 1-sigma mass range and would exclude the region. If epsilon < 10^{-9}, BBN overclosure is a concern. There is a viable window 10^{-9} < epsilon < 10^{-4} where the A' satisfies all constraints, but this requires computing actual branching fractions to verify.

2. **rho constraints** cannot be applied without knowing lambda_HPhi/sin^2(theta). The combined BBN+CMB+beam-dump exclusions cover sin^2(theta) from ~10^{-11} to ~10^{-6}. Only sin^2(theta) < 10^{-11} is clearly viable. Verification requires computing the freeze-in yield and decay lifetime.

3. **Delta N_eff** from dark radiation is the most serious model-independent concern. The xi=1 assumption leads to Delta N_eff ~ 0.57, exceeding Planck bounds. The supercooled PT must dilute the dark sector sufficiently to evade this.

4. **The theory constraints** (perturbativity, CW consistency) are satisfied by the 1-sigma preferred region.

5. **No DM candidate**: The minimal model has no stable particle, so DM constraints do not apply.

---

## 8. Key References

1. LHCb, "Search for A' -> mu+mu- Decays", PRL 124, 041801 (2020) [arXiv:1910.06926]
2. BaBar, "Search for Invisible Decays of a Dark Photon", PRL 119, 131804 (2017) [arXiv:1702.03327]
3. Coy, Kimus, Tytgat, "Light from darkness: history of a hot dark sector", JCAP 02 (2025) 077 [arXiv:2405.10792]
4. Fradette, Pospelov, Pradler, Ritz, "Cosmological beam dump: constraints on dark scalars", JHEP 04 (2019) 040 [arXiv:1812.07585]
5. Caputo, Essig, "The Dark Photon: a 2026 Perspective", arXiv:2603.08430
6. Caputo, Park, Yun, "The Heavy Dark Photon Handbook", arXiv:2511.15785
7. Dolan, Hiskens, Volkas, "Constraining dark photons with self-consistent simulations of globular cluster stars", arXiv:2306.13335
8. Caputo, Janka, Raffelt, Yun, "Cooling the Shock: New Supernova Constraints on Dark Photons", PRL 134, 151002 (2025) [arXiv:2502.01731]
9. Gorbunov, Krasnov, Suvorov, "Constraints on light scalars from PS191 results", arXiv:2105.11102
10. Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters", A&A 641, A6 (2020) [arXiv:1807.06209]